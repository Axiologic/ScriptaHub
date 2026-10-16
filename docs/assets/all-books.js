(() => {
  "use strict";
  const host = document.querySelector("[data-all-books]");
  const collection = globalThis.SCRIPTA_COLLECTION;
  if (!host || !collection) return;

  const shelves = [
    ["ai-systems", "AI systems", "Sisteme AI"],
    ["ai-society", "AI and society", "AI și societate"],
    ["computing", "Computing and software", "Informatică și software"],
    ["research", "Research and scientific methods", "Cercetare și metode științifice"],
    ["mathematics", "Mathematics and logic", "Matematică și logică"],
    ["natural-science", "Natural sciences", "Științe naturale"],
    ["space", "Space and astronomy", "Spațiu și astronomie"],
    ["knowledge", "Knowledge and reasoning", "Cunoaștere și raționament"],
    ["ethics", "Ethics and meaning", "Etică și sens"],
    ["religion", "Religion and myth", "Religie și mit"],
    ["money", "Money and finance", "Bani și finanțe"],
    ["economics", "Economics", "Economie"],
    ["business", "Business and entrepreneurship", "Afaceri și antreprenoriat"],
    ["politics", "Politics and power", "Politică și putere"],
    ["rights", "Rights and freedom", "Drepturi și libertate"],
    ["society", "Society and culture", "Societate și cultură"],
    ["history", "History and biography", "Istorie și biografii"],
    ["education", "Education and learning", "Educație și învățare"],
    ["classics", "Literary classics", "Clasici literari"],
    ["literary-guides", "Guides to literature", "Ghiduri literare"],
    ["science-fiction", "Science fiction", "Science-fiction"],
    ["fantasy", "Fantasy and horror", "Fantasy și horror"],
    ["literary-fiction", "Literary fiction", "Ficțiune literară"],
    ["speculative", "Speculative ideas", "Idei speculative"],
  ];
  const shelfTranslations = {
    fr: ["Systèmes d’IA", "IA et société", "Informatique et logiciels", "Recherche et méthodes scientifiques", "Mathématiques et logique", "Sciences naturelles", "Espace et astronomie", "Savoir et raisonnement", "Éthique et sens", "Religion et mythes", "Argent et finance", "Économie", "Affaires et entrepreneuriat", "Politique et pouvoir", "Droits et liberté", "Société et culture", "Histoire et biographies", "Éducation et apprentissage", "Classiques littéraires", "Guides littéraires", "Science-fiction", "Fantastique et horreur", "Fiction littéraire", "Idées spéculatives"],
    de: ["KI-Systeme", "KI und Gesellschaft", "Informatik und Software", "Forschung und wissenschaftliche Methoden", "Mathematik und Logik", "Naturwissenschaften", "Weltraum und Astronomie", "Wissen und Denken", "Ethik und Sinn", "Religion und Mythos", "Geld und Finanzen", "Wirtschaft", "Unternehmen und Gründung", "Politik und Macht", "Rechte und Freiheit", "Gesellschaft und Kultur", "Geschichte und Biografien", "Bildung und Lernen", "Literarische Klassiker", "Literaturführer", "Science-Fiction", "Fantasy und Horror", "Literarische Fiktion", "Spekulative Ideen"],
    es: ["Sistemas de IA", "IA y sociedad", "Informática y software", "Investigación y métodos científicos", "Matemáticas y lógica", "Ciencias naturales", "Espacio y astronomía", "Conocimiento y razonamiento", "Ética y sentido", "Religión y mito", "Dinero y finanzas", "Economía", "Negocios y emprendimiento", "Política y poder", "Derechos y libertad", "Sociedad y cultura", "Historia y biografías", "Educación y aprendizaje", "Clásicos literarios", "Guías literarias", "Ciencia ficción", "Fantasía y terror", "Ficción literaria", "Ideas especulativas"],
    pt: ["Sistemas de IA", "IA e sociedade", "Informática e software", "Investigação e métodos científicos", "Matemática e lógica", "Ciências naturais", "Espaço e astronomia", "Conhecimento e raciocínio", "Ética e sentido", "Religião e mito", "Dinheiro e finanças", "Economia", "Negócios e empreendedorismo", "Política e poder", "Direitos e liberdade", "Sociedade e cultura", "História e biografias", "Educação e aprendizagem", "Clássicos literários", "Guias literários", "Ficção científica", "Fantasia e terror", "Ficção literária", "Ideias especulativas"],
    it: ["Sistemi di IA", "IA e società", "Informatica e software", "Ricerca e metodi scientifici", "Matematica e logica", "Scienze naturali", "Spazio e astronomia", "Conoscenza e ragionamento", "Etica e significato", "Religione e mito", "Denaro e finanza", "Economia", "Impresa e imprenditorialità", "Politica e potere", "Diritti e libertà", "Società e cultura", "Storia e biografie", "Educazione e apprendimento", "Classici letterari", "Guide letterarie", "Fantascienza", "Fantasy e horror", "Narrativa letteraria", "Idee speculative"],
    pl: ["Systemy AI", "AI i społeczeństwo", "Informatyka i oprogramowanie", "Badania i metody naukowe", "Matematyka i logika", "Nauki przyrodnicze", "Kosmos i astronomia", "Wiedza i rozumowanie", "Etyka i sens", "Religia i mit", "Pieniądze i finanse", "Ekonomia", "Biznes i przedsiębiorczość", "Polityka i władza", "Prawa i wolność", "Społeczeństwo i kultura", "Historia i biografie", "Edukacja i nauka", "Klasyka literatury", "Przewodniki literackie", "Fantastyka naukowa", "Fantasy i horror", "Proza literacka", "Idee spekulatywne"],
  };
  const ui = {
    en: ["All Books", "Browse the complete library by subject. Every book appears in one shelf; use search to find a title or idea across all shelves.", "Search books, subjects or ideas", "books across", "shelves", "No books match your search.", "Categories"],
    fr: ["Tous les livres", "Parcourez toute la bibliothèque par sujet. Chaque livre figure dans un rayon ; cherchez un titre ou une idée dans tous les rayons.", "Rechercher un livre, un sujet ou une idée", "livres dans", "rayons", "Aucun livre ne correspond à cette recherche.", "Catégories"],
    de: ["Alle Bücher", "Entdecken Sie die gesamte Bibliothek nach Themen. Jedes Buch steht in einem Regal; die Suche erfasst alle Regale.", "Bücher, Themen oder Ideen suchen", "Bücher in", "Regalen", "Keine Bücher gefunden.", "Kategorien"],
    es: ["Todos los libros", "Explora toda la biblioteca por temas. Cada libro aparece en una sección; la búsqueda abarca todas.", "Buscar libros, temas o ideas", "libros en", "secciones", "No hay libros que coincidan.", "Categorías"],
    pt: ["Todos os livros", "Explore toda a biblioteca por assunto. Cada livro aparece numa secção; a pesquisa abrange todas.", "Pesquisar livros, temas ou ideias", "livros em", "secções", "Nenhum livro corresponde à pesquisa.", "Categorias"],
    it: ["Tutti i libri", "Esplora tutta la biblioteca per argomento. Ogni libro compare in una sezione; la ricerca le comprende tutte.", "Cerca libri, argomenti o idee", "libri in", "sezioni", "Nessun libro corrisponde alla ricerca.", "Categorie"],
    ro: ["Toate cărțile", "Răsfoiește întreaga bibliotecă pe teme. Fiecare carte are un raft; căutarea acoperă toate rafturile.", "Caută cărți, subiecte sau idei", "cărți în", "rafturi", "Nicio carte nu corespunde căutării.", "Categorii"],
    pl: ["Wszystkie książki", "Przeglądaj całą bibliotekę według tematów. Każda książka należy do jednej kategorii; wyszukiwarka obejmuje wszystkie.", "Szukaj książek, tematów lub pomysłów", "książek w", "kategoriach", "Brak pasujących książek.", "Kategorie"],
  };
  const escape = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
  const normalise = value => String(value ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase();
  const local = (value, language) => value?.[language] || value?.en || "";
  const label = (shelf, language) => shelfTranslations[language]?.[shelves.indexOf(shelf)] || (language === "ro" ? shelf[2] : shelf[1]);

  // A stable editorial shelf for each book, derived from its existing subject and title.
  function shelfFor(book) {
    const title = normalise(book.title?.en);
    const category = normalise(book.category);
    const group = book.group;
    if (group === "fiction") {
      if (/quick guide to notorious conspiracy theories/.test(title)) return "society";
      if (/hitchhiker.s guide|oriven and origaya|science and wisdom of limits/.test(title)) return "science-fiction";
      if (/guide|explor|navigat|unveil|revealing|discovering|journey.*(hobbit|gatsby|alchemist)|hidden|wisdom of|impact on|take on|unbound|world of|universe|vision of|mysteries of|dilemma|freedom: jane|chaos$/.test(title)) return "literary-guides";
      if (/science fiction|human & philosophical sf|political & social sf/.test(category) || /star trek|star wars|warhammer|foundation|three.body|expanse|cyberpunk|altered carbon|matrix|sg 1|robots|galactic|mars|solips|substrate|omnis|oriven|dystopia/.test(title)) return "science-fiction";
      if (/dracula|frankenstein|sleepy hollow|jekyll|veil|basilisk|predator/.test(title)) return "fantasy";
      if (/alice|catcher in the rye|moby dick|oliver twist|peter pan|pride and prejudice|robinson crusoe|white fang|wuthering heights|yellow wallpaper|call of the wild|enchanted april|ferdinand count fathom|lost world/.test(title)) return "classics";
      if (/specul|philosoph|experiment/.test(category)) return "speculative";
      return "literary-fiction";
    }
    if (/education|learning|grades|curious kids|introductory guide/.test(title + " " + category)) return "education";
    if (/einstein|newton|darwin|tesla|edison|leonardo|steve jobs|elon musk|frederick douglass/.test(title)) return "history";
    if (/space|astronom|alien|planetary sky/.test(title)) return "space";
    if (group === "business") return /econom|capitalism|keynes|marshall|crash|finance|investing/.test(title + " " + category) ? "economics" : "business";
    if (/bitcoin|bank|money|finance|currency|satoshi|asset management|financial/.test(title)) return "money";
    if (category === "economics" || /scarcity|markets|capitalism|economic/.test(title)) return "economics";
    if (/logic|mathematics|equations|calculus/.test(title)) return "mathematics";
    if (/religion|kabbalah|taoism|jesus|prays|messiah|gospel/.test(title)) return "religion";
    if (/rights|freedom|liberty|serfdom|responsibility|permission|copy|saved|nobility/.test(title)) return "rights";
    if (/power|rule|control|government|institutions|contract|strategist|masters|predator|civilization|civilisation/.test(title + " " + category)) return "politics";
    if (group === "technology") return /\bai\b|agent|intelligence|\brag\b|\blm\b|coherence|judgment|bias/.test(title) || category === "ai systems & infrastructure" ? "ai-systems" : "computing";
    if (group === "science") {
      if (/flat earth/.test(title)) return "natural-science";
      if (/research|executable|scientific|rules|relevance/.test(title + " " + category)) return "research";
      if (/technology|machine|circuits|symbolic/.test(title + " " + category)) return "computing";
      return "natural-science";
    }
    if (group === "philosophy") {
      if (/outfinit|reality|reason|knowing|explanation|logic|evidence|meaning/.test(title + " " + category)) return "knowledge";
      return "ethics";
    }
    if (/\bai\b|digital|feed|internet|technology|machine/.test(title)) return "ai-society";
    if (/history|ancient|holocaust|war|peace|conspirac/.test(title)) return "history";
    if (/future|world|speculat/.test(title)) return "speculative";
    return "society";
  }

  const assigned = collection.books.map(book => ({book, shelf: shelfFor(book)}));
  function render(language) {
    const words = ui[language] || ui.en;
    document.title = `${words[0]} · ScriptaHub`;
    document.documentElement.lang = language;
    const prior = host.querySelector("input")?.value || "";
    host.innerHTML = `<header class="library-heading"><h1>${escape(words[0])}</h1><p>${escape(words[1])}</p></header><div class="library-controls"><input class="library-search" type="search" aria-label="${escape(words[2])}" placeholder="${escape(words[2])}" value="${escape(prior)}"><details class="library-category-picker"${matchMedia("(max-width: 600px)").matches ? "" : " open"}><summary>${escape(words[6])}</summary><nav class="library-categories" aria-label="${escape(words[6])}"></nav></details></div><p class="library-count" aria-live="polite"></p><div class="library-sections"></div>`;
    const input = host.querySelector("input");
    const categories = host.querySelector(".library-categories");
    categories.addEventListener("click", event => { if (event.target.closest("a") && matchMedia("(max-width: 600px)").matches) categories.closest("details").open = false; });
    const sections = host.querySelector(".library-sections");
    const count = host.querySelector(".library-count");
    const draw = () => {
      const needle = normalise(input.value.trim());
      const matching = assigned.filter(({book, shelf}) => !needle || normalise([local(book.title, language), ...Object.values(book.title || {}), local(book.subtitle, language), local(book.shortDescription, language), ...(book.keywords?.[language] || []), label(shelves.find(item => item[0] === shelf), language)].join(" ")).includes(needle));
      const activeShelves = shelves.map(shelf => ({shelf, books: matching.filter(item => item.shelf === shelf[0]).map(item => item.book).sort((a, b) => local(a.title, language).localeCompare(local(b.title, language), language))})).filter(item => item.books.length);
      categories.innerHTML = activeShelves.map(({shelf, books}) => `<a href="#${shelf[0]}">${escape(label(shelf, language))}<small>${books.length}</small></a>`).join("");
      count.textContent = `${matching.length} ${words[3]} ${activeShelves.length} ${words[4]}`;
      sections.innerHTML = activeShelves.length ? activeShelves.map(({shelf, books}) => `<section class="library-section" id="${shelf[0]}"><h2>${escape(label(shelf, language))}</h2><div class="library-list">${books.map(book => {
        const path = book.editions?.[language]?.book || book.editions?.en?.book;
        const href = new URL(`../${path}?lang=${language}`, location.href).href;
        const thumbnail = new URL(`../${local(book.thumbnailUrl, language)}`, location.href).href;
        return `<article class="library-item"><a href="${escape(href)}" tabindex="-1" aria-hidden="true"><img src="${escape(thumbnail)}" alt="" loading="lazy"></a><div><h3><a href="${escape(href)}">${escape(local(book.title, language))}</a></h3><p>${escape(local(book.subtitle, language) || book.category)}</p></div></article>`;
      }).join("")}</div></section>`).join("") : `<p class="library-empty">${escape(words[5])}</p>`;
    };
    input.addEventListener("input", draw);
    draw();
  }
  const language = () => ui[document.documentElement.lang] ? document.documentElement.lang : "en";
  document.addEventListener("scriptahub:language", event => render(event.detail.language));
  render(language());
})();
