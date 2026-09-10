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
 return {...art,objects,actions,connections,add,reveal,hide,move,label,link,finish};
}
