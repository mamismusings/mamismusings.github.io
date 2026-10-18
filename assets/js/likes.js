/* Like hearts for Mami's Musings. Counts come from a Google Apps Script (see tools/likes.gs).
   One like per sketch per browser, remembered in localStorage. */
(function () {
  var endpoint = document.body.getAttribute('data-likes');
  if (!endpoint) return;

  function store(get, id, val) {
    try {
      var key = 'mm-liked-' + id;
      if (get) return localStorage.getItem(key) === '1';
      if (val) localStorage.setItem(key, '1'); else localStorage.removeItem(key);
    } catch (e) { return false; }
  }

  function setCount(id, n) {
    document.querySelectorAll('[data-like-count="' + id + '"]').forEach(function (el) {
      el.textContent = n > 0 ? n : '';
      var wrap = el.closest('.card-likes');
      if (wrap) wrap.hidden = !(n > 0);
    });
  }

  var counts = {};
  fetch(endpoint + '?action=all')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      counts = d.counts || {};
      Object.keys(counts).forEach(function (id) { setCount(id, counts[id]); });
    })
    .catch(function () {});

  document.querySelectorAll('[data-like-btn]').forEach(function (btn) {
    var id = btn.getAttribute('data-like-btn');
    btn.hidden = false;
    btn.setAttribute('aria-pressed', store(true, id) ? 'true' : 'false');
    btn.addEventListener('click', function () {
      var liked = btn.getAttribute('aria-pressed') === 'true';
      var action = liked ? 'unlike' : 'like';
      btn.setAttribute('aria-pressed', liked ? 'false' : 'true');
      store(false, id, !liked);
      counts[id] = Math.max(0, (counts[id] || 0) + (liked ? -1 : 1));
      setCount(id, counts[id]);
      if (!liked) { btn.classList.remove('pop'); void btn.offsetWidth; btn.classList.add('pop'); }
      fetch(endpoint + '?action=' + action + '&id=' + encodeURIComponent(id))
        .then(function (r) { return r.json(); })
        .then(function (d) { if (typeof d.count === 'number') { counts[id] = d.count; setCount(id, d.count); } })
        .catch(function () {});
    });
  });
})();
