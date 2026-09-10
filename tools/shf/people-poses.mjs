// Neutral pose adaptation; each film authors the situation, palette and blocking.
import {ASSETS} from '../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';
export function storyPerson(q,id,x,y,{identity='person-02-neutral',coat='#558f7d',seated=false,scale=.88,chair='#558f7d',ink='#35445c'}={}){
 const {n,path}=q;let visual=ASSETS[identity]('$asset',{coat,dynamicExpressions:true});
 visual.children=visual.children.filter(p=>p.id!=='$asset.shadow');
 if(seated){
  for(const [part,d]of [['legL','M-20 -82L-46 -53L-40 -10H-60'],['legR','M18 -82L46 -53L43 -10H65']])visual.children.find(c=>c.id==='$asset.'+part).children=[{...path(d,ink,20),id:'$asset.'+part+'.bent'}];
  visual.children.unshift({...n('g'),children:[n('path',{d:'M-76 -183Q0 -210 76 -183L70 -65H-70Z',fill:chair}),path('M-80 -68H80M-70 -66V0M70 -66V0',ink,9)]});
 }
 // Dark stage needs independent lower-body contrast; facial ink remains dark.
 const nightLeg=node=>{for(const key of ['fill','stroke'])if(node.attrs?.[key]&&node.attrs[key]!=='none')node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:'#9aafc3'}};for(const child of node.children||[])nightLeg(child);};
 for(const part of visual.children)if(part.id==='$asset.legL'||part.id==='$asset.legR')nightLeg(part);
 if(seated){const chairNode=visual.children[0];for(const child of chairNode.children||[])if(child.attrs?.stroke&&child.attrs.stroke!=='none')child.themeAttrs={night:{stroke:'#9aafc3'}};}
 return q.add({id,asset:'custom',x,y,scale,visual,meaning:'Expressive participant in an authored illustrative situation, not a historical portrait.',options:{rig:'character'}});
}
export function storyGesture(q,id,beat,gesture,durationMs=1900){q.actions.push({actor:id,action:'character.gesture',gesture,beat,durationMs});}
