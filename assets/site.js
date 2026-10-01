/* 6th WIMPA site: shared header/footer, galleries and lightbox */
(function () {
  var D = window.WIMPA || [], CATS = window.WIMPA_CATS || {};
  var AW = { gold: '1st Place · Gold', silver: '2nd Place · Silver', bronze: '3rd Place · Bronze', hm: 'Honorable Mention' };
  var ED = { 1: '1st WIMPA', 2: '2nd WIMPA', 3: '3rd WIMPA', 4: '4th WIMPA', 5: '5th WIMPA' };
  var page = document.body.getAttribute('data-page');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var W = function (id) { return 'images/w/' + id + '.jpg'; };
  var Tn = function (id) { return 'images/t/' + id + '.jpg'; };

  /* ---------- header / footer ---------- */
  var links = [['winners.html', '5th Winners', 'winners'], ['archive.html', 'Past Winners', 'archive'], ['enter.html', 'Categories & Rules', 'enter'], ['jury.html', 'Jury', 'jury'], ['about.html', 'About', 'about']];
  var hdr = document.createElement('header'); hdr.className = 'hdr';
  hdr.innerHTML = '<div class="wrap"><a class="logo" href="index.html"><b>6th WIMPA</b><span>Washington International Mobile Photography Awards</span></a>' +
    '<button class="burger" aria-label="Menu">&#9776;</button><nav class="nav">' +
    links.map(function (l) { return '<a href="' + l[0] + '"' + (page === l[2] ? ' class="on"' : '') + '>' + l[1] + '</a>'; }).join('') +
    '<a class="btn" href="enter.html#submit">Enter Now</a></nav></div>';
  document.body.insertBefore(hdr, document.body.firstChild);
  $('.burger', hdr).onclick = function () { $('.nav', hdr).classList.toggle('open'); };

  var ftr = document.createElement('footer'); ftr.className = 'ftr';
  ftr.innerHTML = '<div class="wrap"><div class="cols">' +
    '<div><a class="logo" href="index.html"><b>6th WIMPA</b></a><p style="margin-top:14px;max-width:340px">The Washington International Mobile Photography Awards: a platform for mobile photographers everywhere to tell the stories around them, one frame at a time.</p></div>' +
    '<div><h4>Explore</h4>' + links.map(function (l) { return '<a href="' + l[0] + '">' + l[1] + '</a>'; }).join('') + '</div>' +
    '<div><h4>Enter</h4><a href="enter.html#categories">Categories</a><a href="enter.html#awards">Awards</a><a href="enter.html#requirements">Entry Requirements</a><a href="enter.html#submit">How to Submit</a></div>' +
    '<div><h4>Contact</h4><a href="mailto:info.wcaf@gmail.com">info.wcaf@gmail.com</a><a href="http://www.gwmpa.org">www.gwmpa.org</a><p style="margin-top:12px">Organized by the Washington Cultural Arts Foundation (WCAF)</p></div>' +
    '</div><div class="legal"><span>&copy; 2021&ndash;' + new Date().getFullYear() + ' Washington International Mobile Photography Awards. All rights reserved.</span><span>All photographs are copyright of their respective photographers and may not be used without permission.</span></div></div>';
  document.body.appendChild(ftr);

  /* ---------- cards ---------- */
  function card(e, opts) {
    opts = opts || {};
    var im = e.img[0], big = opts.big;
    return '<div class="card" data-id="' + e.id + '"><div class="ph">' +
      '<img loading="lazy" src="' + (big ? W(im[0]) : Tn(im[0])) + '" alt="' + esc(e.title) + '" width="' + im[1] + '" height="' + im[2] + '">' +
      (e.img.length > 1 ? '<span class="n">Series · ' + e.img.length + '</span>' : '') + '</div>' +
      '<div class="meta"><span class="badge ' + e.aw + '"><i></i>' + AW[e.aw] + '</span>' +
      '<div class="t">' + esc(e.title || 'Untitled') + '</div>' +
      (e.name ? '<div class="a">' + esc(e.name) + (e.state ? ', ' + esc(e.state) : '') + '</div>' : '') +
      (opts.cat ? '<div class="c">' + esc(CATS[e.cat]) + (opts.ed ? ' · ' + ED[e.ed] : '') + '</div>' : '') +
      '</div></div>';
  }
  var byId = {}; D.forEach(function (e) { byId[e.id] = e; });

  /* ---------- lightbox ---------- */
  var lb = document.createElement('div'); lb.className = 'lb';
  lb.innerHTML = '<div class="stage"><img alt=""></div><div class="info"></div><button class="x" aria-label="Close">&times;</button><button class="pv" aria-label="Previous">&#8249;</button><button class="nx" aria-label="Next">&#8250;</button>';
  document.body.appendChild(lb);
  var list = [], li = 0, sub = 0;
  function show() {
    var e = list[li], im = e.img[sub];
    $('.stage img', lb).src = W(im[0]);
    $('.info', lb).innerHTML = '<span class="badge ' + e.aw + '"><i></i>' + AW[e.aw] + '</span>' +
      '<div class="t">' + esc(e.title || 'Untitled') + '</div>' +
      (e.name ? '<div class="a">' + esc(e.name) + (e.state ? ', ' + esc(e.state) : '') + '</div>' : '') +
      '<div class="c">' + esc(CATS[e.cat]) + ' · ' + ED[e.ed] + '</div>' +
      (e.img.length > 1 ? '<div class="dots">' + e.img.map(function (m, k) { return '<img data-k="' + k + '" class="' + (k === sub ? 'on' : '') + '" src="' + Tn(m[0]) + '">'; }).join('') + '</div>' : '') +
      (e.desc ? '<p>' + esc(e.desc) + '</p>' : '');
    lb.querySelectorAll('.dots img').forEach(function (d) { d.onclick = function () { sub = +d.getAttribute('data-k'); show(); }; });
  }
  function open(id, scope) {
    list = []; (scope || document).querySelectorAll('.card[data-id]').forEach(function (c) { var e = byId[c.getAttribute('data-id')]; if (e && list.indexOf(e) < 0) list.push(e); });
    li = Math.max(0, list.indexOf(byId[id])); sub = 0; show(); lb.classList.add('on'); document.body.style.overflow = 'hidden';
  }
  function close() { lb.classList.remove('on'); document.body.style.overflow = ''; }
  function step(d) {
    var e = list[li];
    if (e.img.length > 1 && sub + d >= 0 && sub + d < e.img.length) sub += d;
    else { li = (li + d + list.length) % list.length; sub = d < 0 ? list[li].img.length - 1 : 0; }
    show();
  }
  $('.x', lb).onclick = close; $('.pv', lb).onclick = function () { step(-1); }; $('.nx', lb).onclick = function () { step(1); };
  lb.addEventListener('click', function (ev) { if (ev.target === lb || ev.target.classList.contains('stage')) close(); });
  document.addEventListener('keydown', function (ev) { if (!lb.classList.contains('on')) return; if (ev.key === 'Escape') close(); if (ev.key === 'ArrowRight') step(1); if (ev.key === 'ArrowLeft') step(-1); });
  document.addEventListener('click', function (ev) {
    var c = ev.target.closest && ev.target.closest('.card[data-id]');
    if (c) open(c.getAttribute('data-id'), c.closest('[data-scope]') || document);
  });

  var medal = function (e) { return e.aw !== 'hm'; };
  var landscape = function (e) { return e.img[0][1] > e.img[0][2] * 1.25; };

  /* ---------- home ---------- */
  if (page === 'home') {
    var heroPool = D.filter(function (e) { return medal(e) && landscape(e) && e.img.length === 1 && e.ed >= 3; });
    var hero = $('.hero'), slides = [], hi = 0;
    heroPool.sort(function (a, b) { return a.ed === 5 && b.ed !== 5 ? -1 : b.ed === 5 && a.ed !== 5 ? 1 : 0; });
    heroPool.slice(0, 10).forEach(function (e, k) {
      var s = document.createElement('div'); s.className = 'slide' + (k === 0 ? ' on' : ''); s.style.backgroundImage = 'url(' + W(e.img[0][0]) + ')';
      hero.insertBefore(s, hero.firstChild); slides.push([s, e]);
    });
    var credit = $('.hero .credit');
    function setCredit() { var e = slides[hi][1]; credit.innerHTML = '<b>' + esc(e.title) + '</b><br>' + esc(e.name) + ' · ' + AW[e.aw] + ', ' + ED[e.ed]; }
    if (slides.length) { setCredit(); setInterval(function () { slides[hi][0].classList.remove('on'); hi = (hi + 1) % slides.length; slides[hi][0].classList.add('on'); setCredit(); }, 7000); }

    // photograph of the day: rotates daily through 5th-edition medal winners
    var pool = D.filter(function (e) { return e.ed === 5 && medal(e) && e.desc; });
    var day = Math.floor(Date.now() / 864e5), p = pool[day % pool.length];
    if (p) $('#potd').innerHTML = '<div data-scope><div class="card" data-id="' + p.id + '"><img src="' + W(p.img[0][0]) + '" alt="' + esc(p.title) + '"></div></div>' +
      '<div><p class="kicker">Photograph of the Day</p><h2>' + esc(p.title) + '</h2><p class="a" style="font-size:18px;margin:0 0 6px">' + esc(p.name) + (p.state ? ', ' + esc(p.state) : '') + '</p>' +
      '<span class="badge ' + p.aw + '"><i></i>' + AW[p.aw] + ' · ' + esc(CATS[p.cat]) + '</span><p style="color:var(--ink-2);margin-top:20px">' + esc(p.desc) + '</p>' +
      '<a class="more" href="winners.html">See all 5th WIMPA winners</a></div>';

    // 5th edition first-place winners
    var golds = D.filter(function (e) { return e.ed === 5 && e.aw === 'gold'; });
    $('#golds').innerHTML = golds.map(function (e) { return card(e, { cat: 1 }); }).join('');
    // archive highlights: earlier first places
    var past = D.filter(function (e) { return e.ed < 5 && e.aw === 'gold'; }).slice(0, 8);
    $('#past').innerHTML = past.map(function (e) { return card(e, { cat: 1, ed: 1 }); }).join('');
    // category tiles
    document.querySelectorAll('.cat[data-cat]').forEach(function (t) {
      var e = D.filter(function (x) { return x.ed === 5 && x.cat === t.getAttribute('data-cat') && medal(x); })[+t.getAttribute('data-pick') || 0];
      if (e) $('img', t).src = Tn(e.img[0][0]);
    });
    var ctaImg = D.filter(function (e) { return e.ed === 5 && e.title === 'Dreamy Night in a Fishing Village'; })[0] || D.filter(function (e) { return e.ed === 5 && medal(e) && landscape(e); })[0];
    if (ctaImg) $('.cta').style.backgroundImage = 'url(' + W(ctaImg.img[0][0]) + ')';
  }

  /* ---------- winners (5th) and archive (1st-4th) ---------- */
  function renderEdition(root, ed) {
    var cats = Object.keys(CATS).filter(function (c) { return D.some(function (e) { return e.ed === ed && e.cat === c; }); });
    root.innerHTML = cats.map(function (c) {
      var es = D.filter(function (e) { return e.ed === ed && e.cat === c; });
      var g = es.filter(function (e) { return e.aw === 'gold'; }), rest = es.filter(function (e) { return e.aw === 'silver' || e.aw === 'bronze'; }), hm = es.filter(function (e) { return e.aw === 'hm'; });
      var h = '<div class="catblock" id="' + c + '" data-scope><h3>' + esc(CATS[c]) + '</h3>';
      if (g.length) h += '<div class="podium"><div class="big">' + card(g[0], { big: 1 }) + '</div><div class="side">' + rest.slice(0, 2).map(function (e) { return card(e); }).join('') + '</div></div>';
      var r2 = g.length ? rest.slice(2) : rest;
      if (r2.length) h += '<div class="grid three">' + r2.map(function (e) { return card(e); }).join('') + '</div>';
      if (hm.length) h += '<p class="subhead">Honorable Mentions · ' + hm.length + '</p><div class="masonry">' + hm.map(function (e) { return card(e); }).join('') + '</div>';
      return h + '</div>';
    }).join('');
    return cats;
  }
  function tabs(el, items, onPick) {
    el.innerHTML = items.map(function (it, k) { return '<button data-k="' + k + '"' + (k === 0 ? ' class="on"' : '') + '>' + esc(it[1]) + '</button>'; }).join('');
    el.querySelectorAll('button').forEach(function (b) {
      b.onclick = function () { el.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); onPick(items[+b.getAttribute('data-k')][0]); };
    });
  }
  if (page === 'winners') {
    var cats = renderEdition($('#gallery'), 5);
    tabs($('#tabs'), [['all', 'All Categories']].concat(cats.map(function (c) { return [c, CATS[c]]; })), function (c) {
      document.querySelectorAll('.catblock').forEach(function (b) { b.style.display = c === 'all' || b.id === c ? '' : 'none'; });
    });
  }
  if (page === 'archive') {
    var eds = [4, 3, 2, 1], blurb = {
      1: 'The inaugural awards, themed "Impressions of Washington", drew nearly 500 entries from the Greater Washington area.',
      2: 'Under the theme "Care", the 2nd awards opened to photographers across the United States and Canada.',
      3: 'The 3rd awards added the themed category "The Journey" alongside three open categories.',
      4: 'Nearly 2,000 entries from eight countries competed under the theme "Life".'
    };
    var pick = function (ed) { $('#edblurb').textContent = blurb[ed]; renderEdition($('#gallery'), ed); };
    tabs($('#tabs'), eds.map(function (e) { return [e, ED[e]]; }), pick); pick(4);
  }
})();
