import * as oidc from 'openid-client';

export const SESSION_KEY = 'scriptahub:account:v1';
export const CALLBACK_MESSAGE = 'scriptahub:oidc-callback';
export const MEMBER_ROLES = ['selfRegistered', 'user', 'admin'];

export function authError(code) {
  return Object.assign(new Error(code), { code });
}

export function normalizeConfig(input, callbackUrl) {
  if (!input || typeof input.issuer !== 'string' || !input.issuer) throw authError('unavailable');
  let issuer;
  let callback;
  try { issuer = new URL(input.issuer); callback = new URL(callbackUrl); } catch { throw authError('unavailable'); }
  const loopback = (url) => ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname);
  const secure = (url) => url.protocol === 'https:' || (url.protocol === 'http:' && loopback(url));
  if (!secure(issuer) || issuer.href !== input.issuer || issuer.username || issuer.password
    || issuer.search || issuer.hash || !issuer.pathname.endsWith('/service/oidc')
    || !secure(callback) || callback.username || callback.password || callback.search || callback.hash
    || typeof input.clientId !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._~-]{2,127}$/.test(input.clientId)) {
    throw authError('unavailable');
  }
  return { issuer: issuer.href, clientId: input.clientId, callback: callback.href };
}

export function readSession(storage, config, now = Date.now()) {
  try {
    const value = JSON.parse(storage?.getItem(SESSION_KEY) || 'null');
    if (value?.issuer === config.issuer && value?.clientId === config.clientId
      && typeof value.sub === 'string' && value.sub && typeof value.accessToken === 'string'
      && value.accessToken.length > 0 && value.accessToken.length < 16384
      && Number.isFinite(value.expiresAt) && value.expiresAt > now + 5000) return value;
  } catch { /* An unavailable or malformed browser store is not a session. */ }
  return null;
}

export function acceptedAccount(info, expectedSub) {
  if (!info || typeof expectedSub !== 'string' || !expectedSub || info.sub !== expectedSub
    || !Array.isArray(info.roles) || !info.roles.some((role) => MEMBER_ROLES.includes(role))) {
    throw authError('accountDenied');
  }
  return { sub: info.sub, email: typeof info.email === 'string' ? info.email : '', roles: info.roles.filter((role) => MEMBER_ROLES.includes(role)) };
}

export function matchingCallback(event, popup, callbackUrl, state) {
  const expected = new URL(callbackUrl);
  if (event.source !== popup || event.origin !== expected.origin || event.data?.type !== CALLBACK_MESSAGE
    || typeof event.data.url !== 'string' || event.data.url.length > 16384) return null;
  try {
    const url = new URL(event.data.url);
    if (url.origin !== expected.origin || url.pathname !== expected.pathname || url.username || url.password || url.hash
      || url.searchParams.getAll('state').length !== 1 || url.searchParams.get('state') !== state) return null;
    return url;
  } catch { return null; }
}

export function waitForCallback(host, popup, callbackUrl, state, timeoutMs = 300000) {
  let dispose = () => {};
  const promise = new Promise((resolve, reject) => {
    const finish = (fn, result) => { dispose(); fn(result); };
    const receive = (event) => {
      const url = matchingCallback(event, popup, callbackUrl, state);
      if (url) finish(resolve, url);
    };
    const closed = host.setInterval(() => {
      if (popup.closed) finish(reject, authError('cancelled'));
    }, 350);
    const timer = host.setTimeout(() => finish(reject, authError('timeout')), timeoutMs);
    dispose = () => {
      host.removeEventListener('message', receive);
      host.clearInterval(closed);
      host.clearTimeout(timer);
    };
    host.addEventListener('message', receive);
  });
  return { promise, dispose };
}

export function createAccountClient(config, { storage, host = window, fetcher = fetch } = {}) {
  let discovery;
  let memorySession = readSession(storage, config);
  function clear() {
    memorySession = null;
    try { storage?.removeItem(SESSION_KEY); } catch { /* Storage may be disabled. */ }
  }
  async function provider() {
    if (!discovery) {
      discovery = oidc.discovery(new URL(config.issuer), config.clientId, undefined, oidc.None(), {
        timeout: 15,
        [oidc.customFetch]: (url, options) => fetcher(url, { ...options, credentials: 'omit' }),
        execute: [oidc.enableNonRepudiationChecks, ...(config.issuer.startsWith('http:') ? [oidc.allowInsecureRequests] : [])],
      }).catch((error) => { discovery = undefined; throw error; });
    }
    return discovery;
  }
  async function current() {
    const session = memorySession || readSession(storage, config);
    if (!session || session.expiresAt <= Date.now() + 5000) { clear(); return null; }
    try {
      const info = await oidc.fetchUserInfo(await provider(), session.accessToken, session.sub);
      return acceptedAccount(info, session.sub);
    } catch (error) {
      clear();
      if (error.code === 'accountDenied') throw error;
      if (Number(error.status) === 401 || Number(error.cause?.status) === 401 || error.error === 'invalid_token') return null;
      throw authError('unavailable');
    }
  }
  async function signIn(popup, mode = 'signup') {
    let callback;
    try {
      const client = await provider();
      if (popup.closed) throw authError('cancelled');
      const verifier = oidc.randomPKCECodeVerifier();
      const state = oidc.randomState();
      const nonce = oidc.randomNonce();
      const url = oidc.buildAuthorizationUrl(client, {
        redirect_uri: config.callback, scope: 'openid email roles', state, nonce,
        code_challenge: await oidc.calculatePKCECodeChallenge(verifier), code_challenge_method: 'S256',
        ...(mode === 'signup' ? { screen_hint: 'signup' } : {}),
      });
      callback = waitForCallback(host, popup, config.callback, state);
      popup.location.replace(url.href);
      const response = await callback.promise;
      const tokens = await oidc.authorizationCodeGrant(client, response, {
        pkceCodeVerifier: verifier, expectedState: state, expectedNonce: nonce,
      });
      const claims = tokens.claims();
      if (!claims?.sub || !tokens.access_token || tokens.token_type?.toLowerCase() !== 'bearer'
        || !Number.isFinite(tokens.expires_in) || tokens.expires_in <= 0) throw authError('accountDenied');
      const info = await oidc.fetchUserInfo(client, tokens.access_token, claims.sub);
      const account = acceptedAccount(info, claims.sub);
      memorySession = {
        issuer: config.issuer, clientId: config.clientId, sub: claims.sub, accessToken: tokens.access_token,
        expiresAt: Math.min(Date.now() + tokens.expires_in * 1000, claims.exp * 1000),
      };
      try { storage?.setItem(SESSION_KEY, JSON.stringify(memorySession)); } catch { /* Keep the session in memory. */ }
      return account;
    } catch (error) {
      clear();
      if (error.error === 'access_denied') throw authError('cancelled');
      throw error;
    } finally {
      callback?.dispose();
      if (!popup.closed) popup.close();
    }
  }
  return { current, signIn, clear, hasSession: () => Boolean(memorySession && memorySession.expiresAt > Date.now() + 5000) };
}
