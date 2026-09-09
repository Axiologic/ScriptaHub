# ScriptaHub reader accounts

Reading stays public. Site PDF and edition-feedback actions request a UserPersisto
account in a popup and resume after successful authentication. PDF file URLs stay
public, including context-menu downloads and direct links. Feedback still opens
the visitor's email application; this change does not store or publish reviews.

## Configure the account service

Set `issuer` in `config.json` to the deployed UserPersisto issuer, including its
complete path ending in `/service/oidc`. Leave `clientId` as `scriptahub-web`, or
change it to match the registered public client. An empty issuer deliberately
keeps gated actions unavailable while reading remains usable. No credentials or
client secret belong in this repository.

Register this client through UserPersisto's authenticated administrator client
management API:

```json
{
  "client_id": "scriptahub-web",
  "client_name": "ScriptaHub",
  "redirect_uris": ["https://scriptahub.com/auth/callback.html"],
  "token_endpoint_auth_method": "none",
  "grant_types": ["authorization_code"],
  "scope": "openid email roles"
}
```

Initialize the service owner using the existing UserPersisto setup flow before
enabling public registration. Enable password login and self-registration, with
`selfRegistered` as the registration role. The provider's `user-persisto-v2`
changes support `screen_hint=signup` and prevent the OIDC signup endpoint from
creating the initial administrator. Existing `user` and `admin` accounts also
qualify for the site's gated actions.

UserPersisto's issuer must be publicly reachable over HTTPS, and the Ploinky
public-protocol route must preserve OIDC discovery, JWKS, authorization, token,
and UserInfo responses. Cross-origin token and UserInfo requests use bearer
tokens with `credentials: omit`. UserPersisto allows the exact origins of the
client's registered callback URLs. Do not enable credentialed wildcard CORS.
The canonical production origin is `https://scriptahub.com`; a `www` hostname
or GitHub project preview needs its own exact registered callback URL. Local
development permits HTTP only on loopback addresses.

## Browser contract

`src/auth.js` exposes `window.ScriptaHubAuth.requireAccount(action)`, resolving to
an account or `null` when cancelled or unavailable. Links use
`data-auth-action="download"` or `data-auth-action="feedback"`. The shared reader
and standalone reader also gate local PDF anchors. Feedback submission rechecks
the account even when the visitor opens the feedback URL directly.

The popup uses Authorization Code with S256 PKCE, fresh state and nonce.
`openid-client` validates the authorization response and ID token, including its
signature. The callback has no analytics, removes the response query from its
history, and sends the result only to its same-origin opener. The opener checks
the exact callback origin, path, source window, and transaction state.

Only the short-lived access token, its expiry, issuer, client ID and subject are
kept in `sessionStorage` for that tab. Passwords stay on UserPersisto. No refresh
token is requested. Every gated action checks UserInfo for current membership;
stored role flags are never authorization evidence. Expired sessions restart the
popup flow. UserPersisto's existing session may avoid another password prompt.
Cancelling leaves the current page and feedback draft intact. Duplicate clicks
share one authentication attempt, including same-origin embedded readers.
New-tab requests retain their intent through a Continue link after authentication,
providing a fresh user gesture even after a long signup. Popup blockers receive an explicit Continue
button. An unavailable issuer or denied account leaves the action unperformed.

This is a voluntary site interaction gate. A future stored-review endpoint must
independently validate the access token, allowed client/resource, current account
status and role on its server. A browser check cannot enforce write access to an
API, and this release makes no such API available.

## Build and verify

The browser bundle is checked in so GitHub Pages can serve it directly. Use
Node.js 22.12 or newer for book generation, validation, and the browser bundle. Edit `src/`, then regenerate the bundles; do not edit
`docs/assets/auth*.js` by hand.

```sh
npm ci
npm run build
npm test
```

Pinned browser dependencies and their licences are included by the build. Book
page changes originate in `tools/build_books.mjs` and are emitted by
`node tools/build_books.mjs refresh` (also available as `npm run build:books`).
The generator, catalogue checker, link auditor, and their tests use native
Node.js modules. Optional keyword inference still uses a local Python worker;
see [dependencies.md](../../dependencies.md). The browser account flow remains JavaScript. Canonical reader HTML
and PDFs are preserved.

Before publishing, test against the selected deployed issuer: anonymous reading,
signup to `selfRegistered`, existing-account sign-in, explicit consent, download
resumption, feedback-draft preservation, popup cancellation/blocking, expiry and
blocked accounts. Local browser tests cannot establish the deployed proxy's
headers, TLS configuration or registered-client state.
