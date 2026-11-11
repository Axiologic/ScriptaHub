import fs from'node:fs';
const specs=JSON.parse(fs.readFileSync('.book-work/ai-completion-20261111/film-specs.json'));
for(const spec of specs){const root='presentations/'+spec.slug,file=root+'/work/scenes.json',scenes=JSON.parse(fs.readFileSync(file));let changed=false;
 for(const scene of scenes)for(const object of scene.visual.objects){if(object.meaning==='symbols'){for(const child of object.visual.children||[])if(child.type==='text'){child.themeAttrs={...(child.themeAttrs||{}),night:{fill:'#cfdcdd'}};changed=true;}}}
 if(spec.slug==='exploring-formal-logic-an-ai-assisted-educational-journey'){
  const object=scenes[3].visual.objects.find(o=>o.id==='item-1');let serial=0;const n=(type,attrs,text)=>({id:'$asset.truth-'+(++serial),type,attrs,...(text?{text}:{})});const text=(v,x,y)=>n('text',{x,y,'font-size':22,'font-weight':600,'text-anchor':'middle',fill:'#183a41'},v);
  object.visual.children=[n('rect',{x:-120,y:-110,width:240,height:220,rx:8,fill:'#d9e3e4',stroke:'#365d80','stroke-width':5}),...[-40,30].map(x=>n('line',{x1:x,y1:-110,x2:x,y2:110,stroke:'#365d80','stroke-width':2})),...[-52,-10,30,70].map(y=>n('line',{x1:-120,y1:y,x2:120,y2:y,stroke:'#365d80','stroke-width':2})),...['P','Q','P⇒Q'].map((v,i)=>text(v,[-80,-5,75][i],-75)),...['TTT','TFF','FTT','FFT'].flatMap((row,j)=>[...row].map((v,i)=>text(v,[-80,-5,75][i],-22+j*40)))];object.meaning='A complete truth table for material implication, including the false T/F row.';
  const wet=scenes[1].visual.objects.find(o=>o.id==='label-1');wet.y+=25;changed=true;
 }
 if(changed)fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
}
console.log('Actual logical truth table, clear wet-street label, and readable Night symbols installed; narration unchanged.');
