/* Derive a simplified full-body logo from the actual mascot, never a head crop. */
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import '../../docs/assets/librarian-mascot.js';
const mascot=globalThis.ScriptaMascot.visual('happy');
// Keep the complete silhouette, book, vest, spectacles and both feet.
// Omit only micro-detail that turns into noise at favicon sizes.
function simplify(node, spectacles=false) {
  if (node.opacity===0 || (node.type==='circle' && node.attrs.r<=3)) return null;
  spectacles ||= node.id==='$asset.spectacles';
  if (node.type==='path' && node.attrs.fill==='none' && node.attrs['stroke-width']<=2.5 && !spectacles) return null;
  const result={...node,attrs:{...node.attrs}};
  if (spectacles && result.attrs.stroke) result.attrs['stroke-width']=5;
  if (node.children) result.children=node.children.map(child=>simplify(child,spectacles)).filter(Boolean);
  return result;
}
const logo=simplify(mascot);
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const render=node=>node.opacity===0?'':`<${node.type} ${Object.entries(node.attrs).map(([key,value])=>`${key}="${escape(value)}"`).join(' ')}>${node.text?escape(node.text):''}${(node.children||[]).map(render).join('')}</${node.type}>`;
const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="-114 -338 228 350"><title>ScriptaHub librarian</title>${render(logo)}</svg>\n`;
await fs.writeFile(fileURLToPath(new URL('../../docs/assets/librarian-icon.svg',import.meta.url)),svg);
const themePalettes={
 orange:{'#50746e':'#916344','#163e3b':'#4d2d17','#133633':'#402619','#b8e1cc':'#f5d7b4','#245e54':'#9c471d','#12584f':'#843913'},
 nord:{'#50746e':'#6d5f65','#163e3b':'#493c43','#133633':'#382f34','#b8e1cc':'#ded5ce','#245e54':'#8d6674','#12584f':'#684653'},
};
for(const [theme,palette] of Object.entries(themePalettes)){
 const themedSvg=svg.replace(/#[0-9a-f]{6}/gi,color=>palette[color.toLowerCase()]||color);
 await fs.writeFile(fileURLToPath(new URL(`../../docs/assets/librarian-icon-${theme}.svg`,import.meta.url)),themedSvg);
}
const asset=name=>fileURLToPath(new URL('../../docs/'+name,import.meta.url));
execFileSync('magick',['-background','none',asset('assets/librarian-icon.svg'),'-resize','192x192','-gravity','center','-extent','192x192',asset('assets/librarian-icon.png')]);
execFileSync('magick',[asset('assets/librarian-icon.png'),'-define','icon:auto-resize=48,32,16',asset('favicon.ico')]);
console.log('Derived SVG, 192px PNG and 16/32/48px ICO from ScriptaMascot.visual().');
