import { connect } from './browser-session.mjs';

const base = process.env.SCRIPTA_TEST_BASE || 'http://127.0.0.1:8080/';
const browser = await connect('about:blank');

try {
  await browser.send('Page.navigate', { url: `${base}librarian/index.html?lang=ro#request=Right` });
  await browser.wait('document.querySelectorAll(".librarian-results-list > *").length > 0');
  const result = await browser.evaluate(`(() => {
    const cards = [...document.querySelectorAll('.librarian-results-list [data-book-id]')];
    return {
      collectionHasBook: SCRIPTA_COLLECTION.books.some(book => book.id === 'bk-991e0f6de1884c5e'),
      resultIds: cards.map(card => card.dataset.bookId),
      titles: cards.map(card => card.querySelector('h2,h3')?.textContent || '')
    };
  })()`);
  if (!result.collectionHasBook || !result.resultIds.includes('bk-991e0f6de1884c5e')) {
    throw new Error(`English title word did not find the Romanian book card: ${JSON.stringify(result)}`);
  }
  console.log('Romanian Librarian finds The Right to Copy from the English query “Right”.');
} finally {
  await browser.close();
}
