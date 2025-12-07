## React 開発環境構築（Vite + TypeScript）

### 手順メモ（PowerShell 1〜67 行）

1. **Node.js のバージョン確認**

   - `node -v`
   - 結果: `v24.11.1`

2. **Vite プロジェクトの作成**

   - コマンド: `npm create vite@4.1.0`
   - プロンプトに従って入力:
     - Project name: `react-app`
     - Select a framework: `React`
     - Select a variant: `TypeScript`
   - `D:\dev\taitech\hairou\react-app` にプロジェクトが作成される。

3. **プロジェクトディレクトリへ移動**

   - `cd react-app`

4. **依存パッケージのインストール**

   - `npm install`
   - パッケージが 61 個追加され、いくつかの脆弱性の注意が表示される（必要に応じて `npm audit` や `npm audit fix --force` を実行）。

5. **開発サーバーの起動**
   - `npm run dev`
   - Vite の開発サーバーが起動し、以下の URL が表示される:
     - Local: `http://localhost:5173/`
   - ブラウザで上記 URL にアクセスすると、React + Vite + TypeScript の初期画面が表示される。

### ブラウザで React コードが JavaScript に変換されていることを確認する

1. **ブラウザでアプリを開く**

   - URL: `http://localhost:5173/`

2. **開発者ツールを開く**

   - Windows: `F12` または `Ctrl + Shift + I`
   - 「Network」タブや「Sources」タブを開く。

3. **読み込まれている JavaScript を確認する**
   - `http://localhost:5173/` をリロードすると、Vite がバンドルした JavaScript ファイルが Network に表示される。
   - `Sources` タブでも、`/src/main.tsx` などのソースがモジュールとして読み込まれていることが確認できる。
   - これらは、ブラウザが直接 TypeScript/JSX を解釈しているのではなく、Vite によって変換された JavaScript として実行されている。
