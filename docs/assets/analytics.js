(() => {
  "use strict";

  // One tracker per document, independent of catalogue and reader loading.
  if (document.querySelector('script[data-website-id]')) return;
  const script = document.createElement('script');
  script.defer = true;
  script.src = 'https://bizanso.com/base-agent-additional-server/umamiAgent/3000/script.js';
  script.dataset.websiteId = 'b1ee0e11-362a-479a-be3c-c238f72aec35';
  document.head.append(script);
})();
