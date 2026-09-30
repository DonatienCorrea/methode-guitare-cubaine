/* =========================================================================
   metronome.js — boîte à rythme de la section 7
   -------------------------------------------------------------------------
   Deux principes gouvernent ce fichier :

   1. On n'ordonnance PAS le son avec setInterval. Les timers du navigateur
      dérivent de plusieurs millisecondes et sont étranglés dès que l'onglet
      passe en arrière-plan ; sur un outil dont le seul rôle est la précision,
      c'est rédhibitoire. On utilise le patron « deux horloges » : un timer
      grossier réveille l'ordonnanceur toutes les 25 ms, et celui-ci programme
      les événements 100 ms à l'avance sur l'horloge de l'AudioContext, qui est
      échantillonnée et ne dérive pas.

   2. Aucun fichier audio. Les sons sont synthétisés : rien à télécharger,
      rien à licencier, rien qui puisse renvoyer un 404 dans cinq ans.
   ========================================================================= */
(function () {
  "use strict";

  var root = document.getElementById("metro");
  if (!root || !(window.AudioContext || window.webkitAudioContext)) return;

  /* ------------------------------------------------------------- motifs
     16 cases = deux mesures de 4/4 découpées en croches.
     Les positions suivent la représentation standard à 16 pulsations :
       son 3-2    X..X..X...X.X...
       rumba 3-2  X..X...X..X.X...
     La rumba ne diffère du son que par sa troisième frappe, qui glisse du
     temps 4 au « et » du 4. C'est tout, et ça change tout.                */
  var PATTERNS = {
    pulse:     { hits: [0, 2, 4, 6, 8, 10, 12, 14], voice: "click",
                 label: "Une frappe par temps — la pulsation nue." },
    croches:   { hits: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], voice: "click",
                 label: "Huit croches par mesure : « un et deux et trois et quatre et »." },
    son32:     { hits: [0, 3, 6, 10, 12], voice: "clave",
                 label: "Clave son 3-2 · cinq frappes sur deux mesures." },
    son23:     { hits: [2, 4, 8, 11, 14], voice: "clave",
                 label: "Clave son 2-3 · le même motif, l'autre moitié en premier." },
    rumba32:   { hits: [0, 3, 7, 10, 12], voice: "clave",
                 label: "Clave rumba 3-2 · la troisième frappe tombe sur le « et » du 4." },
    tresillo:  { hits: [0, 3, 6, 8, 11, 14], voice: "clave",
                 label: "Tresillo · 3+3+2, la cellule mère du rythme cubain." },
    cinquillo: { hits: [0, 2, 3, 5, 6, 8, 10, 11, 13, 14], voice: "clave",
                 label: "Cinquillo · cinq frappes par mesure, le tresillo ornementé." }
  };

  // Attention : les 16 cases couvrent DEUX mesures. Les temps 2 et 4 tombent
  // donc sur 2 et 6 dans la première mesure, 10 et 14 dans la seconde.
  var BACKBEAT = [2, 6, 10, 14];
  var QUARTERS = [0, 2, 4, 6, 8, 10, 12, 14];

  /* -------------------------------------------------------------- état */
  var S = {
    bpm: 80,
    pattern: "son32",
    bg: "quarter",                     // none | quarter | backbeat
    ramp: false,
    playing: false,
    step: 0,                           // 0..15
    bars: 0,
    nextTime: 0
  };

  var LOOKAHEAD = 25;                  // ms, réveil du timer
  var HORIZON = 0.1;                   // s, fenêtre de programmation
  var ctx = null, master = null, timer = null, raf = null;
  var queue = [];                      // {step, time} pour la synchro visuelle

  /* -------------------------------------------------------------- DOM */
  var el = {
    grid:    document.getElementById("metro-grid"),
    legend:  document.getElementById("metro-legend"),
    play:    document.getElementById("m-play"),
    bpm:     document.getElementById("m-bpm"),
    bpmOut:  document.getElementById("m-bpm-out"),
    tap:     document.getElementById("m-tap"),
    bars:    document.getElementById("m-bars"),
    ramp:    document.getElementById("m-ramp"),
    pulseOpt: document.getElementById("m-pulse-opt")
  };
  var cells = Array.prototype.slice.call(el.grid.querySelectorAll(".c"));
  var patBtns = Array.prototype.slice.call(root.querySelectorAll("[data-p]"));
  var bgBtns  = Array.prototype.slice.call(root.querySelectorAll("[data-bg]"));

  /* ------------------------------------------------------------- audio */
  function audio() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      master = ctx.createGain();
      master.gain.value = 0.9;
      master.connect(ctx.destination);
    }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }

  // La clave est un bois : très aigu, très bref, sans queue. Deux partiels
  // non harmoniques suffisent à en donner l'illusion.
  function clave(t, gain) {
    [2500, 3730].forEach(function (f, i) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = "triangle";
      o.frequency.setValueAtTime(f, t);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(gain * (i ? 0.35 : 1), t + 0.001);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.045);
      o.connect(g); g.connect(master);
      o.start(t); o.stop(t + 0.06);
    });
  }

  function click(t, gain, accent) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.type = "sine";
    o.frequency.setValueAtTime(accent ? 1600 : 1000, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + 0.001);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.035);
    o.connect(g); g.connect(master);
    o.start(t); o.stop(t + 0.05);
  }

  /* ------------------------------------------------------- ordonnanceur */
  function stepDuration() { return 30 / S.bpm; }   // une croche = ½ temps

  function bgHits() {
    if (S.bg === "none" || S.pattern === "pulse" || S.pattern === "croches") return [];
    return S.bg === "backbeat" ? BACKBEAT : QUARTERS;
  }

  function schedule(step, t) {
    var p = PATTERNS[S.pattern];
    var bg = bgHits();
    if (bg.indexOf(step) !== -1) click(t, 0.18, false);
    if (p.hits.indexOf(step) !== -1) {
      if (p.voice === "clave") clave(t, 0.5);
      else click(t, 0.5, step === 0 || step === 8);
    }
  }

  function advance() {
    S.nextTime += stepDuration();
    S.step = (S.step + 1) % 16;
    if (S.step === 0 || S.step === 8) {
      S.bars++;
      el.bars.textContent = S.bars;
      if (S.ramp && S.bars % 4 === 0 && S.bpm < 208) setBpm(Math.min(208, S.bpm + 4));
    }
  }

  function tick() {
    while (S.nextTime < ctx.currentTime + HORIZON) {
      schedule(S.step, S.nextTime);
      queue.push({ step: S.step, time: S.nextTime });
      advance();
    }
  }

  /* ---------------------------------------------------- synchro visuelle */
  function draw() {
    var now = ctx ? ctx.currentTime : 0, cur = -1;
    while (queue.length && queue[0].time <= now) cur = queue.shift().step;
    if (cur !== -1) {
      cells.forEach(function (c, i) { c.classList.toggle("on", i === cur); });
    }
    raf = requestAnimationFrame(draw);
  }

  /* ------------------------------------------------------- commandes */
  function start() {
    audio();
    S.step = 0; S.bars = 0; queue = [];
    el.bars.textContent = "0";
    S.nextTime = ctx.currentTime + 0.08;
    S.playing = true;
    el.play.setAttribute("aria-pressed", "true");
    el.play.querySelector(".m-ico").innerHTML = "&#9632;";
    el.play.querySelector(".m-lab").textContent = "Arrêter";
    root.classList.add("playing");
    timer = setInterval(tick, LOOKAHEAD);   // réveille l'ordonnanceur, ne sonne pas
    tick();
    raf = requestAnimationFrame(draw);
  }

  function stop() {
    S.playing = false;
    clearInterval(timer); timer = null;
    cancelAnimationFrame(raf); raf = null;
    queue = [];
    el.play.setAttribute("aria-pressed", "false");
    el.play.querySelector(".m-ico").innerHTML = "&#9654;";
    el.play.querySelector(".m-lab").textContent = "Lancer";
    root.classList.remove("playing");
    cells.forEach(function (c) { c.classList.remove("on"); });
  }

  function toggle() { S.playing ? stop() : start(); }

  function setBpm(v) {
    S.bpm = Math.max(40, Math.min(208, Math.round(v)));
    el.bpm.value = S.bpm;
    el.bpmOut.textContent = S.bpm + " BPM";
    save();
  }

  function paint() {
    var p = PATTERNS[S.pattern];
    cells.forEach(function (c, i) {
      c.classList.toggle("hit", p.hits.indexOf(i) !== -1);
    });
    el.legend.textContent = p.label;
    var off = (S.pattern === "pulse" || S.pattern === "croches");
    el.pulseOpt.classList.toggle("off", off);
    bgBtns.forEach(function (b) { b.disabled = off; });
  }

  function setPattern(name) {
    if (!PATTERNS[name]) return;
    S.pattern = name;
    patBtns.forEach(function (b) {
      b.setAttribute("aria-checked", b.dataset.p === name ? "true" : "false");
    });
    paint(); save();
  }

  function setBg(v) {
    S.bg = v;
    bgBtns.forEach(function (b) {
      b.setAttribute("aria-checked", b.dataset.bg === v ? "true" : "false");
    });
    save();
  }

  /* ------------------------------------------------------ persistance */
  function save() {
    try {
      localStorage.setItem("metro", JSON.stringify(
        { bpm: S.bpm, pattern: S.pattern, bg: S.bg }));
    } catch (e) { /* mode privé : tant pis, ce n'est qu'un confort */ }
  }
  function load() {
    try {
      var d = JSON.parse(localStorage.getItem("metro") || "{}");
      if (d.bpm) setBpm(d.bpm);
      if (d.pattern) setPattern(d.pattern);
      if (d.bg) setBg(d.bg);
    } catch (e) { /* ignoré */ }
  }

  /* ----------------------------------------------------------- tap tempo */
  var taps = [];
  function tap() {
    var now = performance.now();
    taps = taps.filter(function (t) { return now - t < 2500; });
    taps.push(now);
    if (taps.length < 2) return;
    var sum = 0;
    for (var i = 1; i < taps.length; i++) sum += taps[i] - taps[i - 1];
    setBpm(60000 / (sum / (taps.length - 1)));
  }

  /* -------------------------------------------------------- événements */
  el.play.addEventListener("click", toggle);
  el.tap.addEventListener("click", tap);
  el.bpm.addEventListener("input", function () { setBpm(this.value); });
  el.ramp.addEventListener("click", function () {
    S.ramp = !S.ramp;
    this.setAttribute("aria-pressed", S.ramp ? "true" : "false");
  });
  patBtns.forEach(function (b) {
    b.addEventListener("click", function () { setPattern(b.dataset.p); });
  });
  bgBtns.forEach(function (b) {
    b.addEventListener("click", function () { if (!b.disabled) setBg(b.dataset.bg); });
  });

  // Espace lance et arrête, sauf si le focus est déjà sur une commande.
  root.addEventListener("keydown", function (e) {
    if (e.key !== " " && e.key !== "Spacebar") return;
    var t = e.target.tagName;
    if (t === "BUTTON" || t === "INPUT") return;
    e.preventDefault(); toggle();
  });
  root.setAttribute("tabindex", "0");

  // Un métronome qu'on laisse tourner en quittant la page est une nuisance.
  document.addEventListener("visibilitychange", function () {
    if (document.hidden && S.playing) stop();
  });

  paint(); setBpm(S.bpm); setBg(S.bg); load();
})();
