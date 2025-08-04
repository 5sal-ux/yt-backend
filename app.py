from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import yt_dlp.utils

app = Flask(__name__)

# Updated yt-dlp options
ytdl_opts = {
    'format': 'best',
    'noplaylist': True,
    'quiet': True,
    'forcejson': True,
    'simulate': True,
    'nocheckcertificate': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  # Spoof browser
    'geo_bypass': True,  # Optional: bypass region lock
}

@app.route('/')
def home():
    return 'YouTube Backend API is running!'

@app.route('/stream')
def stream():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        with YoutubeDL(ytdl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info_dict.get('title'),
                'uploader': info_dict.get('uploader'),
                'thumbnail': info_dict.get('thumbnail'),
                'direct_url': info_dict.get('url')  # this is the actual streamable link
            })

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)