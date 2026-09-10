// Tiny authoring helpers for original vector stories; no book-specific scene templates.
export function vectorArt(){let serial=0;const n=(type,attrs={},text)=>({id:'$asset.part'+(++serial),type,attrs,...(text===undefined?{}:{text})});
 const tint=(node,night)=>({...node,themeAttrs:{night:{[node.attrs.fill&&node.attrs.fill!=='none'?'fill':'stroke']:night}}});
 const path=(d,color,width=8)=>n('path',{d,fill:'none',stroke:color,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round'});
 const text=(value,x=0,y=0,size=30,color='$ink')=>n('text',{x,y,'font-size':size,'font-weight':size>=32?700:600,'letter-spacing':-.3,'text-anchor':'middle',fill:color},value);
 const dot=(x,y,r,color)=>n('circle',{cx:x,cy:y,r,fill:color});
 const object=(id,x,y,children,meaning,scale=1)=>({id,asset:'custom',x,y,scale,meaning,visual:{id:'$asset',type:'g',attrs:{},anchors:{left:[-70,0],right:[70,0],top:[0,-70],bottom:[0,70]},children}});
 const knot=(id,x,y,color,night,label='',scale=1,form='open')=>{
  const curves=form==='woven'?['M-68 0 C-68 -105 68 -105 68 0 S-68 105 -68 0','M0 -67 C100 -67 100 67 0 67 S-100 -67 0 -67']:['M-79 -10 C-106 -98 12 -106 32 -52 C100 -102 123 11 66 34 C62 110 -45 113 -62 49 C-112 65 -118 -1 -79 -10Z'];
  const result=object(id,x,y,[...curves.map(d=>tint(path(d,color,13),night)),tint(dot(0,0,13,color),night),...(label?[text(label,0,116,30)]:[])],label?`Abstract process identity: ${label}; no body or literal physical location.`:'A possible conscious process, illustrated relationally.',scale);
  const extent=form==='woven'?82:108;result.visual.anchors={left:[-extent,0],right:[extent,0],top:[0,-90],bottom:[0,90]};return result;
 };
 return {n,tint,path,text,dot,object,knot};
}
