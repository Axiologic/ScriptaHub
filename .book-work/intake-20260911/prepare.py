from pathlib import Path
import sys,json
sys.path.insert(0,'tools');import book_tasks as b
rows=[('ARHITECTURA_REALULUI.docx','The Architecture of Reality','ro'),('Arta_de_a_sti_ce_conteaza.docx','The Art of Knowing What Matters','ro'),('CARTEA_NU_DA_NOTIFICARI.docx','The Book Sends No Notifications','ro'),('Din_reguli_lumi_program_de_cercetare.docx','From Rules, Worlds','ro'),('Frumosul_Anatomia_unei_fascinatii_editie_extinsa.docx','Beauty: The Anatomy of Fascination','ro'),('Inca_o_incercare_carte.docx','One More Try','ro'),('INTRE_CREDINTA_SI_DOVADA.docx','Between Faith and Evidence','ro'),('Libertatea_si_pretul_ei.docx','Freedom and Its Price','ro'),('Lumea_nu_citeste_ecuatii.docx','The World Does Not Read Equations','ro'),('Masini_de_intelegere_prin_circuite_SOP_Lang.docx','Machines of Understanding Through Circuits','ro'),('Meta_Rational_Pragmatics_Carte_RO.docx','Meta-Rational Pragmatics','ro'),('Noutatea_care_seamana_cu_trecutul.docx','Novelty That Resembles the Past','ro'),('RESPONSABILITATEA.DOCX','Responsibility','ro'),('RIGHT_TO_COPY.docx','The Right to Copy','en'),('The_Network_of_Intent.docx','The Network of Intent','en'),('Ultimul_naiv.docx','The Last Naive Person','ro')]
out=[]
for filename,title,lang in rows:
 work=b.prepare(Path('tasks')/filename,lang,title);out.append({'filename':filename,'title':title,'language':lang,'workdir':str(work.relative_to(Path.cwd()))})
Path('.book-work/intake-20260911/books.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,indent=2))
