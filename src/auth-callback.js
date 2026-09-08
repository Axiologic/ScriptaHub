import { CALLBACK_MESSAGE } from './auth-client.js';

const responseUrl = location.href;
const messages = {
  en: ['Completing sign in… You can close this window if it stays open.', 'Return to ScriptaHub and start sign in again.'],
  fr: ['Connexion en cours… Vous pouvez fermer cette fenêtre si elle reste ouverte.', 'Revenez sur ScriptaHub et recommencez la connexion.'],
  de: ['Anmeldung wird abgeschlossen… Sie können dieses Fenster schließen, falls es geöffnet bleibt.', 'Kehren Sie zu ScriptaHub zurück und starten Sie die Anmeldung erneut.'],
  es: ['Completando el inicio de sesión… Puedes cerrar esta ventana si permanece abierta.', 'Vuelve a ScriptaHub e inicia sesión de nuevo.'],
  pt: ['A concluir o início de sessão… Pode fechar esta janela se permanecer aberta.', 'Volte ao ScriptaHub e inicie sessão novamente.'],
  it: ['Completamento dell’accesso… Puoi chiudere questa finestra se rimane aperta.', 'Torna su ScriptaHub e avvia nuovamente l’accesso.'],
  ro: ['Se finalizează autentificarea… Poți închide această fereastră dacă rămâne deschisă.', 'Revino la ScriptaHub și începe din nou autentificarea.'],
  pl: ['Kończenie logowania… Możesz zamknąć to okno, jeśli pozostaje otwarte.', 'Wróć do ScriptaHub i rozpocznij logowanie ponownie.'],
};
let language = navigator.language?.split('-')[0];
try { language = localStorage.getItem('scripta-language') || language; } catch { /* Preferences are optional. */ }
if (!messages[language]) language = 'en';
document.documentElement.lang = language;
// Keep the response out of subsequent history/referrer navigation.
history.replaceState(null, '', location.pathname);
if (window.opener) {
  window.opener.postMessage({ type: CALLBACK_MESSAGE, url: responseUrl }, location.origin);
  document.getElementById('auth-callback-status').textContent = messages[language][0];
} else {
  document.getElementById('auth-callback-status').textContent = messages[language][1];
}
