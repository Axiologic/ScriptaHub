import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {scriptHash} from './marketing-review.mjs';

export async function setMigrationStage(project,stage,status,detail={}){
  const file=path.join(project,'work/migration-state.json');
  const data=await fs.readFile(file,'utf8').then(JSON.parse).catch(error=>{
    if(error.code==='ENOENT')return {version:1,stages:{}};
    throw error;
  });
  const scenes=JSON.parse(await fs.readFile(path.join(project,'work/scenes.json'),'utf8'));
  data.updatedAt=new Date().toISOString();
  data.stages[stage]={status,updatedAt:data.updatedAt,scriptSha256:scriptHash(scenes),...detail};
  await fs.writeFile(`${file}.${process.pid}.tmp`,JSON.stringify(data,null,2)+'\n');
  await fs.rename(`${file}.${process.pid}.tmp`,file);
}

export async function refreshMigrationStatus(){
  await new Promise((resolve,reject)=>{
    const child=spawn(process.execPath,['tools/shf/update-voice-migration-status.mjs'],{stdio:'inherit'});
    child.on('exit',code=>code===0?resolve():reject(new Error(`Status refresh exited ${code}`)));
    child.on('error',reject);
  });
}

export async function trackMigrationStage(project,stage,operation){
  await setMigrationStage(project,stage,'running',{pid:process.pid});
  await refreshMigrationStatus();
  try {
    const result=await operation();
    await setMigrationStage(project,stage,stage==='voice'?'generated':'built',{note:stage==='voice'?'Listening review pending.':'Visual inspection pending.'});
    await refreshMigrationStatus();
    return result;
  }catch(error){
    await setMigrationStage(project,stage,'failed',{error:error.message});
    await refreshMigrationStatus();
    throw error;
  }
}
