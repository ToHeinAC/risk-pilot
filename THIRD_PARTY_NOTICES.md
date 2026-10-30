# Third-party notices

Code or text copied into this repository from other projects, with source and license. Dependencies
installed through `uv` are not listed here; their licenses ship with the packages.

Add one section per source:

```
## <project>
- Used in: <files>
- Source: <URL>
- License: <SPDX id>, plus the license text if it requires reproduction
```

## Vue Flow and its bundled dependencies

- Used in: `src/app/web/canvas/lib/vueflow.js` (one ESM bundle, `vue` external) and
  `src/app/web/canvas/lib/vueflow.css`; the canvas of the model page (M9).
- Source: <https://github.com/bcakmakoglu/vue-flow> (`@vue-flow/core` 1.48.2), with
  `@vueuse/core` and `@vueuse/shared` 10.11.1 and `d3-color`, `d3-dispatch`, `d3-drag`,
  `d3-ease`, `d3-interpolate`, `d3-selection`, `d3-timer`, `d3-transition`, `d3-zoom` (d3 v3).
- License: MIT (Vue Flow, VueUse), ISC (d3 modules), BSD-3-Clause (`d3-ease`); full texts in
  `src/app/web/canvas/lib/LICENSES.txt`.
- Built, unmodified, with `npm install @vue-flow/core@1.48.2 vue esbuild@0.24.2`, an entry
  `export * from '@vue-flow/core';` and `esbuild entry.js --bundle --format=esm --external:vue
  --minify --outfile=vueflow.js`; the CSS is `dist/style.css` followed by
  `dist/theme-default.css`. The pre-commit hooks skip `src/app/web/canvas/lib/` so the files stay
  byte-identical.
