/* =========================================================================
   tests/metronome.test.js — banc d'essai de src/js/metronome.js
   -------------------------------------------------------------------------
   Lancement :  node tests/metronome.test.js
   Sortie 0 si tout passe, 1 sinon.

   Pourquoi un faux DOM plutôt qu'un vrai navigateur : l'ordonnanceur audio
   est la partie du code où une erreur ne se voit pas (elle s'entend, trois
   minutes plus tard, sous forme de décalage). Une horloge que l'on pilote à
   la main permet de vérifier la régularité au milliardième de seconde, ce
   qu'aucune écoute ne ferait. Le rendu visuel, lui, reste à contrôler à l'œil.
   ========================================================================= */
const fs = require('fs');

function El(tag, attrs = {}) {
  const e = {
    tagName: tag.toUpperCase(), dataset: {}, disabled: false, value: "",
    textContent: "", innerHTML: "", children: [], _attr: {}, _cls: new Set(),
    _ev: {},
    classList: {
      add: c => e._cls.add(c), remove: c => e._cls.delete(c),
      contains: c => e._cls.has(c),
      toggle: (c, f) => { if (f === undefined) f = !e._cls.has(c); f ? e._cls.add(c) : e._cls.delete(c); return f; }
    },
    setAttribute: (k, v) => { e._attr[k] = String(v); },
    getAttribute: k => e._attr[k],
    addEventListener: (n, fn) => { (e._ev[n] = e._ev[n] || []).push(fn); },
    fire: (n, ev = {}) => (e._ev[n] || []).forEach(fn => fn.call(e, Object.assign({ target: e, preventDefault() {} }, ev))),
    querySelector: s => e.children.find(c => c._sel === s) || null,
    querySelectorAll: s => e.children.filter(c => (c._sel === s) || (s === '.c' && c._cls.has('c')) ||
                                                  (s === '[data-p]' && c.dataset.p) || (s === '[data-bg]' && c.dataset.bg)),
    focus() {}
  };
  Object.assign(e, attrs);
  return e;
}

// --- structure du widget, calquée sur src/widgets/metronome.html
const cells = [];
const HITS0 = [0, 3, 6, 10, 12];
for (let i = 0; i < 16; i++) {
  const c = El('li'); c._cls.add('c'); c.dataset.i = String(i);
  if (HITS0.includes(i)) c._cls.add('hit');
  cells.push(c);
}
const grid = El('ol'); grid.children = cells;
const ico = El('span'); ico._sel = '.m-ico';
const lab = El('span'); lab._sel = '.m-lab';
const play = El('button'); play.children = [ico, lab];
const patBtns = ['pulse','croches','son32','son23','rumba32','tresillo','cinquillo']
  .map(p => { const b = El('button'); b.dataset.p = p; b.setAttribute('aria-checked', p === 'son32'); return b; });
const bgBtns = ['none','quarter','backbeat']
  .map(v => { const b = El('button'); b.dataset.bg = v; b.setAttribute('aria-checked', v === 'quarter'); return b; });
const root = El('div'); root.children = [...patBtns, ...bgBtns];

const byId = {
  'metro': root, 'metro-grid': grid, 'metro-legend': El('p'), 'm-play': play,
  'm-bpm': El('input', { value: '80' }), 'm-bpm-out': El('output'),
  'm-tap': El('button'), 'm-bars': El('b'), 'm-ramp': El('button'),
  'm-pulse-opt': El('div')
};

// --- fausse horloge audio : je la fais avancer à la main
let CLOCK = 0;
const played = [];               // {t, kind}
const node = () => ({ type:'', frequency:{setValueAtTime(){}}, gain:{setValueAtTime(){},exponentialRampToValueAtTime(){}},
                      connect(){}, start(){}, stop(){} });
class FakeCtx {
  constructor() { this.destination = {}; this.state = 'running'; }
  get currentTime() { return CLOCK; }
  resume() { this.state = 'running'; }
  createGain() { return node(); }
  createOscillator() { return node(); }
}

// --- globaux
global.window = { AudioContext: FakeCtx };
global.document = {
  getElementById: id => byId[id] || null,
  addEventListener() {}, hidden: false
};
global.localStorage = { _d: {}, getItem(k){return this._d[k]||null;}, setItem(k,v){this._d[k]=v;} };
global.performance = { now: () => PERF };
let PERF = 0;
let rafCb = null;
global.requestAnimationFrame = cb => { rafCb = cb; return 1; };
global.cancelAnimationFrame = () => { rafCb = null; };
let intervalCb = null;
global.setInterval = cb => { intervalCb = cb; return 1; };
global.clearInterval = () => { intervalCb = null; };

// --- on espionne les sons en interceptant createOscillator
const origOsc = FakeCtx.prototype.createOscillator;
FakeCtx.prototype.createOscillator = function () {
  const o = origOsc.call(this);
  o.frequency.setValueAtTime = (f, t) => played.push({ t: +t.toFixed(6), f });
  return o;
};

const TARGET = process.argv[2] ||
  require('path').join(__dirname, '..', 'src', 'js', 'metronome.js');
eval(fs.readFileSync(TARGET, 'utf8'));

/* ============================== assertions ============================== */
let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✓ ' + name); }
  else { fail++; console.log('  ✗ ' + name + (extra ? '  → ' + extra : '')); }
}
const hits = () => cells.map((c,i) => c._cls.has('hit') ? i : -1).filter(i => i >= 0);

console.log('\n— initialisation —');
ok('motif par défaut = clave son 3-2', JSON.stringify(hits()) === JSON.stringify(HITS0), hits());
ok('tempo affiché', byId['m-bpm-out'].textContent === '80\u00a0BPM', byId['m-bpm-out'].textContent);

console.log('\n— lecture —');
play.fire('click');
ok('bouton passé en pressé', play.getAttribute('aria-pressed') === 'true');
ok('classe playing posée', root._cls.has('playing'));
ok('ordonnanceur armé', intervalCb !== null);
ok('libellé changé', lab.textContent === 'Arrêter', lab.textContent);

// on avance l'horloge de 6 s = un cycle complet à 80 BPM
played.length = 0;
const t0 = CLOCK;
for (let k = 0; k < 400; k++) { CLOCK += 0.015; intervalCb(); }
const claveHits = played.filter(p => p.f === 2500).map(p => p.t);
const clicks    = played.filter(p => p.f === 1000 || p.f === 1600).map(p => p.t);
const step = 30 / 80;
// positions attendues sur les 2 premiers cycles
const expected = [];
for (let cyc = 0; cyc < 2; cyc++) HITS0.forEach(h => expected.push(h));
ok('la clave sonne 5 fois par cycle',
   Math.abs(claveHits.length / (CLOCK - t0) - 5 / (16 * step)) < 0.2,
   claveHits.length + ' frappes en ' + (CLOCK - t0).toFixed(1) + ' s');
ok('pulsation de fond = 8 clics par cycle',
   Math.abs(clicks.length / (CLOCK - t0) - 8 / (16 * step)) < 0.3,
   clicks.length + ' clics');
// régularité : les intervalles entre clics de pulsation doivent être constants
clicks.sort((a,b)=>a-b);
const gaps = clicks.slice(1).map((v,i) => +(v - clicks[i]).toFixed(6));
const uniq = [...new Set(gaps)];
ok('aucune dérive : intervalle de pulsation constant',
   uniq.length === 1 && Math.abs(uniq[0] - 2 * step) < 1e-9, JSON.stringify(uniq));
ok('compteur de mesures cohérent',
   Math.abs(+byId['m-bars'].textContent - (CLOCK - t0) / (8 * step)) <= 1.5,
   byId['m-bars'].textContent);

console.log('\n— motifs —');
patBtns[4].fire('click');                        // rumba 3-2
ok('rumba 3-2 = [0,3,7,10,12]', JSON.stringify(hits()) === JSON.stringify([0,3,7,10,12]), hits());
ok('radio coché exclusif',
   patBtns.filter(b => b.getAttribute('aria-checked') === 'true').length === 1);
patBtns[0].fire('click');                        // pulsation
ok('pulsation = les 8 temps', JSON.stringify(hits()) === JSON.stringify([0,2,4,6,8,10,12,14]), hits());
ok('pulsation de fond désactivée sur ce motif', bgBtns.every(b => b.disabled === true));
patBtns[2].fire('click');
ok('retour clave : fond réactivé', bgBtns.every(b => b.disabled === false));

console.log('\n— mode 2 et 4 —');
bgBtns[2].fire('click');
played.length = 0;
const t1 = CLOCK;
for (let k = 0; k < 400; k++) { CLOCK += 0.015; intervalCb(); }
const c2 = played.filter(p => p.f === 1000 || p.f === 1600).map(p => p.t).sort((a,b)=>a-b);
const g2 = [...new Set(c2.slice(1).map((v,i) => +(v - c2[i]).toFixed(6)))];
ok('deux clics par mesure au lieu de quatre',
   Math.abs(c2.length / (CLOCK - t1) - 2 / (8 * step)) < 0.2, c2.length + ' clics');
ok('espacés d\'une demi-mesure', g2.length === 1 && Math.abs(g2[0] - 4 * step) < 1e-9, JSON.stringify(g2));

console.log('\n— tap tempo —');
byId['m-tap'].fire('click'); PERF += 500;
byId['m-tap'].fire('click'); PERF += 500;
byId['m-tap'].fire('click'); PERF += 500;
byId['m-tap'].fire('click');
ok('4 taps à 500 ms → 120 BPM', byId['m-bpm-out'].textContent === '120\u00a0BPM', byId['m-bpm-out'].textContent);

console.log('\n— accélération progressive —');
byId['m-ramp'].fire('click');
ok('bascule pressée', byId['m-ramp'].getAttribute('aria-pressed') === 'true');
play.fire('click'); play.fire('click');            // stop puis relance (remet les compteurs)
const before = 120;
for (let k = 0; k < 1200; k++) { CLOCK += 0.015; intervalCb(); }
const after = parseInt(byId['m-bpm-out'].textContent);
ok('le tempo a monté', after > before, before + ' → ' + after);
ok('+4 BPM par tranche de 4 mesures', (after - before) % 4 === 0, 'delta ' + (after - before));
ok('plafonné à 208', after <= 208, String(after));

console.log('\n— arrêt —');
play.fire('click');
ok('ordonnanceur désarmé', intervalCb === null);
ok('aucune cellule allumée', cells.every(c => !c._cls.has('on')));
ok('classe playing retirée', !root._cls.has('playing'));

console.log('\n— persistance —');
ok('état sauvegardé', !!localStorage.getItem('metro'), localStorage.getItem('metro'));

console.log('\n' + (fail ? '✗ ' + fail + ' échec(s), ' : '✓ ') + pass + ' assertions passées\n');
process.exit(fail ? 1 : 0);
