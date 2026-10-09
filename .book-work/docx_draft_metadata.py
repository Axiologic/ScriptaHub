#!/usr/bin/env python3
"""One-time authored draft metadata for the 2026-10-08 DOCX intake."""
from __future__ import annotations

from pathlib import Path
import json
import re

import torch
from transformers import MarianMTModel, MarianTokenizer

from tools.build_books import LANGUAGES, keyword_catalog, title_route

ROOT = Path(__file__).resolve().parents[1]

# Six source-grounded sentences per book. These are draft landing-page copy;
# full reader translations and editorial QA are separate release gates.
BOOKS = {
    "Anti_Smoothing_Clienti_Piete_Model_de_Afaceri": (
        "business", "Business & Startups", "Clients, Markets, and Business Model",
        ["This business thesis proposes an AI service that keeps evidence and consequences visible during collaboration.",
         "It distinguishes three possible businesses before estimating customers or revenue.",
         "The proposed product checks past commitments and monitors material changes over time.",
         "Chapters compare enterprise AI pilots, research reports, and other entry markets.",
         "The discussion examines buyers, procurement committees, pricing, and the cost of unsuitable clients.",
         "Its commercial assumptions remain proposals to test rather than established financial results."],
    ),
    "Calculul_Afectiv_AI_Verificabil_RO": (
        "science", "Science & Research", "A Cognitive Grammar of Emotions for Verifiable AI",
        ["This research monograph proposes a cognitive grammar for emotions, feelings, and attitudes.",
         "It treats goals, norms, and relationships as part of emotional state.",
         "The framework examines fear, shame, love, trust, respect, and compassion.",
         "Counterfactual tests probe whether an emotional interpretation remains coherent.",
         "Mixed emotions are treated as ordinary cases requiring explicit representation.",
         "The proposal connects conceptual analysis with requirements for verifiable artificial intelligence."],
    ),
    "Capitalism_Against_Itself": (
        "society", "Power, Institutions & Society", "Can a System Reform the Forces That Make It Powerful?",
        ["This essay asks whether capitalism can reform the forces that sustain its power.",
         "It separates personal virtue from institutions capable of changing incentives.",
         "Chapters examine capture, incumbent delay, and conflicts across jurisdictions.",
         "The future appears as a party with weak bargaining power.",
         "The argument tests why successful reforms may later lose their force.",
         "It closes with questions about organized opposition and the limits of correction."],
    ),
    "Enthusiasm_The_Missing_Energy_of_a_Successful_Civilization": (
        "society", "Society & Institutions", "Why Abundant Possibility Can Still Feel Empty",
        ["This essay asks why capable societies can struggle to desire a future.",
         "It studies the success trap, compressed dreams, and attention without direction.",
         "Enthusiasm appears as a social emotion linked to meaningful possibility.",
         "The book considers work, science, culture, and artificial intelligence.",
         "Its chapters also examine disappointment, limits, and the danger of compulsory passion.",
         "The proposed response joins small dreams with institutions that permit experimentation."],
    ),
    "Incomplete_Tribes": (
        "society", "Society & Institutions", "Belonging and Conflict Among Imperfect Humans",
        ["This philosophical essay examines belonging without assuming that people or groups become complete.",
         "It asks why promising ideals can harden into exclusion and conflict.",
         "The discussion compares universalism, loneliness, and synthetic forms of community.",
         "Overlapping loyalties and the right to dissent become practical safeguards.",
         "Later chapters consider polycentric institutions and cooperation among imperfect people.",
         "Artificial intelligence and abundance add new pressures to tribal organization."],
    ),
    "Luminita_la_capatul_tunelului_prima_versiune": (
        "society", "Power, Institutions & Society", "Power, Freedom, and a Civilization Able to Correct Itself",
        ["This first version investigates recurring contradictions in politics, freedom, and institutional power.",
         "It examines meritocracy, expertise, capitalism, security, and the control of attention.",
         "The author distinguishes genuine antinomies from ordinary disagreements.",
         "Artificial intelligence changes both the tools of control and prospects for correction.",
         "The chapters test proposals against opponents able to exploit their weaknesses.",
         "Hope is considered alongside institutional limits rather than offered as a prediction."],
    ),
    "MESSIAH_FACTORY": (
        "society", "Power, Institutions & Society", "Influence, Judgment, and Belonging",
        ["This book studies how audiences turn persuasive figures into authorities beyond correction.",
         "It asks who gets heard and why changing one's mind carries a price.",
         "Names, belonging, and complete worldviews can replace independent judgment.",
         "The argument also examines algorithms that might be mistaken for oracles.",
         "Later chapters test alternatives against their own tendency toward certainty.",
         "The goal is commitment without surrendering the ability to correct power."],
    ),
    "Noul_contract_social_AI_analiza_clauzelor": (
        "society", "Power, Institutions & Society", "Twenty-One Clauses for a Free and Durable Civilization",
        ["This political proposal develops twenty-one clauses for an AI shaped society.",
         "It begins with equal personal status and limits on delegated authority.",
         "Further clauses address material guarantees, ownership, alternatives, and institutional oversight.",
         "Each clause names duties and considers how violations might be detected.",
         "The text asks who controls abundance and how citizens retain effective exit.",
         "Its framework remains a proposal for debate, revision, and public testing."],
    ),
    "O_minte_nu_incape_intr_un_feed": (
        "society", "Society & Institutions", "Books, Attention, and Understanding Beyond the Feed",
        ["This essay examines what sustained reading can offer amid continuous digital feeds.",
         "It separates encountering information from understanding a connected argument.",
         "Chapters compare books, blogs, short videos, screens, paper, and voice.",
         "The author also presents objections to exaggerated claims about books.",
         "Reading matters when readers test ideas and connect them with action.",
         "The final discussion considers small, verifiable changes in attention and practice."],
    ),
    "The_Unfinished_World": (
        "philosophy", "Philosophy & Reasoning", "Why the Future Is Still Worth Wanting",
        ["This book considers hope as loyalty to possibility rather than certainty about outcomes.",
         "It asks how people begin projects in a world that remains unfinished.",
         "The argument connects imagination, agency, and responsibility for shared futures.",
         "It refuses easy assurances that progress or collapse is inevitable.",
         "Readers encounter questions about commitment when evidence cannot guarantee success.",
         "The essay invites renewed action without concealing uncertainty or loss."],
    ),
    "We_Manufacture_Our_Own_Masters_EN": (
        "society", "Power, Institutions & Society", "Power, Freedom, Resentment, and Artificial Intelligence",
        ["This book asks how people repeatedly build systems that come to dominate them.",
         "It examines equality, capitalism, speech, expertise, resentment, and organized force.",
         "Political ideals are tested against the mechanisms that may reverse them.",
         "Artificial intelligence could reduce scarcity while creating new forms of dependence.",
         "The chapters distinguish local freedom from control over large institutions.",
         "The argument seeks arrangements that expose contradictions and permit correction."],
    ),
    "World_as_a_System_1000_Reasoning_Problems_Grades_1-4_EN": (
        "science", "Science & Research", "1000 Reasoning Problems in Geography, History, Civics, and Environmental Studies",
        ["This workbook offers one thousand reasoning problems for children in grades one through four.",
         "Problems use explicit facts, rules, relationships, and constraints rather than hidden knowledge.",
         "Geography exercises cover routes, rivers, maps, climate, and regions.",
         "History tasks explore evidence, chronology, change, and conflicting sources.",
         "Civics and environmental studies introduce decisions, rights, systems, and consequences.",
         "The sequence develops reasoning skills across fifty families of problems."],
    ),
    "two_ways_to_build_a_world": (
        "society", "Society & Institutions", "Partnership, Domination, and Human Cooperation",
        ["This essay reconstructs the contrast between partnership and domination as social patterns.",
         "It treats the framework as an idea to test rather than a finished theory.",
         "Chapters examine hierarchy, cooperation, institutions, and cultural narratives.",
         "The discussion asks how relationships distribute power and make disagreement possible.",
         "It considers the strengths and limits of interpreting history through one contrast.",
         "The resulting questions concern the technology and habits of human cooperation."],
    ),
}

ROMANIAN_TITLES = {
    'Anti_Smoothing_Clienti_Piete_Model_de_Afaceri': 'Anti-Smoothing: clienți, piețe și model de afaceri',
    'Calculul_Afectiv_AI_Verificabil_RO_v2': 'Calculul afectiv',
    'Capitalism_Against_Itself': 'Capitalismul împotriva sa',
    'Enthusiasm_The_Missing_Energy_of_a_Successful_Civilization': 'Entuziasmul: energia lipsă a unei civilizații de succes',
    'Incomplete_Tribes': 'Triburi incomplete',
    'Luminita_la_capatul_tunelului_prima_versiune': 'Există vreo luminiță la capătul tunelului?',
    'MESSIAH_FACTORY': 'Fabrica de mesia',
    'Noul_contract_social_AI_analiza_clauzelor': 'Noul contract social în epoca inteligenței artificiale',
    'O_minte_nu_incape_intr_un_feed': 'O minte nu încape într-un feed',
    'The_Unfinished_World': 'Lumea neterminată',
    'We_Manufacture_Our_Own_Masters_EN': 'Ne fabricăm propriii stăpâni',
    'World_as_a_System_1000_Reasoning_Problems_Grades_1-4_EN': 'Lumea ca sistem: 1000 de probleme de raționament pentru clasele I–IV',
    'two_ways_to_build_a_world': 'Două moduri de a construi o lume',
}

def translate_all(lines: list[str]) -> dict[str, list[str]]:
    results = {'en': lines}
    groups = (
        ('Helsinki-NLP/opus-mt-en-ROMANCE', [('fr','>>fr<< '),('es','>>es<< '),('pt','>>pt<< '),('it','>>it<< '),('ro','>>ro<< ')]),
        ('Helsinki-NLP/opus-mt-en-de', [('de','')]),
        ('Helsinki-NLP/opus-mt-en-zlw', [('pl','>>pol<< ')]),
    )
    torch.set_num_threads(6)
    for name, targets in groups:
        tokenizer=MarianTokenizer.from_pretrained(name,local_files_only=True)
        model=MarianMTModel.from_pretrained(name,local_files_only=True)
        model.eval()
        for lang,prefix in targets:
            out=[]
            for start in range(0,len(lines),32):
                batch=lines[start:start+32]
                encoded=tokenizer([prefix+s for s in batch],return_tensors='pt',padding=True,truncation=True,max_length=100)
                with torch.inference_mode(): generated=model.generate(**encoded,max_new_tokens=110,num_beams=1)
                out.extend(tokenizer.batch_decode(generated,skip_special_tokens=True))
            results[lang]=[re.sub(r'\s+',' ',s).strip().rstrip('.!?')+'.' for s in out]
        del model,tokenizer
    return results

def main():
    releases=[]; strings=[]
    for release_path in sorted(ROOT.glob('.book-work/*/release.json')):
        release=json.loads(release_path.read_text())
        if not release['source'].startswith('income/') or not release['source'].endswith('.docx'): continue
        stem=Path(release['source']).stem
        metadata_key=re.sub(r'_v[1-9][0-9]*$', '', stem, flags=re.I)
        group,category,subtitle,sentences=BOOKS[metadata_key]
        releases.append((release_path,release,stem,group,category))
        strings.extend([release['englishTitle'],subtitle,*sentences])
    localized=translate_all(strings)
    for index,(release_path,release,stem,group,category) in enumerate(releases):
        start=index*8
        title={lang:localized[lang][start].rstrip('.!?') for lang in LANGUAGES}
        title['en']=release['englishTitle']
        title['ro']=ROMANIAN_TITLES[stem]
        subtitle={lang:localized[lang][start+1].rstrip('.!?') for lang in LANGUAGES}
        short_description={}
        about={}
        for lang in LANGUAGES:
            sentences=localized[lang][start+2:start+8]
            short_description[lang]=' '.join(sentences)
            about[lang]=[' '.join(sentences[:3]),' '.join(sentences[3:])]
        catalog=keyword_catalog(group)
        keyword_ids=[row[0] for row in catalog]
        keywords={lang:[row[2][lang] for row in catalog] for lang in LANGUAGES}
        editions={lang:{'book':f'{lang}/book.html','cover':f'{lang}/cover.webp','sourceCover':f'{lang}/cover.png','thumbnail':f'{lang}/thumbnail.webp'} for lang in LANGUAGES}
        manifest={
            'schemaVersion':1,'id':release['bookId'],'sourceId':stem,'sourceAliases':[stem],
            'route':list(title_route(release['englishTitle'])),'category':category,'group':group,
            'title':title,'subtitle':subtitle,'shortDescription':short_description,
            'shortDescriptionEditorial':{'version':1,'createdOn':'2026-10-08','sentences':6,'basis':'original DOCX chapter map; draft local metadata translations pending editorial review'},
            'aboutBook':about,'keywordIds':keyword_ids,'keywords':keywords,
            'coverUrl':{lang:f'{lang}/cover.webp' for lang in LANGUAGES},
            'thumbnailUrl':{lang:f'{lang}/thumbnail.webp' for lang in LANGUAGES},
            'editions':editions,'availableLanguages':[],'publicationStatus':'preparing',
            'currentEdition':None,'releasePolicy':'en-ro-on-request',
        }
        out=release_path.parent/'book/manifest.json'
        out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        print(release['englishTitle'],{lang:len(' '.join(about[lang]).split()) for lang in LANGUAGES})

if __name__=='__main__':main()
