// Browser-side geometric evidence for labels printed on rectangular objects.
// Labels outside rectangles and semantic correspondence need separate review.
export function findLabelOverflow(svg){
 const visible=node=>{for(let n=node;n&&n!==svg.parentElement;n=n.parentElement){const style=getComputedStyle(n);if(style.display==='none'||style.visibility==='hidden'||Number(style.opacity)<.1)return false;}return true;};
 const failures=[];
 for(const text of svg.querySelectorAll('text')){
  if(!visible(text))continue;
  const box=text.getBoundingClientRect();if(!box.width||!box.height)continue;
  const x=(box.left+box.right)/2,y=(box.top+box.bottom)/2;
  const candidates=[...text.parentElement.children].filter(node=>node.tagName.toLowerCase()==='rect'&&visible(node)).map(node=>({node,box:node.getBoundingClientRect()})).filter(({box:r})=>x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom);
  candidates.sort((a,b)=>a.box.width*a.box.height-b.box.width*b.box.height);
  if(!candidates.length)continue;
  const r=candidates[0].box;
  const over={left:r.left-box.left,right:box.right-r.right,top:r.top-box.top,bottom:box.bottom-r.bottom};
  if(Object.values(over).some(value=>value>2))failures.push({id:text.id,text:text.textContent,backing:candidates[0].node.id,overflow:over});
 }
 return failures;
}
