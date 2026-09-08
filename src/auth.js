import { authError, createAccountClient, normalizeConfig } from './auth-client.js';

// Resolve against this asset so book routes and GitHub project previews agree.
const asset = new URL(document.currentScript.src);
const configUrl = new URL('../auth/config.json', asset);
const callbackUrl = new URL('../auth/callback.html', asset);
let parentGate;
try {
  if (window.parent !== window && window.parent.location.origin === location.origin) parentGate = window.parent.ScriptaHubAuth;
} catch { /* A cross-origin embed owns its authentication flow. */ }
const messages = {
  en: ['Create an account to continue', 'Sign in or register to download this PDF.', 'Sign in or register to leave feedback.', 'Continue', 'Cancel', 'Opening sign in…', 'Sign in is temporarily unavailable. Please try again later.', 'This account cannot use this action.', 'Your browser blocked the sign-in window. Select Continue to try again.', 'Sign in timed out. Please try again.', 'Close'],
  fr: ['Créez un compte pour continuer', 'Connectez-vous ou inscrivez-vous pour télécharger ce PDF.', 'Connectez-vous ou inscrivez-vous pour laisser un avis.', 'Continuer', 'Annuler', 'Ouverture de la connexion…', 'La connexion est temporairement indisponible. Réessayez plus tard.', 'Ce compte ne peut pas effectuer cette action.', 'Votre navigateur a bloqué la fenêtre de connexion. Sélectionnez Continuer pour réessayer.', 'Le délai de connexion a expiré. Réessayez.', 'Fermer'],
  de: ['Konto erstellen, um fortzufahren', 'Melden Sie sich an oder registrieren Sie sich, um dieses PDF herunterzuladen.', 'Melden Sie sich an oder registrieren Sie sich, um Feedback zu geben.', 'Weiter', 'Abbrechen', 'Anmeldung wird geöffnet…', 'Die Anmeldung ist vorübergehend nicht verfügbar. Versuchen Sie es später erneut.', 'Dieses Konto kann diese Aktion nicht ausführen.', 'Ihr Browser hat das Anmeldefenster blockiert. Wählen Sie Weiter, um es erneut zu versuchen.', 'Die Anmeldung hat zu lange gedauert. Versuchen Sie es erneut.', 'Schließen'],
  es: ['Crea una cuenta para continuar', 'Inicia sesión o regístrate para descargar este PDF.', 'Inicia sesión o regístrate para dejar comentarios.', 'Continuar', 'Cancelar', 'Abriendo el inicio de sesión…', 'El inicio de sesión no está disponible temporalmente. Inténtalo más tarde.', 'Esta cuenta no puede realizar esta acción.', 'Tu navegador bloqueó la ventana de inicio de sesión. Selecciona Continuar para reintentarlo.', 'Se agotó el tiempo de inicio de sesión. Inténtalo de nuevo.', 'Cerrar'],
  pt: ['Crie uma conta para continuar', 'Inicie sessão ou registe-se para descarregar este PDF.', 'Inicie sessão ou registe-se para deixar comentários.', 'Continuar', 'Cancelar', 'A abrir o início de sessão…', 'O início de sessão está temporariamente indisponível. Tente mais tarde.', 'Esta conta não pode efetuar esta ação.', 'O navegador bloqueou a janela de início de sessão. Selecione Continuar para tentar novamente.', 'O tempo para iniciar sessão expirou. Tente novamente.', 'Fechar'],
  it: ['Crea un account per continuare', 'Accedi o registrati per scaricare questo PDF.', 'Accedi o registrati per lasciare un commento.', 'Continua', 'Annulla', 'Apertura dell’accesso…', 'L’accesso non è temporaneamente disponibile. Riprova più tardi.', 'Questo account non può eseguire questa azione.', 'Il browser ha bloccato la finestra di accesso. Seleziona Continua per riprovare.', 'Il tempo per accedere è scaduto. Riprova.', 'Chiudi'],
  ro: ['Creează un cont pentru a continua', 'Autentifică-te sau înregistrează-te pentru a descărca acest PDF.', 'Autentifică-te sau înregistrează-te pentru a lăsa feedback.', 'Continuă', 'Anulează', 'Se deschide autentificarea…', 'Autentificarea este temporar indisponibilă. Încearcă din nou mai târziu.', 'Acest cont nu poate efectua această acțiune.', 'Browserul a blocat fereastra de autentificare. Selectează Continuă pentru a încerca din nou.', 'Timpul pentru autentificare a expirat. Încearcă din nou.', 'Închide'],
  pl: ['Utwórz konto, aby kontynuować', 'Zaloguj się lub zarejestruj, aby pobrać ten PDF.', 'Zaloguj się lub zarejestruj, aby zostawić opinię.', 'Kontynuuj', 'Anuluj', 'Otwieranie logowania…', 'Logowanie jest chwilowo niedostępne. Spróbuj ponownie później.', 'To konto nie może wykonać tej czynności.', 'Przeglądarka zablokowała okno logowania. Wybierz Kontynuuj, aby spróbować ponownie.', 'Upłynął czas logowania. Spróbuj ponownie.', 'Zamknij'],
};
const continuation = {
  en: ['Your account is ready', 'Continue to open the requested page in a new tab.'],
  fr: ['Votre compte est prêt', 'Continuez pour ouvrir la page demandée dans un nouvel onglet.'],
  de: ['Ihr Konto ist bereit', 'Öffnen Sie die gewünschte Seite in einem neuen Tab.'],
  es: ['Tu cuenta está lista', 'Continúa para abrir la página solicitada en una pestaña nueva.'],
  pt: ['A sua conta está pronta', 'Continue para abrir a página pedida num novo separador.'],
  it: ['Il tuo account è pronto', 'Continua per aprire la pagina richiesta in una nuova scheda.'],
  ro: ['Contul tău este pregătit', 'Continuă pentru a deschide pagina solicitată într-o filă nouă.'],
  pl: ['Twoje konto jest gotowe', 'Kontynuuj, aby otworzyć wybraną stronę w nowej karcie.'],
};
function language() {
  return (new URL(location.href).searchParams.get('lang') || document.documentElement.lang)?.split('-')[0];
}
function copy() {
  return messages[language()] || messages.en;
}

const style = document.createElement('link');
style.rel = 'stylesheet';
style.href = new URL('auth.css', asset).href;
document.head.append(style);
let client;
let loading;
let pending;
function getClient() {
  if (!loading) loading = fetch(configUrl, { credentials: 'omit', cache: 'no-store', signal: AbortSignal.timeout(15000) })
    .then((response) => { if (!response.ok) throw authError('unavailable'); return response.json(); })
    .then((input) => {
      let storage;
      try { storage = sessionStorage; } catch { /* In-memory sessions still work. */ }
      client = createAccountClient(normalizeConfig(input, callbackUrl), { storage });
      return client;
    }).catch((error) => { loading = undefined; throw error; });
  return loading;
}
// Prefetch configuration only; browsing does not contact the identity service.
if (!parentGate) getClient().catch(() => {});

function openPopup() {
  const popup = window.open('about:blank', '_blank', 'popup,width=520,height=720');
  if (popup) {
    popup.document.title = copy()[0];
    popup.document.body.textContent = copy()[5];
  }
  return popup;
}

function dialog(message, continueAction, { destination, heading } = {}) {
  const labels = copy();
  const previousFocus = document.activeElement;
  const element = document.createElement('dialog');
  element.className = 'scriptahub-auth-dialog';
  element.setAttribute('aria-labelledby', 'scriptahub-auth-title');
  element.setAttribute('aria-describedby', 'scriptahub-auth-message');
  const title = document.createElement('h2');
  title.id = 'scriptahub-auth-title';
  title.textContent = heading || labels[0];
  const body = document.createElement('p');
  body.id = 'scriptahub-auth-message';
  body.textContent = message;
  const actions = document.createElement('div');
  actions.className = 'scriptahub-auth-actions';
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = continueAction || destination ? labels[4] : labels[10];
  actions.append(close);
  element.append(title, body, actions);
  document.body.append(element);
  return new Promise((resolve) => {
    let result = null;
    element.addEventListener('close', () => {
      element.remove();
      previousFocus?.focus();
      resolve(result);
    }, { once: true });
    close.addEventListener('click', () => element.close());
    if (continueAction) {
      const proceed = document.createElement('button');
      proceed.type = 'button';
      proceed.className = 'scriptahub-auth-primary';
      proceed.textContent = labels[3];
      proceed.addEventListener('click', () => {
        result = continueAction();
        if (result) element.close();
        else body.textContent = labels[8];
      });
      actions.append(proceed);
    }
    if (destination) {
      const proceed = document.createElement('a');
      proceed.href = destination.href;
      proceed.target = '_blank';
      proceed.rel = 'noopener noreferrer';
      proceed.className = 'scriptahub-auth-primary';
      proceed.textContent = labels[3];
      resumed.add(proceed);
      proceed.addEventListener('click', () => { result = true; element.close(); });
      actions.append(proceed);
    }
    element.showModal();
  });
}

function requireAccount(action = 'feedback') {
  if (pending) return pending;
  // Reserve the window within the click gesture, before any network request.
  let popup = client?.hasSession() ? null : openPopup();
  pending = (async () => {
    try {
      const accountClient = await getClient();
      const account = await accountClient.current();
      if (account) return account;
      if (!popup || popup.closed) {
        popup = await dialog(copy()[action === 'download' ? 1 : 2], openPopup);
        if (!popup) return null;
      }
      return await accountClient.signIn(popup);
    } catch (error) {
      if (popup && !popup.closed) popup.close();
      if (error.code !== 'cancelled') {
        const index = { accountDenied: 7, timeout: 9 }[error.code] || 6;
        await dialog(copy()[index]);
      }
      return null;
    } finally {
      if (popup && !popup.closed) popup.close();
      pending = undefined;
    }
  })();
  return pending;
}

const resumed = new WeakSet();
let activeLink;
async function gateLink(event) {
  const link = event.target.closest?.('a[href]');
  if (!link || resumed.has(link) || event.defaultPrevented || (event.type === 'auxclick' && event.button !== 1)) return;
  const url = new URL(link.href, location.href);
  // This also covers PDF links created later by the reader's fallback renderer.
  const action = link.dataset.authAction || (url.origin === location.origin && /\.pdf$/i.test(url.pathname) ? 'download' : '');
  if (!['download', 'feedback'].includes(action)) return;
  event.preventDefault();
  if (activeLink) return;
  activeLink = link;
  const newWindow = link.target === '_blank' || event.button === 1 || event.ctrlKey || event.metaKey || event.shiftKey;
  link.setAttribute('aria-busy', 'true');
  try {
    if (!await window.ScriptaHubAuth.requireAccount(action)) return;
    // Action URLs stay on this site. Account-service input never selects a destination.
    if (url.origin !== location.origin) return;
    if (newWindow && !link.hasAttribute('download')) {
      // Authentication can outlive transient activation. A real click reliably
      // opens the requested new tab instead of silently losing it to a blocker.
      const text = continuation[language()] || continuation.en;
      await dialog(text[1], undefined, { destination: url, heading: text[0] });
      return;
    }
    resumed.add(link);
    link.click();
  } finally {
    resumed.delete(link);
    link.removeAttribute('aria-busy');
    activeLink = undefined;
  }
}
document.addEventListener('click', gateLink);
document.addEventListener('auxclick', gateLink);
window.ScriptaHubAuth = Object.freeze({ requireAccount: parentGate?.requireAccount || requireAccount });
