#!/usr/bin/env python3
"""Local ASR evidence for narration accuracy; does not certify acting quality."""
import argparse, hashlib, json, pathlib, re, time, unicodedata
from difflib import SequenceMatcher
from faster_whisper import WhisperModel

def sha(data): return hashlib.sha256(data).hexdigest()
def words(text):
    text=unicodedata.normalize('NFKC',text).lower().replace('’',"'")
    return re.findall(r"[\w]+(?:'[\w]+)?",text)
def distance(a,b):
    row=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        new=[i]
        for j,y in enumerate(b,1): new.append(min(new[-1]+1,row[j]+1,row[j-1]+(x!=y)))
        row=new
    return row[-1]
parser=argparse.ArgumentParser();parser.add_argument('projects',nargs='+');args=parser.parse_args()
model_dir=pathlib.Path('.book-work/voice-qa-model')
model_sha=sha((model_dir/'model.bin').read_bytes())
model=WhisperModel(str(model_dir),device='cpu',compute_type='int8',cpu_threads=1,num_workers=1,local_files_only=True)
for project_name in args.projects:
    project=pathlib.Path(project_name);receipt=json.loads((project/'work/voice-receipts.json').read_text())
    if 'Qwen3-TTS' not in receipt.get('provider',''):raise ValueError(f'{project}: expected current Qwen receipts')
    scenes=json.loads((project/'work/scenes.json').read_text());expected=[(f"{s['id']}-line-{i+1}",text) for s in scenes for i,text in enumerate(s['lines'])]
    by_id={line['id']:line for line in receipt['lines']};inputs=[]
    for id,text in expected:
        line=by_id[id];file=project/'work'/line['file'];audio_sha=sha(file.read_bytes())
        if audio_sha!=line['sha256'] or sha(text.encode())!=line['textSha256']:raise ValueError(f'{id}: stale audio or text')
        inputs.append({'id':id,'text':text,'file':str(file),'audioSha256':audio_sha})
    input_sha=sha(json.dumps(inputs,sort_keys=True).encode());output=project/'qa/spoken-audio-review.json'
    if output.exists():
        prior=json.loads(output.read_text())
        if prior.get('inputSha256')==input_sha and prior.get('modelSha256')==model_sha:
            print(json.dumps({'project':project_name,'cached':True,'status':prior['status']}),flush=True);continue
    started=time.monotonic();results=[]
    for item in inputs:
        segments,info=model.transcribe(item['file'],language='en',beam_size=5,temperature=0,condition_on_previous_text=False,vad_filter=False)
        segments=list(segments);recognized=' '.join(s.text.strip() for s in segments).strip();a,b=words(item['text']),words(recognized)
        edits=distance(a,b);differences=[{'kind':tag,'expected':' '.join(a[i:j]),'heard':' '.join(b[k:l])} for tag,i,j,k,l in SequenceMatcher(None,a,b).get_opcodes() if tag!='equal']
        results.append({**item,'recognized':recognized,'wordEdits':edits,'wordErrorRate':edits/max(1,len(a)),'differences':differences,'durationSeconds':info.duration,'wordsPerMinute':60*len(a)/max(.1,info.duration),'segments':[{'text':s.text,'start':s.start,'end':s.end,'avgLogprob':s.avg_logprob,'noSpeechProbability':s.no_speech_prob} for s in segments]})
        print(json.dumps({'project':project_name,'clip':item['id'],'wordEdits':edits}),flush=True)
    report={'version':1,'provider':'local faster-whisper base.en int8','modelSha256':model_sha,'inputSha256':input_sha,'status':'matched' if all(not r['wordEdits'] for r in results) else 'review-required','scope':'Independent local speech recognition; differences need semantic review and ASR can misrecognize names. Does not establish emotional quality or replace listening.','elapsedSeconds':round(time.monotonic()-started,3),'clips':results}
    temporary=output.with_suffix('.json.tmp');temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');temporary.replace(output)
    print(json.dumps({'project':project_name,'status':report['status'],'elapsedSeconds':report['elapsedSeconds']}),flush=True)
