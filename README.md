# vega-hbmx-pages

GitHub Pages repository for the public HTML materials of the Vega HBM / gfx900 investigation.

公開先: https://aets-magi.github.io/vega-hbmx-pages/

## はじめに

このリポジトリは、旧世代 HBM GPU（AMD Radeon RX Vega / gfx900）上で、ROCm/HIP と Vulkan で挙動がどう違うかをまとめた公開用ページ群です。

まずは難しいコードやログを読む前に、

1. 全体像をつかむ
2. 実験の流れを追う
3. 必要ならコード根拠まで降りる

という順番で見られるように構成しています。

## 一般向けのおすすめ閲覧順

### 1. `index.html`
- 公開トップページです。
- 全資料への入口になっています。

### 2. `general-audience.html`
- 非エンジニア向けの入口ページです。
- 専門用語を減らして、今回の調査の結論を先につかめるようにしています。

### 3. `media.html`
- NotebookLM による解説音声と、ポスター PDF を見られるページです。
- 最初に雰囲気をつかみたい人向けです。

### 4. `experiment-history.html`
- 調査がどう進んだかを時系列で追えるページです。
- 非専門向けの説明や凡例も入っています。

## 発表・補助資料

### `presentation_advanced_en-jp.html`
- 日英切替つきの発表・補助スライドです。
- 実験設定、matched backend comparison、crash localization、follow-up tests をまとめています。
- 会場でそのまま表示することを想定した HTML です。

## 研究向け資料

### `code-tracing.html`
- `num_gpu` の意味を client → server → runner → llama.cpp まで、厳密な行番号つきで追う単体資料です。
- 「`num_gpu` は GPU 枚数ではなく offload 層数である」という点を、ソースコードから順に確認できます。
- 発表中の質疑や、実装上の意味を厳密に確認したい場合に向いています。

## 収録ファイル一覧

- `index.html`
  - Landing page for the published materials.
- `general-audience.html`
  - A non-technical overview page.
  - Explains the main finding in plain language with presentation-style visuals.
- `media.html`
  - Media viewer page for bundled assets under `media/`.
  - Includes the NotebookLM commentary audio and embedded poster PDF.
- `presentation_advanced_en-jp.html`
  - Main bilingual slide deck (English/Japanese toggle).
- `experiment-history.html`
  - Timeline-style summary of the investigation flow.
- `code-tracing.html`
  - Standalone supplementary deck for the exact meaning of `num_gpu`.

## Media assets

- `media/notebooklm-discuss.m4a`
  - NotebookLM commentary audio.
- `media/A0_Final_Poster_revised.pdf`
  - Final poster PDF.

## 公開構成メモ

- ファイル名は公開用にそのまま維持しています。
- `index.html` から各資料へ相対リンクで移動できます。
- GitHub Pages の `/vega-hbmx-pages/` 配下でそのまま動作する構成です。
- これらの HTML は、研究用ワークスペースで作成した資料を公開向けに整理したものです。

## Quick English guide

- Start with `index.html` for navigation.
- Open `general-audience.html` for a plain-language overview first.
- Use `media.html` for the audio commentary and poster PDF.
- Read `experiment-history.html` for the investigation timeline.
- Open `presentation_advanced_en-jp.html` for the main bilingual slide deck.
- Use `code-tracing.html` for the most technical evidence on `num_gpu` semantics.
