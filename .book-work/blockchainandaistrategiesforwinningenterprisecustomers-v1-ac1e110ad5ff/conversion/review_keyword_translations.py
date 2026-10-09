#!/usr/bin/env python3
"""Correct literal-model errors in the local keyword translation cache."""
import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json')
d=json.loads(p.read_text())
fix={
'enterprise customers':{'fr':'clients professionnels','de':'Unternehmenskunden','es':'clientes empresariales','ro':'clienți corporativi','pl':'klienci korporacyjni'},
'large enterprise customers':{'fr':'grands clients professionnels','es':'grandes clientes empresariales','pt':'grandes clientes empresariais','it':'grandi clienti aziendali','ro':'clienți corporativi mari','pl':'duzi klienci korporacyjni'},
'customer-funded pilots':{'fr':'projets pilotes financés par les clients','de':'kundenfinanzierte Pilotprojekte','es':'proyectos piloto financiados por clientes','pt':'projetos-piloto financiados por clientes','it':'progetti pilota finanziati dai clienti','ro':'proiecte pilot finanțate de clienți','pl':'pilotaże finansowane przez klientów'},
'customer-funded pilot':{'fr':'projet pilote financé par un client','de':'kundenfinanziertes Pilotprojekt','es':'proyecto piloto financiado por un cliente','pt':'projeto-piloto financiado por um cliente','it':'progetto pilota finanziato da un cliente','ro':'proiect pilot finanțat de un client','pl':'pilotaż finansowany przez klienta'},
'minimum viable product':{'de':'Minimum Viable Product','it':'prodotto minimo funzionante','pl':'minimalny produkt funkcjonalny'},
'MVP':{'fr':'MVP'},
'enterprise problems':{'pl':'problemy przedsiębiorstw'},
'tailored proposals':{'pl':'propozycje dostosowane do potrzeb'},
'open-source resources':{'fr':'ressources open source','ro':'resurse open source','pl':'zasoby open source'},
'demonstrations':{'fr':'démonstrations','pt':'demonstrações','it':'dimostrazioni'},
'wireframes':{'fr':'maquettes filaires','de':'Wireframes','es':'esquemas de interfaz','pt':'esboços de interface','it':'schemi di interfaccia','ro':'machete de interfață','pl':'makiety interfejsu'},
'early discussions':{'es':'primeras conversaciones','pt':'conversas iniciais','it':'prime discussioni','ro':'discuții inițiale'},
'high-profile enterprise clients':{'ro':'clienți corporativi importanți','pl':'ważni klienci korporacyjni'},
'competitive market':{'de':'Wettbewerbsmarkt','ro':'piață competitivă'},
'scarce opportunities':{'ro':'oportunități limitate'},
'blockchain':{'pl':'blockchain','ro':'blockchain'},
'rapid MVP iteration':{'fr':'itération rapide du MVP','pl':'szybka iteracja MVP'},
'Jobs to Be Done':{'fr':'Jobs to Be Done','de':'Jobs to Be Done','es':'Jobs to Be Done','pt':'Jobs to Be Done','it':'Jobs to Be Done','ro':'Jobs to Be Done','pl':'Jobs to Be Done'},
'early adopters':{'fr':'premiers utilisateurs','de':'frühe Anwender','es':'primeros usuarios','pt':'primeiros utilizadores','it':'primi utilizzatori','ro':'primii utilizatori','pl':'pierwsi użytkownicy'},
'mainstream customers':{'fr':'clients du marché de masse','es':'clientes del mercado general','pt':'clientes do mercado geral','it':'clienti del mercato generale','ro':'clienți de pe piața de masă','pl':'klienci rynku masowego'},
'annual fees':{'pt':'quotas anuais','it':'quote annuali','ro':'cotizații anuale'},
'membership base':{'fr':'base de membres','it':'base di membri','pl':'baza członków'},
'networking':{'pt':'contactos profissionais','it':'contatti professionali','ro':'relații profesionale','pl':'nawiązywanie kontaktów'},
'peer collaboration':{'de':'Zusammenarbeit unter Fachkollegen','pl':'współpraca między specjalistami'},
'accelerators':{'de':'Startup-Acceleratoren','pl':'akceleratory startupów'},
'incubators':{'de':'Startup-Inkubatoren'},
'early mentorship':{'pl':'wczesne wsparcie mentorów'},
'online specialist community':{'de':'Online-Fachgemeinschaft','ro':'comunitate online de specialiști','pl':'internetowa społeczność specjalistów'},
'content and moderation':{'ro':'conținut și moderare','pl':'treści i moderacja'},
'qualified leads':{'fr':'contacts commerciaux qualifiés','de':'qualifizierte Vertriebskontakte','es':'contactos comerciales cualificados','pt':'contactos comerciais qualificados','it':'contatti commerciali qualificati','ro':'contacte comerciale calificate','pl':'kwalifikowane kontakty handlowe'},
'consortium':{'de':'Konsortium'},
'research problem':{'es':'problema de investigación','ro':'problemă de cercetare','pl':'problem badawczy'},
'complementary capabilities':{'ro':'competențe complementare'},
'market feedback':{'de':'Marktrückmeldungen','ro':'reacții ale pieței'},
'market reach':{'de':'Marktreichweite','ro':'acoperire de piață'},
'thought leadership':{'fr':'autorité intellectuelle','de':'Meinungsführerschaft','es':'liderazgo de opinión','pt':'liderança de opinião','it':'autorevolezza di settore','ro':'autoritate de specialitate','pl':'pozycja lidera opinii'},
'regulatory compliance':{'ro':'conformitate cu reglementările'},
'enterprise AI':{'fr':'IA en entreprise','de':'KI in Unternehmen','es':'IA empresarial','pt':'IA empresarial','it':'IA aziendale','ro':'IA pentru companii','pl':'AI w przedsiębiorstwach'},
'scalable offerings':{'es':'ofertas escalables','pl':'oferty skalowalne'},
'recurring revenue':{'fr':'revenus récurrents'},
'enterprise sale':{'fr':'vente aux entreprises','de':'Verkauf an Unternehmenskunden','es':'venta a empresas','pt':'venda a empresas','it':'vendita alle imprese','ro':'vânzare către companii','pl':'sprzedaż klientom korporacyjnym'},
'Innovative Health Initiative':{'fr':'Innovative Health Initiative','de':'Innovative Health Initiative','es':'Innovative Health Initiative','pt':'Innovative Health Initiative','it':'Innovative Health Initiative','ro':'Innovative Health Initiative','pl':'Innovative Health Initiative'},
'client organizations':{'ro':'organizații cliente','pl':'organizacje klientów'},
}
for term,langs in fix.items():
    for lang,value in langs.items():
        assert term in d['translations'][lang],(term,lang)
        d['translations'][lang][term]=value
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(sum(map(len,fix.values())),'labels corrected')
