import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0001.json';d=json.loads(p.read_text())
t=[
'Impactul romanului Să ucizi o pasăre cântătoare asupra societății de astăzi — Lectură de zece minute',
'Impactul romanului Să ucizi o pasăre cântătoare asupra societății de astăzi',
'Un parcurs de zece minute prin eseu',
'Introducere: De ce mai contează Maycomb',
'Acest eseu citește romanul lui Harper Lee',
'Să ucizi o pasăre cântătoare',
'alături de întrebările actuale despre nedreptatea rasială, empatie, curaj moral, educație și memorie culturală. Orașul imaginar Maycomb devine o cale de a cerceta cum supraviețuiesc prejudecățile în instituții și în relațiile obișnuite. Apărarea lui Tom Robinson de către Atticus Finch întreabă ce cere dreptatea atunci când o comunitate s-a hotărât deja. Perspectiva lui Scout arată cum copiii învață regulile sociale, dar le pot și pune la îndoială.',
'Cartea nu susține că un roman poate, singur, să pună capăt discriminării. Le cere cititorilor să lege interpretarea de conduită: să asculte dincolo de diferențe, să observe părtinirea, să conteste sistemele nedrepte și să apere oamenii pe care comunitatea i-a făcut vulnerabili.',
'1. Nedreptatea rasială și procesul',
'Tom Robinson, un bărbat de culoare acuzat pe nedrept că a agresat o femeie albă, este judecat într-un proces modelat de ierarhia rasială din Maycomb. Atticus prezintă dovezi care contrazic acuzația, dar verdictul reflectă prejudecățile orașului, nu faptele. Eseul vede în acest eșec un avertisment: procedurile juridice formale pot coexista cu rezultate inegale. O sală de judecată nu poate fi dreaptă când stereotipurile stabilesc a cui mărturie este crezută.',
'Capitolul leagă romanul de inegalitățile contemporane din poliție, condamnări, educație, muncă și oportunități. Îi îndeamnă pe cititori să vadă rasismul ca pe mai mult decât ostilitate individuală: regulile, obiceiurile și instituțiile pot reproduce tratamentul inegal. Schimbarea cere conștientizare publică, dialog, acțiune civică și politici care abordează aceste structuri.',
'Citește capitolul integral despre nedreptatea rasială',
'2. Empatie și curaj moral',
'Atticus îl apără pe Tom în ciuda ostilității vecinilor și a pericolului pentru familia sa. Alegerea lui oferă eseului un model de curaj moral: să acționezi din principiu când rezultatul este nesigur, iar prețul social este mare. Sfatul dat lui Scout de a privi lucrurile din perspectiva altuia face din empatie o practică, nu doar un sentiment plăcut. Înțelegerea experienței cuiva poate clătina judecățile facile și poate deschide o conversație sinceră.',
'Eseul privește și dincolo de sala de judecată. Scout și Jem se confruntă cu prejudecățile moștenite; viața lui Boo Radley arată cum zvonurile pot ascunde umanitatea unui vecin. Capitolul leagă aceste lecții de susținerea celor nedreptățiți, de dialogul comunitar și de munca celor care combat nedreptatea în sistemul juridic. Empatia contează cel mai mult când schimbă hotărâri și comportamente.',
'Citește capitolul integral despre empatie și curaj',
'3. Educație, conștientizare și acțiune',
'Discuțiile de la clasă despre roman îi pot ajuta pe elevi să cerceteze părtinirea, contextul istoric și distanța dintre idealurile juridice și experiența trăită. Eseul susține că educația trebuie să invite la întrebări critice, nu la acord mecanic. Elevii pot compara conflictele din Maycomb cu dovezi din prezent și pot asculta vocile ignorate de comunitatea din roman. Literatura oferă o poveste comună, iar discuția îi ajută pe oameni să își verifice presupunerile.',
'Capitolul prezintă conștientizarea ca început, nu ca punct final. Lectura îi poate îndrepta pe elevi spre conversații, proiecte locale sau acțiune publică. Profesorii și cititorii trebuie să lase loc și disconfortului: a discuta responsabil despre rasism înseamnă a înfrunta istorii dureroase fără a le reduce la o morală simplă.',
'Citește capitolul integral despre educație',
'4. Conversații culturale dincolo de roman',
'Adaptările și lucrările ulterioare au dus întrebările din Maycomb către alte publicuri. Eseul discută interpretarea lui Atticus Finch în film, montările teatrale și scrierile contemporane care revin la dreptate, inocență și răspundere morală. Fiecare repovestire poate reînnoi conversația, dar poate și îngusta povestea dacă spectatorii trec cu vederea experiența lui Tom Robinson sau ordinea rasială mai largă. A cui voce primește atenție rămâne o întrebare centrală.',
'Media și arta pot păstra un clasic în atenția publicului, invitând totodată la examinarea limitelor sale. Capitolul le cere cititorilor să caute perspective diverse, să cerceteze cum înfățișează poveștile nedreptatea și să lege admirația culturală de răspunderile prezentului.',
'Citește capitolul integral despre media și cultură',
'Concluzie',
'În eseu, pasărea cântătoare simbolizează inocența și datoria de a-i proteja pe cei vulnerabili. Procesul lui Tom, apărarea lui Atticus, învățarea copiilor și viața ulterioară a romanului arată laturi diferite ale acestei datorii. Întrebarea durabilă a cărții este dacă cititorii vor duce empatia și curajul moral în instituțiile și relațiile pe care contribuie să le modeleze.',
'Citește eseul integral',
]
assert len(t)==len(d['segments'])
for s,x in zip(d['segments'],t):s['translation']=x
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
