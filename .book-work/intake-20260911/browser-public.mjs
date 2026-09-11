import {connect} from '../../tests/browser-session.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const workspace=path.resolve(process.argv[2]), release=JSON.parse(await fs.readFile(path.join(workspace,'release.json'),'utf8'));
const root=path.resolve('docs',release.directory),qa=path.join(workspace,'qa');
const results=[];
for(const page of ['ro/book.html','en/full_content.html','ro/full_content.html','en/short_content.html','ro/short_content.html']){
 const c=await connect('about:blank');
 try {await c.send('Network.enable');await c.send('Network.setBlockedURLs',{urls:['http://*','https://*']});await c.send('Page.navigate',{url:pathToFileURL(path.join(root,page)).href+'?lang=ro'});await c.wait('document.readyState==="complete"');
 for(const width of [1280,390]) {await c.size(width,900);await c.evaluate('document.fonts.ready');const data=await c.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,title:document.title,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length})');results.push({page,width,...data,errors:c.errors});if(data.scroll>width+1||data.brokenImages||c.errors.length)throw Error(JSON.stringify(results.at(-1)));await c.capture(path.join(qa,page.replaceAll('/','-')+'-'+width+'.png'));}
 }finally{await c.close()}
}
await fs.writeFile(path.join(qa,'browser-public-review.json'),JSON.stringify(results,null,2)+'\n');console.log('Passed '+results.length+' browser page/viewport checks');
