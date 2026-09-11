#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {atomicWriteFile} from './atomic-write.mjs';

// A separate reader must never observe a partial archive during replacement.
const directory=fs.mkdtempSync(path.join(os.tmpdir(),'shf-atomic-'));
const target=path.join(directory,'film.shf');
const bytes=1024*1024;
let reader;
try {
  atomicWriteFile(target,Buffer.alloc(bytes,65));
  reader=spawn(process.execPath,['--input-type=module','-e',`
    import fs from 'node:fs';
    const file=process.argv[1], bytes=Number(process.argv[2]);
    process.send('ready');
    let reads=0,stopped=false;
    process.on('message',()=>{stopped=true});
    function inspect(){
      const data=fs.readFileSync(file); const value=data[0];
      if(data.length!==bytes||![65,66].includes(value)||data.some(byte=>byte!==value))process.exit(2);
      reads++;
      if(stopped){process.send({reads});process.disconnect();return;}
      setImmediate(inspect);
    }
    inspect();
  `,target,String(bytes)],{stdio:['ignore','ignore','inherit','ipc']});
  const done=new Promise((resolve,reject)=>{reader.once('error',reject);reader.once('exit',code=>code===0?resolve():reject(Error('Concurrent reader observed incomplete publication: '+code)));});
  await new Promise(resolve=>reader.once('message',resolve));
  let observations=0;reader.on('message',value=>{if(value?.reads)observations=value.reads});
  for(let i=0;i<24;i++){
    atomicWriteFile(target,Buffer.alloc(bytes,i%2?65:66));
    await new Promise(resolve=>setTimeout(resolve,2));
  }
  reader.send('stop');await done;
  if(!observations)throw Error('No concurrent observations');
  if(fs.readdirSync(directory).some(name=>name.endsWith('.tmp')))throw Error('Temporary publication file remained');
  console.log(JSON.stringify({valid:true,replacements:24,concurrentReads:observations,bytes}));
} finally { if(reader?.exitCode===null)reader.kill();fs.rmSync(directory,{recursive:true,force:true}); }
