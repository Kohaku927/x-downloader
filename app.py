import streamlit as st
import yt_dlp

# 1. ページ基本設定
st.set_page_config(
    page_title="X Video Downloader Pro",
    page_icon="🎬",
    layout="centered",
)

# 2. デザインCSS（余白の調整とスタイリッシュなカード）
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .main-title {
        font-size: 2.0rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        color: #94a3b8;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .result-box {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
    }
    .guide-box {
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        padding: 10px 15px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #e2e8f0;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. ヘッダー
st.markdown(
    "<div class='main-title'>🎬 X Video Downloader</div>", unsafe_allow_html=True
)
st.markdown(
    "<div class='sub-title'>URLを貼るだけで、どんな動画も簡単に保存</div>",
    unsafe_allow_html=True,
)

# 4. 入力カード
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
url = st.text_input(
    "🔗 X（Twitter）のポストURLを入力",
    placeholder="https://x.com/username/status/...",
)
submit_btn = st.button(
    "✨ 動画を抽出する", type="primary", use_container_width=True
)
st.markdown("</div>", unsafe_allow_html=True)

# 5. 抽出処理
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
                    title = info.get("title", "x_video")

                if video_url:
                    st.markdown(
                        "<div class='result-box'>", unsafe_allow_html=True
                    )
                    st.success("✅ 抽出成功！")

                    # 動画プレビュー
                    st.video(video_url)

                    # スマホ向け説明ガイド
                    st.markdown(
                        """
                    <div class="guide-box">
                        <b>💡 保存方法:</b><br>
                        下のボタンをタップすると、iPhoneのダウンロード確認画面が表示されます。
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # iPhoneのSafariで「ダウンロードしますか？」ポップアップを出しやすくするHTMLリンク
                    st.markdown(
                        f"""
                    <div style="text-align: center; margin-top: 10px;">
                        <a href="{video_url}" download="{title}.mp4" rel="noopener" 
                           style="background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; padding: 14px 20px; 
                                  text-decoration: none; border-radius: 10px; font-weight: bold; display: block; text-align: center; font-size: 1.05rem;">
                           📥 端末に動画をダウンロード
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ 動画が見つかりませんでした。")

            except Exception as e:
                st.error(f"❌ エラーが発生しました。\n\n詳細: `{e}`")