#!/bin/bash

# 監視対象フォルダ
WATCH_DIR="/d/dev/font"

# 既存のファイルのタイムスタンプを記録するファイル
STATE_FILE="/tmp/font_watch_state.txt"

# 初期化: 既存のファイル一覧を記録
if [ ! -f "$STATE_FILE" ]; then
    touch "$STATE_FILE"
    find "$WATCH_DIR" -type f -exec stat -c "%Y %n" {} \; > "$STATE_FILE" 2>/dev/null || \
    find "$WATCH_DIR" -type f -exec stat -f "%m %N" {} \; > "$STATE_FILE" 2>/dev/null
fi

echo "監視を開始します: $WATCH_DIR"
echo "新しいファイルを検出したら、内容を読み込んで cursor-agent に渡します..."
echo ""

# 無限ループで監視
while true; do
    # 現在のファイル一覧を取得

    # 対応済みリストを読み込む
    RESPONSE_FILE="/tmp/response.txt"
    if [ -f "$RESPONSE_FILE" ]; then
        RESPONSE_LIST=$(cat "$RESPONSE_FILE")
    else
        RESPONSE_LIST=""
    fi

    CURRENT_STATE=$(mktemp)
    find "$WATCH_DIR" -type f -exec stat -c "%Y %n" {} \; > "$CURRENT_STATE" 2>/dev/null || \
    find "$WATCH_DIR" -type f -exec stat -f "%m %N" {} \; > "$CURRENT_STATE" 2>/dev/null
    
    # 新しいファイルまたは更新されたファイルを検出
    while IFS= read -r line; do
        FILE_PATH=$(echo "$line" | cut -d' ' -f2-)
        
        # 前回の状態に存在しない、またはタイムスタンプが異なる場合
        if ! grep -q "$FILE_PATH" "$STATE_FILE" 2>/dev/null; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 新しいファイルを検出: $FILE_PATH"
            
            # ファイルの内容を読み込む
            if [ -f "$FILE_PATH" ]; then
                FILE_CONTENT=$(cat "$FILE_PATH")
                
                # ファイルが空でない場合のみ処理
                if [ -n "$FILE_CONTENT" ]; then
                    echo "ファイルの内容を読み込みました。cursor-agent に渡します..."
                    echo ""
                    
                    # cursor-agent コマンドを実行
                    cursor-agent -p --force "$FILE_CONTENT"
                    
                    echo ""
                    echo "処理が完了しました。"
                else
                    echo "ファイルが空のため、スキップします。"
                fi
            fi
        fi
    done < "$CURRENT_STATE"
    
    # 状態ファイルを更新
    cp "$CURRENT_STATE" "$STATE_FILE"
    rm "$CURRENT_STATE"
    
    # 1秒待機してから再度チェック
    sleep 1
done

再起動処理

テストを実行する

テストがもし成功したら対応済みリスト二issue番号を記載する