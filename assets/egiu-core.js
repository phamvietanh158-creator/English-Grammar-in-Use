/* EGIU core: lưu trữ, tuỳ chọn, giọng đọc (UK/US), chấm đáp án.
   Dùng chung cho mọi unit. Giọng đọc port từ dự án PRONOUNCE (epu-core.js). */
(function () {
  "use strict";
  const E = (window.EGIU = {});

  // ── Tiện ích ────────────────────────────────────────────
  E.PASS = 70; // % tối thiểu để tính là đã hoàn thành unit
  E.esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  E.plain = t => String(t).replace(/<[^>]+>/g, "").replace(/\*\*/g, "").replace(/_{2,}/g, " ").replace(/\s+/g, " ").trim();
  E.rich = t => E.esc(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  E.store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };

  // ── Tuỳ chọn người dùng ─────────────────────────────────
  E.prefs = Object.assign({ accent: "uk", ipa: false, vi: false }, E.store.get("egiu_prefs", {}));
  E.applyPrefs = function () {
    document.body.classList.toggle("show-ipa", !!E.prefs.ipa);
    document.body.classList.toggle("show-vi", !!E.prefs.vi);
  };
  E.setPref = function (k, v) {
    E.prefs[k] = v;
    E.store.set("egiu_prefs", E.prefs);
    if (k === "accent") E.stop();
    E.applyPrefs();
    if (E.onVoices) E.onVoices();
  };

  // ── Giọng đọc ───────────────────────────────────────────
  const LANG = { uk: "en-GB", us: "en-US" };
  const PREFS = {
    uk: ["Microsoft Sonia Online", "Microsoft Libby Online", "Microsoft Ryan Online", "Microsoft Maisie Online",
         "Google UK English Female", "Google UK English Male", "Daniel", "Kate", "Serena",
         "Microsoft Hazel", "Microsoft Susan", "Microsoft George"],
    us: ["Microsoft Aria Online", "Microsoft Jenny Online", "Microsoft Guy Online", "Microsoft Ava Online",
         "Microsoft Andrew Online", "Google US English", "Samantha", "Alex", "Microsoft Zira", "Microsoft David"]
  };
  const NEURAL = /Online|Natural|Google|Neural|Premium|Enhanced/i;
  const RATE = { normal: 0.9, slow: 0.7 }; // pitch luôn 1.0; không đọc chậm hơn 0.7 để khỏi méo âm
  let voices = [], token = 0, curAudio = null;

  const normLang = l => (l || "").replace("_", "-").toLowerCase();
  function loadVoices() {
    if (!window.speechSynthesis) return;
    voices = speechSynthesis.getVoices();
    if (E.onVoices) E.onVoices();
  }
  E.voice = function () {
    const lang = LANG[E.prefs.accent].toLowerCase();
    const match = voices.filter(v => normLang(v.lang) === lang);
    for (const p of PREFS[E.prefs.accent]) {
      const v = match.find(x => x.name.includes(p));
      if (v) return v;
    }
    return match[0] || null;
  };
  E.voiceQuality = () => { const v = E.voice(); return !v ? "none" : NEURAL.test(v.name) ? "good" : "basic"; };
  if (window.speechSynthesis) {
    loadVoices();
    speechSynthesis.onvoiceschanged = loadVoices;
    [300, 1000, 2500].forEach(t => setTimeout(loadVoices, t));
  }

  E.stop = function () {
    token++;
    if (window.speechSynthesis) speechSynthesis.cancel();
    if (curAudio) { curAudio.pause(); curAudio = null; }
  };

  // Giai đoạn sau: window.EGIU_AUDIO = { uk: { "slug": "audio/uk/slug.mp3" } } (mp3 sinh sẵn)
  E.slug = t => E.plain(t).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  function audioFor(t) {
    const m = window.EGIU_AUDIO && window.EGIU_AUDIO[E.prefs.accent];
    return m ? (m[E.slug(t)] || null) : null;
  }

  function tts(text, slow, my) {
    return new Promise(res => {
      if (!window.speechSynthesis || my !== token) return res();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = LANG[E.prefs.accent];
      const v = E.voice();
      if (v) u.voice = v;
      u.rate = slow ? RATE.slow : RATE.normal;
      u.pitch = 1;
      let done = false;
      const fin = () => { if (!done) { done = true; clearTimeout(tm); res(); } };
      u.onend = fin; u.onerror = fin;
      const tm = setTimeout(fin, 2500 + text.length * 120 / u.rate); // phòng khi onend không bắn
      setTimeout(() => (my === token ? speechSynthesis.speak(u) : fin()), 40);
    });
  }

  E.speak = function (text, slow) {
    const t = E.plain(text);
    if (!t) return Promise.resolve();
    E.stop();
    const my = token;
    const file = audioFor(t);
    if (file) {
      return new Promise(res => {
        const a = new Audio(file);
        curAudio = a;
        a.playbackRate = slow ? 0.75 : 1;
        a.onended = () => res(true);
        a.onerror = () => res(false);
        a.play().catch(() => res(false));
      }).then(ok => (ok || my !== token) ? null : tts(t, slow, my));
    }
    return tts(t, slow, my);
  };

  // Bấm bất kỳ phần tử có data-say="…" để nghe (data-slow="1" để đọc chậm)
  document.addEventListener("click", ev => {
    const el = ev.target.closest("[data-say]");
    if (!el) return;
    el.classList.add("playing");
    E.speak(el.getAttribute("data-say"), el.dataset.slow === "1").then(() => el.classList.remove("playing"));
  });

  // ── Chấm đáp án ─────────────────────────────────────────
  // Đưa cả đáp án mẫu lẫn bài làm về dạng viết đầy đủ để "I'm" = "I am", "isn't" = "is not".
  const CONTR = [[/\bcan't\b/g, "cannot"], [/\bwon't\b/g, "will not"], [/n't\b/g, " not"], [/'m\b/g, " am"],
                 [/'re\b/g, " are"], [/'ve\b/g, " have"], [/'ll\b/g, " will"], [/'d\b/g, " would"], [/'s\b/g, " is"]];
  E.canon = function (s) {
    s = String(s).toLowerCase().replace(/[‘’]/g, "'");
    CONTR.forEach(([re, to]) => { s = s.replace(re, to); });
    return s.replace(/,/g, " ").replace(/[.!?;:]+\s*$/, "").replace(/\s+/g, " ").trim();
  };
  E.isCorrect = function (value, item) {
    const v = E.canon(value);
    if (!v) return false;
    return [item.answer].concat(item.alts || []).some(a => E.canon(a) === v);
  };

  // ── Thanh công cụ: giọng UK/US, phiên âm, dịch nghĩa ────
  E.toolbarHTML = () =>
    '<div class="toolbar">' +
    '<div class="seg" role="group" aria-label="Giọng đọc">' +
    '<button type="button" data-accent="uk">🇬🇧 UK</button><button type="button" data-accent="us">🇺🇸 US</button></div>' +
    '<label class="tg"><input type="checkbox" id="tgIpa"> Phiên âm (UK)</label>' +
    '<label class="tg"><input type="checkbox" id="tgVi"> Dịch nghĩa</label>' +
    '<span class="voice-status"></span></div>';

  E.bindToolbar = function (root) {
    const accentBtns = root.querySelectorAll("[data-accent]");
    const ipa = root.querySelector("#tgIpa"), vi = root.querySelector("#tgVi");
    const status = root.querySelector(".voice-status");
    function sync() {
      accentBtns.forEach(b => b.classList.toggle("on", b.dataset.accent === E.prefs.accent));
      ipa.checked = !!E.prefs.ipa;
      vi.checked = !!E.prefs.vi;
      const v = E.voice(), q = E.voiceQuality();
      if (!window.speechSynthesis) status.innerHTML = '<span class="warn">⚠️ Trình duyệt không hỗ trợ đọc. Hãy dùng Edge hoặc Chrome.</span>';
      else if (q === "none") status.innerHTML = '<span class="warn">⚠️ Máy chưa có giọng ' + LANG[E.prefs.accent] + '.</span>';
      else if (q === "basic") status.innerHTML = 'Giọng: ' + E.esc(v.name) + ' · <span class="warn">Dùng Microsoft Edge để có giọng tự nhiên hơn.</span>';
      else status.textContent = "Giọng: " + v.name;
    }
    accentBtns.forEach(b => b.addEventListener("click", () => E.setPref("accent", b.dataset.accent)));
    ipa.addEventListener("change", () => E.setPref("ipa", ipa.checked));
    vi.addEventListener("change", () => E.setPref("vi", vi.checked));
    E.onVoices = sync;
    sync();
  };

  document.addEventListener("DOMContentLoaded", E.applyPrefs);
})();
