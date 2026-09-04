'use strict';

// Which language to patch in, and why.
//
// The game ships en/fr/de/pt/tr and picks one from the system locale itself.
// Anything else falls back to `en` — which is the slot this mod overwrites. So a
// language is only patched in when the game does not already have it, and the
// system's own choice is what decides.
//
// This module does no I/O and knows nothing about the game: it takes the catalogue
// and a locale and returns a decision. (lib/language.test.js)

/** `ko_KR.UTF-8` becomes `ko-kr`. Locales arrive in several shapes. */
function normalise(locale) {
  if (typeof locale !== 'string') return '';
  return locale
    .trim()
    .split('.')[0] // drop any encoding suffix
    .replace(/_/g, '-')
    .toLowerCase();
}

/** The primary subtag: `zh-hant-tw` becomes `zh`. */
const primary = (locale) => normalise(locale).split('-')[0];

/**
 * The language whose `matches` best fits this locale, or null.
 * Longer prefixes win, so `zh-hant` beats `zh` for `zh-Hant-TW`.
 */
function match(catalogue, locale) {
  const want = normalise(locale);
  if (!want) return null;
  let best = null;
  for (const [lang, def] of Object.entries(catalogue.languages || {})) {
    for (const prefix of def.matches || []) {
      const p = normalise(prefix);
      if (want !== p && !want.startsWith(`${p}-`)) continue;
      if (!best || p.length > best.length) best = { lang, length: p.length };
    }
  }
  return best ? best.lang : null;
}

/**
 * Decide what to apply.
 *
 * @param catalogue        locale/languages.json
 * @param opts.requested   an explicit choice (--lang, or an environment variable)
 * @param opts.locale      the system locale
 * @param opts.available   the languages we actually have files for
 * @returns {{lang: string|null, reason: string}}
 */
function resolve(catalogue, opts) {
  const available = opts.available || [];
  const supported = catalogue.gameSupports || [];

  // An explicit choice is taken at face value, including one the game already
  // supports — asking for it is a deliberate override.
  if (opts.requested) {
    const want = normalise(opts.requested);
    // An exact code first: `zh-Hans` must not be reduced to `zh`, which is a
    // different language as far as this catalogue is concerned.
    let lang = available.find((a) => normalise(a) === want);
    // Otherwise treat it as a locale, so `ko-KR` and `zh-Hant-TW` also work.
    if (!lang) {
      const hit = match(catalogue, opts.requested);
      if (hit && available.includes(hit)) lang = hit;
    }
    if (lang) return { lang, reason: `requested: ${opts.requested}` };
    const have = available.join(', ') || 'none';
    return { lang: null, reason: `no translation for ${opts.requested} (have: ${have})` };
  }

  const hit = match(catalogue, opts.locale);
  if (!hit) {
    return { lang: null, reason: `no translation for the system locale (${opts.locale || 'unknown'})` };
  }
  // The game already speaks this one; ours would only get in the way.
  if (supported.includes(hit)) {
    return { lang: null, reason: `the game supports ${hit} natively` };
  }
  if (!available.includes(hit)) {
    return { lang: null, reason: `no ${hit} translation files are present` };
  }
  return { lang: hit, reason: `system locale: ${opts.locale}` };
}

module.exports = { normalise, primary, match, resolve };
