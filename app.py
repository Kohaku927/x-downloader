import base64
import streamlit as st
import yt_dlp

# 1. ページ基本設定
st.set_page_config(
    page_title="X Video Downloader Pro",
    page_icon="🎬",
    layout="centered",
)

# 2. デザインCSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 0.95rem;
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
        margin-top: 20px;
        word-break: break-all;
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
    "<div class='sub-title'>URLを貼り付けるだけで簡単・安全に動画を抽出</div>",
    unsafe_allow_html=True,
)

# 4. 入力カード
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
url = st.text_input(
    "🔗 X（Twitter）のポストURL",
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
                    st.success("✅ 抽出に成功しました！")

                    # プレビュー表示
                    st.video(video_url)

                    # Streamlit標準のダウンロードボタン（これがiPhoneやPCで最も確実に保存できます）
                    import urllib.request

                    try:
                        # 動画データを一時的にダウンロードしてボタンに組み込む
                        with urllib.request.urlopen(video_url) as response:
                            video_bytes = response.read()

                        st.download_button(
                            label="📥 【保存】動画ファイルをダウンロード",
                            data=video_bytes,
                            file_name=f"{title}.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                        )
                    except Exception:
                        # 万が一データ取得が重い場合のフォールバック（別タブ直リンク）
                        st.markdown(
                            f"""
                        <div style="text-align: center; margin-top: 15px;">
                            <a href="{video_url}" target="_blank" 
                               style="background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; padding: 12px 20px; 
                                      text-decoration: none; border-radius: 8px; font-weight: bold; display: block; text-align: center;">
                                📥 動画を開く（長押ししてダウンロード）
                            </a>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(
                        "❌ 動画が見つかりませんでした。動画が含まれていない可能性があります。"
                    )

            except Exception as e:
                st.error(f"❌ エラーが発生しました。\n\n詳細: `{e}`")