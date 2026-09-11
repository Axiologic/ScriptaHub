import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// Write beside the destination, then replace it in one rename. Readers therefore
// see either the previous complete artifact or the new complete artifact.
export function atomicWriteFile(file, data){
  fs.mkdirSync(path.dirname(file), {recursive:true});
  const temporary=`${file}.${process.pid}.${Date.now()}.${crypto.randomBytes(6).toString('hex')}.tmp`;
  try {
    fs.writeFileSync(temporary, data, {flag:'wx'});
    fs.renameSync(temporary, file);
  } finally {
    try { fs.unlinkSync(temporary); } catch (error) { if(error.code!=='ENOENT') throw error; }
  }
}
