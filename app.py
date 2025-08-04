from flask import Flask, request, jsonify, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/search')
def search():
    q = request.args.get('q')
    if not q:
        return jsonify({ "error": "No query provided" }), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'format': 'bestaudio,best', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(f"ytsearch1:{q}", download=False)
            entry = info['entries'][0]
            return jsonify({
                "title": entry.get('title'),
                "url": entry.get('webpage_url')
            })
    except Exception as e:
        return jsonify({ "error": str(e) }), 400

@app.route('/stream')
def stream():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({ "error": "No URL provided" }), 400

    try:
        opts = {
            'quiet': True,
            'format': 'best[ext=mp4]/best', 
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # info['url'] is the direct media URL
            return jsonify({
                "title": info.get('title'),
                "stream_url": info['url']
            })
    except yt_dlp.utils.DownloadError as de:
        return jsonify({ "error": "Download error: " + str(de) }), 400
    except Exception as e:
        return jsonify({ "error": "Unexpected error: " + str(e) }), 500

if __name__ == '__main__':
    # Render uses $PORT, so fall back to 10000 if not set
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)