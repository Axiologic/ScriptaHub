import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks'
t={
 't000001':'Iluzia stabilității în crizele financiare — Ediția de zece minute',
 't000002':'Iluzia stabilității în crizele financiare',
 't000003':'Agentul IA Zach Lawsone · 2024',
 't000004':'Cartea examinează de ce piețele financiare aparent stabile pot deveni vulnerabile la crize bruște. Cele patru capitole urmăresc tipare repetate de optimism, speculație și panică; compară episoade istorice; evaluează intervențiile guvernelor și băncilor centrale; și urmăresc deciziile monetare dincolo de granițe. Introducerea și concluzia pun accent pe psihologia investitorilor, vulnerabilitățile sistemice și legăturile internaționale. Argumentul invită la examinarea atât a protecției oferite de intervenții, cât și a noilor riscuri pe care acestea le pot crea.',
 't000005':'Introducere — Stabilitatea poate fi înșelătoare',
 't000006':'Perioadele de încredere pot ascunde o fragilitate crescândă. Introducerea leagă prețurile umflate ale activelor, schimbarea sentimentului investitorilor și răspândirea șocurilor prin piețe interconectate. Îi îndeamnă pe cititori să privească dincolo de indicatorii liniștitori și să examineze cum lăcomia, frica și deciziile instituționale modelează ciclurile financiare. Legăturile globale fac ca un șoc pe o piață să afecteze economii îndepărtate, ridicând întrebări despre cooperare și supraveghere.',
 't000007':'Citește introducerea în ediția integrală',
 't000008':'Descifrarea crizei — Psihologie și speculație',
 't000009':'Primul capitol descrie un ciclu cunoscut: prețurile în creștere hrănesc optimismul, investitorii intră pe piață văzând profiturile altora, iar inversarea tendinței poate transforma încrederea în panică. Înțelegerea piețelor cere atenție la psihologia tranzacțiilor, nu doar la mecanismele economice. Știrile și rețelele sociale pot amplifica sentimentul și accelera vechiul tipar de manie și prăbușire. Cartea cere vigilență și judecată critică tocmai când prosperitatea pare sigură.',
 't000010':'Citește capitolul I în ediția integrală',
 't000011':'Crize istorice — Active diferite, comportamente repetate',
 't000012':'Al doilea capitol trece prin mania lalelelor din Țările de Jos, prăbușirea bursieră din 1929, bula „dot-com” și criza imobiliară și a creditului din 2008. Activele, instituțiile și tehnologiile diferă, dar euforia colectivă este urmată de frică rapidă. Cumpărarea pe marjă, ignorarea profitabilității și împrumuturile subprime riscante arată expuneri ascunse de optimism. Criza din 2008 arată și cum prăbușirea locuințelor într-o țară se poate răspândi prin finanțele globale. Exemplele invită la identificarea semnelor de avertizare actuale.',
 't000013':'Citește capitolul II în ediția integrală',
 't000014':'Intervenție — Sprijin și compromisuri',
 't000015':'După o prăbușire, băncile centrale pot reduce dobânzile sau cumpăra active prin relaxare cantitativă, iar guvernele pot spori cheltuielile sau reduce taxele. Capitolul al treilea prezintă instrumentele drept încercări de a reface încrederea, cererea și creditarea. Întreabă dacă împrumuturile ieftine mult timp pot umfla prețul activelor ori aloca greșit resursele și dacă sprijinul fiscal poate mări datoria. Coordonarea și comunicarea contează: episodul „taper tantrum” din 2013 arată cum un simplu semnal despre politica viitoare poate mișca piețele.',
 't000016':'Citește capitolul III în ediția integrală',
 't000017':'Băncile centrale — Efecte în lanț peste granițe',
 't000018':'Capitolul final urmărește cum politica Rezervei Federale, fluxurile de capital, cursurile valutare și datoriile în dolari pot afecta alte economii. Discută devalorizarea competitivă și refugiul investitorilor în active considerate sigure. Răspunsul la criza din 2008 este un exemplu de coordonare internațională, iar criptomonedele și monedele digitale ale băncilor centrale ridică întrebări noi. Nicio bancă centrală nu acționează izolată; transparența și cooperarea contează când deciziile circulă prin piețe conectate.',
 't000019':'Citește capitolul IV în ediția integrală',
 't000020':'Concluzie — Rezistența cere discernământ',
 't000021':'Concluzia revine la tensiunea dintre stabilizarea imediată și efectele de durată. Cere adaptare, vigilență și comunicare deschisă între băncile centrale, recunoscând rolul comportamentului uman în crizele recurente. Finanțele digitale pot schimba instrumentele, dar nu elimină slăbiciunile sistemului sau interdependența globală. Cartea încheie cu un obiectiv prudent: să învățăm din șocurile trecute și să construim un sistem mai rezistent. Bibliografia include lucrări de Kindleberger, Reinhart și Rogoff, Krugman, Minsky și Greenspan.',
 't000022':'Citește concluzia în ediția integrală',
}
for x in sorted(p.glob('*.json')):
 d=json.loads(x.read_text())
 for s in d['segments']:
  assert s['id'] in t
  assert not s['translation'] or s['translation']==t[s['id']]
  s['translation']=t[s['id']]
 x.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
