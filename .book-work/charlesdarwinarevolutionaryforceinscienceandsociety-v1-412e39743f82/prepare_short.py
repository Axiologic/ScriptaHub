from html import escape
from pathlib import Path

root = Path('.book-work/charlesdarwinarevolutionaryforceinscienceandsociety-v1-412e39743f82/book/en')
title = 'Charles Darwin A Revolutionary Force in Science and Society'
sections = [
    ('opening', '', [
        "Darwin's theory of evolution by natural selection changed how scientists explain the diversity of life. This book follows the making, refinement, and wider consequences of that theory. It begins with a deliberately speculative question about what Darwin might think of present-day biology, then returns to his education, the Beagle voyage, and the reasoning behind his work. Later chapters trace genetics, disputes about science and religion, social misuse of evolutionary language, and practical applications. The through-line is Darwin's method: observe carefully, compare evidence, and revise explanations when new knowledge arrives.",
    ]),
    ('chapter-1', 'Darwin and modern biology', [
        "The first chapter imagines Darwin encountering discoveries unavailable in his lifetime. DNA and genetics give a physical account of inheritance that he did not possess. The text considers how mutations, population genetics, genetic drift, and evolutionary developmental biology would extend questions he raised about variation and selection. It also mentions neutral mutations, changes that need not improve survival. These imagined reactions are presented as speculation, not as quotations from Darwin. The chapter asks where biological evolution ends and whether technology and culture introduce new forces of change.",
    ]),
    ('chapter-2', 'The path to the Beagle', [
        "Darwin was born into a family with scientific interests. He preferred observing nature to the classical curriculum at school and found the medical training at Edinburgh ill-suited to him. At Cambridge, although preparing for the clergy, he collected beetles and formed a decisive connection with the botanist John Stevens Henslow. Henslow later recommended him for the place aboard HMS Beagle. The chapter shows how family, study, mentors, and an early habit of observation converged before Darwin had a theory of evolution.",
    ]),
    ('chapter-3', 'The Beagle voyage', [
        "The Beagle sailed in 1831 on a survey that became a voyage of almost five years. Darwin traveled as a naturalist, gathering specimens and notes across South America and beyond. Geological layers at Cape Verde suggested slow change over vast time; fossils and living animals prompted comparisons across places. The Galápagos Islands became especially important as he examined how closely related forms differed from island to island. The voyage did not deliver natural selection as a finished idea. It supplied observations that made the fixity of species increasingly difficult to accept.",
    ]),
    ('chapter-4', "The theory's origins", [
        "After returning to England in 1836, Darwin organized his collections and began notebooks on the transformation of species. John Gould's identification of related Galápagos finches sharpened his attention to geographical distribution. Reading Thomas Malthus helped him see that organisms produce more offspring than limited resources can support. If inherited traits vary, individuals with advantageous traits can leave more descendants, and populations can change over generations. The chapter follows that intellectual work toward the publication of On the Origin of Species in 1859.",
    ]),
    ('chapter-5', 'Evolution after Darwin', [
        "Darwin's publication began another phase of inquiry. The rediscovery of Mendel's inheritance research and the rise of population genetics later connected heredity to natural selection. The book notes an early period when competing accounts, including inheritance of acquired traits and directed evolution, challenged Darwinism. The Modern Synthesis brought genetics and selection together; molecular biology and evolutionary developmental biology continued to refine the account. The lesson is that evolutionary theory grew through criticism, measurement, and integration with new fields.",
    ]),
    ('chapter-6', 'Thought and society', [
        "Evolution challenged literal accounts of fixed, separately created species and raised questions about humanity's place in nature. Darwin's arguments entered theological and philosophical debates, but the chapter also distinguishes scientific explanation from political uses made of its vocabulary. Social Darwinism and eugenics borrowed evolutionary language to justify hierarchy and coercion; those programs do not follow simply from natural selection. The discussion then turns to continuing debates about human behavior, morality, and the interaction of biological and cultural influences.",
    ]),
    ('chapter-7', 'Technological implications', [
        "The final content chapter connects evolutionary ideas with practice. Artificial selection shaped crop and animal breeding; attention to genetic diversity informs seed preservation and conservation. Understanding the evolution of bacteria and viruses matters for antibiotic resistance and vaccine development. The book also describes genetic algorithms, swarm intelligence, and synthetic biology as fields that draw, in different ways, on variation, selection, and adaptation. These are applications and analogies, not evidence that every technology works like a living species.",
    ]),
    ('conclusion', 'What remains useful', [
        "Darwin's legacy is both a theory and a model of inquiry. Modern genomics and developmental biology have strengthened and revised evolutionary explanations, while biodiversity loss, disease, and environmental change keep the questions urgent. Read the complete chapters to follow the evidence and disputes behind this compressed account, including where the book speculates about Darwin's reaction to knowledge he could not have seen.",
    ]),
]
body = [f'<h1 id="short-title">{escape(title)}</h1>', '<p class="book-byline">AI Agent Ava DuRhodes</p>']
for anchor, heading, paragraphs in sections:
    if heading:
        body.append(f'<h2 id="summary-{anchor}">{escape(heading)}</h2>')
    for paragraph in paragraphs:
        body.append(f'<p>{escape(paragraph)}</p>')
    if anchor.startswith('chapter-'):
        body.append(f'<p><a href="full_content.html#{anchor}">Read this chapter in full</a>.</p>')
body.append('<p><a href="full_content.html">Read the complete book</a>.</p>')
html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" '
        'content="width=device-width,initial-scale=1"/><title>' + escape(title) + '</title></head><body>'
        '<article data-reader-content>' + '\n'.join(body) + '</article></body></html>\n')
(root / 'short_content.html').write_text(html)
print(root / 'short_content.html', 'words', sum(len(p.split()) for _,_,ps in sections for p in ps))
