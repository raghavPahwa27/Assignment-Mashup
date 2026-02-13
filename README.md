# YouTube Mashup Generator

A Python-based application that creates audio mashups by downloading YouTube videos of a singer, extracting audio clips, and merging them into a single cohesive mashup file.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Methodology](#methodology)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Input/Output Specifications](#inputoutput-specifications)
- [Deployment Notes](#deployment-notes)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎵 Overview

This project provides two programs for creating audio mashups:

1. **Command-Line Interface (CLI)**: A standalone Python script for quick mashup generation
2. **Web Application**: A Flask-based web service with email delivery functionality

The application downloads YouTube videos, converts them to audio, extracts the first few seconds from each track, and merges them into a single mashup file.

## ✨ Features

- Download multiple YouTube videos automatically
- Convert video to high-quality MP3 audio
- Trim audio clips to specified duration
- Merge clips into seamless mashup
- Web interface for easy interaction
- Email delivery of generated mashups
- Input validation and error handling

## 🔧 Methodology

### Program 1: Command Line Interface

1. **Download Videos**: Uses `yt-dlp` to download N YouTube videos of specified singer
2. **Convert to Audio**: Utilizes `ffmpeg` to convert videos to MP3 format
3. **Trim Clips**: Extracts first Y seconds from each audio file using `pydub`
4. **Merge Audio**: Combines all clips into single mashup MP3 file

### Program 2: Web Service

1. **User Input**: Flask form collects Singer Name, Number of Videos, Duration, and Email
2. **Process Mashup**: Backend performs same operations as CLI program
3. **Package & Send**: Zips final MP3 and sends to user via SMTP email

## 💻 Usage

### Program 1: Command Line

```bash
python 102303608.py "<SingerName>" <NumberOfVideos> <DurationSec> <OutputFileName>
```

**Example:**
```bash
python 102303608.py "Sharry Maan" 20 30 output.mp3
```

**Parameters:**
- `SingerName`: Name of the singer (enclosed in quotes)
- `NumberOfVideos`: Number of videos to download (integer)
- `DurationSec`: Duration in seconds to extract from each video (integer)
- `OutputFileName`: Name of the output mashup file (with .mp3 extension)

### Program 2: Web Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Access the application**
```
http://127.0.0.1:5000/
```

3. **Fill in the form**
   - Singer Name: Name of the artist
   - Number of Videos: Minimum 10 videos
   - Duration: Minimum 20 seconds per clip
   - Email ID: Valid email address for delivery

4. **Submit and wait**
   - The mashup will be generated and sent to your email as `mashup.zip`

## 📁 Project Structure

```
Mashup/
│
├── 102303608.py          # CLI program for mashup generation
├── app.py                # Flask web application
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
└── templates/
    └── index.html       # Web interface HTML template
```


## 🌐 Deployment Notes

### Local Deployment Only

This project **cannot be reliably deployed** on cloud platforms like Render, Heroku, or Streamlit Cloud due to YouTube's bot detection mechanisms.

**Common Issues on Cloud Platforms:**
- ❌ HTTP 429 (Too Many Requests)
- ❌ "Sign in to confirm you're not a bot"
- ❌ Signature solving failures
- ❌ Format unavailability errors

**Solution:** Run the application locally on your machine where YouTube's bot detection is less aggressive.

**Local Access:**
```
http://127.0.0.1:5000/
```

## 📸 Screenshots

### Web Interface
![Web Interface](screenshot.png)

*The interface includes fields for Singer Name, Number of Videos, Duration, Email ID, and a Submit button.*
