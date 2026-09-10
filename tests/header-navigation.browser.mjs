/* Run against the prebuilt site after build_books.py refresh; never plays audio. */
import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const session=await connect(base+'create/index.html?lang=ro');
let checks=0;
try {
  for(const route of ['index.html?lang=en','create/index.html?lang=ro','legal/privacy.html?lang=de','books/assistos/bk-c0f6d112218f4c52/en/book.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/Animation/index.html?lang=en']) {
    await session.send('Page.navigate',{url:new URL(route,base).href});
    await session.wait('document.querySelector("[data-home-link]") && document.querySelector(".brand-icon")?.complete');
    const expected=new URL(route,base).searchParams.get('lang');
    await session.wait(`new URL(document.querySelector('[data-home-link]').href).searchParams.get('lang')===${JSON.stringify(expected)}`);
    await session.wait(`document.querySelector('.site-header .wordmark').href===document.querySelector('[data-home-link]').href`);
    const state=await session.evaluate(`({home:document.querySelector('[data-home-link]').href,wordmark:document.querySelector('.site-header .wordmark').href,beforeCreate:document.querySelector('[data-home-link]').nextElementSibling.hasAttribute('data-create-link'),logo:document.querySelector('.brand-icon').naturalWidth,icons:document.querySelectorAll('link[rel="icon"]').length})`);
    assert.equal(new URL(state.home).pathname,'/index.html');assert.equal(state.home,state.wordmark);assert(state.beforeCreate);assert(state.logo>0);assert.equal(state.icons,2);checks+=5;
    for(const width of [1366,393,320]) {
      await session.size(width,768);
      const geometry=await session.evaluate(`({scroll:document.documentElement.scrollWidth,width:innerWidth,home:document.querySelector('[data-home-link]').getBoundingClientRect().toJSON(),create:document.querySelector('[data-create-link]').getBoundingClientRect().toJSON()})`);
      assert(geometry.scroll<=geometry.width,route+' no horizontal overflow at '+width);
      assert(geometry.home.right<=geometry.create.left+1,route+' Home precedes Create without overlap');checks+=2;
    }
  }
  await session.send('Page.navigate',{url:base+'reader/index.html?lang=ro'});
  await session.wait('document.querySelector("[data-reader-home]")?.title === "Acasă"');
  assert.equal(new URL(await session.evaluate('document.querySelector("[data-reader-home]").href')).search,'?lang=ro');checks++;
  console.log(JSON.stringify({checks,errors:session.errors.length}));
  assert.equal(session.errors.length,0);
} finally { await session.close(); }
