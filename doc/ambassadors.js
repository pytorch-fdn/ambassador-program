(async function () {
  const DATA_URL = "./ambassadors.json";
  let people = [];
  try {
    const r = await fetch(DATA_URL, { cache: "no-store" });
    if (!r.ok) throw new Error();
    people = await r.json();
  } catch { return; }

  const grid = document.getElementById("ambassadors-grid");
  if (!grid) return;

  const card = a => `
    <div class="ambassador-card" data-id="${a.id}">
      <img class="avatar" src="${a.avatar}" alt="${a.name}" width="140" height="140" loading="lazy" />
      <h3 class="name">${a.name}</h3>
      <p class="pronouns">${a.pronouns || "—"}</p>
      <div class="social-icons">
        ${a.github ? `<a class="icon" href="${a.github}" target="_blank" rel="noopener" aria-label="GitHub">
          <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="20" height="20"></a>` : ``}
        ${a.linkedin ? `<a class="icon" href="${a.linkedin}" target="_blank" rel="noopener" aria-label="LinkedIn">
          <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="20" height="20"></a>` : ``}
      </div>
    </div>
  `;

  const modal = a => `
    <section id="${a.id}-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="${a.id}-title">
      <a href="#" class="modal__backdrop" aria-hidden="true"></a>
      <div class="modal__card">
        <a href="#" class="modal__close" aria-label="Close">×</a>

        <!-- avatar inside modal -->
        <div class="modal__avatar-wrap">
          <img class="modal__avatar" src="${a.avatar}" alt="${a.name}" width="140" height="140" loading="lazy" />
        </div>

        <div class="modal__header">
          <h3 id="${a.id}-title">${a.name}</h3>
          <p class="pronouns">${a.pronouns || "—"}</p>
          ${a.location ? `<p class="location">Location: ${a.location}</p>` : ``}
        </div>
        <p class="bio">${a.bio || "—"}</p>
      </div>
    </section>
  `;

  // cards
  const frag = document.createDocumentFragment();
  people.forEach(a => {
    const t = document.createElement("template");
    t.innerHTML = card(a).trim();
    frag.appendChild(t.content.firstElementChild);
  });
  grid.replaceChildren(frag);

  // modals
  const mfrag = document.createDocumentFragment();
  people.forEach(a => {
    const t = document.createElement("template");
    t.innerHTML = modal(a).trim();
    mfrag.appendChild(t.content.firstElementChild);
  });
  document.body.appendChild(mfrag);

  // open/close
  function setModalOpenClass() {
    const open = !!(location.hash && document.querySelector(location.hash + '.modal'));
    document.body.classList.toggle('modal-open', open);
    try { parent.postMessage({ type: 'ambassador-modal', open }, '*'); } catch {}
  }

  document.addEventListener('click', e => {
    if (e.target.closest('.social-icons a')) return;
    const cardEl = e.target.closest('.ambassador-card');
    if (!cardEl) return;
    location.hash = cardEl.getAttribute('data-id') + '-modal';
    setModalOpenClass();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && location.hash) { location.hash = ''; setModalOpenClass(); }
  });

  window.addEventListener('hashchange', setModalOpenClass);
  setModalOpenClass();
})();
