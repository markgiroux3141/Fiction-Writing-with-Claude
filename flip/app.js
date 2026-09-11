/* A reader for book bundles.
 *
 * The app knows nothing about any particular book. A book is a bundle:
 *
 *     <id>/book.json
 *     <id>/pages/0001.jpg ...
 *
 * and book.json is the whole contract (see render/scripts/build_bundle.py).
 * Nothing is bundled into the apk: every book is found at runtime in the app's
 * own folder on the device, so adding one is copying a directory and adding a
 * shelf of them needs no new build.
 */
(function () {
  'use strict';

  const inApp = !!(window.Capacitor && window.Capacitor.isNativePlatform &&
                   window.Capacitor.isNativePlatform());

  const $ = id => document.getElementById(id);
  const views = { shelf: $('shelf'), reader: $('reader') };

  function show(name) {
    for (const k in views) views[k].classList.toggle('on', k === name);
    document.body.classList.toggle('reading', name === 'reader');
  }

  /* ── where the reader left off ─────────────────────────────────────────
   * Keyed by the bundle's id, which is why build_bundle.py insists the id is
   * stable across rebuilds: change it and the reader silently loses its place.
   * localStorage can throw outright in some contexts, so every access is
   * guarded and a failure degrades to "no saved place" rather than no book. */
  const PROGRESS = 'sw.progress.v1';

  function readProgress() {
    try { return JSON.parse(localStorage.getItem(PROGRESS) || '{}'); }
    catch (e) { return {}; }
  }
  function saveProgress(id, page) {
    try {
      const all = readProgress();
      all[id] = { page: page, at: Date.now() };
      localStorage.setItem(PROGRESS, JSON.stringify(all));
    } catch (e) { /* reading still works without a remembered place */ }
  }
  function progressFor(id) {
    const p = readProgress()[id];
    return p && typeof p.page === 'number' ? p : null;
  }

  /* ── sources ───────────────────────────────────────────────────────────── */

  // The WebView is served from https://localhost and cannot read /sdcard, so
  // the native Books plugin enumerates what was added and hands back each
  // manifest plus its absolute path. convertFileSrc turns that path into a URL
  // the native layer streams, so pages stay ordinary <img src> — no base64,
  // and no second copy of the book in memory.
  let externalDir = null;

  async function externalBooks() {
    if (!inApp) return [];
    const Books = window.Capacitor.Plugins.Books;
    if (!Books) return [];

    let res;
    try { res = await Books.list(); }
    catch (e) { console.warn('Books.list failed', e); return []; }

    externalDir = res.dir || null;
    const out = [];
    for (const entry of (res.books || [])) {
      let manifest;
      try { manifest = JSON.parse(entry.manifest); }
      catch (e) {
        console.warn('skipping ' + entry.dir + ': book.json is not valid JSON');
        continue;
      }
      if (!manifest.pages || !manifest.pages.length) {
        console.warn('skipping ' + entry.dir + ': no pages listed');
        continue;
      }
      out.push(Object.assign({}, manifest, {
        origin: 'external',
        id: manifest.id || entry.dir,
        url: rel => window.Capacitor.convertFileSrc(entry.base + '/' + rel),
      }));
    }
    return out;
  }

  /* ── the shelf ─────────────────────────────────────────────────────────── */

  let library = [];

  function shelfLabel(b) {
    const n = b.count || (b.pages || []).length;
    const p = progressFor(b.id);
    // Report the reader's place in the same folio the reader itself shows,
    // so "page 12" in one view is never "page 13" in the other.
    return p && p.page > 0 ? `${n} leaves · at ${p.page + 1}` : `${n} leaves`;
  }

  function drawShelf() {
    const list = $('books');
    list.textContent = '';

    if (!library.length) {
      const p = document.createElement('p');
      p.id = 'empty';
      // The real path the plugin reports, not one written from memory — the
      // folder is created on first run precisely so it can be named here.
      const where = externalDir ||
        'Android/data/com.standingwater.facsimile/files/books';
      p.append('No books yet.', document.createElement('br'),
               'Put a bundle here:');
      const code = document.createElement('code');
      code.textContent = where + '/<name>/';
      p.append(document.createElement('br'), code);
      list.append(p);
      return;
    }

    for (const b of library) {
      const card = document.createElement('button');
      card.className = 'book';
      card.type = 'button';

      const boards = document.createElement('div');
      boards.className = 'boards';
      const img = document.createElement('img');
      img.alt = '';
      img.loading = 'lazy';
      img.src = b.url(b.cover || (b.pages && b.pages[0]) || '');
      boards.append(img);

      const name = document.createElement('div');
      name.className = 'name';
      name.textContent = b.title || b.id;

      // Without the subtitle two editions of the same book are the same card
      // with the same cover and the same title, and the shelf is a guess.
      let sub = null;
      if (b.subtitle) {
        sub = document.createElement('div');
        sub.className = 'sub2';
        sub.textContent = b.subtitle;
      }

      const meta = document.createElement('div');
      meta.className = 'meta';
      meta.textContent = shelfLabel(b);

      card.append(boards, name);
      if (sub) card.append(sub);
      card.append(meta);
      card.onclick = () => openBook(b);
      list.append(card);
    }
  }

  async function loadLibrary() {
    const external = await externalBooks().catch(() => []);
    // By title. A shelf that reorders itself between launches is a shelf you
    // cannot learn.
    const byTitle = (x, y) => String(x.title || x.id)
      .localeCompare(String(y.title || y.id));
    library = external.sort(byTitle);
    drawShelf();
  }

  /* ── the reader ────────────────────────────────────────────────────────── */

  let flip = null;
  let current = null;
  let idle = null;
  // Set when a book opens, because the loupe closes over that book's pages.
  let loupeToggle = null;
  let loupeCleanup = null;

  function wake() {
    const chrome = $('chrome');
    chrome.classList.remove('gone');
    clearTimeout(idle);
    idle = setTimeout(() => chrome.classList.add('gone'), 3800);
  }

  // page-flip's destroy() ends with this.block.remove() — it takes its own
  // container out of the DOM, not just its contents. So closing a book has to
  // put a fresh #book back, or the next one opens into nothing.
  function resetStage() {
    const stage = $('stage');
    const old = $('book');
    if (old) old.remove();
    const fresh = document.createElement('div');
    fresh.id = 'book';
    stage.insertBefore(fresh, $('gutter'));
  }

  function closeBook() {
    if (loupeCleanup) { loupeCleanup(); loupeCleanup = null; }
    loupeToggle = null;
    if (flip) {
      try { flip.destroy(); } catch (e) { /* already gone */ }
      flip = null;
    }
    resetStage();
    current = null;
    show('shelf');
    drawShelf();          // pick up the place we just left off at
  }

  function openBook(b) {
    current = b;
    const pages = (b.pages || []).map(p => b.url(p));
    if (!pages.length) return;

    $('opening').classList.add('on');
    show('reader');
    resetStage();

    const spread = b.spread !== false;
    document.documentElement.style.setProperty('--spread',
      ((spread ? 2 : 1) * b.pageWidth / b.pageHeight).toFixed(4));
    $('stage').classList.toggle('single', !spread);

    // size:'stretch' with autoSize hands sizing to page-flip, which keeps the
    // aspect with a percentage padding and rebinds on window resize. Measuring
    // the viewport once at load — which this did originally — left the book at
    // the old trim after a tablet rotated or a window was restored.
    // minWidth is doing something non-obvious for single-leaf books.
    //
    // page-flip decides its own orientation, and in stretch mode the whole
    // test is `blockWidth < 2 * minWidth`. On a landscape tablet the block is
    // far wider than 400, so a book asking for one leaf at a time still got a
    // two-page spread drawn into a container sized for one leaf, and rendered
    // as an empty rectangle. Forcing minWidth enormous makes the portrait
    // branch always win.
    //
    // The catch is that the constructor also writes `style.minWidth` from the
    // same number, which would shove the book far wider than the screen — so
    // it is cleared immediately after the UI is built.
    flip = new St.PageFlip($('book'), {
      width: b.pageWidth,
      height: b.pageHeight,
      size: 'stretch',
      autoSize: true,
      minWidth: spread ? 200 : 100000,
      maxWidth: 1400,
      showCover: b.showCover !== false,
      usePortrait: !spread,
      drawShadow: true,
      maxShadowOpacity: 0.6,
      flippingTime: 850,
      mobileScrollSupport: false,
      swipeDistance: 20,
    });

    flip.loadFromImages(pages);
    if (!spread) $('book').style.minWidth = '0px';

    const resume = progressFor(b.id);
    if (resume && resume.page > 0 && resume.page < pages.length) {
      flip.turnToPage(resume.page);
    }

    const n = pages.length;
    function label() {
      const i = flip.getCurrentPageIndex();   // 0-based, left leaf of spread
      $('folio').textContent = (i === 0 && b.showCover !== false)
        ? 'cover'
        : (!spread || i + 1 >= n ? `${i + 1} of ${n}`
                                 : `${i + 1}–${i + 2} of ${n}`);
      $('prev').disabled = i <= 0;
      $('next').disabled = spread ? i + 2 >= n : i + 1 >= n;
    }

    // Turning a leaf should not require dragging it.
    //
    // page-flip accepts a swipe only if it is finished within 250 ms (a
    // hardcoded swipeTimeout) and drifts less than 40 px vertically. Anything
    // slower becomes a DRAG, and a drag pivots about whichever corner is
    // nearer the finger — so grabbing the fore-edge halfway up folds the page
    // diagonally off a corner instead of lifting it, and has to be dragged
    // most of the way across before it takes. A plain tap does nothing at all:
    // the library only arms itself 250 ms after touchdown, by which time a tap
    // has already ended.
    //
    // So this fills in the gestures it drops, and only those. At pointerup it
    // waits 40 ms — long enough for the library's own touchend to run, since
    // pointer events fire first — and acts only if the state is still 'read',
    // which means nothing happened. A fast swipe, a completed drag and a drag
    // that snapped back all leave a non-read state, so none of them can be
    // turned twice.
    const bookEl = $('book');
    let press = null;
    bookEl.addEventListener('pointerdown', e => {
      press = { x: e.clientX, y: e.clientY, t: Date.now() };
    }, { passive: true });
    bookEl.addEventListener('pointerup', e => {
      if (!press) return;
      const p = press; press = null;
      const dx = e.clientX - p.x;
      const dy = e.clientY - p.y;
      const ms = Date.now() - p.t;
      const travel = Math.sqrt(dx * dx + dy * dy);
      const tap = travel < 16 && ms < 500;
      const swipe = Math.abs(dx) > 28 && Math.abs(dy) < 90 && ms < 1200;
      if (!tap && !swipe) return;

      const rect = bookEl.getBoundingClientRect();
      const forward = tap ? (e.clientX >= rect.left + rect.width / 2) : (dx < 0);
      setTimeout(() => {
        if (!flip) return;
        let state = 'read';
        try { state = flip.getState(); } catch (err) { /* older build */ }
        if (state !== 'read') return;      // the library handled it
        forward ? flip.flipNext() : flip.flipPrev();
      }, 40);
    }, { passive: true });

    /* ── the loupe ───────────────────────────────────────────────────────
     * Measured off the artwork in cover art/magnifying glass.png: the clear
     * aperture is centred 49.84% across and 35.37% down the cropped image,
     * with a radius of 19.70% of its width. The magnified circle has to sit
     * exactly on that aperture or the glass reads as a sticker.
     */
    // Measured off cover art/magnifying glass short handle.png by flood-
    // filling the alpha: the enclosed transparent region IS the aperture.
    // The artwork is used whole. The first attempt cropped the long-handled
    // version to keep it on screen, which cut through the middle of the
    // handle and showed as a straight edge slicing the glass in half.
    const GLASS_ASPECT = 1.7440;   // height / width of glass.png
    const LENS_X = 0.4994;         // of glass width
    const LENS_Y = 0.2817;         // of glass height
    const LENS_R = 0.4242;         // of glass width
    const ZOOM = 1.75;             // 2.2 read as too strong; the ceiling is 2.5
    const ROT = -45;               // handle hangs south-east, as in the hand
    const GRIP = 0.85;             // how far down the handle the finger holds

    const layer = $('loupeLayer');
    const loupe = $('loupe');
    const lens = $('loupeLens');
    const lensImg = $('loupeImg');
    let glassW = 0, lensR = 0, lift = { x: 0, y: 0 };

    let box = 0;
    function sizeGlass() {
      // Sized by the LENS, not by the artwork. The aperture is what the
      // reader is looking through, and it is the one dimension that should
      // not change when the artwork does — this glass is 85% lens by width,
      // the last one 39%, and sizing by width made it taller than the screen.
      const lensD = Math.min(250, Math.round(window.innerWidth * 0.19));
      glassW = lensD / (2 * LENS_R);
      const glassH = glassW * GLASS_ASPECT;
      lensR = lensD / 2;

      // The box has to contain the artwork however it is rotated, so it is a
      // square of twice the distance from the lens centre to the furthest
      // corner of the image. Anything tighter clips the handle.
      const cx = LENS_X * glassW, cy = LENS_Y * glassH;
      const reach = Math.max(
        Math.hypot(cx, cy), Math.hypot(glassW - cx, cy),
        Math.hypot(cx, glassH - cy), Math.hypot(glassW - cx, glassH - cy));
      box = Math.ceil(reach * 2) + 4;

      loupe.style.width = loupe.style.height = box + 'px';
      const glass = $('loupeGlass');
      glass.style.width = glassW + 'px';
      glass.style.height = glassH + 'px';
      glass.style.left = (box / 2 - cx) + 'px';
      glass.style.top = (box / 2 - cy) + 'px';
      glass.style.transform = `rotate(${ROT}deg)`;

      lens.style.width = lens.style.height = (lensR * 2) + 'px';
      lens.style.left = (box / 2 - lensR) + 'px';
      lens.style.top = (box / 2 - lensR) + 'px';

      // The finger grips near the end of the handle, so the lens rides clear
      // of the hand — a magnifier held any other way has your own knuckles in
      // it. The grip offset rotates with the handle, so the lens ends up up
      // and to the left of the finger.
      const along = (GRIP - LENS_Y) * glassH;
      const rad = ROT * Math.PI / 180;
      lift = { x: -Math.sin(rad) * along, y: Math.cos(rad) * along };
    }

    // Which leaf is under the point, and where on it. With showCover the
    // first spread is a single leaf drawn on the RIGHT, so index 0 has no
    // left-hand page; every later spread is [i, i+1].
    function sample(px, py) {
      const r = $('book').getBoundingClientRect();
      if (!r.width) return null;
      const i = flip.getCurrentPageIndex();
      const half = r.width / 2;
      const onRight = px >= r.left + half;
      let idx;
      if (i === 0 && b.showCover !== false) idx = onRight ? 0 : -1;
      else idx = onRight ? i + 1 : i;
      if (idx < 0 || idx >= pages.length) return null;
      const leafLeft = r.left + (onRight ? half : 0);
      return {
        src: pages[idx],
        u: (px - leafLeft) / half,          // 0..1 across the leaf
        v: (py - r.top) / r.height,         // 0..1 down the leaf
        leafW: half,
        leafH: r.height,
      };
    }

    function moveGlass(px, py) {
      // Where the glass is actually looking: the lens centre, not the finger.
      const lx = px - lift.x;
      const ly = py - lift.y;
      const s = sample(lx, ly);
      loupe.style.transform =
        `translate(${Math.round(lx - box / 2)}px, ${Math.round(ly - box / 2)}px)`;

      if (!s || s.u < 0 || s.u > 1 || s.v < 0 || s.v > 1) {
        lens.classList.add('blank');
        return;
      }
      lens.classList.remove('blank');
      if (lensImg.getAttribute('src') !== s.src) lensImg.src = s.src;
      const w = s.leafW * ZOOM, h = s.leafH * ZOOM;
      lensImg.style.width = w + 'px';
      lensImg.style.height = h + 'px';
      lensImg.style.transform =
        `translate(${(lensR - s.u * w).toFixed(1)}px, ${(lensR - s.v * h).toFixed(1)}px)`;
    }

    function loupeOn() { return document.body.classList.contains('loupe'); }

    function toggleLoupe(on) {
      const want = (on === undefined) ? !loupeOn() : on;
      document.body.classList.toggle('loupe', want);
      $('glassBtn').style.borderColor = want ? 'var(--ink)' : '';
      if (want) {
        sizeGlass();
        const r = $('book').getBoundingClientRect();
        // Start over the middle of the right-hand leaf, which is where the
        // text is on an opening, rather than at 0,0 off the corner.
        moveGlass(r.left + r.width * 0.72 + lift.x, r.top + r.height * 0.45 + lift.y);
      }
      wake();
    }

    layer.addEventListener('pointerdown', e => moveGlass(e.clientX, e.clientY));
    layer.addEventListener('pointermove', e => {
      if (e.buttons || e.pointerType === 'touch') moveGlass(e.clientX, e.clientY);
    });
    window.addEventListener('resize', () => { if (loupeOn()) sizeGlass(); });
    $('glassBtn').onclick = () => toggleLoupe();
    loupeCleanup = () => { document.body.classList.remove('loupe'); };
    loupeToggle = toggleLoupe;

    flip.on('flip', () => { label(); wake(); saveProgress(b.id, flip.getCurrentPageIndex()); });
    flip.on('changeState', e => {
      $('stage').classList.toggle('turning', e.data !== 'read');
    });
    label();
    wake();
    $('hint').classList.remove('gone');
    setTimeout(() => $('hint').classList.add('gone'), 7000);

    // The first spread has to decode before the book stops being a dark
    // rectangle; one frame is not enough on a tablet.
    setTimeout(() => $('opening').classList.remove('on'), 450);
  }

  /* ── wiring ────────────────────────────────────────────────────────────── */

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
  }

  $('prev').onclick = () => flip && flip.flipPrev();
  $('next').onclick = () => flip && flip.flipNext();
  $('shelfBtn').onclick = closeBook;
  $('full').onclick = fullscreen;

  window.addEventListener('keydown', e => {
    if (!current) return;
    if (e.key === 'ArrowLeft'  || e.key === 'PageUp')   flip.flipPrev();
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') flip.flipNext();
    if (e.key === 'Home') flip.turnToPage(0);
    if (e.key === 'End')  flip.turnToPage((current.pages || []).length - 1);
    if (e.key === 'Escape') closeBook();
    if (e.key === 'f' || e.key === 'F') fullscreen();
    if (e.key === 'b' || e.key === 'B') document.body.classList.toggle('bare');
    if (e.key === 'i' || e.key === 'I') document.body.classList.toggle('inset');
    if ((e.key === 'm' || e.key === 'M') && loupeToggle) loupeToggle();
  });

  ['pointerdown', 'pointermove', 'keydown', 'wheel'].forEach(
    t => window.addEventListener(t, () => { if (current) wake(); }, { passive: true }));

  // Pinch-zoom and the browser's own swipe-to-navigate both fight the page
  // turn on a touchscreen. Neither belongs in a book.
  document.addEventListener('gesturestart', e => e.preventDefault());
  document.addEventListener('contextmenu', e => e.preventDefault());

  // Android's back gesture should close the book, not the app. Without this
  // it leaves the app from the middle of a story, and coming back means
  // finding your place again.
  if (inApp && window.Capacitor.Plugins.App) {
    window.Capacitor.Plugins.App.addListener('backButton', () => {
      if (current) closeBook();
      else window.Capacitor.Plugins.App.exitApp();
    });
  }

  if (screen.orientation && screen.orientation.lock) {
    screen.orientation.lock('landscape').catch(() => {});
  }

  // ?book=<id> opens straight into one, and #p=12 lands on a leaf — for
  // checking a single spread without walking the shelf to reach it.
  loadLibrary().then(() => {
    const want = new URLSearchParams(location.search).get('book');
    const b = want && library.find(x => x.id === want);
    if (b) {
      openBook(b);
      const jump = /(?:^|#|&)p=(\d+)/.exec(location.hash);
      if (jump) flip.turnToPage(Math.min(+jump[1], b.pages.length - 1));
    } else {
      show('shelf');
    }
  });
})();
