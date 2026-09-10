// Reusable scene-construction verbs; layouts, palette and referents remain book-owned.
import {vectorArt} from './vector-story-art.mjs';
export function stageAuthor(){
 const art=vectorArt(),objects=[],actions=[],connections=[];
 const add=o=>(objects.push(o),o.id);
 const reveal=(id,beat,durationMs=1300)=>actions.push({actor:id,action:'appear',beat,durationMs});
 const hide=(id,beat)=>actions.push({actor:id,action:'disappear',beat,durationMs:1100});
 const move=(id,beat,x,y,durationMs=2000)=>actions.push({actor:id,action:'moveTo',beat,x,y,durationMs});
 const label=(id,value,x,y,size=32)=>add(art.object(id,x,y,[art.text(value,0,0,size)],value));
 const link=(id,from,to,beat,meaning,color='$ink')=>{connections.push({id,from:{node:from,anchor:'right'},to:{node:to,anchor:'left'},width:4,color,meaning});actions.push({actor:id,action:'connection.draw',beat,durationMs:1800});};
 const finish=meaning=>({objects,actions,connections,meaning});
 const person=(id,x,y,{coat='#496580',night='#a4bfd7',skin='#bd896c',hair='#393333',hairStyle='short',pose='attentive',scale=1}={})=>{
  const {n,tint,path,object}=art,low=pose==='concerned',open=pose==='open';
  return add(object(id,x,y,[
   tint(n('path',{d:low?'M-40 -16Q-9 -36 31 -12L49 106H-49Z':'M-35 -22Q0 -36 35 -22L49 106H-49Z',fill:coat}),night),
   n('ellipse',{cx:low?7:0,cy:low?-66:-76,rx:35,ry:43,fill:skin}),
   n('path',{d:hairStyle==='long'?'M-35 -57Q-51 -120 1 -126Q55 -120 35 -50L28 -98Q-2 -91 -26 -101L-27 -49Z':'M-34 -87Q-45 -131 1 -126Q42 -125 35 -86L19 -105Q-7 -92 -28 -103Z',fill:hair}),
   ...(hairStyle==='long'?[n('ellipse',{cx:36,cy:-61,rx:16,ry:22,fill:hair})]:[]),
   path(low?'M-11 -70L-2 -68M16 -68L25 -71':'M-17 -82H-9M10 -82H18','#241e1b',3),
   path(low?'M-7 -44Q7 -52 22 -43':'M-11 -54Q0 -46 12 -54','#241e1b',3),
   path(open?'M-35 -9Q-80 14 -94 -19':'M-35 -9Q-59 43 -15 58','$ink',9),
   path(open?'M35 -9Q73 -26 99 -68':low?'M35 -9Q67 32 13 49':'M35 -9Q56 32 77 9','$ink',9),
   path('M-24 106L-33 154M24 106L33 154','$ink',19),
   path('M-33 155H-54M33 155H54','$ink',12),
   path('M-14 8L8 12L2 72','$ink',2)
  ],'Stylized person: '+pose,scale));
 };
 return {...art,objects,actions,connections,add,reveal,hide,move,label,link,finish,person};
}
