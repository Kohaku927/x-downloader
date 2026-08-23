import io
from flask import Flask, render_template, request, send_file
import requests
import yt_dlp

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
  video_url = None
  error_message = None

  if request.method == "POST":
    url = request.form.get("url")
    if not url:
      error_message = "URLを入力してください。"
    else:
      try:
        if "x.com" in url:
          url = url.replace("x.com", "twitter.com")

        ydl_opts = {
            "format": "best",
            "quiet": True,
            "no_warnings": True,
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url, download=False)
          video_url = info.get("url")

        if not video_url:
          error_message = "動画が見つかりませんでした。"
      except Exception as e:
        error_message = f"エラーが発生しました: {e}"

  return render_template(
      "index.html", video_url=video_url, error_message=error_message
  )


# サーバー経由で安全に動画ファイルをダウンロードさせるルート
@app.route("/download")
def download_file():
  video_url = request.args.get("url")
  if not video_url:
    return "URLがありません", 400

  try:
    # サーバー側で動画データを取得
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    resp = requests.get(video_url, headers=headers, stream=True)

    # バイナリデータとしてブラウザにストリーミング送信（強制ダウンロード）
    return send_file(
        io.BytesIO(resp.content),
        mimetype="video/mp4",
        as_attachment=True,
        download_name="x_video.mp4",
    )
  except Exception as e:
    return f"ダウンロードに失敗しました: {e}", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)