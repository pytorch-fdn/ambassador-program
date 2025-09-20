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
    // If the hash points to an actual modal section…
    var isOpen = !!(location.hash && document.querySelector(location.hash + '.modal'));

    if (isOpen) {
      document.body.classList.add('modal-open');
    } else {
      document.body.classList.remove('modal-open');
    }

    notifyParentModal(isOpen);
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
      // Ignore clicks on social icons so they behave normally
      if (e.target.closest('.social-icons a')) return;

      var card = e.target.closest('.ambassador-card');
      if (!card) return;

      var idx = cards.indexOf(card);
      if (idx > -1 && modalIds[idx]) {
        location.hash = modalIds[idx];
        setModalOpenClass(); //
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && location.hash) {
        location.hash = '';
        setModalOpenClass();
      }
    });

    // Handle browser back/forward or backdrop clicks
    window.addEventListener('hashchange', setModalOpenClass);

    // If the page loads with a modal already open (e.g., shared link)
    setModalOpenClass();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
