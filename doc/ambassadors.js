/* Build cards & modals from JSON (keeps existing design and behavior) */
(async function () {
  // Use your published JSON on GitHub Pages, or "./ambassadors.json" if colocated
  const DATA_URL = "https://pytorch-fdn.github.io/ambassador-program/doc/ambassadors.json";

  let people = [];
  try {
    const r = await fetch(DATA_URL, { cache: "no-store" });
    if (!r.ok) throw new Error(`Fetch failed: ${r.status}`);
    people = await r.json();
  } catch (err) {
    console.error("[Ambassadors] Could not load data:", err);
    return;
  }

  // Sort by name A→Z
  people.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" }));

  const grid = document.getElementById("ambassadors-grid");
  if (!grid) return;

  // Normalize helpers
  const safe = (s) => (s == null ? "" : String(s).trim());
  const has = (s) => !!safe(s);

  const cardHTML = (a) => `
    <div class="ambassador-card" data-id="${a.id}">
      <img class="avatar" src="${safe(a.avatar)}" alt="${safe(a.name)}" width="140" height="140" loading="lazy" />
      <h3 class="name">${safe(a.name)}</h3>
      <p class="pronouns">${has(a.pronouns) ? safe(a.pronouns) : "—"}</p>
      <div class="social-icons">
        ${has(a.github) ? `
          <a class="icon" href="${safe(a.github)}" target="_blank" rel="noopener" aria-label="GitHub">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="20" height="20" />
          </a>` : ``}
        ${has(a.linkedin) ? `
          <a class="icon" href="${safe(a.linkedin)}" target="_blank" rel="noopener" aria-label="LinkedIn">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="20" height="20" />
          </a>` : ``}
      </div>
    </div>
  `;

  const modalHTML = (a) => `
    <section id="${a.id}-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="${a.id}-title">
      <a href="#" class="modal__backdrop" aria-hidden="true"></a>
      <div class="modal__card">
        <a href="#" class="modal__close" aria-label="Close">×</a>

        <div class="modal__avatar-wrap">
          <img class="modal__avatar" src="${safe(a.avatar)}" alt="${safe(a.name)}" width="140" height="140" />
        </div>

        <div class="modal__header">
          <h3 id="${a.id}-title">${safe(a.name)}</h3>
          <p class="pronouns">${has(a.pronouns) ? safe(a.pronouns) : "—"}</p>
          ${has(a.location) ? `<p class="location">Location: ${safe(a.location)}</p>` : ``}
        </div>

        <p class="bio">${has(a.bio) ? safe(a.bio) : "—"}</p>
      </div>
    </section>
  `;

  // Build cards
  {
    const frag = document.createDocumentFragment();
    people.forEach((p) => {
      const t = document.createElement("template");
      t.innerHTML = cardHTML(p).trim();
      frag.appendChild(t.content.firstElementChild);
    });
    grid.replaceChildren(frag);
  }

  // Build modals (append to <body>, like your previous layout)
  {
    const frag = document.createDocumentFragment();
    people.forEach((p) => {
      const t = document.createElement("template");
      t.innerHTML = modalHTML(p).trim();
      frag.appendChild(t.content.firstElementChild);
    });
    document.body.appendChild(frag);
  }

  // ===== Behavior: open/close, scroll lock, background blur, iframe notify =====
  function notifyParentModal(isOpen) {
    try { parent.postMessage({ type: 'ambassador-modal', open: isOpen }, '*'); } catch (_) {}
  }
  function setModalOpenClass() {
    const isOpen = !!(location.hash && document.querySelector(location.hash + '.modal'));
    document.body.classList.toggle('modal-open', isOpen);
    notifyParentModal(isOpen);
  }

  // Click a card → open its modal
  document.addEventListener('click', function (e) {
    if (e.target.closest('.social-icons a')) return; // let social links work normally
    const cardEl = e.target.closest('.ambassador-card');
    if (!cardEl) return;
    const id = cardEl.getAttribute('data-id');
    if (!id) return;
    location.hash = id + '-modal';
    setModalOpenClass();
  });

  // ESC closes the modal
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && location.hash) {
      location.hash = '';
      setModalOpenClass();
    }
  });

  // Back/forward or clicking backdrop
  window.addEventListener('hashchange', setModalOpenClass);

  // If the page loads with a modal already open (e.g., shared link)
  setModalOpenClass();
})();
