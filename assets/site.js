/* 6th WIMPA site: shared header/footer, galleries and lightbox (English and Chinese) */
(function () {
  var D = window.WIMPA || [];
  var ZH = (document.documentElement.lang || '').indexOf('zh') === 0;
  var BASE = ZH ? '../' : '';   // Chinese pages live in /zh/ and share images with the English site
  var page = document.body.getAttribute('data-page');
  var file = (location.pathname.split('/').pop() || 'index.html');

  var L = ZH ? {
    CATS: { 'everyday-single': '日常生活 · 单图', 'everyday-series': '日常生活 · 组图', people: '人物纪实', nature: '自然风光', art: '艺术创意', open: '开放类',
      'theme-journey': '命题《旅途》', 'theme-life-single': '命题《生命》· 单图', 'theme-life-series': '命题《生命》· 组图' },
    AW: { gold: '一等奖 · 金奖', silver: '二等奖 · 银奖', bronze: '三等奖 · 铜奖', hm: '优秀奖' },
    ED: { 1: '第一届', 2: '第二届', 3: '第三届', 4: '第四届', 5: '第五届' },
    links: [['winners.html', '第五届获奖作品', 'winners'], ['archive.html', '往届获奖作品', 'archive'], ['enter.html', '参赛类别与规则', 'enter'], ['jury.html', '评委', 'jury'], ['about.html', '关于大赛', 'about']],
    logo: '第六届 WIMPA', logoSub: '华盛顿国际手机摄影大赛', enter: '立即参赛', toggle: 'English', toggleTitle: 'Switch to English',
    about: '华盛顿国际手机摄影大赛：为世界各地的手机摄影爱好者搭建平台，用一帧帧影像讲述身边的故事。',
    explore: '浏览', enterH: '参赛', enterLinks: [['categories', '参赛类别'], ['awards', '奖项设置'], ['requirements', '作品要求'], ['submit', '投稿方式']],
    contact: '联系我们', org: '主办单位：华盛顿文化艺术基金会（WCAF）',
    rights: '华盛顿国际手机摄影大赛 版权所有。', photoRights: '所有摄影作品版权归原作者所有，未经许可不得使用。',
    series: '组图', untitled: '无题', potd: '每日一图', seeAll: '查看第五届全部获奖作品', hms: '优秀奖', all: '全部类别',
    sep: '，', state: { Virginia: '弗吉尼亚州', California: '加利福尼亚州', Maryland: '马里兰州', 'New Jersey': '新泽西州', Massachusetts: '马萨诸塞州', Texas: '得克萨斯州',
      Pennsylvania: '宾夕法尼亚州', Alabama: '亚拉巴马州', 'New York': '纽约州', Montana: '蒙大拿州', 'Rhode Island': '罗得岛州', Washington: '华盛顿州', 'North Carolina': '北卡罗来纳州',
      Illinois: '伊利诺伊州', Connecticut: '康涅狄格州', Georgia: '佐治亚州', Nevada: '内华达州', Colorado: '科罗拉多州', Michigan: '密歇根州', Indiana: '印第安纳州' },
    blurb: { 1: '首届大赛以“华府印象”为主题，收到来自大华府地区的近 500 幅作品。', 2: '第二届以“关爱”为主题，征稿范围扩展到全美和加拿大。',
      3: '第三届在三个开放类别之外，新增命题类别《旅途》。', 4: '第四届以“生命”为主题，近两千幅来自八个国家的作品同台竞技。' }
  } : {
    CATS: window.WIMPA_CATS || {},
    AW: { gold: '1st Place · Gold', silver: '2nd Place · Silver', bronze: '3rd Place · Bronze', hm: 'Honorable Mention' },
    ED: { 1: '1st WIMPA', 2: '2nd WIMPA', 3: '3rd WIMPA', 4: '4th WIMPA', 5: '5th WIMPA' },
    links: [['winners.html', '5th Winners', 'winners'], ['archive.html', 'Past Winners', 'archive'], ['enter.html', 'Categories & Rules', 'enter'], ['jury.html', 'Jury', 'jury'], ['about.html', 'About', 'about']],
    logo: '6th WIMPA', logoSub: 'Washington International Mobile Photography Awards', enter: 'Enter Now', toggle: '中文', toggleTitle: '切换到中文',
    about: 'The Washington International Mobile Photography Awards: a platform for mobile photographers everywhere to tell the stories around them, one frame at a time.',
    explore: 'Explore', enterH: 'Enter', enterLinks: [['categories', 'Categories'], ['awards', 'Awards'], ['requirements', 'Entry Requirements'], ['submit', 'How to Submit']],
    contact: 'Contact', org: 'Organized by the Washington Cultural Arts Foundation (WCAF)',
    rights: 'Washington International Mobile Photography Awards. All rights reserved.', photoRights: 'All photographs are copyright of their respective photographers and may not be used without permission.',
    series: 'Series', untitled: 'Untitled', potd: 'Photograph of the Day', seeAll: 'See all 5th WIMPA winners', hms: 'Honorable Mentions', all: 'All Categories',
    sep: ', ', state: {},
    blurb: { 1: 'The inaugural awards, themed "Impressions of Washington", drew nearly 500 entries from the Greater Washington area.',
      2: 'Under the theme "Care", the 2nd awards opened to photographers across the United States and Canada.',
      3: 'The 3rd awards added the themed category "The Journey" alongside three open categories.',
      4: 'Nearly 2,000 entries from eight countries competed under the theme "Life".' }
  };
  var CATS = L.CATS, AW = L.AW, ED = L.ED;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var W = function (id) { return BASE + 'images/w/' + id + '.jpg'; };
  var Tn = function (id) { return BASE + 'images/t/' + id + '.jpg'; };
  var T = function (e) { return (ZH ? e.tz : e.title) || L.untitled; };
  var N = function (e) { return ZH ? e.nz : e.name; };
  var Ds = function (e) { return ZH ? e.dz : e.desc; };
  var who = function (e) { var n = N(e); return n ? esc(n) + (e.state ? L.sep + esc(L.state[e.state] || e.state) : '') : ''; };

  /* ---------- header / footer ---------- */
  var other = (ZH ? '../' : 'zh/') + file + location.hash;
  var hdr = document.createElement('header'); hdr.className = 'hdr';
  hdr.innerHTML = '<div class="wrap"><a class="logo" href="index.html"><b>' + L.logo + '</b><span>' + L.logoSub + '</span></a>' +
    '<div class="hright"><a class="lang" href="' + other + '" title="' + L.toggleTitle + '" lang="' + (ZH ? 'en' : 'zh-CN') + '">' + L.toggle + '</a>' +
    '<button class="burger" aria-label="Menu">&#9776;</button></div><nav class="nav">' +
    L.links.map(function (l) { return '<a href="' + l[0] + '"' + (page === l[2] ? ' class="on"' : '') + '>' + l[1] + '</a>'; }).join('') +
    '<a class="btn" href="enter.html#submit">' + L.enter + '</a></nav></div>';
  document.body.insertBefore(hdr, document.body.firstChild);
  $('.burger', hdr).onclick = function () { $('.nav', hdr).classList.toggle('open'); };

  var ftr = document.createElement('footer'); ftr.className = 'ftr';
  ftr.innerHTML = '<div class="wrap"><div class="cols">' +
    '<div><a class="logo" href="index.html"><b>' + L.logo + '</b></a><p style="margin-top:14px;max-width:340px">' + L.about + '</p></div>' +
    '<div><h4>' + L.explore + '</h4>' + L.links.map(function (l) { return '<a href="' + l[0] + '">' + l[1] + '</a>'; }).join('') + '</div>' +
    '<div><h4>' + L.enterH + '</h4>' + L.enterLinks.map(function (l) { return '<a href="enter.html#' + l[0] + '">' + l[1] + '</a>'; }).join('') + '</div>' +
    '<div><h4>' + L.contact + '</h4><a href="mailto:info.wcaf@gmail.com">info.wcaf@gmail.com</a><a href="https://www.gwmpa.org">www.gwmpa.org</a><a href="' + other + '">' + L.toggle + '</a><p style="margin-top:12px">' + L.org + '</p></div>' +
    '</div><div class="legal"><span>&copy; 2021&ndash;' + new Date().getFullYear() + ' ' + L.rights + '</span><span>' + L.photoRights + '</span></div></div>';
  document.body.appendChild(ftr);

  /* ---------- cards ---------- */
  function card(e, opts) {
    opts = opts || {};
    var im = e.img[0], big = opts.big, w = who(e);
    return '<div class="card" data-id="' + e.id + '"><div class="ph">' +
      '<img loading="lazy" src="' + (big ? W(im[0]) : Tn(im[0])) + '" alt="' + esc(T(e)) + '" width="' + im[1] + '" height="' + im[2] + '">' +
      (e.img.length > 1 ? '<span class="n">' + L.series + ' · ' + e.img.length + '</span>' : '') + '</div>' +
      '<div class="meta"><span class="badge ' + e.aw + '"><i></i>' + AW[e.aw] + '</span>' +
      '<div class="t">' + esc(T(e)) + '</div>' +
      (w ? '<div class="a">' + w + '</div>' : '') +
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
    var e = list[li], im = e.img[sub], w = who(e), d = Ds(e);
    $('.stage img', lb).src = W(im[0]);
    $('.info', lb).innerHTML = '<span class="badge ' + e.aw + '"><i></i>' + AW[e.aw] + '</span>' +
      '<div class="t">' + esc(T(e)) + '</div>' +
      (w ? '<div class="a">' + w + '</div>' : '') +
      '<div class="c">' + esc(CATS[e.cat]) + ' · ' + ED[e.ed] + '</div>' +
      (e.img.length > 1 ? '<div class="dots">' + e.img.map(function (m, k) { return '<img data-k="' + k + '" class="' + (k === sub ? 'on' : '') + '" src="' + Tn(m[0]) + '">'; }).join('') + '</div>' : '') +
      (d ? '<p>' + esc(d) + '</p>' : '');
    lb.querySelectorAll('.dots img').forEach(function (x) { x.onclick = function () { sub = +x.getAttribute('data-k'); show(); }; });
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
    function setCredit() { var e = slides[hi][1]; credit.innerHTML = '<b>' + esc(T(e)) + '</b><br>' + esc(N(e)) + ' · ' + AW[e.aw] + (ZH ? '，' : ', ') + ED[e.ed]; }
    if (slides.length) { setCredit(); setInterval(function () { slides[hi][0].classList.remove('on'); hi = (hi + 1) % slides.length; slides[hi][0].classList.add('on'); setCredit(); }, 7000); }

    // photograph of the day: rotates daily through 5th-edition medal winners
    var pool = D.filter(function (e) { return e.ed === 5 && medal(e) && Ds(e); });
    var day = Math.floor(Date.now() / 864e5), p = pool[day % pool.length];
    if (p) $('#potd').innerHTML = '<div data-scope><div class="card" data-id="' + p.id + '"><img src="' + W(p.img[0][0]) + '" alt="' + esc(T(p)) + '"></div></div>' +
      '<div><p class="kicker">' + L.potd + '</p><h2>' + esc(T(p)) + '</h2><p class="a" style="font-size:18px;margin:0 0 6px">' + who(p) + '</p>' +
      '<span class="badge ' + p.aw + '"><i></i>' + AW[p.aw] + ' · ' + esc(CATS[p.cat]) + '</span><p style="color:var(--ink-2);margin-top:20px">' + esc(Ds(p)) + '</p>' +
      '<a class="more" href="winners.html">' + L.seeAll + '</a></div>';

    var golds = D.filter(function (e) { return e.ed === 5 && e.aw === 'gold'; });
    $('#golds').innerHTML = golds.map(function (e) { return card(e, { cat: 1 }); }).join('');
    var past = D.filter(function (e) { return e.ed < 5 && e.aw === 'gold'; }).slice(0, 8);
    $('#past').innerHTML = past.map(function (e) { return card(e, { cat: 1, ed: 1 }); }).join('');
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
      if (hm.length) h += '<p class="subhead">' + L.hms + ' · ' + hm.length + '</p><div class="masonry">' + hm.map(function (e) { return card(e); }).join('') + '</div>';
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
    tabs($('#tabs'), [['all', L.all]].concat(cats.map(function (c) { return [c, CATS[c]]; })), function (c) {
      document.querySelectorAll('.catblock').forEach(function (b) { b.style.display = c === 'all' || b.id === c ? '' : 'none'; });
    });
  }
  if (page === 'archive') {
    var pick = function (ed) { $('#edblurb').textContent = L.blurb[ed]; renderEdition($('#gallery'), ed); };
    tabs($('#tabs'), [4, 3, 2, 1].map(function (e) { return [e, ED[e]]; }), pick); pick(4);
  }
})();
