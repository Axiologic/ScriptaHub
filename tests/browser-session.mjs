import fs from 'node:fs/promises';
export async function connect(url){
 const endpoint=process.env.SCRIPTA_CDP_URL||'http://127.0.0.1:9222';
 const t=await (await fetch(endpoint+'/json/new?'+encodeURIComponent(url),{method:'PUT'})).json();
 const ws=new WebSocket(t.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let id=0;const pending=new Map(),errors=[],listeners=new Map();
 ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else{if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);for(const fn of listeners.get(m.method)||[])fn(m.params);}});
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 await send('Runtime.enable');await send('Page.enable');
 const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 const wait=async expression=>{for(let i=0;i<120;i++){if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,250));}throw Error('Timed out: '+expression);};
 const size=async(width,height)=>send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<600});
 const capture=async(file)=>{const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(file,Buffer.from(r.data,'base64'));};
 return {send,evaluate,wait,size,capture,errors,on:(event,fn)=>{if(!listeners.has(event))listeners.set(event,[]);listeners.get(event).push(fn);},close:async()=>{try{await evaluate('document.querySelectorAll("shf-player").forEach(p=>{p.setMuted(true);p.pause()})')}finally{ws.close();await fetch(endpoint+'/json/close/'+t.id)}},id:t.id};
}
