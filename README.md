# Reddit Scraper

## Description
A Python-based scraper that uses PRAW and requests to download Reddit submissions and comments based on post IDs or subreddit names. Saves images locally and stores comments in CSV.

## Features
- Fetch submissions by ID or subreddit.
- Download images via requests and OpenCV.
- Save comments to CSV with header handling.
- Load credentials from `.env`.
- Configurable rate limiting.

## Prerequisites
- Python 3.8+
- Reddit App credentials (`CLIENT_ID`, `CLIENT_SECRET`)
- `USER_AGENT` environment string

## Installation
```bash
git clone <repo_url>
cd web_scraper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=your_app/0.1 by u/your_username
```

## License
MIT License