"""A chapter-complete ten-minute guide to Jack London's novel."""
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
parts = [
 ('Part I — The wild', [
  ('The Trail of the Meat', 'Henry and Bill travel through the frozen Northland with a sled, a coffin, and a dwindling team of dogs. A starving wolf pack follows them, and its unsettling closeness turns the journey into a struggle to keep the fire, the dogs, and themselves alive.'),
  ('The She-Wolf', 'The men discover that a she-wolf can draw their dogs away from camp. Their traps and watchfulness do not end the danger; the pack stays near, and Bill grows increasingly determined to confront it.'),
  ('The Hunger Cry', 'Bill pursues a dog lured from the sled and does not return. Henry survives by maintaining a ring of fire until a rescue party finds him; the wolves leave to seek other prey.'),
 ]),
 ('Part II — Born into the wild', [
  ('The Battle of the Fangs', 'The she-wolf travels with the pack as hunger and rivalry govern its movement. When food becomes more plentiful, the pack separates, and the one-eyed wolf survives the contest for her companionship.'),
  ('The Lair', 'The she-wolf chooses a sheltered den and gives birth. One Eye hunts for his mate and the cubs; the northern spring offers food, but every successful hunt still carries danger.'),
  ('The Grey Cub', 'The grey cub is unlike his reddish littermates. He learns the limits of the den, his mother’s warnings, and the pull of the light outside, while famine reduces the family.'),
  ('The Wall of the World', 'At the den entrance the cub meets an unknown world of slopes, water, birds, and predators. Fear and curiosity shape his first experiments, and the consequences teach him more effectively than any explanation could.'),
  ('The Law of Meat', 'The cub’s hunts and encounters with other creatures teach the harsh relation between eating and being eaten. The law is lived through hunger, risk, and his mother’s protection, never given to him as an abstract rule.'),
 ]),
 ('Part III — The gods of men', [
  ('The Makers of Fire', 'The cub and his mother meet an Indigenous camp. The people know Kiche, name the cub White Fang, and command powers he cannot match, above all fire. He begins to learn a new order of obedience and restraint.'),
  ('The Bondage', 'Life in the camp binds White Fang to human masters even as it exposes him to dogs that torment him. He develops caution, cunning, and a fierce capacity to defend himself.'),
  ('The Outcast', 'Lip-lip and the puppy pack keep White Fang apart from the other dogs. Isolation and repeated attacks sharpen his hostility rather than making him naturally sociable.'),
  ('The Trail of the Gods', 'White Fang travels with the people and watches their ways. His attachment to the camp grows alongside a persistent pull toward the wilderness from which he came.'),
  ('The Covenant', 'His relation to the humans becomes a practical bargain of food, protection, service, and power. He learns the rules imposed by his masters while preserving his own wary judgment.'),
  ('The Famine', 'When famine reaches the camp, White Fang survives by returning to the skills of the wild. His movements reveal that his life with humans has changed him without erasing his older instincts.'),
 ]),
 ('Part IV — Violence and care', [
  ('The Enemy of His Kind', 'White Fang’s experience with hostile dogs makes him formidable in conflict. His strength becomes a source of fear for other dogs and eventually a resource that people can exploit.'),
  ('The Mad God', 'Beauty Smith takes control of White Fang and treats him with cruelty. The wolf-dog learns to expect pain from the person who holds power over him.'),
  ('The Reign of Hate', 'Forced into dog fights, White Fang survives by speed, intelligence, and aggression. The chapter makes his savagery a response to deliberate training and abuse, not a simple moral identity.'),
  ('The Clinging Death', 'A fight with the bulldog Cherokee nearly kills White Fang. Weedon Scott and Matt intervene, forcing the dogs apart and ending Beauty Smith’s control over him.'),
  ('The Indomitable', 'Scott and Matt confront an animal who has learned to distrust every hand. Their patience is repeatedly tested, but they refuse to reduce White Fang to the violence bred into him.'),
  ('The Love-Master', 'Scott speaks gently, offers food, and keeps returning. White Fang gradually accepts touch and develops a devotion unlike his earlier obedience, though his habits of watchfulness remain.'),
 ]),
 ('Part V — The Southland', [
  ('The Long Trail', 'Scott plans to leave the North for California, believing White Fang cannot follow. White Fang finds his way to the departing steamer, and Scott chooses to take him along.'),
  ('The Southland', 'San Francisco overwhelms White Fang with noise, machines, crowds, and unfamiliar forms of power. At Scott’s family home, he must also meet animals and people protected by a different set of rules.'),
  ('The God’s Domain', 'At Sierra Vista, White Fang learns which beings belong to the household and which actions are forbidden. His encounters with Collie, the children, and the chickens test the difference between old impulses and learned law.'),
  ('The Call of Kind', 'Human affection continues to change White Fang’s daily life without making him an ordinary pet. He finds ways to express loyalty and protect Scott, while Collie draws him toward another bond.'),
  ('The Sleeping Wolf', 'An escaped convict threatens Judge Scott’s household. White Fang defends the family at terrible cost; his recovery brings the story from the struggle to survive toward a guarded peace among people and young animals.'),
 ]),
]
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>White Fang — Ten-minute read</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h=out.new_tag('h1',id='book-title');h.string='White Fang';article.append(h)
opening=out.new_tag('p');opening.string='Jack London follows a wolf-dog from a northern den through human ownership, violence, care, and a new life in California. The five parts keep the animal’s senses and learned responses close to the reader. This chapter guide follows the complete novel in order; the full edition preserves London’s original prose and dialogue.';article.append(opening)
for i,(part,chapters) in enumerate(parts,1):
 h=out.new_tag('h2',id=f'short-part-{i}');h.string=part;article.append(h)
 for j,(title,summary) in enumerate(chapters,1):
  h=out.new_tag('h3',id=f'short-{i}-{j}');h.string=title;article.append(h)
  p=out.new_tag('p');p.string=summary;article.append(p)
assert sum(len(chapters) for _,chapters in parts)==25
target=root/'book/en/short_content.html';target.write_text(str(out)+'\n')
print(len(article.get_text(' ',strip=True).split()),'words, 25 chapters')
