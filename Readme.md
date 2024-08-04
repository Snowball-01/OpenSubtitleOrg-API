📄 OpenSubtitles Org API
==================

Welcome to the OpenSubtitles Org API, a simple and powerful API to fetch subtitles and information about Asian dramas from [OpenSubtitles.org](https://www.opensubtitles.org). This API is built with FastAPI and provides endpoints to fetch subtitles and query information.

🚀 Getting Started
------------------

### Requirements

*   Python 3.7+
*   FastAPI
*   `requests` library
*   `psutil` library
*   `beautifulsoup4` library

### Installation

1.  Clone the repository:
    
        git clone https://github.com/Snowball-01/Asian-Drama-API.git
    
2.  Install the required dependencies:
    
        pip install fastapi uvicorn requests psutil beautifulsoup4 html5lib
    
3.  Run the FastAPI server:
    
        uvicorn main:app --reload
    

📚 API Documentation
--------------------

### Root Endpoint

#### GET /

Returns basic information about the API, server, and memory usage.

    {
        "success": true,
        "playground": "http://82.180.131.185:8000",
        "endpoint": "https://github.com/Snowball-01/Asian-Drama-API",
        "developer": "https://t.me/Snowball_Official",
        "date": "MM/DD/YYYY, HH:MM:SS AM/PM",
        "rss": "XX.XX MB",
        "heap": "XX.XX MB",
        "server": "City, Region, Country",
        "version": "1.0.0"
    }

### Query Endpoint

#### GET /get

Fetch subtitles or query information based on parameters.

**Parameters:**

*   `query` (optional): A search query to find subtitles.
*   `id` (optional): An ID to fetch specific subtitles.

**Response:**

If `query` is provided:

    [
        {
            "id": "subtitle_id",
            "title": "Subtitle Title",
            "description": "Subtitle Description",
            "lang": "Language",
            "sub_type": "Subtitle Type",
            "imdb": "IMDB Rating/10",
            "rating": "Aggregate Rating",
            "url": "https://www.opensubtitles.org/subtitle_url",
            "download": "https://www.opensubtitles.org/en/subtitleserve/sub/subtitle_id"
        },
        ...
    ]

If `id` is provided:

    {
        "id": "subtitle_id",
        "title": "Subtitle Title",
        "description": "Subtitle Description",
        "lang": "Language",
        "sub_type": "Subtitle Type",
        "imdb": "IMDB Rating/10",
        "rating": "Aggregate Rating",
        "url": "https://www.opensubtitles.org/subtitle_url",
        "download": "https://www.opensubtitles.org/en/subtitleserve/sub/subtitle_id"
    }

If neither `query` nor `id` is provided:

    {
        "error": "Neither query nor id provided"
    }

📬 Contact
----------

If you have any questions or suggestions, feel free to reach out to the developer:

*   [Telegram](https://t.me/Snowball_Official)

🌟 Contributing
---------------

We welcome contributions! Please open an issue or submit a pull request on GitHub.

📄 License
----------

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

* * *

✨ Happy coding!