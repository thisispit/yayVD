from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from pytubefix import YouTube
import subprocess
import uuid
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    # Remove or replace characters not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('Please enter a YouTube URL.', 'error')
            return redirect(url_for('index'))
        try:
            yt = YouTube(url)
            # Get all video-only and progressive streams (mp4)
            video_streams = yt.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc()
            progressive_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            return render_template('select.html', yt=yt, video_streams=video_streams, progressive_streams=progressive_streams, audio_streams=audio_streams, url=url)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    itag = request.form.get('itag')
    stream_type = request.form.get('stream_type')
    audio_itag = request.form.get('audio_itag')
    if not url or not itag:
        flash('Invalid download request.', 'error')
        return redirect(url_for('index'))
    try:
        yt = YouTube(url)
        if stream_type == 'progressive':
            stream = yt.streams.get_by_itag(itag)
            filename = sanitize_filename(stream.default_filename)
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            return send_file(filepath, as_attachment=True)
        elif stream_type == 'video_only':
            video_stream = yt.streams.get_by_itag(itag)
            audio_stream = yt.streams.get_by_itag(audio_itag)
            # Use unique filenames to avoid conflicts
            unique_id = str(uuid.uuid4())
            video_path = os.path.join(DOWNLOAD_FOLDER, f"video_{unique_id}.mp4")
            audio_path = os.path.join(DOWNLOAD_FOLDER, f"audio_{unique_id}.mp4")
            output_path = os.path.join(DOWNLOAD_FOLDER, f"merged_{unique_id}.mp4")
            video_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"video_{unique_id}.mp4")
            audio_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"audio_{unique_id}.mp4")
            # Merge using ffmpeg
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Clean up temp files
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return send_file(output_path, as_attachment=True)
        elif stream_type == 'audio_only':
            stream = yt.streams.get_by_itag(itag)
            filename = sanitize_filename(stream.default_filename)
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            return send_file(filepath, as_attachment=True)
        else:
            flash('Invalid stream type.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 