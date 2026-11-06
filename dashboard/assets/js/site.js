/* Cupertino3 — small client-side enhancements. The site is fully readable without JS. */
(function () {
  'use strict';

  // Mobile navigation toggle.
  var btn = document.querySelector('.menu-btn');
  var sidebar = document.querySelector('.sidebar');
  if (btn && sidebar) {
    btn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  // Live table filtering. Any input[data-filter] filters the table named by its
  // data-filter attribute (an id).
  Array.prototype.forEach.call(document.querySelectorAll('input[data-filter]'), function (input) {
    var table = document.getElementById(input.getAttribute('data-filter'));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (tr) {
        tr.style.display = !q || tr.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
      });
    });
  });

  // Open external source links in a new tab.
  Array.prototype.forEach.call(document.querySelectorAll('a[href^="http"]'), function (a) {
    if (a.host !== window.location.host) {
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'noopener');
    }
  });
})();
