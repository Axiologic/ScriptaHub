import json
from pathlib import Path
w=Path(__file__).resolve().parent
p=w/'translations/en/full/chunks/0016.json'
a=json.loads(p.read_text())
t=[
'Liberal pluralism can become demographically fragile if it is not materially compatible with the reproduction of those who sustain it.',
'APPENDIX 2. FALSIFICATION QUESTIONS FOR THE FUTURE',
'If subclinical psychopathy confers a reproductive advantage, does the effect replicate in large longitudinal registers rather than only small samples?',
'If society selects against future orientation, do validated measures of temporal discounting negatively predict completed fertility after controlling for status and age?',
'If empathy is taxed reproductively, does the effect persist in countries with excellent family infrastructure? If it disappears, the mechanism is institutional rather than intrinsic.',
'If extreme ideologies reproduce more successfully, does the advantage remain after adjusting for religiosity, education, income, and rural–urban setting?',
'If AI reduces parenting costs, does intensive family use precede measurable increases in the probability of a second or third child?',
'If AI substitutes for human relationships, does increased use of artificial companions precede reduced couple formation and reproductive intentions?',
'If digital tribes produce endogamy, does ideological and behavioral similarity between partners increase across cohorts and generate more closed marriage networks?',
'If megalopolises are “reproductive sinks,” what proportion of the deficit reflects contextual effects, and what proportion reflects selection through migration?',
'If institutions can neutralize selection on human capital, do housing and care reforms reduce the fertility gradient by education without pronatalist coercion?',
'If pluralism is demographically sustainable, societies with high freedom and strong family support should show smaller fertility differences between subcultures than societies with high freedom but high family costs.',
'SELECTED BIBLIOGRAPHY']
# Bibliographic entries t000711–t000825 were individually read in this translation pass;
# they are already English reference strings, so retain their exact spelling and identifiers.
t.extend(s['source'] for s in a['segments'][13:128])
t.extend([
'ON SOURCES AND LIMITS',
'The literature used in this book combines behavioral genetics, population genetics, demography, cross-cultural psychology, psychiatric epidemiology, evolutionary anthropology, and philosophy. These fields do not use identical definitions or have the same inferential power. Numbers should therefore not be compared mechanically between studies.',
'In particular:',
'polygenic scores are statistical predictions dependent on the population and study in which they were developed;',
'heritability does not describe the “genetic” proportion of an individual or fix the effect of the environment;',
'psychiatric diagnoses and dimensional personality scores are not interchangeable;',
'“extremism,” “religiosity,” and “conservatism/liberalism” are distinct constructs;',
'number of children is only a proxy for long-term fitness;'])
assert len(t)==len(a['segments'])
(w/'translated-0016.txt').write_text('\n'.join(t)+'\n')
