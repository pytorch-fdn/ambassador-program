/* Build ambassadors from JSON + keep modal behavior and scroll lock */
(function () {
  const DATA_URL = "./ambassadors.json";

  // tiny helpers
  const isBlank = v => !v || String(v).toLowerCase() === "nan" || String(v).trim() === "";
  const safeLink = v => (isBlank(v) ? "" : (/^https?:\/\//i.test(v) ? v : "https://" + v));
  const fixAvatarUrl = url => {
    if (!url) return "";
    // turn github.com/.../blob/main/... into raw.githubusercontent.com/.../main/...
    const m = url.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/blob\/([^/]+)\/(.+)$/i);
    return m ? `https://raw.githubusercontent.com/${m[1]}/${m[2]}/${m[3]}/${m[4]}` : url;
  };

  function notifyParentModal(isOpen) {
    try { parent.postMessage({ type: 'ambassador-modal', open: isOpen }, '*'); } catch (_) {}
  }
  function setModalOpenClass() {
    const open = !!(location.hash && document.querySelector(location.hash + '.modal'));
    document.body.classList.toggle('modal-open', open);
    notifyParentModal(open);
  }

  // FIX: check the attribute (not img.src) and run through fixAvatarUrl
  function loadModalAvatar(modalEl) {
    if (!modalEl) return;
    const img = modalEl.querySelector('.modal__avatar');
    if (!img) return;

    const currentAttr = img.getAttribute('src'); // this is empty when we set src=""
    if (!currentAttr) {
      const url = img.getAttribute('data-src');
      if (url) img.src = fixAvatarUrl(url);
    }
  }

  // card + modal templates
  const cardHTML = a => `
    <div class="ambassador-card" data-id="${a.id}">
      <img class="avatar" src="${a.avatar}" alt="${a.name}" width="140" height="140" loading="lazy" />
      <h3 class="name">${a.name}</h3>
      <p class="pronouns">${isBlank(a.pronouns) ? "—" : a.pronouns}</p>
      <div class="social-icons">
        ${isBlank(a.github) ? "" : `
          <a class="icon" href="${safeLink(a.github)}" target="_blank" rel="noopener" aria-label="GitHub">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="20" height="20" />
          </a>`}
        ${isBlank(a.linkedin) ? "" : `
          <a class="icon" href="${safeLink(a.linkedin)}" target="_blank" rel="noopener" aria-label="LinkedIn">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="20" height="20" />
          </a>`}
      </div>
    </div>
  `;

  const modalHTML = a => `
    <section id="${a.id}-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="${a.id}-title">
      <a href="#" class="modal__backdrop" aria-hidden="true"></a>
      <div class="modal__card">
        <a href="#" class="modal__close" aria-label="Close">×</a>

        <div class="modal__avatar-wrap">
          <img class="modal__avatar"
               src="" data-src="${a.avatar}"
               alt="${a.name}" width="140" height="140" />
        </div>

        <div class="modal__header">
          <h3 id="${a.id}-title">${a.name}</h3>
          <p class="pronouns">${isBlank(a.pronouns) ? "—" : a.pronouns}</p>
          ${isBlank(a.location) ? "" : `<p class="location">Location: ${a.location}</p>`}
        </div>
        <p class="bio">${isBlank(a.bio) ? "—" : a.bio}</p>
      </div>
    </section>
  `;

  async function init() {
    const grid = document.getElementById('ambassadors-grid');
    if (!grid) return;

    // fetch + normalize
    let people = [];
    try {
      const r = await fetch(DATA_URL, { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      people = await r.json();
    } catch (e) {
      console.error("Failed to load ambassadors.json:", e);
      return;
    }

    // normalize avatars + sort by name (defensive)
    people.forEach(p => { p.avatar = fixAvatarUrl(p.avatar); });
    people.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));

    // inject cards
    const frag = document.createDocumentFragment();
    people.forEach(a => {
      const t = document.createElement('template');
      t.innerHTML = cardHTML(a).trim();
      frag.appendChild(t.content.firstElementChild);
    });
    grid.replaceChildren(frag);

    // inject modals (outside page-content so blur doesn't affect them)
    const mfrag = document.createDocumentFragment();
    people.forEach(a => {
      const t = document.createElement('template');
      t.innerHTML = modalHTML(a).trim();
      mfrag.appendChild(t.content.firstElementChild);
    });
    document.body.appendChild(mfrag);

    // open/close behavior
    document.addEventListener('click', e => {
      if (e.target.closest('.social-icons a')) return;
      const card = e.target.closest('.ambassador-card');
      if (!card) return;
      const id = card.getAttribute('data-id');
      location.hash = id + '-modal';
      loadModalAvatar(document.getElementById(id + '-modal'));
      setModalOpenClass();
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && location.hash) {
        location.hash = '';
        setModalOpenClass();
      }
    });

    window.addEventListener('hashchange', () => {
      setModalOpenClass();
      if (location.hash) loadModalAvatar(document.querySelector(location.hash + '.modal'));
    });

    // initial state (handles shared hash links)
    setModalOpenClass();
    if (location.hash) loadModalAvatar(document.querySelector(location.hash + '.modal'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
