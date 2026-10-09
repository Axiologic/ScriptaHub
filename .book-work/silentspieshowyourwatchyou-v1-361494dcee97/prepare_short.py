from bs4 import BeautifulSoup
from pathlib import Path

base = Path(__file__).parent / 'book/en'
soup = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Silent Spies: How Do Your Devices Watch You? — Ten-minute edition</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = soup.article

def h(level, text):
    tag = soup.new_tag(f'h{level}')
    tag.string = text
    article.append(tag)

def p(text, chapter=None):
    tag = soup.new_tag('p')
    tag.append(text)
    if chapter:
        tag.append(' ')
        a = soup.new_tag('a', href=f'full_content.html#chapter-{chapter}')
        a.string = f'Read section {chapter} in full'
        tag.append(a)
        tag.append('.')
    article.append(tag)

h(1, 'Silent Spies: How Do Your Devices Watch You?')
p('Phones, apps and connected household devices can collect more information than their owners expect. This book asks where that data goes, what companies may infer from it, and how a person can limit unwanted collection. It moves from microphones and app permissions to home Wi-Fi, commercial profiling and everyday privacy choices. Some scenarios in the source are presented as concerns or possibilities rather than demonstrated facts about every device. The practical thread is to understand permissions, network connections and data use before deciding what to change.')

h(2, 'Why the book begins with digital privacy')
p('The introduction describes devices that accompany daily life: smartphones, fitness trackers, smart speakers, televisions and other connected appliances. Convenience also creates streams of behavioral information. An app may know a location, a device may report how it is used, and a platform may combine many small signals into a detailed profile. The author links these signals to advertising and asks whether users understand what they have agreed to share. The opening sets up privacy as a question of visibility and control, not a demand to abandon technology.', 1)

h(2, 'Phones, microphones and permissions')
p('The first chapter focuses on the phone. It describes microphones, voice assistants and apps that request access to audio, location and other data. The source uses the familiar experience of seeing an advertisement after a conversation to raise a suspicion about passive listening. That example is an illustration of the book’s concern; the chapter does not establish that every such advertisement was caused by a secretly recorded conversation. More generally, permissions determine which functions an app may use, while background activity can make that use hard to notice.')
p('The reader is encouraged to look at what a phone can collect and what each app actually needs. Microphone access, location access and advertising identifiers are different routes to information. Distinguishing them makes the problem more precise than treating the entire device as a single hidden observer.', 2)

h(2, 'The silent network at home')
p('Chapter two turns to Wi-Fi and the growing number of connected objects in a household. A smart speaker, television, thermostat or camera may exchange data with a service or another device while its owner is not actively using it. The chapter describes both the convenience of that network and the security risks created by weak passwords, outdated software or poorly separated devices. It recommends changing default credentials, installing updates and considering a separate network for less trusted connected appliances.')
p('The key idea is that a home network is an environment, not merely a router and a phone. Each additional connected device can become another source of data or another point requiring maintenance. Knowing what is connected is a first step toward choosing what belongs on the network.', 3)

h(2, 'What companies can do with data')
p('The third chapter follows collected information into commercial systems. Apps and platforms can analyze interests, movements, browsing and device use to build profiles for targeted advertising. The book argues that profiling may also affect the messages people see about public issues. Its examples invite scrutiny of how data is shared, inferred and sold; they should be read as an argument about possible influence, not a claim that one company controls every personal decision.')
p('Permissions sit at the entrance to this system, but the effects may appear far away from the app that gathered the information. A reader who understands the chain from collection to profiling can ask better questions about whether a service is worth the access it requests.', 4)

h(2, 'Practical control and the closing argument')
p('Chapter four and the conclusion turn to choices a person can make: review microphone and location permissions, limit unnecessary background activity, remove apps that demand excessive access, strengthen home-network settings and update devices. The book also suggests privacy-focused search and messaging tools, and points to legal rights that may allow a person to request access to or deletion of their data. The exact rights and settings depend on location, service and device, so the useful habit is to inspect the controls actually available.')
p('The book closes by rejecting an all-or-nothing choice between convenience and privacy. It asks readers to become active participants in decisions about their data: notice the trade-offs, change what they can control, and revisit those choices as devices and services change. Awareness is the first step; repeated maintenance gives it practical effect.', 5)

(base / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
