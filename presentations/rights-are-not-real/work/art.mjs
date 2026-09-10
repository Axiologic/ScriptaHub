import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#46545f',B='#b75d48',AN='#becdd5',BN='#f0b39f';
 const door=(id,x,y)=>add(object(id,x,y,[tint(path('M-90 170V-170H90V170',A,18),AN)],'An access route exists in law but requires working protection.'));
 const leaf=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-70,y:-150,width:140,height:320,fill:B}),BN),tint(dot(45,20,9,A),AN)],'The route can remain closed despite a valid entitlement.'));
 const pass=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-90,y:-60,width:180,height:120,rx:10,fill:A}),AN),tint(path('M-40 0L-10 30L45 -35',B,11),BN)],'A recognized entitlement remains distinct from actual protection.'));
 switch(i){
 case 0:pass('pass',330,300);door('door',870,300);leaf('leaf',870,300);move('pass',2,610,300);hide('leaf',4);break;
 case 1:add(object('moral',255,300,[tint(n('path',{d:'M0 85C-170 -15 -50 -110 0 -40C50 -110 170 -15 0 85Z',fill:B}),BN)],'A moral claim can survive denial by existing legal institutions.'));pass('legal',600,300);door('protection',970,300);label('m','Moral claim',255,500,30);label('l','Legal recognition',600,500,30);label('p','Protection',970,520,30);reveal('legal',2);reveal('l',2);reveal('protection',3);reveal('p',3);break;
 case 2:add(object('lever',550,315,[tint(path('M-200 80H200M0 80V-70M-135 -110L135 -30',A,20),AN)],'Organized power can act but needs independent limits.'));add(object('brake',860,285,[tint(n('path',{d:'M-75 -75H75V75H-75Z',fill:B}),BN),tint(path('M-35 0H35',A,14),AN)],'Counterpower constrains the protector rather than merely trusting intentions.'));reveal('brake',3);move('brake',4,765,285);break;
 case 3:door('door',800,300);pass('pass',320,330);move('pass',3,600,330,2200);add(object('support',800,515,[tint(path('M-145 0H145M-110 0V-45M110 0V-45',B,18),BN)],'Protection is sustained by coordinated institutions rather than a declaration alone.'));reveal('support',2);break;
 }
 s.visual=q.finish('Charcoal and vermilion civic thresholds: the moral claim, legal pass and working route remain distinct, while a brake constrains protective power.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
