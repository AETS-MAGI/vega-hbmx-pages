# vega-hbmx-pages

GitHub Pages repository for the public HTML materials of the Vega HBM / gfx900 investigation.

## Published site

- Root: https://aets-magi.github.io/vega-hbmx-pages/

## Contents

- `index.html`
	- Landing page for the published materials.
- `presentation_advanced_en-jp.html`
	- Main bilingual slide deck (English/Japanese toggle).
	- Covers setup, matched backend comparison, crash localization, and follow-up tests.
- `experiment-history.html`
	- Timeline-style summary of the investigation flow.
	- Includes legends and non-specialist explanations.
- `code-tracing.html`
	- Standalone supplementary deck for the exact meaning of `num_gpu`.
	- Traces the parameter from client to server, runner, and llama.cpp with exact line references.

## Notes

- Filenames are kept as-is for direct publication.
- Links in `index.html` use relative paths so the site works under `/vega-hbmx-pages/`.
- These materials are derived from the investigation artifacts prepared in the main research workspace.

## 日本語メモ

このリポジトリは、旧世代 HBM GPU（Vega / gfx900）に関する調査資料を GitHub Pages で公開するための公開用リポジトリです。

- ルート: https://aets-magi.github.io/vega-hbmx-pages/
- `index.html`: 公開トップページ
- `presentation_advanced_en-jp.html`: 日英切替つき発表・補助スライド
- `experiment-history.html`: 実験の流れを整理した時系列資料
- `code-tracing.html`: `num_gpu` の意味を厳密な行番号で追う単体補助資料

相対リンクで構成しているため、GitHub Pages 配下でそのまま動作します。
