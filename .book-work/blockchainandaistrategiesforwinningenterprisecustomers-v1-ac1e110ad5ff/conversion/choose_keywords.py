#!/usr/bin/env python3
"""Choose ninety specific terms occurring in the canonical short reader."""
import hashlib, importlib.util, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('build_books','tools/build_books.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
work=Path(__file__).resolve().parents[1]
reader=work/'book/en/short_content.html';mp=work/'book/manifest.json'
source=build.keyword_normalise(build.keyword_source_text(reader))
phrases='''enterprise customers
large enterprise customers
customer relationships
direct customer relationships
customer interviews
customer needs
customer-funded pilots
client-backed pilots
customer-funded pilot
minimum viable product
minimum viable products
MVP
product design
product development
product-market fit
pilot
pilots
startup
young company
finished product
problem-solving process
enterprise problems
tailored proposals
demonstrated demand
open-source resources
prototypes
demonstrations
wireframes
early discussions
industry leaders
high-profile enterprise clients
competitive market
scarce opportunities
distinctive value
blockchain
AI
blockchain or AI
lean startup
rapid MVP iteration
customer development
Jobs to Be Done
problem validation
iterative strategy
customer-driven strategy
early adopters
mainstream customers
educational nonprofit community
professional nonprofit community
professional community
nonprofit community
membership fees
annual fees
commercial offerings
knowledge exchange
training
workshops
courses
pharmaceutical sector
membership base
employer
networking
professional development
technology trends
peer collaboration
accelerators
incubators
early mentorship
funding
visibility
investors
online specialist community
content and moderation
qualified leads
European research grants
research grants
development costs
public-private partnership
private partners
staff time
European Union
EU
consortium
research problem
complementary capabilities
academic institutions
market feedback
rapid tests
iteration
strategic partnerships
consortia
expertise
market reach
structured entrepreneurship frameworks
thought leadership
market acceptance
security
data protection
regulatory compliance
enterprise AI
enterprise blockchain
customer and market data
market data
scalable offerings
recurring revenue
professional networking
sales
sales process
enterprise sale
organizational discipline
Innovative Health Initiative
private investment
client relationships
education
research consortia
industry experts
market conditions
technology startups
customer-funded development
enterprise partnerships
revenue
commercial projects
pharmaceutical professionals
online discussion
funding arrangements
public-private partnerships
trust
industry clients
client organizations
data
innovation
business model
subscriptions
long-term growth
research funding
market needs
customer choices
product offerings
industry trends
potential partners
research skills
business growth
enterprise market
client-funded pilots
business accelerators
research programs
market reputation
professional network
training sessions
European funding
industry events
business partnerships
startup funding
startup strategy
enterprise sales
startup incubators
membership fees
market demand
research collaboration
proof of concept
client-funded MVP
market entry'''.splitlines()
shelf={build.keyword_normalise(label).strip() for v in build.SHELF_CATEGORIES.values() for label in v['en'].split('|')}
weak={'pilot','pilots','startup','young company','finished product','ai','blockchain or ai','training','workshops','courses','employer','funding','visibility','investors','eu','expertise','iteration','sales','data','revenue','client relationships'}
chosen=[];seen=set()
for phrase in phrases:
    key=build.keyword_normalise(phrase).strip()
    if not key or key in seen or key in shelf or key in weak or key not in source:continue
    chosen.append(phrase);seen.add(key)
    if len(chosen)==90:break
if len(chosen)!=90:raise SystemExit(f'Only {len(chosen)} terms: {chosen}')
m=json.loads(mp.read_text())
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':chosen,'reviewedOn':'2026-10-08','method':'reader-grounded editorial selection'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('\n'.join(f'{i:02}. {x}' for i,x in enumerate(chosen,1)))
