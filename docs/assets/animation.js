(() => {
  'use strict';
  const collection = globalThis.SCRIPTA_COLLECTION;
  if (!collection) return;
  const root = new URL('../', document.currentScript.src);
  const words = {
    en: { back: 'Back to book', loading: 'Loading the presentation…', error: 'The presentation could not load. Reload this page to try again.', preview: 'Narrated presentation' },
    ro: { back: 'Înapoi la carte', loading: 'Se încarcă prezentarea…', error: 'Prezentarea nu s-a încărcat. Reîncarcă pagina pentru a încerca din nou.', preview: 'Prezentare cu narațiune' },
    fr: { back: 'Retour au livre', loading: 'Chargement de la présentation…', error: 'La présentation n’a pas pu être chargée. Rechargez la page pour réessayer.', preview: 'Présentation commentée' },
    de: { back: 'Zurück zum Buch', loading: 'Präsentation wird geladen…', error: 'Die Präsentation konnte nicht geladen werden. Laden Sie die Seite erneut.', preview: 'Präsentation mit Kommentar' },
    es: { back: 'Volver al libro', loading: 'Cargando la presentación…', error: 'No se pudo cargar la presentación. Vuelve a cargar la página.', preview: 'Presentación narrada' },
    pt: { back: 'Voltar ao livro', loading: 'A carregar a apresentação…', error: 'Não foi possível carregar a apresentação. Recarregue a página.', preview: 'Apresentação narrada' },
    it: { back: 'Torna al libro', loading: 'Caricamento della presentazione…', error: 'Impossibile caricare la presentazione. Ricarica la pagina.', preview: 'Presentazione narrata' },
    pl: { back: 'Powrót do książki', loading: 'Ładowanie prezentacji…', error: 'Nie udało się załadować prezentacji. Odśwież stronę.', preview: 'Prezentacja z narracją' }
  };
  const lang = () => words[document.documentElement.lang] ? document.documentElement.lang : 'en';
  const url = (file, language=lang()) => { const u=new URL(file,root);u.searchParams.set('lang',language);return u.href; };
  const book = collection.books.find(b => b.id === document.body.dataset.animationBook);
  if(!book?.animation)return;
  const shell=document.createElement('main');shell.className='site-shell animation-page';
  shell.innerHTML=`<header class="site-header"><a class="wordmark">ScriptaHub<span>.com</span></a><div class="header-tools"><a class="header-create" data-create-link>Create</a><div class="site-scale" aria-label="Site text size"><button type="button" data-site-smaller aria-label="Decrease site size">A−</button><button type="button" data-site-size aria-label="Reset site size">100%</button><button type="button" data-site-larger aria-label="Increase site size">A+</button></div><div class="theme-switcher" role="group" aria-label="Appearance"><button type="button" data-theme-choice="light" aria-label="Light appearance">☼</button><button type="button" data-theme-choice="dark" aria-label="Dark appearance">◐</button></div><label class="language-picker"><span class="sr-only">Language</span><select data-language-select></select></label></div></header><nav class="animation-navigation"><a class="button button-quiet" data-animation-back data-animation-text="back"></a></nav><section class="animation-player-floor"><p data-animation-status role="status"></p><shf-player id="film"></shf-player></section><section class="animation-feedback" data-workflow-content></section>`;
  document.body.prepend(shell);
  shell.querySelector('[data-create-link]').href=new URL('create/index.html',root).href;
  const player = shell.querySelector('shf-player');
  player.lang=book.animation.language;player.setAttribute('aria-label',book.title.en+' · Animation');
  let loadError=false, loaded=false;
  function localize() {
    if(!book||!player)return;
    const w=words[lang()];
    document.title=(book.title[lang()]||book.title.en)+' · Animation · ScriptaHub';
    for(const node of document.querySelectorAll('[data-animation-text]'))node.textContent=w[node.dataset.animationText];
    document.querySelector('[data-animation-back]').href=url(book.editions[lang()].book);
    const status=document.querySelector('[data-animation-status]');status.textContent=loadError?w.error:loaded?'':w.loading;status.hidden=loaded&&!loadError;
    document.querySelectorAll('.wordmark,.footer-wordmark').forEach(a=>a.href=url('index.html'));
  }
  if(book&&player){
    player.addEventListener('shf-loaded',()=>{loaded=true;loadError=false;localize();});
    player.addEventListener('shf-error',()=>{loadError=true;localize();});
    player.load(new URL(book.animation.shf,root).href).catch(()=>{loadError=true;localize();});
    const theme=()=>player.setTheme(['dark','dark-orange'].includes(document.documentElement.dataset.theme)?'night':'color');theme();
    new MutationObserver(theme).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  }
  document.addEventListener('scriptahub:language',localize);
  new MutationObserver(localize).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  localize();
})();
