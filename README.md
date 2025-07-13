# Yet Another YouTube Video Downloader (YAYVD)

<p align="center">
  <img src="https://github.com/thisispit/yayVD/blob/master/assets/brave_ldBYmC9DQO.gif?raw=true" alt="YAYVD Demo" width="700"/>
</p>
A modern, user-friendly web application for downloading YouTube videos in various formats and qualities. Built with Flask and pytubefix.

## Features

- 🎥 Download YouTube videos in multiple quality options (up to Best Quality)
- 🎵 Extract audio from videos
- 📱 Mobile-friendly interface
- 🔄 Smart format selection with recommended options
- 🎯 Preset quality options (1080p, 720p)
- 🚀 Fast downloads (merges video+audio with ffmpeg)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thisispit/yayvd.git
```
```bash
cd yayvd
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have [ffmpeg](https://ffmpeg.org/download.html) installed and available in your system PATH.

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open the application in your web browser
2. Paste a YouTube video URL
3. Select your preferred format and quality
4. Click download and wait for the process to complete

## Features in Detail

### Quality Selection
- Best Quality: Highest available resolution with audio
- 1080p (Recommended): Full HD quality
- 720p: HD quality
- Custom qualities available based on source video

### Audio Downloads
- Extract audio in best quality (MP4 audio)
- Multiple audio bitrates available

### Mobile Support
- Responsive design
- Optimized for mobile browsers

## Technical Details

- Built with Flask (Python web framework)
- Uses pytubefix for video extraction
- Merges video and audio streams using ffmpeg when needed
- Automatic file cleanup after download

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational purposes only. Please respect YouTube's terms of service and content creators' rights when using this application. 
