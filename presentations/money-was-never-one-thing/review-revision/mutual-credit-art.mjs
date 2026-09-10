import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
export function mutualCreditArt(){
 const q=stageAuthor(),{n,path,text,object,add,label,reveal,hide,move}=q;
 const ink='#293e49',plum='#82495d',teal='#317b78',cream='#f6ead4';
 const member=(id,x,name,kind)=>{
 const contents=kind==='wood'?[n('path',{d:'M-66 0H66V18H-66Z',fill:'#c5935e'}),path('M-48 18V67M48 18V67',ink,9)]:kind==='accounts'?[n('rect',{x:-53,y:-10,width:106,height:78,rx:4,fill:cream}),path('M-35 12H34M-35 29H34M-35 46H12',teal,5)]:[n('rect',{x:-58,y:-9,width:116,height:69,rx:5,fill:ink}),n('rect',{x:-46,y:1,width:92,height:48,fill:'#c3e4df'}),path('M-25 74H25M0 61V74',ink,6)];
 add(object(id,x,200,[n('rect',{x:-135,y:-48,width:270,height:162,rx:7,fill:cream}),text(name,0,-17,27,ink),...contents],name+' has productive capacity inside the illustrative member network.'));
 };
 member('carpenter',205,'Carpenter','wood');member('accountant',600,'Accountant','accounts');member('developer',995,'Web developer','web');
 label('example','Illustrative credits',600,510,18);reveal('example',2);
 const report=(id,x,y,title)=>add(object(id,x,y,[n('rect',{x:-72,y:-42,width:144,height:85,rx:3,fill:'#fffdf5'}),text(title,0,-9,22,ink),path('M-45 8H44M-45 22H23',teal,4)],'A service delivered by one member to another, not new physical resources.'));
 report('accounts-delivered',600,343,'Accounts');reveal('accounts-delivered',1);move('accounts-delivered',2,205,343,2400);
 add(object('trade-entries',600,430,[n('rect',{x:-320,y:-42,width:640,height:92,rx:5,fill:cream}),text('Carpenter −20',-158,-3,27,plum),text('Accountant +20',156,-3,27,teal),text('Same trade · paired entries',0,31,22,ink)],'Illustrative equal20-unit debit and credit created simultaneously; not historical transaction data.'));reveal('trade-entries',2);
 report('website-delivered',995,343,'Website');reveal('website-delivered',3);move('website-delivered',3,600,343,2500);
 add(object('next-entries',600,430,[n('rect',{x:-320,y:-42,width:640,height:92,rx:5,fill:cream}),text('−20',-215,0,30,plum),text('0',0,0,30,ink),text('+20',215,0,30,teal),text('Carpenter',-215,32,22,ink),text('Accountant',0,32,22,ink),text('Web developer',215,32,22,ink)],'A second illustrative20-unit member purchase spends the accountant credit; the network balances still sum to zero.'));hide('trade-entries',3);reveal('next-entries',3);
 label('limit','Agreed limits · default risk remains',600,550,29);reveal('limit',4);
 label('boundary','Member acceptance',600,380,25);reveal('boundary',5);
 // Outside obligations do not become payable merely because this ledger exists.
 hide('accounts-delivered',6);hide('website-delivered',6);
 hide('boundary',6);
 label('cash','Outside payments still need accepted currency',600,353,25);reveal('cash',6);
 return q.finish('One source-grounded member exchange produces paired debit/credit; a second service circulates purchasing capacity while limits, acceptance and external obligations remain. Numerical20-unit trades are explicitly illustrative.');
}
