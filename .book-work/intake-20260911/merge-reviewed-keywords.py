import csv,json,subprocess,os,sys
from pathlib import Path
for arg in sys.argv[1:]:
 w=Path(arg);p=Path('tools/keyword-translations.generated.json');cache=json.loads(p.read_text());lines=(w/'keyword-review.tsv').read_text().splitlines();delimiter='\t' if '\t' in lines[0] else '|';rows=list(csv.reader(lines,delimiter=delimiter));languages=['en','ro','fr','de','es','pt','it','pl']
 if rows[0][0]=='en':languages=rows.pop(0)
 for row in rows:
  assert len(row)==8,(w,row)
  labels=dict(zip(languages,row))
  for lang,value in labels.items():
   if lang!='en':cache['translations'][lang][labels['en']]=value
 p.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
 subprocess.run([sys.executable,'tools/build_books.py','rebuild-keywords','--manifest',str(w/'book/manifest.json')],check=True,env={**os.environ,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'})
