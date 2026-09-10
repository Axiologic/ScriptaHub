import fs from 'node:fs';import path from 'node:path';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.resolve('presentations/ai-agents');const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));
const C={ink:'#273855',indigo:'#454779',orange:'#e8914a',jade:'#3a9d91',pale:'#efefdc',violet:'#947bc7',muted:'#c5ccdc',white:'#fffaf0'};
function compose(i){const a=stageAuthor();const put=(id,x,y,z,b=1,m=id,scale=1)=>{a.add(a.object(id,x,y,z,m,scale));a.reveal(id,b,650);};const rect=(x,y,w,h,fill,rx=0)=>a.n('rect',{x,y,width:w,height:h,rx,fill});const label=(s,x,y,size=28,color=C.ink)=>a.text(s,x,y,size,color);const line=(d,c=C.ink,w=5)=>a.path(d,c,w);const disappear=(id,b)=>a.actions.push({actor:id,action:'disappear',beat:b,durationMs:150});
const person=(id,x,y,coat,identity='person-15-neutral',scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,scale});a.reveal(id,1,650)};
const analyser=(id,x,y,scale=1)=>put(id,x,y,[a.n('path',{d:'M-170 85V-84Q-170 -105 -147 -105H86L155 -49V85Z',fill:C.pale}),a.n('path',{d:'M86 -105V-49H155',fill:C.muted}),rect(-145,-82,169,94,C.indigo,8),a.n('path',{d:'M-122 -54H-1L-15 -7H-132Z',fill:'#bde0d8'}),line('M-116 -43H-29M-119 -28H-55',C.jade,5),rect(69,-24,22,86,C.orange,5),rect(-190,56,145,38,C.indigo,3),...[-170,-140,-110,-80].flatMap(xx=>[rect(xx,20,13,41,C.white,5),rect(xx,17,13,9,C.violet,2)]),a.dot(117,22,9,C.jade),rect(-133,66,70,23,C.orange,2),label('M-17',-98,83,19),line('M-159 87H142',C.indigo,8)],1,'Same fictional laboratory analyser: sample tray, orange latch and M-17 tag preserve incident identity.',scale);
if(i===0){
put('lab',600,395,[a.n('path',{d:'M-480 -150H460V90H-480Z',fill:'#e4e7df'}),a.n('path',{d:'M-480 90H460L500 124H-520Z',fill:C.muted}),line('M-470 124V183M455 124V183',C.indigo,11)],1,'Continuous laboratory bench anchors instrument and upload workstation');
analyser('device',395,375,.95);person('technician',170,575,C.jade);storyGesture(a,'technician',2,'reflect');storyGesture(a,'technician',4,'explain');
put('workstation',850,342,[rect(-147,-89,294,169,C.indigo,13),rect(-129,-71,258,131,C.white,6),line('M-28 80V104M-81 104H78',C.indigo,10),label('Measurements',0,-36,29),...[-77,-12,53].map(xx=>rect(xx,-5,45,42,'#e7e6df',3))],1,'Powered instrument has missing uploads; blank measurement slots do not imply a broken power connection');
put('missing',850,362,[label('No upload',0,15,28,C.indigo)],2,'The source opening incident concerns missing uploads overnight');
put('incident',730,493,[a.n('path',{d:'M-107 -55H96L112 -39V55H-107Z',fill:C.white}),rect(-107,-55,55,23,C.orange),label('M-17',-78,-37,18),label('Support incident',0,0,25),line('M-75 22H69',C.jade,4)],3,'Incident becomes bounded support work');a.move('incident',5,1010,493,1700);
}
if(i===1){
put('surface',590,380,[a.n('path',{d:'M-495 -177H469L503 182H-522Z',fill:'#e4e7df'})],1,'Close view of the same device and the concrete approval transaction');analyser('device',310,370,1.07);
put('evidence',805,300,[a.n('path',{d:'M-154 -114H138L157 -95V128H-154Z',fill:C.white}),rect(-154,-114,69,29,C.orange),label('M-17',-119,-92,23),label('Account • telemetry',0,-53,26),label('Firmware • guidance',0,-13,26),line('M-118 16H112',C.muted,4)],2,'Evidence belongs to the matching device rather than an arbitrary case');
put('read-only',805,361,[label('Read-only first',0,0,27,C.indigo)],2);disappear('read-only',4);
put('proposed-action',805,361,[label('Restart • T-1',0,0,27,C.indigo)],4);
put('restart-control',580,490,[rect(-108,-37,216,76,C.indigo,13),label('Restart',0,10,29,C.white)],4,'Restart is introduced only in the later privileged design');
put('guard',580,477,[a.n('path',{d:'M-122 53V-57Q0 -96 122 -57V53',fill:'none',stroke:C.orange,'stroke-width':13}),label('Await approval',0,-43,24,C.ink)],4,'Proposed action is held for an actual reviewer');
put('review-hand',1070,400,[a.n('path',{d:'M170 -150L56 -70L15 1L-40 15L-56 29L-45 43L20 25L76 -28L186 -75Z',fill:'#c69276'}),a.n('path',{d:'M190 -167L66 -91L99 -23L219 -61Z',fill:C.violet})],4,'Reviewer inspects the transaction and supporting evidence');
put('approval',823,396,[rect(-126,-30,252,67,C.jade,5),label('Approved • T-1',0,12,27,C.white)],5,'Explicit approval is persisted with the proposed action');disappear('guard',5);
}
if(i===2){
put('devicebench',342,445,[a.n('path',{d:'M-210 44H207L233 75H-237Z',fill:C.muted}),line('M-210 76V117M207 76V117',C.indigo,9)],1);analyser('device',330,390,1.06);
put('done',330,276,[rect(-141,-37,282,61,C.jade,5),label('Restart recorded',0,3,28,C.white)],1,'Illustrative completed effect; source runtime must query current state before any repeat');
put('worker',887,301,[rect(-168,-114,336,235,C.indigo,16),rect(-147,-88,294,153,'#202c41',8),label('Worker offline',0,-19,31,'#e6e7f1'),line('M-13 13L13 39M13 13L-13 39',C.orange,6),line('M-35 122V151M-107 151H109',C.indigo,10)],1,'Worker crash does not erase device state or imply the restart did not occur');
put('saved',864,506,[rect(-194,-43,388,98,C.pale,6),rect(-194,-43,81,27,C.orange,3),label('M-17',-153,-22,22),label('Saved task • T-1',22,-6,28),label('Action + approval + evidence',0,28,23)],2,'Checkpoint and transaction identify continuing logical work independently of worker lifetime');
put('query',622,352,[line('M166 4H-141',C.jade,7),line('M-121 -11L-141 4L-121 19',C.jade,7),rect(-85,-35,198,40,C.white,4),label('Check device',15,-7,25)],3,'Explicit observation reaches the physical device before another privileged action');
put('repeat',670,467,[rect(-97,-29,194,58,C.white,6),label('Restart again',0,8,24),line('M-87 20L85 -20',C.orange,7)],4,'A checked existing effect prevents a blind repeated operation');
put('resumed',887,294,[rect(-145,-74,290,148,C.white,7),label('Task resumed',0,-24,30),label('T-1 reconciled',0,22,26,C.jade)],5,'The resolved recovery is represented as a bounded illustrative run, not an empirical performance guarantee');
}
if(i===3){
put('reviewtable',620,404,[a.n('path',{d:'M-412 -126H339L389 159H-442Z',fill:'#e4e7df'}),a.n('path',{d:'M-442 159H389V181H-442Z',fill:C.indigo})],1,'Incident review returns every claim to an ordered account of what happened');person('technician',140,576,C.jade);person('reviewer',1083,574,C.violet,'person-20-neutral');storyGesture(a,'technician',1,'explain');storyGesture(a,'reviewer',2,'reflect');storyGesture(a,'reviewer',5,'resolve');
put('trace',615,352,[a.n('path',{d:'M-347 -47H296L325 -23V70H-347Z',fill:C.white}),rect(-347,-47,69,26,C.orange),label('M-17',-312,-27,20),line('M-273 25H256',C.jade,5),...[-258,-90,82,250].map(x=>a.dot(x,25,7,C.jade)),label('Evidence',-259,3,24),label('Approval',-90,3,24),label('Restart',82,3,24),label('State check',244,3,24)],1,'The same incident is a trajectory, not merely a well-written final response');
put('response',805,475,[rect(-121,-37,242,83,C.white,4),label('Final response',0,-5,25),line('M-94 17H80M-94 31H31',C.muted,4)],2,'Final wording occupies one end of the work and cannot replace checking the run');
put('cost',586,480,[rect(-98,-44,196,97,C.orange,3),label('Outcome cost',0,-10,24),label('Review + retries',0,26,22)],3,'Economic accounting includes supporting work, not only a model call');
put('book',334,482,[a.n('path',{d:'M-82 -75Q-42 -87 -1 -67Q38 -87 83 -75V72Q44 59 0 76Q-39 59 -82 72Z',fill:C.white}),line('M0 -67V74',C.indigo,4),line('M-71 -57H-16M14 -57H70',C.jade,3),label('AI',-39,-22,25,C.indigo),label('Agents',-40,6,20,C.indigo),label('Evaluation',43,-7,17),line('M13 15H71M13 29H64M13 43H70',C.muted,3)],4,'Reading route opens the evaluation chapter beside the same incident evidence');
}
for(const actor of a.objects.filter(o=>o.options?.rig==='character'))for(const [beat,emotion]of [[1,'curious'],[3,'skeptical'],[5,'determined']])a.actions.push({actor:actor.id,action:'character.express',emotion,beat,durationMs:700});
return a.finish('Laboratory incident atlas follows one fictional device through authority, interruption, reconciliation and trajectory review; no empirical measured result is invented.');}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);fs.writeFileSync(path.join(root,'work/scenes.json'),JSON.stringify(scenes,null,2)+'\n');
