/* =========================================================================
   ALMA IBÉRICA ONLINE SHOP – alma.js (Vanilla JS, kein jQuery)
   Module: Warenkorb, Toast, Sticky-Header, Mega-Menü, Suche, Filter, Quick-View,
   Mengen-Stepper, Wunschliste, Galerie, Checkout, Cookie-Consent.
   KONFIG: Versandwerte kommen aus <body data-free-ship / data-ship-cost / data-cool-cost>.
   MIGRATION: Das Objekt "cart" ist die Schnittstelle zum echten Shopsystem
   (Shopware Store-API / Shopify Cart-API / WooCommerce Store-API).
   ========================================================================= */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var body = document.body;
  var CFG = { free: parseFloat(body.dataset.freeShip) || 69, ship: parseFloat(body.dataset.shipCost) || 5.9, cool: parseFloat(body.dataset.coolCost) || 4.9 };
  var PRODUCTS = window.AI_PRODUCTS || [];
  var CATS = window.AI_CATS || {};
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Hilfen ---------- */
  function eur(n) { return n.toLocaleString('de-DE', { style: 'currency', currency: 'EUR' }); }
  function store(key, val) {            // localStorage kann fehlen/werfen -> try/catch
    try { if (val === undefined) { return JSON.parse(localStorage.getItem(key)); } localStorage.setItem(key, JSON.stringify(val)); } catch (e) { /* ignorieren */ }
    return null;
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function icon(cls) { var i = el('i', 'bi ' + cls); i.setAttribute('aria-hidden', 'true'); return i; }
  function byId(id) { return PRODUCTS.filter(function (p) { return p.id === id; })[0]; }

  /* ---------- Toast (aria-live Region #toastRegion) ---------- */
  function toast(msg, ic) {
    var reg = $('#toastRegion'); if (!reg) { return; }
    var t = el('div', 'toast align-items-center border-0 bg-white shadow'); t.setAttribute('role', 'status'); t.setAttribute('aria-atomic', 'true');
    var wrap = el('div', 'd-flex'); var b = el('div', 'toast-body text-dark');
    var i = icon((ic || 'bi-check-circle-fill') + ' text-success me-2'); b.appendChild(i); b.appendChild(document.createTextNode(msg));
    var close = el('button', 'btn-close me-2 m-auto'); close.type = 'button'; close.setAttribute('data-bs-dismiss', 'toast'); close.setAttribute('aria-label', 'Meldung schließen');
    wrap.appendChild(b); wrap.appendChild(close); t.appendChild(wrap); reg.appendChild(t);
    if (window.bootstrap) { var bt = new bootstrap.Toast(t, { delay: 4000 }); t.addEventListener('hidden.bs.toast', function () { t.remove(); }); bt.show(); }
    else { setTimeout(function () { t.remove(); }, 4000); }
  }

  /* ---------- Warenkorb ---------- */
  var cart = {
    items: store('ai_cart') || [],
    mode: store('ai_mode') || 'versand',
    save: function () { store('ai_cart', this.items); store('ai_mode', this.mode); },
    add: function (item, qty) {
      var f = this.items.filter(function (x) { return x.id === item.id; })[0];
      if (f) { f.qty = Math.min(99, f.qty + qty); } else { item.qty = qty; this.items.push(item); }
      this.save(); render();
    },
    setQty: function (id, q) { this.items.forEach(function (x) { if (x.id === id) { x.qty = Math.max(1, Math.min(99, q)); } }); this.save(); render(); },
    remove: function (id) { this.items = this.items.filter(function (x) { return x.id !== id; }); this.save(); render(); },
    clear: function () { this.items = []; this.save(); render(); },
    count: function () { return this.items.reduce(function (s, x) { return s + x.qty; }, 0); },
    subtotal: function () { return this.items.reduce(function (s, x) { return s + x.qty * x.price; }, 0); },
    hasCool: function () { return this.items.some(function (x) { return x.cool; }); },
    shipping: function () {
      if (this.mode === 'abholung' || !this.items.length) { return 0; }
      return (this.subtotal() >= CFG.free ? 0 : CFG.ship) + (this.hasCool() ? CFG.cool : 0);
    }
  };

  function lineEl(it, compact) {
    var row = el('div', 'cart-line');
    var img = document.createElement('img'); img.src = 'assets/img/' + it.img + '-s.webp'; img.alt = ''; img.width = 54; img.height = 72; img.loading = 'lazy';
    var mid = el('div'); mid.appendChild(el('div', 'fw-semibold text-dark', it.name));
    if (it.base) { mid.appendChild(el('div', 'small', 'Grundpreis: ' + it.base)); }
    if (it.cool) { var c = el('div', 'small'); c.appendChild(icon('bi-snow2')); c.appendChild(document.createTextNode(' kühlpflichtig')); mid.appendChild(c); }
    if (compact) { mid.appendChild(el('div', 'small', it.qty + ' × ' + eur(it.price))); }
    else {
      var q = el('div', 'd-flex flex-wrap align-items-center gap-2 mt-2'); var s = el('div', 'qty');
      var m = el('button'); m.type = 'button'; m.setAttribute('aria-label', 'Menge verringern: ' + it.name); m.appendChild(icon('bi-dash'));
      var inp = el('input'); inp.type = 'text'; inp.inputMode = 'numeric'; inp.value = it.qty; inp.setAttribute('aria-label', 'Menge: ' + it.name);
      var p = el('button'); p.type = 'button'; p.setAttribute('aria-label', 'Menge erhöhen: ' + it.name); p.appendChild(icon('bi-plus'));
      m.addEventListener('click', function () { if (it.qty > 1) { cart.setQty(it.id, it.qty - 1); } });
      p.addEventListener('click', function () { cart.setQty(it.id, it.qty + 1); });
      inp.addEventListener('change', function () { cart.setQty(it.id, parseInt(inp.value, 10) || 1); });
      s.appendChild(m); s.appendChild(inp); s.appendChild(p);
      var rm = el('button', 'btn btn-link p-0'); rm.type = 'button'; rm.setAttribute('aria-label', it.name + ' entfernen');
      rm.appendChild(icon('bi-trash')); rm.appendChild(document.createTextNode(' Entfernen'));
      rm.addEventListener('click', function () { cart.remove(it.id); toast(it.name + ' entfernt', 'bi-info-circle-fill'); });
      q.appendChild(s); q.appendChild(rm); mid.appendChild(q);
    }
    row.appendChild(img); row.appendChild(mid); row.appendChild(el('div', 'fw-bold price text-end', eur(it.price * it.qty))); return row;
  }

  function render() {
    var n = cart.count(), sub = cart.subtotal(), ship = cart.shipping();
    $$('[data-cart-badge]').forEach(function (b) { b.textContent = n; b.hidden = n === 0; });
    $$('[data-cart-btn]').forEach(function (b) { b.setAttribute('aria-label', 'Warenkorb öffnen, ' + n + ' Artikel'); });
    $$('[data-cart-lines]').forEach(function (box) {
      box.textContent = '';
      if (!cart.items.length) {
        var e = el('div', 'text-center py-4'); e.appendChild(el('p', 'mb-3', 'Ihr Warenkorb ist noch leer.'));
        var a = el('a', 'btn btn-primary', 'Zum Shop'); a.href = 'shop.html'; e.appendChild(a); box.appendChild(e);
      } else { cart.items.forEach(function (it) { box.appendChild(lineEl(it, box.hasAttribute('data-compact'))); }); }
    });
    $$('[data-cart-subtotal]').forEach(function (x) { x.textContent = eur(sub); });
    $$('[data-cart-shipping]').forEach(function (x) { x.textContent = !cart.items.length ? '–' : (ship === 0 ? 'kostenlos' : eur(ship)); });
    $$('[data-cart-total]').forEach(function (x) { x.textContent = eur(sub + ship); });
    $$('[data-cart-footer]').forEach(function (x) { x.hidden = !cart.items.length; });
    $$('[data-checkout-cta]').forEach(function (x) { x.classList.toggle('disabled', !cart.items.length); x.setAttribute('aria-disabled', String(!cart.items.length)); });
    var rest = Math.max(0, CFG.free - sub);
    $$('[data-free-ship-text]').forEach(function (x) {
      x.textContent = cart.mode === 'abholung' ? 'Bei Abholung fallen keine Versandkosten an.' : (rest > 0 ? 'Noch ' + eur(rest) + ' bis zum kostenlosen Versand' : 'Sie erhalten kostenlosen Versand!');
    });
    $$('[data-free-ship-bar]').forEach(function (x) { x.value = Math.min(100, Math.round(sub / CFG.free * 100)); });
    $$('[data-delivery]').forEach(function (r) { r.checked = (r.value === cart.mode); });
    $$('[data-address]').forEach(function (a) { a.hidden = cart.mode === 'abholung'; var i = $('input', a); if (i) { i.required = cart.mode !== 'abholung'; } });
  }
  function bump() {
    if (reduceMotion) { return; }
    $$('[data-cart-badge]').forEach(function (b) { b.classList.remove('is-bump'); void b.offsetWidth; b.classList.add('is-bump'); });
  }
  function itemFrom(p) { return { id: p.id, name: p.name, price: p.price, img: p.img, cool: !!p.cool, base: p.base }; }
  function addToCart(btn, item, qty) {
    btn.classList.add('is-loading'); btn.setAttribute('aria-busy', 'true');
    setTimeout(function () {
      btn.classList.remove('is-loading'); btn.removeAttribute('aria-busy');
      cart.add(item, qty); bump(); toast(qty + ' × ' + item.name + ' im Warenkorb');
    }, reduceMotion ? 0 : 350);
  }

  /* ---------- Delegierte Klicks ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var add = t.closest('[data-add]');
    if (add) {
      var p = byId(add.dataset.add); if (!p) { return; }
      var scope = add.closest('[data-pdp]') || document.body;
      var qin = add.closest('[data-pdp]') ? $('[data-qty-input]', scope) : null;
      addToCart(add, itemFrom(p), qin ? Math.max(1, parseInt(qin.value, 10) || 1) : 1); return;
    }
    var gift = t.closest('[data-add-gift]');
    if (gift) { addToCart(gift, { id: 'x-' + gift.dataset.addGift, name: gift.dataset.addGift, price: parseFloat(gift.dataset.price), img: 'geschenkkorb', cool: false }, 1); return; }
    var wish = t.closest('[data-wish]'); if (wish) { toggleWish(wish.dataset.wish); return; }
    var quick = t.closest('[data-quick]'); if (quick) { openQuick(quick.dataset.quick); return; }
    var minus = t.closest('[data-qty-minus]'), plus = t.closest('[data-qty-plus]');
    if (minus || plus) {
      var inp = $('[data-qty-input]', (minus || plus).parentNode); var v = parseInt(inp.value, 10) || 1;
      inp.value = Math.max(1, Math.min(99, v + (plus ? 1 : -1)));
    }
  });
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches('[data-qty-input]')) { t.value = Math.max(1, Math.min(99, parseInt(t.value, 10) || 1)); }
    if (t.matches('[data-delivery]')) { cart.mode = t.value; cart.save(); render(); }
  });

  /* ---------- Wunschliste ---------- */
  var wishes = store('ai_wish') || [];
  function syncWish() {
    $$('[data-wish]').forEach(function (b) {
      var on = wishes.indexOf(b.dataset.wish) > -1; b.setAttribute('aria-pressed', String(on));
      var p = byId(b.dataset.wish); var nm = p ? p.name + ' ' : '';
      b.setAttribute('aria-label', nm + (on ? (nm ? 'von der Wunschliste entfernen' : 'Von der Wunschliste entfernen') : (nm ? 'zur Wunschliste hinzufügen' : 'Zur Wunschliste hinzufügen')));
      var ic = $('.bi', b); if (ic) { ic.classList.toggle('bi-heart-fill', on); ic.classList.toggle('bi-heart', !on); }
    });
    $$('[data-wish-badge]').forEach(function (x) { x.textContent = wishes.length; x.hidden = !wishes.length; });
    $$('[data-wish-link]').forEach(function (x) { x.setAttribute('aria-label', 'Wunschliste, ' + wishes.length + ' Artikel'); });
  }
  function toggleWish(id) {
    var i = wishes.indexOf(id); var p = byId(id); var nm = p ? p.name : 'Artikel';
    if (i > -1) { wishes.splice(i, 1); toast(nm + ' von der Wunschliste entfernt', 'bi-info-circle-fill'); } else { wishes.push(id); toast(nm + ' zur Wunschliste hinzugefügt', 'bi-heart-fill'); }
    store('ai_wish', wishes); syncWish();
  }
  function cardsFromTemplate(ids) {
    var tpl = $('#card-tpl'); if (!tpl) { return []; }
    return $$('.p-card', tpl.content).filter(function (c) { return ids.indexOf(c.dataset.id) > -1; }).map(function (c) { var col = el('div', 'col'); col.appendChild(document.importNode(c, true)); return col; });
  }
  var wl = $('[data-wishlist]');
  if (wl) { var wcards = cardsFromTemplate(wishes); if (wcards.length) { $('[data-wishlist-empty]').remove(); wcards.forEach(function (c) { wl.appendChild(c); }); } }

  /* ---------- Quick-View ---------- */
  var qvProduct = null;
  function openQuick(id) {
    var p = byId(id); var m = $('#quickView'); if (!p || !m || !window.bootstrap) { return; }
    qvProduct = p;
    $('[data-qv-title]', m).textContent = p.name; $('[data-qv-brand]', m).textContent = p.brand; $('[data-qv-price]', m).textContent = eur(p.price);
    $('[data-qv-base]', m).textContent = 'Grundpreis: ' + p.base + ' · inkl. MwSt.'; $('[data-qv-desc]', m).textContent = p.desc;
    var im = $('[data-qv-img]', m); im.src = 'assets/img/' + p.img + '.webp'; im.alt = p.name;
    $('[data-qty-input]', m).value = 1; $('[data-qv-link]', m).href = 'product.html?id=' + p.id;
    $('[data-qv-add]', m).disabled = p.stock === 0;
    bootstrap.Modal.getOrCreateInstance(m).show();
  }
  var qvAdd = $('[data-qv-add]');
  if (qvAdd) { qvAdd.addEventListener('click', function () {
    var m = $('#quickView'); var q = parseInt($('[data-qty-input]', m).value, 10) || 1;
    cart.add(itemFrom(qvProduct), q); bump(); toast(q + ' × ' + qvProduct.name + ' im Warenkorb'); bootstrap.Modal.getInstance(m).hide();
  }); }

  /* ---------- Sticky-Header ---------- */
  var hdr = $('#site-header');
  if (hdr) { var onScroll = function () { hdr.classList.toggle('is-stuck', window.scrollY > 8); }; window.addEventListener('scroll', onScroll, { passive: true }); onScroll(); }

  /* ---------- Mega-Menü (Esc schließt, Pfeiltasten wechseln) ---------- */
  var megaBtns = $$('[data-mega]');
  function closeMega(focusBtn) {
    megaBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); var p = document.getElementById(b.dataset.mega); if (p) { p.hidden = true; } });
    if (focusBtn) { focusBtn.focus(); }
  }
  megaBtns.forEach(function (b, idx) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true'; closeMega();
      if (!open) { b.setAttribute('aria-expanded', 'true'); document.getElementById(b.dataset.mega).hidden = false; }
    });
    b.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); megaBtns[(idx + (e.key === 'ArrowRight' ? 1 : -1) + megaBtns.length) % megaBtns.length].focus(); }
      if (e.key === 'ArrowDown' && b.getAttribute('aria-expanded') === 'true') { e.preventDefault(); var l = $('a', document.getElementById(b.dataset.mega)); if (l) { l.focus(); } }
    });
  });
  $$('.mega-panel').forEach(function (p) {
    p.addEventListener('keydown', function (e) {
      var links = $$('a', p), i = links.indexOf(document.activeElement);
      if (e.key === 'ArrowDown' && i < links.length - 1) { e.preventDefault(); links[i + 1].focus(); }
      if (e.key === 'ArrowUp' && i > 0) { e.preventDefault(); links[i - 1].focus(); }
    });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { var o = megaBtns.filter(function (b) { return b.getAttribute('aria-expanded') === 'true'; })[0]; if (o) { closeMega(o); } } });
  document.addEventListener('click', function (e) { if (!e.target.closest('.mega-wrap')) { closeMega(); } });

  /* ---------- Suche mit Autocomplete (ARIA-Combobox) ---------- */
  $$('[data-search]').forEach(function (form, fi) {
    var input = $('input', form), box = $('.suggest', form), active = -1;
    function close() { box.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; }
    function opts() { return $$('a', box); }
    function setActive(i) { var o = opts(); o.forEach(function (a) { a.setAttribute('aria-selected', 'false'); }); if (o[i]) { o[i].setAttribute('aria-selected', 'true'); input.setAttribute('aria-activedescendant', o[i].id); } active = i; }
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase(); box.textContent = '';
      if (q.length < 2) { close(); return; }
      var prods = PRODUCTS.filter(function (p) { return (p.name + ' ' + p.brand).toLowerCase().indexOf(q) > -1; }).slice(0, 4);
      var cats = Object.keys(CATS).filter(function (k) { return CATS[k].toLowerCase().indexOf(q) > -1; }).slice(0, 3);
      var n = 0;
      function opt(href, label, img) {
        var a = el('a'); a.href = href; a.id = 'sg' + fi + '-' + (n++); a.setAttribute('role', 'option'); a.setAttribute('aria-selected', 'false');
        if (img) { var im = document.createElement('img'); im.src = 'assets/img/' + img + '-s.webp'; im.alt = ''; im.width = 36; im.height = 48; a.appendChild(im); }
        a.appendChild(el('span', '', label)); box.appendChild(a);
      }
      if (prods.length) { box.appendChild(el('h2', '', 'Produkte')); prods.forEach(function (p) { opt('product.html?id=' + p.id, p.name, p.img); }); }
      if (cats.length) { box.appendChild(el('h2', '', 'Kategorien')); cats.forEach(function (k) { opt('shop.html?kat=' + k, CATS[k]); }); }
      if (!prods.length && !cats.length) { box.appendChild(el('h2', '', 'Keine Vorschläge')); opt('search.html?q=' + encodeURIComponent(q), 'Alle Ergebnisse für „' + input.value.trim() + '“ anzeigen'); }
      box.hidden = false; input.setAttribute('aria-expanded', 'true'); active = -1;
    });
    input.addEventListener('keydown', function (e) {
      var o = opts();
      if (e.key === 'ArrowDown' && o.length) { e.preventDefault(); setActive((active + 1) % o.length); }
      else if (e.key === 'ArrowUp' && o.length) { e.preventDefault(); setActive((active - 1 + o.length) % o.length); }
      else if (e.key === 'Enter' && active > -1) { e.preventDefault(); location.href = o[active].href; }
      else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', function (e) { if (!form.contains(e.target)) { close(); } });
  });

  /* ---------- Suchergebnisse ---------- */
  var sr = $('[data-search-results]');
  if (sr) {
    var sq = (new URLSearchParams(location.search).get('q') || '').trim(); var ql = sq.toLowerCase();
    $('[data-search-term]').textContent = sq ? '„' + sq + '“' : '';
    var hits = sq ? PRODUCTS.filter(function (p) { return (p.name + ' ' + p.brand + ' ' + (CATS[p.cat] || '')).toLowerCase().indexOf(ql) > -1; }).map(function (p) { return p.id; }) : [];
    cardsFromTemplate(hits).forEach(function (c) { sr.appendChild(c); });
    $('[data-search-status]').textContent = !sq ? 'Bitte geben Sie einen Suchbegriff ein.' : hits.length + ' Treffer gefunden.';
    if (!hits.length) {
      $('[data-noresult]').hidden = false;
      var words = []; PRODUCTS.forEach(function (p) { p.name.split(/[\s,]+/).forEach(function (w) { if (w.length > 3) { words.push(w); } }); });
      var lev = function (a, b) {
        var d = [], i, j; for (i = 0; i <= a.length; i++) { d[i] = [i]; } for (j = 1; j <= b.length; j++) { d[0][j] = j; }
        for (i = 1; i <= a.length; i++) { for (j = 1; j <= b.length; j++) { d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); } }
        return d[a.length][b.length];
      };
      var best = null, bd = 99; if (sq) { words.forEach(function (w) { var d = lev(ql, w.toLowerCase()); if (d < bd) { bd = d; best = w; } }); }
      if (best && bd <= 2) { $('[data-didyoumean]').hidden = false; var dl = $('[data-didyoumean-link]'); dl.textContent = best; dl.href = 'search.html?q=' + encodeURIComponent(best); }
    }
  }

  /* ---------- Shop: Filter, Sortierung, Mehr laden, Pills ---------- */
  var grid = $('[data-grid]');
  if (grid) {
    var form = $('[data-filter-form]'), BATCH = 8, shown = BATCH;
    var cols = $$('.col', grid).map(function (c) { return { col: c, card: $('.p-card', c) }; });
    var sortSel = $('[data-sort]'), priceIn = $('#price-max');
    var state = function () {
      var s = { kat: [], marke: [], region: [], allergen: [], flags: [], preis: parseFloat(priceIn.value) };
      $$('input[type=checkbox]:checked', form).forEach(function (c) { if (s[c.name]) { s[c.name].push(c.value); } else { s.flags.push(c.name); } });
      return s;
    };
    var pass = function (c, s) {
      var d = c.dataset;
      if (s.kat.length && s.kat.indexOf(d.cat) < 0) { return false; }
      if (s.marke.length && s.marke.indexOf(d.brand) < 0) { return false; }
      if (s.region.length && s.region.indexOf(d.region) < 0) { return false; }
      if (parseFloat(d.price) > s.preis) { return false; }
      if (s.flags.indexOf('lager') > -1 && d.stock === '0') { return false; }
      if (s.flags.indexOf('kuehl') > -1 && d.cool !== '1') { return false; }
      if (s.flags.indexOf('bio') > -1 && d.bio !== '1') { return false; }
      if (s.flags.indexOf('trad') > -1 && d.trad !== '1') { return false; }
      for (var i = 0; i < s.allergen.length; i++) { if (d.allergens.indexOf(s.allergen[i]) > -1) { return false; } }
      return true;
    };
    var sorted = function (list) {
      var v = sortSel.value, a = list.slice(); var n = function (x, k) { return parseFloat(x.card.dataset[k]); };
      if (v === 'price-asc') { a.sort(function (x, y) { return n(x, 'price') - n(y, 'price'); }); }
      if (v === 'price-desc') { a.sort(function (x, y) { return n(y, 'price') - n(x, 'price'); }); }
      if (v === 'rating') { a.sort(function (x, y) { return n(y, 'rating') - n(x, 'rating'); }); }
      if (v === 'name') { a.sort(function (x, y) { return x.card.dataset.name.localeCompare(y.card.dataset.name, 'de'); }); }
      return a;
    };
    var pills = function () {
      var box = $('[data-pills]'); box.textContent = '';
      var add = function (label, input) {
        var p = el('span', 'filter-pill', label); var b = el('button'); b.type = 'button'; b.setAttribute('aria-label', 'Filter entfernen: ' + label); b.appendChild(icon('bi-x-lg'));
        b.addEventListener('click', function () { if (input.type === 'range') { input.value = input.max; } else { input.checked = false; } apply(true); });
        p.appendChild(b); box.appendChild(p);
      };
      $$('input[type=checkbox]:checked', form).forEach(function (c) { add($('label[for="' + c.id + '"]', form).textContent, c); });
      if (parseFloat(priceIn.value) < parseFloat(priceIn.max)) { add('bis ' + priceIn.value + ' €', priceIn); }
    };
    var apply = function (reset) {
      if (reset) { shown = BATCH; }
      var s = state(); $('#price-out').textContent = priceIn.value + ' €';
      var list = sorted(cols.filter(function (x) { return pass(x.card, s); }));
      cols.forEach(function (x) { x.col.hidden = true; });
      list.forEach(function (x, i) { grid.appendChild(x.col); x.col.hidden = i >= shown; });
      $('[data-result-count]').textContent = list.length; $('[data-empty]').hidden = list.length > 0;
      $('[data-load-more]').hidden = list.length <= shown; pills(); counts();
    };
    /* Zähler an den Filter-Buttons: „Kategorie (2)“ + Tönung, wenn in der Gruppe etwas gewählt ist */
    var counts = function () {
      $$('.dropdown', form).forEach(function (dd) {
        var n = $$('input[type=checkbox]:checked', dd).length;
        var r = $('input[type=range]', dd); if (r && parseFloat(r.value) < parseFloat(r.max)) { n += 1; }
        var btn = $('.filter-btn', dd), out = $('[data-filter-n]', dd);
        btn.classList.toggle('has-value', n > 0); out.textContent = n > 0 ? n : '';
        if (n > 0) { out.setAttribute('aria-label', n + ' aktiv'); } else { out.removeAttribute('aria-label'); }
      });
    };
    /* Text des Ein-/Ausblenden-Buttons passend umschalten */
    var bar = $('#filterBar'), barLabel = $('[data-filter-toggle-label]');
    if (bar && barLabel) {
      bar.addEventListener('shown.bs.collapse', function () { barLabel.textContent = 'Filter ausblenden'; });
      bar.addEventListener('hidden.bs.collapse', function () { barLabel.textContent = 'Filter einblenden'; });
    }
    form.addEventListener('change', function () { apply(true); });
    form.addEventListener('input', function (e) { if (e.target === priceIn) { apply(true); } });
    form.addEventListener('reset', function () { setTimeout(function () { apply(true); }, 0); });
    sortSel.addEventListener('change', function () { apply(true); });
    $('[data-load-more]').addEventListener('click', function (e) {
      var btn = e.currentTarget, sk = $('[data-skeleton]'); sk.hidden = false; btn.disabled = true;
      setTimeout(function () { sk.hidden = true; btn.disabled = false; shown += BATCH; apply(false); toast('Weitere Produkte geladen', 'bi-box-seam'); }, reduceMotion ? 0 : 600);
    });
    var up = new URLSearchParams(location.search);
    ['kat', 'region'].forEach(function (k) {
      var v = up.get(k); if (!v) { return; }
      var c = $('input[name=' + k + '][value="' + v + '"]', form);
      if (c) { c.checked = true; $('[data-shop-title]').textContent = CATS[v] || c.nextElementSibling.textContent; }
    });
    if (up.get('kuehl')) { $('#v-cool').checked = true; }
    apply(true);
  }

  /* ---------- Produktseite: Galerie, ?id=, Lieferdatum, Zuletzt angesehen ---------- */
  var pdp = $('[data-pdp]');
  if (pdp) {
    var pid = new URLSearchParams(location.search).get('id') || 'bacalhau-graudo'; var pp = byId(pid) || byId('bacalhau-graudo');
    if (pp.id !== 'bacalhau-graudo') {  // Demo: Kernfelder austauschen. Im echten Shop rendert der Server die Seite.
      var set = function (sel, v) { var x = $(sel); if (x) { x.textContent = v; } };
      set('[data-pdp-name]', pp.name); set('[data-pdp-brand]', pp.brand); set('[data-pdp-price]', eur(pp.price)); set('[data-pdp-price-sticky]', eur(pp.price));
      set('[data-pdp-base]', pp.base); set('[data-pdp-crumb]', pp.name); set('[data-pdp-desc]', pp.desc); document.title = pp.name + ' | Alma Ibérica Online Shop';
      var pim = $('[data-pdp-img]'); pim.src = 'assets/img/' + pp.img + '.webp'; pim.alt = pp.name;
      $$('[data-add]', document).forEach(function (b) { if (b.hasAttribute('data-pdp-add')) { b.dataset.add = pp.id; b.disabled = pp.stock === 0; } });
      $$('[data-pdp] [data-wish], .sticky-buy [data-wish]').forEach(function (b) { b.dataset.wish = pp.id; });
      $('[data-thumb="bacalhau"]').dataset.thumb = pp.img;
      var stk = $('[data-pdp-stock]'); stk.textContent = pp.stock === 0 ? 'Derzeit nicht verfügbar' : (pp.stock <= 5 ? 'Nur noch ' + pp.stock + '× verfügbar' : 'Auf Lager');
    }
    var gm = $('[data-gallery-main]'), gi = $('img', gm);
    gm.tabIndex = 0; gm.setAttribute('role', 'button'); gm.setAttribute('aria-label', 'Bild vergrößern');
    var zoom = function () { var z = gm.classList.toggle('is-zoomed'); gm.setAttribute('aria-label', z ? 'Vergrößerung beenden' : 'Bild vergrößern'); };
    gm.addEventListener('click', zoom);
    gm.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); zoom(); } });
    gm.addEventListener('mousemove', function (e) { var r = gm.getBoundingClientRect(); gm.style.setProperty('--zoom-x', ((e.clientX - r.left) / r.width * 100) + '%'); gm.style.setProperty('--zoom-y', ((e.clientY - r.top) / r.height * 100) + '%'); });
    $$('[data-thumb]').forEach(function (t) { t.addEventListener('click', function () {
      gi.src = 'assets/img/' + t.dataset.thumb + '.webp'; $$('[data-thumb]').forEach(function (o) { o.setAttribute('aria-current', 'false'); }); t.setAttribute('aria-current', 'true'); gm.classList.remove('is-zoomed'); }); });
    var addWork = function (n) { var d = new Date(); while (n > 0) { d.setDate(d.getDate() + 1); if (d.getDay() % 6 !== 0) { n--; } } return d.toLocaleDateString('de-DE', { weekday: 'short', day: '2-digit', month: '2-digit' }); };
    $('[data-delivery-date]').textContent = addWork(2) + ' – ' + addWork(4);
    var rec = (store('ai_recent') || []).filter(function (x) { return x !== pp.id; });
    var rcards = cardsFromTemplate(rec.slice(0, 4));
    if (rcards.length) { $('[data-recent-empty]').remove(); var rbox = $('[data-recent]'); rcards.forEach(function (c) { rbox.appendChild(c); }); }
    rec.unshift(pp.id); store('ai_recent', rec.slice(0, 8));
  }

  /* ---------- Checkout (3 Schritte, Validierung, Fehlerübersicht) ---------- */
  var co = $('[data-checkout]');
  if (co) {
    var step = 1, steps = $$('[data-step]', co), stepper = $$('[data-stepper] li'), summary = $('[data-error-summary]'), elist = $('[data-error-list]');
    var MSG = { vorname: 'Bitte geben Sie Ihren Vornamen ein.', nachname: 'Bitte geben Sie Ihren Nachnamen ein.', email: 'Bitte geben Sie eine gültige E-Mail-Adresse ein.', strasse: 'Bitte geben Sie Straße und Hausnummer ein.', plz: 'Bitte geben Sie eine fünfstellige PLZ ein.', ort: 'Bitte geben Sie Ihren Ort ein.', agb: 'Bitte bestätigen Sie AGB, Datenschutz und Widerruf.' };
    var show = function (n) {
      step = n; steps.forEach(function (s) { s.hidden = Number(s.dataset.step) !== n; });
      stepper.forEach(function (li, i) { li.removeAttribute('aria-current'); li.classList.toggle('is-done', i < n - 1); if (i === n - 1) { li.setAttribute('aria-current', 'step'); } });
      $('[data-step-heading]').focus(); window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      if (n === 3) { review(); }
    };
    var validate = function (scope) {
      var errs = []; summary.hidden = true; elist.textContent = '';
      $$('input[required]', scope).forEach(function (i) {
        var err = document.getElementById(i.id + '-err');
        var bad = i.type === 'checkbox' ? !i.checked : (!i.checkValidity() || !i.value.trim());
        if (i.closest('[hidden]')) { bad = false; }
        i.classList.toggle('is-invalid-ai', bad); i.setAttribute('aria-invalid', String(bad));
        if (err) { err.hidden = !bad; err.textContent = bad ? MSG[i.name] : ''; }
        if (bad) { errs.push(i); }
      });
      if (errs.length) {
        errs.forEach(function (i) { var li = el('li'); var a = el('a', '', MSG[i.name]); a.href = '#' + i.id; a.addEventListener('click', function (ev) { ev.preventDefault(); i.focus(); }); li.appendChild(a); elist.appendChild(li); });
        summary.hidden = false; summary.focus();
      }
      return !errs.length;
    };
    var review = function () {
      var dl = $('[data-review]'); dl.textContent = ''; var f = new FormData(co);
      var rows = [['Lieferart', f.get('lieferart') === 'abholung' ? 'Click & Collect am [Standort auswählen]' : 'Versand'], ['Name', f.get('vorname') + ' ' + f.get('nachname')], ['E-Mail', f.get('email')]];
      if (f.get('lieferart') !== 'abholung') { rows.push(['Adresse', f.get('strasse') + ', ' + f.get('plz') + ' ' + f.get('ort')]); }
      rows.push(['Zahlung', f.get('zahlung')]);
      rows.forEach(function (r) { dl.appendChild(el('dt', 'col-sm-3', r[0])); dl.appendChild(el('dd', 'col-sm-9', r[1])); });
    };
    $$('[data-next]', co).forEach(function (b) { b.addEventListener('click', function () { if (validate(steps[step - 1])) { show(step + 1); } }); });
    $$('[data-prev]', co).forEach(function (b) { b.addEventListener('click', function () { summary.hidden = true; show(step - 1); }); });
    co.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!cart.items.length) { toast('Ihr Warenkorb ist leer.', 'bi-exclamation-circle-fill'); return; }
      if (!validate(steps[2])) { return; }
      var btn = $('button[type=submit]', co); btn.classList.add('is-loading');
      setTimeout(function () { btn.classList.remove('is-loading'); co.hidden = true; var ok = $('[data-success]'); ok.hidden = false; ok.tabIndex = -1; ok.focus(); cart.clear(); }, 700);
    });
    $$('[data-express]').forEach(function (b) { b.addEventListener('click', function () { toast(b.dataset.express + ' ist im Prototyp nicht angebunden.', 'bi-info-circle-fill'); }); });
  }

  /* ---------- Newsletter ---------- */
  $$('[data-newsletter]').forEach(function (f) { f.addEventListener('submit', function (e) {
    e.preventDefault(); var i = $('input[type=email]', f);
    if (!i.checkValidity() || !i.value) { i.setAttribute('aria-invalid', 'true'); i.focus(); toast('Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'bi-exclamation-circle-fill'); return; }
    i.removeAttribute('aria-invalid'); f.reset(); toast('Danke! Bitte bestätigen Sie Ihre Anmeldung per E-Mail (Double-Opt-in).');
  }); });

  /* ---------- Geschenke: Anlass-Filter ---------- */
  $$('[data-occ]').forEach(function (b) { b.addEventListener('click', function () {
    $$('[data-occ]').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
    $$('[data-occasion]').forEach(function (c) { c.hidden = !(b.dataset.occ === 'alle' || c.dataset.occasion.split(' ').indexOf(b.dataset.occ) > -1); });
  }); });

  /* ---------- Cookie-Consent ---------- */
  var bar = $('#cookieBar');
  if (bar) {
    var consent = function (v) { store('ai_consent', v); bar.hidden = true; };
    if (!store('ai_consent')) { bar.hidden = false; }
    $$('[data-cookie]').forEach(function (b) { b.addEventListener('click', function () {
      var a = b.dataset.cookie;
      if (a === 'accept') { consent({ stat: true, mkt: true }); }
      if (a === 'decline') { consent({ stat: false, mkt: false }); }
      if (a === 'save') { consent({ stat: $('#ck-stat').checked, mkt: $('#ck-mkt').checked }); bootstrap.Modal.getInstance($('#cookieModal')).hide(); }
    }); });
    $$('[data-cookie-settings]').forEach(function (b) { b.addEventListener('click', function () { var c = store('ai_consent') || {}; $('#ck-stat').checked = !!c.stat; $('#ck-mkt').checked = !!c.mkt; bootstrap.Modal.getOrCreateInstance($('#cookieModal')).show(); }); });
  }

  /* ---------- Hero-Video: Pause/Weiter (WCAG 2.2.2), Standbild bei reduzierter Bewegung ---------- */
  var heroVid = $('#hero-video'), heroBtn = $('.hero-anim .drone-toggle');
  if (heroVid && heroBtn) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { heroVid.removeAttribute('autoplay'); heroVid.pause(); }
    var setHeroBtn = function (playing) {
      heroBtn.setAttribute('aria-label', playing ? 'Animation anhalten' : 'Animation fortsetzen');
      heroBtn.firstElementChild.className = 'bi ' + (playing ? 'bi-pause-fill' : 'bi-play-fill');
    };
    heroBtn.addEventListener('click', function () {
      if (heroVid.paused) { heroVid.play(); setHeroBtn(true); } else { heroVid.pause(); setHeroBtn(false); }
    });
  }

  /* ---------- Sprachumschalter (Prototyp: nur Auswahl, noch keine Übersetzungen) ---------- */
  var langBtns = $$('.lang-btn');
  langBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      langBtns.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
      if (b.dataset.lang !== 'de') { toast('Prototyp: Sprachversion „' + b.textContent + '“ ist noch nicht verfügbar.', 'bi-translate'); }
    });
  });

  /* ---------- Karussell: Pfeile (Desktop) und Punkte (kleine Geräte) ---------- */
  $$('.ai-carousel').forEach(function (car) {
    var wrap = document.createElement('div'); wrap.className = 'ai-carousel-wrap';
    car.parentNode.insertBefore(wrap, car); wrap.appendChild(car);
    function mk(cls, icon, label) {
      var b = document.createElement('button'); b.type = 'button'; b.className = cls; b.setAttribute('aria-label', label);
      b.innerHTML = '<i class="bi ' + icon + '" aria-hidden="true"></i>'; return b;
    }
    var prev = mk('ai-car-btn ai-car-prev', 'bi-chevron-left', 'Zurück'), next = mk('ai-car-btn ai-car-next', 'bi-chevron-right', 'Weiter');
    var dots = document.createElement('div'); dots.className = 'ai-car-dots';
    wrap.insertBefore(prev, car); wrap.appendChild(next); wrap.appendChild(dots);
    function pages() { return Math.max(1, Math.ceil((car.scrollWidth - 2) / car.clientWidth)); }
    function current() { var max = car.scrollWidth - car.clientWidth; return max <= 0 ? 0 : Math.round(car.scrollLeft / max * (pages() - 1)); }
    function buildDots() {
      dots.innerHTML = '';
      for (var i = 0; i < pages(); i++) {
        (function (n) {
          var d = document.createElement('button'); d.type = 'button'; d.className = 'ai-car-dot'; d.setAttribute('aria-label', 'Seite ' + (n + 1) + ' von ' + pages());
          d.addEventListener('click', function () { var max = car.scrollWidth - car.clientWidth; car.scrollTo({ left: pages() > 1 ? max * n / (pages() - 1) : 0 }); });
          dots.appendChild(d);
        })(i);
      }
      update();
    }
    function update() {
      var max = car.scrollWidth - car.clientWidth;
      prev.disabled = car.scrollLeft <= 2; next.disabled = car.scrollLeft >= max - 2;
      var c = current();
      Array.prototype.forEach.call(dots.children, function (d, i) { if (i === c) { d.setAttribute('aria-current', 'true'); } else { d.removeAttribute('aria-current'); } });
    }
    prev.addEventListener('click', function () { car.scrollBy({ left: -car.clientWidth * 0.9 }); });
    next.addEventListener('click', function () { car.scrollBy({ left: car.clientWidth * 0.9 }); });
    car.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', buildDots);
    window.addEventListener('load', buildDots);
    buildDots();
  });

  /* ---------- Sonstiges ---------- */
  $$('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
  $$('form').forEach(function (f) {
    var own = f.hasAttribute('data-checkout') || f.hasAttribute('data-search') || f.hasAttribute('data-newsletter') || f.hasAttribute('data-filter-form');
    if (!own) { f.addEventListener('submit', function (e) { e.preventDefault(); toast('Prototyp: Formular wurde nicht gesendet.', 'bi-info-circle-fill'); }); }
  });
  render(); syncWish();

  /* ---------- Anker-Sprünge: Ziel nicht unter dem festen Header verstecken ---------- */
  function fixAnchorOffset() {
    var h = $('.site-header');
    if (h) { document.documentElement.style.scrollPaddingTop = (h.offsetHeight + 16) + 'px'; }
  }
  fixAnchorOffset();
  window.addEventListener('resize', fixAnchorOffset);
  if (location.hash.length > 1) {
    var anchorEl = null;
    try { anchorEl = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { anchorEl = null; }
    if (anchorEl) { anchorEl.scrollIntoView(); }
  }
})();
