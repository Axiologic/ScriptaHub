import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
// The imagined refund case makes the book's comparisons visible, without pretending these are product screens.
export function remainingVisual(i){
 const a=stageAuthor(),paper='#edf1e9',blue='#278da3',ink='#213b4b',copper='#bc673d',gold='#d9b85d',wood='#aa8267';
 const put=(id,x,y,n,b=1,m=id)=>{a.add(a.object(id,x,y,n,m));a.reveal(id,b,850);};
 const t=(s,x,y,z=28,c=ink)=>a.text(s,x,y,z,c),r=(x,y,w,h,c=paper)=>a.n('rect',{x,y,width:w,height:h,rx:7,fill:c});
 const person=(id,x,y,{b=1,identity='person-09-neutral',coat=blue,scale=.96,seated=false}={})=>{storyPerson(a,id,x,y,{identity,coat,scale,seated,chair:'#a6a3c4'});a.reveal(id,b);};
 const expression=(id,b,emotion)=>a.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1000});
 const parcel=(id,x,y,b=1)=>put(id,x,y,[a.n('path',{d:'M-88 -56H88V62H-88Z',fill:'#d8b88a'}),a.n('path',{d:'M-88 -56L-54 -91H121L88 -56Z',fill:'#e8cea1'}),a.n('path',{d:'M88 -56L121 -91V27L88 62Z',fill:'#b18b63'}),a.path('M-12 -56V62M-12 -56L22 -91',paper,17),r(22,-25,45,34,paper),a.path('M28 -13H57M28 -4H49',ink,2)],b,'A returned parcel gives the imagined refund request a material referent.');
 const receipt=(id,x,y,b=1,{complete=false,scale=1,title='Order receipt'}={})=>{a.add(a.object(id,x,y,[a.n('path',{d:'M-93 -104H93V111L75 101L57 111L39 101L21 111L3 101L-15 111L-33 101L-51 111L-69 101L-93 111Z',fill:paper}),t(title,0,-60,26),a.path('M-65 -32H65M-65 -7H39',blue,4),...(complete?[a.path('M-65 29H65M-65 51H39',blue,4)]:[r(-66,20,132,47,'#e9d1be'),t('Missing',0,51,24)])],complete?'The order record is present; this alone does not authorize payment.':'Inspection reveals missing evidence in the imagined order record.',scale));a.reveal(id,b);};
 const desk=(id,x,y,w=400)=>put(id,x,y,[r(-w/2,-13,w,26,wood),a.path(`M${-w/2+20} 15L${-w/2+5} 123M${w/2-20} 15L${w/2-5} 123`,wood,14)],1,'A supporting work surface for actual records and review.');
 const phone=(id,x,y,b=1)=>put(id,x,y,[r(-35,-64,70,128,ink),r(-27,-52,54,99,paper),a.dot(0,55,4,paper)],b,'A device in the customer’s hand carries the task request.');
 const payment=(id,x,y,b=2)=>put(id,x,y,[r(-137,-84,274,168,'#bfd4d8'),r(-119,-63,238,98,paper),t('Refund',0,-23,33),t('Pending approval',0,16,24),a.path('M-40 60H40',ink,8)],b,'Money-changing operation remains pending throughout the illustration.');
 const book=(id,x,y,b=1,scale=1)=>{a.add(a.object(id,x,y,[a.n('path',{d:'M-130 -93Q-66 -115 0 -93Q68 -115 130 -93V96Q68 76 0 97Q-67 76 -130 96Z',fill:paper}),a.path('M0 -90V96',blue,3),t('Architecture',-66,-39,22),t('Evidence',65,-39,22),a.path('M-105 -3H-26M-105 23H-26M-105 49H-40M25 -3H104M25 23H104M25 49H85',blue,3)],'An open reading spread supporting the task-based invitation; labels identify the book’s topics, not fabricated quotations.',scale));a.reveal(id,b);};
 if(i===0){
  person('customer',285,532,{identity:'person-04-neutral',coat:copper,seated:true});phone('customer-phone',352,376);parcel('parcel',542,476);
  put('request',713,238,[a.n('path',{d:'M-163 -52H163V55H-105L-151 80L-134 55H-163Z',fill:paper}),t('Return this order',0,9,30)],2,'The customer’s requested outcome, distinguished from permission to execute a payment.');
  payment('payment',972,412,3);put('review-hand',991,548,[t('Authority checked',0,0,29,'$ink')],4,'Consequential action requires its own authority.');
  storyGesture(a,'customer',2,'question');expression('customer',3,'curious');storyGesture(a,'customer',5,'reflect');
 }
 if(i===2){
  // An oversized receipt is inspected, then the missing part changes the active plan.
  receipt('receipt',312,318,1,{complete:false,scale:1.22});
  put('inspection',312,345,[a.path('M-88 -26H88M-88 43H88',copper,5)],3,'The validator isolates the missing-evidence region of the actual order record.');
  put('plan',859,300,[r(-198,-121,396,242),t('Next step',0,-75,32)],1);
 }
 if(i===5){
  person('reviewer',932,537,{coat:'#767ea5',seated:true});desk('review-desk',942,420,337);
  put('laptop',281,314,[r(-148,-99,296,192,blue),r(-131,-82,262,151,paper),t('Reply ready',0,-20,32),a.path('M-101 17H100M-101 43H66',blue,5),a.path('M-170 96H172',ink,13)],1,'A short ready-looking model answer hides the executed work around it.');
  receipt('first-lookup',524,333,2,{complete:true,scale:.63});receipt('repeated-lookup',525,333,3,{complete:true,scale:.63});a.move('repeated-lookup',3,736,338,3300);
  receipt('review-copy',1045,340,3,{complete:false,scale:.61});storyGesture(a,'reviewer',3,'reflect');expression('reviewer',3,'worried');
  put('clock',723,190,[a.dot(0,0,48,paper),a.path('M0 -29V0L24 16',copper,6)],3,'Time passes during repeated retrieval and review; no fabricated duration or cost amount is asserted.');
  a.hide('repeated-lookup',4);put('reuse-mark',525,350,[a.path('M-29 -2L-7 19L31 -26',blue,8)],4,'A constrained alternative reuses the valid record instead of retrieving it again.');
  put('cost-label',516,531,[t('Repeated work • Review time',0,0,30,'$ink')],3,'The visible work items are qualitative cost categories, not a quantitative benchmark.');
  expression('reviewer',4,'relieved');storyGesture(a,'reviewer',6,'question');
 }
 if(i===6){
  person('customer',227,532,{identity:'person-04-neutral',coat:copper});phone('customer-phone',294,376);parcel('returned-parcel',438,474);
  put('unexpected-request',484,172,[a.n('path',{d:'M-199 -47H199V51H-125L-175 76L-157 51H-199Z',fill:paper}),t('The order details are missing',0,9,26)],2,'An unfamiliar request lacks expected order evidence; this is an illustration of semantic uncertainty.');
  payment('payment',942,420,2);
  put('clarification',800,260,[a.n('path',{d:'M-218 -49H218V50H130L172 76L151 50H-218Z',fill:'#d6e4df'}),t('Can you share the receipt?',0,8,28)],4,'The bounded system asks for missing evidence without broadening payment authority.');a.hide('unexpected-request',4);
  storyGesture(a,'customer',3,'question');expression('customer',3,'worried');storyGesture(a,'customer',4,'explain');expression('customer',4,'relieved');
  put('boundary-note',941,548,[t('Approval still required',0,0,28,'$ink')],4,'Adaptable interpretation coexists with unchanged limits on side effects.');
 }
 if(i===7){
  // Technical representations are appropriate here, but tests visibly change a result.
  put('stable',275,299,[r(-177,-129,354,260),t('Stable procedure',0,-82,31),a.path('M-135 -40H135M-135 0H70M-135 40H115',blue,6),t('Tested version',0,92,25)],1,'Reusable code with a known version and assurance history.');
  put('generated',873,277,[r(-192,-108,384,224),t('Generated program',0,-63,31),a.path('M-121 -14L-143 10L-121 34M121 -14L143 10L121 34',copper,5),t('Isolated run',0,19,26)],2,'Task-adapted code is untrusted and remains under isolation and tests.');
  put('test-input',588,333,[r(-70,-30,140,60,'#dfd6ba'),t('Test input',0,8,23)],3,'A test record enters isolated evaluation, not production execution.');a.move('test-input',3,842,363,2000);
  put('held-result',876,460,[r(-160,-25,320,50,copper),t('Result held for checks',0,8,25,'#fff')],3,'Running generated code does not establish its correctness or authorize use.');
  for(const id of ['stable','generated','test-input','held-result'])a.hide(id,4);
  put('named',600,320,[r(-365,-145,730,290),t('Named working state',0,-95,35),t('order_id',-220,-22,27),t('eligibility',0,-22,27),t('approval',220,-22,27),t('Known',-220,44,25),t('Needs receipt',0,44,25),t('Pending',220,44,25)],4,'Illustrative named intermediate values rather than a transcript; not a claimed MRP-VM product screen.');
  put('question',600,520,[t('What improves under the same test?',0,0,30,'$ink')],5,'Comparative evidence remains necessary.');
 }
 if(i===8){
  person('reader',317,536,{coat:blue,seated:true});desk('reading-surface',425,415,429);book('reading-book',500,321,1,1);
  put('pencil',644,403,[a.path('M-31 0L27 -23',gold,8),a.path('M27 -23L37 -27',ink,4)],2,'The reader works through architecture and evaluation with a concrete task.');
  parcel('case-parcel',877,482,1);payment('case-payment',1003,245,2);
  put('annotation',728,330,[r(-102,-59,204,119,'#dfd4b4'),t('Evidence?',0,-18,27),t('Authority?',0,24,27)],3,'The same case is annotated with what would justify acting, not just with a broad autonomy slogan.');
  storyGesture(a,'reader',2,'reflect');expression('reader',4,'curious');storyGesture(a,'reader',5,'invite');
 }
 if(i===2){
  // Fill the revisable task record after the receipt inspection, preserving a single active next step.
  const plan=a.objects.find(o=>o.id==='plan');plan.visual.children=[r(-198,-121,396,242),t('Next step',0,-75,32),t('Prepare refund request',0,-17,27),a.path('M-145 17H145',blue,3),t('Evidence required',0,68,26)];
  put('revision',859,295,[r(-181,-38,362,78,'#dfd6ba'),t('Request the missing receipt',0,8,26)],3,'The observation changes the explicit next step instead of letting the plan proceed blindly.');
  put('handoff',719,489,[t('Review handoff',0,0,28,'$ink')],5,'Another reviewer or agent needs the same missing-evidence context.');
  person('second-reviewer',1116,533,{b:5,coat:'#767ea5',scale:.74});storyGesture(a,'second-reviewer',5,'question');
 }
 return a.finish(['A customer with a returned parcel asks through a device, while the proposed payment remains pending; an imagined task grounds the book’s engineering argument.','','An enlarged order receipt exposes missing evidence, changes the active next step and requires a review handoff. No refund is executed.','','','A ready-looking reply is surrounded by visible duplicate lookup documents, a review workstation and passing time; valid-record reuse removes duplicate work, without invented cost or latency figures.','An unfamiliar order lacks evidence; clarification adapts to the task while payment authority remains unchanged.','Stable code and isolated generated-code testing precede an illustrative named-state view; proposed runtime benefits remain comparative hypotheses.','A reader works through the book beside the same concrete returned-parcel case, annotating evidence and authority while payment stays pending.'][i]);
}
