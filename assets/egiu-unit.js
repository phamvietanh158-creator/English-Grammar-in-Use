/* EGIU unit renderer: dựng trang unit từ window.EGIU_UNITS[id] (xem docs/DATA_FORMAT.md). */
(function () {
  "use strict";
  const E = window.EGIU;
  const unitId = +document.body.dataset.unit;
  const U = (window.EGIU_UNITS || {})[unitId];
  const app = document.getElementById("app");
  if (!U) { app.innerHTML = '<div class="wrap">Chưa có dữ liệu cho unit này.</div>'; return; }

  // ── Câu (en + IPA + dịch) ───────────────────────────────
  function sentHTML(s, opts) {
    opts = opts || {};
    const say = E.esc(E.plain(s.en));
    return '<div class="sent"><div class="sent-main">' +
      '<span class="sent-en">' + (opts.label ? opts.label + " " : "") + E.rich(s.en) + "</span>" +
      '<button type="button" class="say" data-say="' + say + '" title="Nghe">🔊</button>' +
      '<button type="button" class="say" data-say="' + say + '" data-slow="1" title="Nghe chậm">🐢</button>' +
      (s.note ? ' <span class="note">' + E.esc(s.note) + "</span>" : "") + "</div>" +
      (s.ipa ? '<div class="s-ipa">/' + E.esc(s.ipa) + "/</div>" : "") +
      (s.vi ? '<div class="s-vi">' + E.esc(s.vi) + "</div>" : "") + "</div>";
  }

  // ── Lý thuyết ───────────────────────────────────────────
  function theoryHTML(t) {
    const body = (t.blocks || []).map(b => {
      let h = b.h ? "<h3>" + E.esc(b.h) + "</h3>" : "";
      if (b.p) h += "<p>" + E.rich(b.p) + "</p>";
      if (b.table) {
        h += '<table class="form-table"><tr>' + b.table.head.map(c => "<th>" + E.esc(c) + "</th>").join("") + "</tr>" +
          b.table.rows.map(r => "<tr>" + r.map(c => "<td>" + E.rich(c) + "</td>").join("") + "</tr>").join("") + "</table>";
      }
      (b.ex || []).forEach(s => { h += sentHTML(s); });
      return h;
    }).join("");
    return '<section class="theory" id="theory"><button type="button" class="theory-head" id="theoryHead">' +
      "<span>📘 Lý thuyết: " + E.esc(t.title) + '</span><span class="arrow">▾</span></button>' +
      '<div class="theory-body">' + body + "</div></section>";
  }

  // ── Bài tập ─────────────────────────────────────────────
  const items = []; // {el, kind, data, key}

  function exerciseHTML(ex, ei) {
    let n = 0;
    const body = ex.kind === "match" ? matchHTML(ex, ei) : ex.items.map((it, ii) => {
      n++;
      const key = ei + "_" + ii;
      const hint = it.hint ? ' <span class="hint">(' + E.esc(it.hint) + ")</span>" : "";
      const sentence = ex.kind === "write"
        ? '<div class="item-ctx">' + E.esc(it.context || "") + "</div>" +
          (it.pre ? '<div class="item-sent">' + E.esc(it.pre) + "</div>" : "") +
          '<input class="fill-inp wide" data-key="' + key + '" placeholder="Viết câu của bạn…" autocomplete="off">'
        : '<div class="item-sent">' + E.esc(it.pre || "") + ' <input class="fill-inp" data-key="' + key + '" placeholder="…" autocomplete="off"> ' + E.esc(it.suf || "") + "</div>";
      return '<div class="item" data-key="' + key + '"><div class="item-num">' + n + hint + "</div>" + sentence +
        '<div class="fb"></div><div class="sline">' + sentHTML(it) + "</div></div>";
    }).join("");
    return '<section class="ex-block"><div class="ex-head"><span class="ex-badge">' + E.esc(ex.id) + "</span><div>" +
      '<div class="ex-title">' + E.esc(ex.title) + "</div>" +
      '<div class="ex-instr">' + E.esc(ex.instr || "") + "</div>" +
      (ex.source ? '<div class="ex-src">' + E.esc(ex.source) + "</div>" : "") +
      '</div></div><div class="ex-body">' + body + "</div></section>";
  }

  // Nối câu: cả hai cột đều hiện đủ nội dung; chọn số ở cột trái.
  function matchHTML(ex, ei) {
    const opts = '<option value="">–</option>' + ex.right.map(r => '<option value="' + E.esc(r.n) + '">' + E.esc(r.n) + "</option>").join("");
    const left = ex.left.map(l =>
      '<div class="item match-item" data-key="' + ei + "_" + l.k + '"><div class="match-row"><span class="match-key">' + E.esc(l.k) + "</span>" +
      '<span class="match-txt">' + E.esc(l.en) + '</span><select class="match-sel" data-key="' + ei + "_" + l.k + '">' + opts +
      '</select><span class="match-fb"></span></div><div class="match-lines sline"></div></div>').join("");
    const right = ex.right.map(r => '<div class="match-row"><span class="match-key">' + E.esc(r.n) + '</span><span class="match-txt">' + E.esc(r.en) + "</span></div>").join("");
    return '<div class="match-grid"><div><div class="match-col-head">Câu A</div>' + left +
      '</div><div><div class="match-col-head">Câu B</div>' + right + "</div></div>";
  }

  // ── Dựng trang ──────────────────────────────────────────
  const total = U.exercises.reduce((s, ex) => s + (ex.kind === "match" ? ex.left.length : ex.items.length), 0);

  function renderExercises() {
    document.getElementById("exercises").innerHTML = U.exercises.map(exerciseHTML).join("");
    items.length = 0;
    U.exercises.forEach((ex, ei) => {
      if (ex.kind === "match") {
        ex.left.forEach(l => items.push({ kind: "match", ex, key: ei + "_" + l.k, data: l }));
      } else {
        ex.items.forEach((it, ii) => items.push({ kind: ex.kind, ex, key: ei + "_" + ii, data: it }));
      }
    });
    items.forEach(o => { o.el = document.querySelector('.item[data-key="' + o.key + '"]'); });
    // Enter → ô nhập kế tiếp
    const inputs = [...document.querySelectorAll("#exercises input.fill-inp")];
    inputs.forEach((inp, i) => inp.addEventListener("keydown", ev => {
      if (ev.key === "Enter") { ev.preventDefault(); (inputs[i + 1] || document.getElementById("btnCheck")).focus(); }
    }));
    document.getElementById("scoreCard").classList.remove("show");
  }

  app.innerHTML =
    '<nav><a class="nav-back" href="index.html">← Trang chủ</a><div class="nav-title">Unit ' + U.id + " · " + E.esc(U.title) + "</div>" +
    '<div class="nav-sub">' + U.exercises.length + " bài · " + total + " câu</div></nav>" + E.toolbarHTML() +
    '<div class="wrap">' + theoryHTML(U.theory) + '<div id="exercises"></div>' +
    '<div class="actions"><button type="button" class="btn primary" id="btnCheck">Chấm điểm</button>' +
    '<button type="button" class="btn" id="btnReset">Làm lại</button></div>' +
    '<div class="score-card" id="scoreCard"><div class="score-pct" id="scPct">—</div><div class="score-msg" id="scMsg"></div>' +
    '<div class="score-stars" id="scStars"></div><div class="score-row">' +
    '<div><div class="score-n c-ok" id="scOk">0</div><div class="score-l">Đúng</div></div>' +
    '<div><div class="score-n c-ng" id="scNg">0</div><div class="score-l">Sai</div></div>' +
    '<div><div class="score-n" id="scTot">0</div><div class="score-l">Tổng</div></div></div>' +
    '<div class="done-notice" id="scDone"></div></div></div>';
  E.bindToolbar(app);
  renderExercises();

  document.getElementById("theoryHead").addEventListener("click", () => document.getElementById("theory").classList.toggle("closed"));
  document.getElementById("btnReset").addEventListener("click", () => { renderExercises(); window.scrollTo({ top: 0, behavior: "smooth" }); });
  document.getElementById("btnCheck").addEventListener("click", check);

  function feedback(o, ok) {
    o.el.classList.add("checked");
    const fb = o.el.querySelector(".fb");
    if (!fb) return;
    fb.className = "fb " + (ok ? "ok" : "ng");
    fb.innerHTML = ok ? '<div class="fb-ans">✓ Đúng!</div>' : '<div class="fb-ans">✗ Đáp án: ' + E.esc(o.data.answer) + "</div>";
    if (o.data.exp) fb.innerHTML += '<div class="fb-exp">' + E.esc(o.data.exp) + "</div>";
  }

  function check() {
    let ok = 0;
    items.forEach(o => {
      let good;
      if (o.kind === "match") {
        const sel = o.el.querySelector("select");
        good = sel.value === o.ex.ans[o.data.k];
        sel.className = "match-sel " + (good ? "ok" : "ng");
        o.el.querySelector(".match-fb").textContent = good ? "✓" : "✗";
        o.el.classList.add("checked");
        const right = o.ex.right.find(r => r.n === o.ex.ans[o.data.k]);
        o.el.querySelector(".match-lines").innerHTML = sentHTML(o.data) + (right ? sentHTML(right, { label: "→ " + right.n + "." }) : "");
      } else {
        const inp = o.el.querySelector("input");
        good = E.isCorrect(inp.value, o.data);
        inp.className = "fill-inp" + (o.kind === "write" ? " wide " : " ") + (good ? "ok" : "ng");
        feedback(o, good);
      }
      if (good) ok++;
    });
    const pct = Math.round(ok / total * 100);
    document.getElementById("scPct").textContent = pct + "%";
    document.getElementById("scOk").textContent = ok;
    document.getElementById("scNg").textContent = total - ok;
    document.getElementById("scTot").textContent = total;
    document.getElementById("scStars").textContent = pct >= 90 ? "⭐⭐⭐" : pct >= E.PASS ? "⭐⭐" : "⭐";
    document.getElementById("scMsg").textContent = pct >= 90 ? "Xuất sắc!" : pct >= E.PASS ? "Khá tốt, xem lại các câu sai nhé." : "Cần xem lại lý thuyết rồi thử lại!";
    const done = document.getElementById("scDone");
    done.textContent = "";
    // egiu_done (mảng id) giữ nguyên định dạng cũ để index.html đọc được
    if (pct >= E.PASS) {
      const d = E.store.get("egiu_done", []);
      if (d.indexOf(U.id) === -1) { d.push(U.id); E.store.set("egiu_done", d); }
      done.textContent = "✓ Đã lưu tiến độ Unit " + U.id + "!";
    }
    const sc = E.store.get("egiu_scores", {});
    sc[U.id] = { pct: pct, ts: Date.now(), best: Math.max(pct, (sc[U.id] || {}).best || 0) };
    E.store.set("egiu_scores", sc);
    const card = document.getElementById("scoreCard");
    card.classList.add("show");
    card.scrollIntoView({ behavior: "smooth", block: "center" });
  }
})();
