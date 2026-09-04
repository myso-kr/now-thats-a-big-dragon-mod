'use strict';

// Adds a language to the game's own language list, so it appears in the settings
// screen as one more flag to click.
//
// This is a different job from merging a translation into a table (i18n.js). Here we
// are editing the game's *list* of languages in four places:
//
//   resources   the i18next bundle, `{en:{…},fr:{…},…}`
//   supported   `["en","fr","de","pt","tr"]`, which the settings UI maps over
//   flags       `{en:"us.png",…}`, the image for each code
//   labels      `languages:{en:"English",…}` inside every locale's settings namespace
//
// The flag list the UI renders is derived from the supported array, so adding a code
// there and a file here is enough for the button to appear.
//
// Every edit is optional and reported separately. If any of them fails the caller can
// fall back to overwriting `en`, which needs only the resources anchor — a game update
// that moves the settings UI then costs the settings integration, not the translation.
// Mirrors src/patch/locale.rs.

const { scanBalanced } = require('./scan');

/** `["en","fr","de","pt","tr"]` — the codes the settings screen offers. */
const SUPPORTED_PATTERN = /\["en","fr","de","pt","tr"\]/;

/** `{en:"us.png",fr:"fr.png",…}` — the flag image for each code. */
const FLAGS_PATTERN = /\{en:"us\.png",fr:"fr\.png",de:"de\.png",pt:"br\.png",tr:"tr\.png"\}/;

/** `languages:{en:"English",…}` — one per locale, so every UI language can name ours. */
const LABELS_PATTERN = /languages:\{en:"[^"]*",fr:"[^"]*",de:"[^"]*",pt:"[^"]*",tr:"[^"]*"\}/g;

/** The i18next init, which has no `fallbackLng` of its own. */
const INIT_PATTERN = /\.init\(\{resources:([A-Za-z0-9_$]+),lng:([A-Za-z0-9_$]+),/;

/**
 * Insert a whole locale into the i18next resources object.
 *
 * The tables have to be merged over English already: the game does not set
 * `fallbackLng`, so a key missing from our locale renders as the key itself rather
 * than falling back to the original text.
 */
function addLocale(src, lang, tables) {
  // The resources object is the one whose `en` entry holds every namespace. Finding
  // it by that shape rather than by its minified name is what survives a rebuild.
  const m = /en:\{upgrades:[A-Za-z0-9_$]+,common:[A-Za-z0-9_$]+/.exec(src);
  if (!m) return { ok: false, reason: 'resources object not found' };
  const insert = `${JSON.stringify(lang)}:${JSON.stringify(tables)},`;
  return {
    ok: true,
    code: src.slice(0, m.index) + insert + src.slice(m.index),
  };
}

/** Add the code to the list the settings screen offers. */
function addSupported(src, lang) {
  const m = SUPPORTED_PATTERN.exec(src);
  if (!m) return { ok: false, reason: 'supported-language list not found' };
  const replaced = `${m[0].slice(0, -1)},${JSON.stringify(lang)}]`;
  return { ok: true, code: src.slice(0, m.index) + replaced + src.slice(m.index + m[0].length) };
}

/** Name the flag image for the code. The file is served by the launcher. */
function addFlag(src, lang, file) {
  const m = FLAGS_PATTERN.exec(src);
  if (!m) return { ok: false, reason: 'flag map not found' };
  const replaced = `${m[0].slice(0, -1)},${JSON.stringify(lang)}:${JSON.stringify(file)}}`;
  return { ok: true, code: src.slice(0, m.index) + replaced + src.slice(m.index + m[0].length) };
}

/**
 * Add our language's name to every locale's list of language names, so the button has
 * a label whichever language the UI is in.
 *
 * The same name is used in all of them: a language is best named in itself, and
 * "한국어" is more use to a French player than "Coréen" would be to a Korean one.
 */
function addLabels(src, lang, label) {
  LABELS_PATTERN.lastIndex = 0;
  let count = 0;
  const code = src.replace(LABELS_PATTERN, (whole) => {
    count += 1;
    return `${whole.slice(0, -1)},${JSON.stringify(lang)}:${JSON.stringify(label)}}`;
  });
  return { ok: count > 0, code, count };
}

// `{en:new X.Scale({seconds:1,…}),fr:…}` — the unit names printed in "5.28 minutes".
// They are not in the i18n tables; each language has its own Scale, keyed by code,
// and the keys themselves are what gets printed.
// The `en:` key is part of the match so the insertion point is the start of an
// entry, not an offset counted backwards from one.
const SCALE_PATTERN =
  /en:new ([A-Za-z0-9_$]+)\.Scale\(\{seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3\}\)/;

const TIME_UNITS = ['seconds', 'minutes', 'hours', 'days', 'months', 'years'];
const TIME_VALUES = ['1', '60', '3600', '86400', '2592e3', '31536e3'];

/**
 * Give the new language its own time-unit Scale.
 *
 * The game looks these up as `Fj[lang] ?? Fj.en`, so a language without one simply
 * shows English units — which is why this is added rather than the English entry
 * being overwritten. Overwriting would put Korean units in front of English players.
 *
 * The Scale constructor's minified name is read out of the anchor itself, so nothing
 * here depends on knowing what a rebuild called it.
 */
function addTimeScale(src, lang, labels) {
  if (!Array.isArray(labels) || labels.length !== TIME_UNITS.length
      || labels.some((l) => typeof l !== 'string' || !l)) {
    return { ok: false, reason: 'incomplete unit names' };
  }
  const m = SCALE_PATTERN.exec(src);
  if (!m) return { ok: false, reason: 'time scale not found' };

  const ctor = m[1];
  const units = labels.map((l, i) => `${JSON.stringify(l)}:${TIME_VALUES[i]}`).join(',');
  const entry = `${JSON.stringify(lang)}:new ${ctor}.Scale({${units}}),`;
  return { ok: true, code: src.slice(0, m.index) + entry + src.slice(m.index) };
}

// The default settings object, which applies only until the player saves a choice.
const DEFAULT_LANGUAGE_PATTERN = /(chromaticAberration:\d+,largerTextSize:!\d,language:)"en"/;

/**
 * Make our language the one a fresh profile starts in.
 *
 * This is the default, not an override: the moment the player picks a language in the
 * settings screen the game persists that, and the persisted value wins from then on.
 * So the system's language decides where to start, and the player decides after that.
 */
function setDefaultLanguage(src, lang) {
  const m = DEFAULT_LANGUAGE_PATTERN.exec(src);
  if (!m) return { ok: false, reason: 'default settings not found' };
  return {
    ok: true,
    code: src.slice(0, m.index) + m[1] + JSON.stringify(lang)
      + src.slice(m.index + m[0].length),
  };
}

/**
 * Give i18next a fallback language.
 *
 * The game sets none, so i18next falls back to its own default of `dev` — and a key
 * missing from the selected locale renders as the key itself. That is what a player
 * sees if their saved language is one this build does not carry: a screen of
 * `TABS.TROOPS` and `smallDragon`. Falling back to English is always readable.
 */
function setFallback(src, lang) {
  const m = INIT_PATTERN.exec(src);
  if (!m) return { ok: false, reason: 'i18next init not found' };
  const at = m.index + m[0].length;
  return { ok: true, code: `${src.slice(0, at)}fallbackLng:${JSON.stringify(lang)},${src.slice(at)}` };
}

/**
 * Add every language at once.
 *
 * They have to go in together: each anchor is matched by the shape the game shipped,
 * and adding one language changes that shape. Doing them one at a time would find the
 * anchor once and miss it for everyone after.
 *
 * All of them are added, not just the one being selected — the settings screen is a
 * list, and a player whose saved choice is missing from it gets untranslated keys.
 *
 * `defaultLang` is the one a fresh profile starts in. It is only a default: the
 * moment the player picks a language the game persists that, and the persisted value
 * wins from then on.
 */
function addLanguages(src, langs, defaultLang) {
  const report = {
    langs: langs.map((l) => l.lang),
    resources: 0,
    supported: false,
    flag: false,
    labels: 0,
    timeScale: 0,
    fallback: false,
    default: false,
  };
  let code = src;

  for (const l of langs) {
    const r = addLocale(code, l.lang, l.tables);
    if (!r.ok) return { code: src, report, reason: r.reason };
    code = r.code;
    report.resources += 1;
  }

  const sup = SUPPORTED_PATTERN.exec(code);
  if (sup) {
    const codes = langs.map((l) => JSON.stringify(l.lang)).join(',');
    code = code.slice(0, sup.index) + `${sup[0].slice(0, -1)},${codes}]`
      + code.slice(sup.index + sup[0].length);
    report.supported = true;
  }

  const flags = FLAGS_PATTERN.exec(code);
  if (flags) {
    const entries = langs
      .map((l) => `${JSON.stringify(l.lang)}:${JSON.stringify(l.flagFile)}`).join(',');
    code = code.slice(0, flags.index) + `${flags[0].slice(0, -1)},${entries}}`
      + code.slice(flags.index + flags[0].length);
    report.flag = true;
  }

  LABELS_PATTERN.lastIndex = 0;
  code = code.replace(LABELS_PATTERN, (whole) => {
    report.labels += 1;
    const entries = langs
      .map((l) => `${JSON.stringify(l.lang)}:${JSON.stringify(l.label)}`).join(',');
    return `${whole.slice(0, -1)},${entries}}`;
  });

  for (const l of langs) {
    const scale = addTimeScale(code, l.lang, l.units);
    if (scale.ok) { code = scale.code; report.timeScale += 1; }
  }

  const fb = setFallback(code, 'en');
  if (fb.ok) { code = fb.code; report.fallback = true; }

  if (defaultLang) {
    const d = setDefaultLanguage(code, defaultLang);
    if (d.ok) { code = d.code; report.default = true; }
  }

  return { code, report };
}

/**
 * Everything needed for one language to appear in the settings screen.
 *
 * Returns the patched source plus what actually happened, anchor by anchor. The
 * caller decides what an incomplete result means.
 */
function addLanguage(src, { lang, label, flagFile, tables, units }) {
  const report = {
    lang,
    resources: false,
    supported: false,
    flag: false,
    labels: 0,
    timeScale: false,
    default: false,
  };
  let code = src;

  const res = addLocale(code, lang, tables);
  if (!res.ok) return { code, report, reason: res.reason };
  code = res.code;
  report.resources = true;

  const sup = addSupported(code, lang);
  if (sup.ok) { code = sup.code; report.supported = true; }

  const flag = addFlag(code, lang, flagFile);
  if (flag.ok) { code = flag.code; report.flag = true; }

  const labels = addLabels(code, lang, label);
  if (labels.ok) { code = labels.code; report.labels = labels.count; }

  const scale = addTimeScale(code, lang, units);
  if (scale.ok) { code = scale.code; report.timeScale = true; }

  const dflt = setDefaultLanguage(code, lang);
  if (dflt.ok) { code = dflt.code; report.default = true; }

  return { code, report };
}

module.exports = {
  addLocale,
  addLanguages,
  setFallback,
  INIT_PATTERN,
  setDefaultLanguage,
  DEFAULT_LANGUAGE_PATTERN,
  addTimeScale,
  addSupported,
  addFlag,
  addLabels,
  addLanguage,
  SUPPORTED_PATTERN,
  FLAGS_PATTERN,
  LABELS_PATTERN,
  scanBalanced,
};
