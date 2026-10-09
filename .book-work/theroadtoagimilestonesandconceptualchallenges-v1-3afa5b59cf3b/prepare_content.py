import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/3afa5b59cf3bc900/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
title_text = 'The Road to AGI: Milestones and Conceptual Challenges'
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>', 'html.parser')
out.title.string = title_text
article = out.article
h1 = out.new_tag('h1', id='book-title'); h1.string = title_text; article.append(h1)
chapters = {
    8: ('Chapter I — The Neurosymbolic Phase', 'The Neurosymbolic Phase'),
    15: ('Chapter II — AI "Sleep" and AGI', 'AI "Sleep" and AGI'),
    24: ('Chapter III — AGI: Complexity and Computability', 'AGI: Complexity and Computability'),
    29: ('Chapter IV — Towards Digital Science(s)', 'Towards Digital Science(s)'),
    35: ('Chapter V — The Meta-Rationality Phase', 'The Meta-Rationality Phase'),
    43: ('Chapter VI — Knowledge Transfer Across Domains', 'Knowledge Transfer Across Domains'),
    48: ('Chapter VII — Autonomous Experimentation', 'Autonomous Experimentation'),
    54: ('Chapter VIII — Dynamic Goal Prioritization', 'Dynamic Goal Prioritization'),
    60: ('Chapter IX — Adaptive Emotional Phase', 'Adaptive Emotional Phase'),
    66: ('Chapter X — Recursive Self-Improvement', 'Recursive Self-Improvement'),
    72: ('Chapter XI — Situational Ethics Phase', 'Situational Ethics Phase'),
    78: ('Chapter XII — Self-Awareness Phase', 'Self-Awareness Phase'),
    84: ('Chapter XIII — Summary of pre-AGI Phases', 'Summary of pre-AGI Phases'),
}
rows = [
('Advanced LLM & Neurosymbolic Integration', 'Evaluating AI’s ability to perform symbolic reasoning alongside deep learning; benchmarks in neurosymbolic processing; tests of logical inference combined with natural language understanding.', '3–10 years'),
('AI “Sleep” Phase', 'Metrics on knowledge consolidation and adaptive learning from “offline” processing; performance improvement post-sleep cycles; robustness of fine-tuning based on experience.', '3–12 years'),
('Complexity & Computability', 'Capability to handle chaotic systems and provide theories for unpredictable phenomena; accuracy in modeling complex systems like weather or economies; success in managing non-linear, ergotic scenarios.', '5–15 years'),
('Dynamic Goal Prioritization', 'AI’s ability to reprioritize goals based on new information; efficiency of adaptive decision-making algorithms; real-time adjustment in complex, evolving environments.', '5–15 years'),
('Cross-Domain Knowledge Transfer', 'Measuring AI’s success in applying knowledge from one field to another; evaluations of interdisciplinary problem-solving; ability to recognize and leverage analogies across domains.', '5–20 years'),
('Situational Ethics', 'Evaluation of AI’s ethical reasoning in complex, culturally sensitive dilemmas; consistency with human ethical standards; tests of moral adaptability across contexts.', '5–20 years'),
('Digitalization of Sciences', 'Assessment of AI’s ability to autonomously review and contribute to scientific literature; successful hypothesis generation and experiment design; peer-reviewed contributions.', '5–25 years'),
('Autonomous Experimentation', 'AI performance in designing, conducting, and refining experiments without human oversight; accuracy in predicting experimental outcomes; learning efficiency over multiple iterations.', '5–30 years'),
('Meta-Rationality', 'Tests on AI’s ability to develop and juggle multiple, competing theories; evaluation of context-based theory application; creative problem-solving and abstract reasoning metrics.', '10–30 years'),
('Adaptive Emotional Phase', 'AI’s proficiency in recognizing and simulating human emotions; performance in empathy-based interactions; feedback from human-AI collaboration on emotional and social tasks.', '20–35 years'),
('Recursive Self-Improvement', 'Measuring the frequency and impact of AI-driven self-optimizations; success rates of self-modification experiments; stability and improvement of algorithms over time.', '25–40 years'),
('Self-Awareness Phase', 'Assessments of AI’s understanding of its own state and limitations; performance in self-reflection tasks; ability to anticipate and explain the consequences of its actions.', '30–50 years'),
]
def add_table():
    table = out.new_tag('table', id='pre-agi-phases')
    caption = out.new_tag('caption'); caption.string = 'Pre-AGI phases, proposed measurement methods and speculative post-2024 timelines'; table.append(caption)
    thead = out.new_tag('thead'); tr = out.new_tag('tr')
    for text in ('Pre-AGI Phases', 'Measurement Methods', 'Post-2024'):
        th = out.new_tag('th', scope='col'); th.string=text; tr.append(th)
    thead.append(tr); table.append(thead)
    tbody = out.new_tag('tbody')
    for phase, method, duration in rows:
        tr = out.new_tag('tr')
        th = out.new_tag('th', scope='row'); th.string=phase; tr.append(th)
        for value in (method, duration):
            td = out.new_tag('td'); td.string=value; tr.append(td)
        tbody.append(tr)
    table.append(tbody); article.append(table)

sections=[]
for page in range(8, 90):
    if page in (85,86,87):
        if page == 85: add_table()
        continue
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in source.find_all('p', recursive=False)]
    paragraphs = [p for p in paragraphs if p and not re.fullmatch(r'\d+', p)]
    if page in chapters:
        heading, subtitle = chapters[page]
        h2 = out.new_tag('h2', id=f'chapter-{len(sections)+1}'); h2.string=heading; article.append(h2)
        sections.append({'id':h2['id'], 'title':heading, 'sourcePage':page})
        assert paragraphs[0].startswith('Chapter '), (page,paragraphs[0][:100])
        paragraphs[0] = re.sub(r'^Chapter\s+[IVX]+\s*', '', paragraphs[0]).strip()
        paragraphs = [p for p in paragraphs if p]
        assert paragraphs[0].startswith(subtitle), (page,paragraphs[0][:100],subtitle)
        paragraphs[0] = paragraphs[0][len(subtitle):].strip()
        paragraphs = [p for p in paragraphs if p]
    for value in paragraphs:
        p = out.new_tag('p'); p.string=value; article.append(p)

# PDF page boundaries sometimes divide a sentence without punctuation. Reflow those
# fragments while retaining chapter headings and distinct complete paragraphs.
for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ',strip=True), p.get_text(' ',strip=True)
        if left and right and (not re.search(r'[.!?:;”"\)]$',left) or re.match(r'^[a-z]', right)):
            prev.string = left + ' ' + right
            p.decompose()

for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ',strip=True)
    if len(value.split()) <= 230: continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
    if len(sentences) < 3: continue
    groups=[]; group=[]; words=0
    for sentence in sentences:
        count=len(sentence.split())
        if group and words+count>170:
            groups.append(' '.join(group)); group=[]; words=0
        group.append(sentence); words+=count
    if group: groups.append(' '.join(group))
    if len(groups)>1:
        for group_text in groups:
            node=out.new_tag('p'); node.string=group_text; p.insert_before(node)
        p.decompose()

body=article.get_text(' ',strip=True)
assert len(body.split())>12000, len(body.split())
assert len(article.find_all('h2'))==13 and len(article.select('table tbody tr'))==12
assert not any(term in body.lower() for term in ('outfinitygift','outfinity gift','outfinitygift.com'))
target=root/'book/en/full_content.html'; target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(str(out)+'\n',encoding='utf-8')
(root/'qa/source-selection.json').write_text(json.dumps({'source':'income/The_Road_to_AGI__Milestones_and_Conceptual_Challenges/content.pdf','retainedPdfPages':list(range(8,90)),'excludedPdfPages':list(range(1,8))+list(range(90,97)),'reason':'Preserve the original thirteen substantive chapters, including the final phases table; exclude rights, contents, retired-project promotion and annex.','tableReconstruction':{'sourcePages':[85,86,87],'columns':['Pre-AGI Phases','Measurement Methods','Post-2024'],'rows':len(rows),'note':'Semantic HTML table transcribed from the source; time ranges remain the author’s speculative projections.'},'sections':sections,'readerWords':len(body.split())},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared AGI reader:',len(body.split()),'words,',len(rows),'table rows')
