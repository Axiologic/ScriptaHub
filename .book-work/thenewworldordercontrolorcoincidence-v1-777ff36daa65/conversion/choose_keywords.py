#!/usr/bin/env python3
"""Select ninety discovery phrases occurring in the English short reader."""
import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('build_books','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';source=b.keyword_normalise(b.keyword_source_text(reader))
phrases='''Illuminati
historical Bavarian Illuminati
historical Illuminati
Bavarian society
Adam Weishaupt
1776
Enlightenment ideals
secret-society theories
secret societies
secret group
modern legends
modern claims
modern myth
conspiracy theories
conspiracy theorists
New World Order
New World Order theory
secret global plot
hidden power
hidden plan
unseen elite
hidden elites
global government
single global government
central direction
coordinated hidden plan
coordinated effort
coordinated plan
pandemic
COVID-19 pandemic
lockdowns
emergency restrictions
emergency measures
emergency power
emergency powers
public authorities
public-health messages
public-health purpose
public-health responses
health response
public health
health crisis
viral spread
crisis responses
restrictions
travel restrictions
curfews
online work
digital work
digital systems
digital surveillance
digital tracking
digital contact tracing
vaccine passports
vaccine-passport proposals
online monitoring
social life
physical movement
mass compliance
lasting control
control
surveillance
surveillance and loss of autonomy
loss of autonomy
autonomy
freedom
safety and freedom
individual freedoms
societal control
crisis
emergency
emergency surveillance
emergency controls
information channels
mass communication
media messages
repeated media messages
media coverage
news coverage
media conglomerates
mass media
media narratives
public perception
public opinion
media influence
news outlets
social media
social platforms
online discussion
public debate
public-health messaging
conspiracy
fear
fear and uncertainty
uniformity of messages
consistent messages
information
misinformation
dystopian entertainment
dystopian futures
popular culture
films
television programs
fictional images
concentrated power
political possibilities
celebrity influence
entertainment industry
powerful institutions
Nazi Germany
corporate relationships
historical origin
modern speculation
financial institutions
government control
government authority
government mandates
political power
influence
control over communication
major channels
critical thinking
vigilance
uncertainty
alternative interpretations
competing interpretations
structured debate
public safety
balance between safety and freedom
source bibliography
five references
historical society
elite power
online life
public-health response
digital platforms
political narratives
secret governing project
storytelling
media literacy
data collection
crisis governance
emergency governance
social restrictions
health measures
global coordination
global crisis
centralized authority
online education
remote work
internet
autonomy and freedom
power of media
secret government
permanent surveillance
social conditioning
monitoring
public consent
media and popular culture'''.splitlines()
phrases += '''pandemic-era surveillance
isolation and uncertainty
dependence on authorities
necessary health response
fear-driven explanation
public willingness
intrusive control
temporary control
channels of communication
secret-society legends
organized reality
repeated fictional images
form of conditioning
Bavarian government
means of protection
continuing organization
contemporary test case
far-reaching measures
power of media conglomerates
explanation for complex events'''.splitlines()
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
weak={'1776','pandemic','restrictions','control','surveillance','autonomy','freedom','crisis','emergency','information','conspiracy','fear','influence','films','internet','monitoring'}
chosen=[];seen=set()
for phrase in phrases:
 key=b.keyword_normalise(phrase).strip()
 if not key or key in weak or key in seen or key in shelf or key not in source or key==b.keyword_normalise('The New World Order: Control or Coincidence?').strip():continue
 chosen.append(phrase);seen.add(key)
 if len(chosen)==90:break
if len(chosen)!=90:raise SystemExit(f'Only {len(chosen)} source terms')
m=json.loads(mp.read_text());m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':chosen,'reviewedOn':'2026-10-08','method':'reader-grounded editorial selection'};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('\n'.join(f'{i:02}. {x}' for i,x in enumerate(chosen,1)))
