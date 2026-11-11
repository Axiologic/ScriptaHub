import fs from'node:fs';import{spawnSync}from'node:child_process';
const specs=JSON.parse(fs.readFileSync('.book-work/ai-completion-20261111/film-specs.json')),worker=Number(process.argv[2]||0);
for(const [i,spec]of specs.entries()){
 if(i%2!==worker)continue;
 const root='presentations/'+spec.slug;if(!fs.existsSync(root+'/work/voice-receipts.json'))continue;
 const state=JSON.parse(fs.readFileSync(root+'/work/migration-state.json'));if(state.stages.voice?.status==='running')continue;
 for(const [command,args]of [[process.execPath,[root+'/build.mjs','--output='+root+'/output']],[process.execPath,['tools/shf/qa-film.mjs',root]]]){
  const result=spawnSync(command,args,{stdio:'inherit',env:process.env});if(result.status!==0)throw Error('Film QA failed for '+spec.slug);
 }
 console.log('MEASURED QA READY',spec.slug);
}
