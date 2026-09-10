import fs from 'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';import{storyPerson,storyGesture}from'../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,path,text,dot,object,add,reveal,hide,move,label}=q,ink='#394b68',gold='#d9a441',blue='#729dbc',red='#c87563',green='#70a18a',cream='#f2e6cd';const shape=(d,fill)=>n('path',{d,fill});
 const person=(id,x,y,c,scale=.6,identity='person-02-neutral')=>storyPerson(q,id,x,y,{coat:c,scale,identity});
 const gesture=(id,b,g)=>storyGesture(q,id,b,g);
 function apartment(id,x,y,c){add(object(id,x,y,[shape('M-115 -115H115V155H-115Z',c),shape('M-95 -96H95V140H-95Z',cream),path('M-95 142H95',ink,10),n('rect',{x:-85,y:90,width:80,height:50,rx:4,fill:gold}),path('M-70 87V40',green,8),shape('M-70 66Q-105 36 -70 45Q-38 8 -42 48Z',green)],'A domestic cutaway makes individually held perceptions separate but adjacent.'));}
 function paper(id,x,y,{rough=true,word='Observation',scale=1}={}){add(object(id,x,y,[shape(rough?'M-92 -117H63V-68H94V-17H63V117H-92Z':'M-92 -117H92V117H-92Z',cream),text(word,-7,-72,25,ink),path('M-64 -27H45M-64 10H30M-64 47H42',ink,6),...(rough?[shape('M63 -68H94V-17H63Z',red),dot(-43,85,10,gold)]:[])],'The manuscript’s irregular feature carries a potentially meaningful distinction.',scale));}
 switch(i){
 case 0:
  for(let j=0;j<3;j++){const x=300+j*300;apartment('room'+j,x,310,[blue,red,green][j]);person('resident'+j,x+15,442,[red,green,blue][j],.69,j===1?'person-04-neutral':'person-02-neutral');add(object('curtain'+j,x,305,[shape('M-108 -105H108V138H-108Z',ink)],'A privacy screen prevents people from seeing what others recognize.'));hide('curtain'+j,j+2);gesture('resident'+j,j+2,'question');}
  break;
 case 1:
  add(object('courtyard',600,455,[n('ellipse',{cx:0,cy:0,rx:410,ry:88,fill:'#bdd5bf'}),path('M-320 0H320',cream,14)],'A shared public meeting place makes the same signal mutually visible.'));
  person('speaker',595,445,red,.96,'person-04-neutral');person('listener1',330,475,blue,.85);person('listener2',870,475,green,.85,'person-09-neutral');
  add(object('notice',600,115,[shape('M-105 -52H105V65H-105Z',gold),text('Meeting today',0,16,28,ink)],'An illustrative public invitation can change expectations about participation.'));reveal('notice',2);gesture('speaker',2,'invite');gesture('listener1',3,'question');gesture('listener2',4,'resolve');move('listener1',4,440,475,1800);move('listener2',4,765,475,1800);break;
 case 2:
  add(object('press',600,385,[path('M-180 100V-110H180V100',ink,17),n('rect',{x:-145,y:-60,width:290,height:80,rx:40,fill:blue}),n('rect',{x:-145,y:30,width:290,height:65,rx:32,fill:gold}),path('M-225 113H225',ink,12),dot(120,-20,18,red)],'A physical editorial press illustrates AI smoothing, not literal computational mechanics.'));
  paper('original',225,285,{rough:true,word:'Exception',scale:.8});move('original',2,525,385,2300);hide('original',3);paper('smoothed',930,360,{rough:false,word:'Clean copy',scale:.8});reveal('smoothed',3);
  add(object('discard',675,505,[shape('M-14 -30H17V21H-14Z',red)],'A decision-relevant exception has been removed from the fluent output.'));reveal('discard',3);label('exception','Missing exception',675,560,27);reveal('exception',4);break;
 case 3:
  person('editor',325,500,green,1,'person-04-neutral');gesture('editor',2,'reflect');gesture('editor',4,'question');
  add(object('workbench',745,455,[shape('M-255 -115H225L265 -75H-255Z',gold),path('M-235 -75V85M240 -75V85',ink,14)],'The reader tests a filtering process through a concrete comparison.'));
  paper('rough',625,342,{rough:true,word:'Source',scale:.58});paper('clean',850,342,{rough:false,word:'Output',scale:.58});
  add(object('margin',745,440,[shape('M-90 -35H90V35H-90Z',red),text('What disappeared?',0,8,24,'#fff8e9')],'The comparison asks what was lost without assuming every rejected idea was valuable.'));reveal('margin',3);gesture('editor',5,'invite');break;
 }
 s.visual=q.finish('Colorful domestic cutaways open into a shared courtyard; an editorial press physically loses a meaningful exception; a reader inspects both source and output. These are authored conceptual situations, not historical reconstructions.');
}fs.writeFileSync(file,JSON.stringify(scenes,null,2));
