/* Open the matching modal when a card is clicked; social links keep their behavior
   + add body.modal-open as a fallback for browsers without :has()
   + notify parent page (if embedded in an <iframe>) to lock/unlock scroll */
(function () {
  function notifyParentModal(isOpen) {
    try {
      parent.postMessage({ type: 'ambassador-modal', open: isOpen }, '*');
    } catch (_) {}
  }

  function setModalOpenClass() {
    var isOpen = !!(location.hash && document.querySelector(location.hash + '.modal'));
    if (isOpen) document.body.classList.add('modal-open');
    else document.body.classList.remove('modal-open');
    notifyParentModal(isOpen);
  }

  // load the big image inside the modal the first time it's opened
  function loadModalAvatar(modalEl) {
    if (!modalEl) return;
    var img = modalEl.querySelector('.modal__avatar');
    if (img && !img.src) {
      var url = img.getAttribute('data-src');
      if (url) img.src = url;
    }
  }

  function init() {
    var cards = Array.prototype.slice.call(
      document.querySelectorAll('.ambassadors-grid .ambassador-card')
    );

    var modalIds = [
      'regina-modal',
      'alejandro-modal',
      'orestis-modal',
      'abdulsalam-modal',
      'giorgio-modal',
      'eyup-modal'
    ];

    document.addEventListener('click', function (e) {
      if (e.target.closest('.social-icons a')) return;

      var card = e.target.closest('.ambassador-card');
      if (!card) return;

      var idx = cards.indexOf(card);
      if (idx > -1 && modalIds[idx]) {
        location.hash = modalIds[idx];
        // NEW: load deferred avatar now
        var modalEl = document.getElementById(modalIds[idx]);
        loadModalAvatar(modalEl);

        setModalOpenClass();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && location.hash) {
        location.hash = '';
        setModalOpenClass();
      }
    });

    // Ensure image loads when arriving with a hash or using back/forward
    window.addEventListener('hashchange', function () {
      setModalOpenClass();
      if (location.hash) {
        loadModalAvatar(document.querySelector(location.hash + '.modal'));
      }
    });

    setModalOpenClass();
    // If page loads with a hash, also try to load that modal image
    if (location.hash) {
      loadModalAvatar(document.querySelector(location.hash + '.modal'));
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
