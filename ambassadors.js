/* Open the matching modal when a card is clicked; social links keep their behavior */
(function () {
  function init() {
    var cards = Array.prototype.slice.call(
      document.querySelectorAll('.ambassadors-grid .ambassador-card')
    );
    // Keep this order aligned with the cards order in the HTML
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
      }
    });

    // ESC closes the modal
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && location.hash) location.hash = '';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
