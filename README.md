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
- 「未来の道具を、みんなの手に。」— 理念と思想を伝える宣言ページです。
- 技術の説明ではなく、「なぜやるのか」「誰のためか」を、専門知識なしで読める構成にしています。
- 1画面1テーマのスクロール構成で、読み物として気持ちが入るデザインです。

### 3. `media.html`
- NotebookLM による解説音声と、ポスター PDF を見られるページです。
- 最初に雰囲気をつかみたい人向けです。

### 4. `experiment-history.html`
- 調査がどう進んだかを時系列で追えるページです。
- runtime / code tracing だけでなく、2026-03-15 時点の GitHub chronology / PR-context synthesis まで含みます。
- 非専門向けの説明や凡例も入っています。

### 5. `page-history.html`
- 公開ページ側の更新内容を残す監査ログです。
- 「旧記述 → 新記述 → 根拠 → 影響ページ」の順で、何をどう差し替えたかを共有できます。

### 6. `reveal-hypothesis.html`
- gfx900 個別調査を起点にしながら、ROCm 一般の設計思想を GitHub 側の一次資料で検証した要約ページです。
- layered support、capability-based fallback、staged deprecation、repo-level consolidation、deprecated branch に残る legacy knowledge、support の層分解、AMD とコミュニティの役割分解を扱います。

### 7. `rocm-structure.html`
- ROCm 全体を、GitHub 側の一次資料から layered stack、support の意味の分離、repo topology の統合、AMD と community の寄与レイヤという観点で整理した独立ページです。
- `TheRock`、`rocm-systems`、retired repo README、public issue / PR のような複数の public source をまとめて読みたい人向けです。

### 8. `rocm-history.html`
- これまでに確定した commit、release block、issue trail をもとに、ROCm の変遷を public 向けの年表として整理したページです。
- `gfx900` を入口にしつつ、component ごとの追加・後退・統合・fallback に加えて、retired/deprecated repo の再編と late-phase layout/docs 再編も時間軸で読めるようにしています。

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

### `solver-trace.html` ★ 2026-03-14 更新
- MIOpen・rocBLAS・CK・Tensile における gfx900（Vega10）計算経路を、ソース行番号と実機ログで対応づけた技術参照資料です。
- 静的コード監査（code_verified）と実機 Vega64 での動的検証（runtime_verified）の両方を収録。
- 主な内容:
  - MLIR iGEMM の gfx900 除外コミット（2407d2f, 2021-12-22）とソースコード証跡
  - ASM implicit GEMM v4r1 dynamic の gfx900/gfx906 ホワイトリスト
  - Winograd・旧 ASM 系の生存経路
  - XDLops 系の系統的除外（IsXdlopsSupport の gfx900 不在）
  - CK inner_product.hpp の dot4 不在時逐次積和フォールバック
  - Tensile AsmCaps での (9,0,0) の dot4 全 False
  - rocBLAS getLazyLoadingArch の gfx900 明示マップ + 多段フォールバック
  - 実機逆アセンブルで INT8 naive カーネルに dot4 命令が存在しないことを確認
  - `IsMlirSupportedHardware()` と `ConvMlirIgemm*::IsApplicable()` の二重構造
  - 強制 MLIR 実行で露出した `Perf Db: record not found` / `boost::optional::get()` 系の下流失敗
  - 「維持（build）・管理（selection）・補充（fallback）」3 層構造の説明

## 収録ファイル一覧

- `index.html`
  - Landing page for the published materials.
- `general-audience.html`
  - Vision and philosophy declaration page: "Putting the tools of the future into everyone's hands."
  - Explains why this work is done and who it is for, without requiring technical knowledge.
- `media.html`
  - Media viewer page for bundled assets under `media/`.
  - Includes the NotebookLM commentary audio and embedded poster PDF.
- `presentation_advanced_en-jp.html`
  - Main bilingual slide deck (English/Japanese toggle).
- `experiment-history.html`
  - Timeline-style summary of the investigation flow (Steps 1–12 as of 2026-03-15), including the GitHub chronology / PR-context synthesis phase.
- `page-history.html`
  - Audit-log page for public-site wording changes, including old wording, new wording, rationale, and affected pages.
- `reveal-hypothesis.html`
  - Public summary page for the ROCm-wide design-model hypotheses revealed by the gfx900 investigation, including repo-level consolidation and legacy knowledge left in deprecated branches.
- `rocm-structure.html`
  - Standalone public page that reads ROCm-wide structure and contribution layers from GitHub-side primary evidence, including layered stack boundaries, support splitting, repository consolidation, and AMD/community role layering.
- `rocm-history.html`
  - Public-facing ROCm chronology built from the already-confirmed GitHub-side timeline anchors, including retired/deprecated-repo reorganization and late layout/docs migration signals.
- `code-tracing.html`
  - Standalone supplementary deck for the exact meaning of `num_gpu`.
- `solver-trace.html`
  - Technical reference: gfx900 computation paths in MIOpen / rocBLAS / CK / Tensile — code-verified and runtime-verified.

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
- Open `general-audience.html` for the vision and philosophy — why this work matters.
- Use `media.html` for the audio commentary and poster PDF.
- Read `experiment-history.html` for the investigation timeline (Steps 1–12, including the GitHub chronology / PR-context synthesis phase).
- Open `reveal-hypothesis.html` for the ROCm-wide design-model interpretation revealed by the gfx900 investigation, including repo-level consolidation and legacy knowledge left in deprecated branches.
- Open `rocm-structure.html` for a GitHub-grounded reading of ROCm-wide structure and contribution layers beyond the gfx900-specific case.
- Open `rocm-history.html` for the public GitHub-side chronology of ROCm itself, including retired/deprecated-repo reorganization and late layout/docs migration.
- Open `presentation_advanced_en-jp.html` for the main bilingual slide deck.
- Use `code-tracing.html` for the most technical evidence on `num_gpu` semantics.
- Use `solver-trace.html` for gfx900 computation path tracing through the ROCm library stack (code + runtime verified).
