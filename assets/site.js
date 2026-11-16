(function () {
  var btn = document.querySelector('.menu-btn'), side = document.getElementById('nav');
  if (btn && side) btn.addEventListener('click', function () {
    var o = side.classList.toggle('open');
    btn.setAttribute('aria-expanded', o ? 'true' : 'false');
  });

  var q = document.getElementById('q'), res = document.getElementById('res'), idx = window.IDX || [];
  if (!q || !res) return;
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var cache = null;
  function run() {
    var term = norm(q.value.trim());
    if (term.length < 2) { res.hidden = true; res.innerHTML = ''; return; }
    if (!cache) cache = idx.map(function (s) { return { s: s, h: norm(s.h), t: norm(s.t) }; });
    var words = term.split(/\s+/), hits = [];
    cache.forEach(function (c) {
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], inH = c.h.indexOf(w) > -1, inT = c.t.indexOf(w) > -1;
        if (!inH && !inT) return;
        score += (inH ? 5 : 0) + (inT ? 1 : 0);
      }
      hits.push({ c: c, score: score });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    res.innerHTML = hits.slice(0, 12).map(function (h) {
      var s = h.c.s, pos = h.c.t.indexOf(words[0]), start = Math.max(0, pos - 50);
      var snip = (start > 0 ? '…' : '') + s.t.slice(start, start + 140) + '…';
      return '<li><a href="' + s.u + '"><b>' + esc(s.h) + '</b><small>' + esc(s.p) + ' — ' + esc(snip) + '</small></a></li>';
    }).join('') || '<li><a><small>Aucun résultat dans le dossier.</small></a></li>';
    res.hidden = false;
  }
  q.addEventListener('input', run);
  q.addEventListener('keydown', function (e) { if (e.key === 'Escape') { q.value = ''; run(); } });
})();
