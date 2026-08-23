import streamlit as st
import yt_dlp

# 1. ページ基本設定
st.set_page_config(
    page_title="X Video Downloader Pro",
    page_icon="🎬",
    layout="centered",
)

# 2. 洗練されたカスタムCSSデザイン（背景・カード・ボタン装飾）
st.markdown(
    """
    <style>
    /* 全体の背景と文字色 */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* メインタイトルの中央寄せ＆グラデーション */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    /* サブタイトルのスタイル */
    .sub-title {
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2.5rem;
        font-size: 1.05rem;
    }

    /* 入力エリアのコンテナ風カード */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* 成功メッセージやプレビューの枠組み */
    .result-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. ヘッダー表示
st.markdown(
    "<div class='main-title'>🎬 X Video Downloader</div>", unsafe_allow_html=True
)
st.markdown(
    "<div class='sub-title'>URLを貼り付けるだけで、どんな環境でも高速・安全に動画を抽出</div>",
    unsafe_allow_html=True,
)

# 4. メイン入力をカード風のデザインで囲む
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

url = st.text_input(
    "🔗 X（Twitter）のポストURL",
    placeholder="https://x.com/username/status/123456789...",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_btn = st.button(
        "✨ 動画を抽出する", type="primary", use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# 5. 抽出ロジック
if submit_btn:
    if not url:
        st.warning("⚠️ URLを入力してください。")
    else:
        with st.spinner("🚀 動画データを解析中..."):
            try:
                if "x.com" in url:
                    url = url.replace("x.com", "twitter.com")

                ydl_opts = {
                    "format": "best",
                    "quiet": True,
                    "no_warnings": True,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_url = info.get("url")
                    title = info.get("title", "video")

                if video_url:
                    st.markdown(
                        "<div class='result-box'>", unsafe_allow_html=True
                    )
                    st.success("✅ 抽出に成功しました！")
                    st.video(video_url)
                    st.markdown(
                        f"""
                    <div style="text-align: center; margin-top: 15px;">
                        <a href="{video_url}" target="_blank" download="{title}.mp4" 
                           style="background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; padding: 10px 24px; 
                                  text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                           📥 動画ファイルを保存する
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(
                        "❌ 動画が見つかりませんでした。このポストには動画が含まれていない可能性があります。"
                    )

            except Exception as e:
                st.error(f"❌ 抽出エラーが発生しました。\n\n詳細: `{e}`")