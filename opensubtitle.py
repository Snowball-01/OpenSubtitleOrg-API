from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from datetime import datetime
import psutil
from typing import Union
from utility.utils import fetch_server_location, fetch_subtitles, fetch_query

app = FastAPI()

OPENSUBTITLE_URL = "https://www.opensubtitles.org/en/search/sublanguageid-all"

favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/")
async def get_api_info():
    process = psutil.Process()
    rss = process.memory_info().rss / (1024**2)  # RSS in MB
    vms = process.memory_info().vms / (1024**2)  # VMS in MB
    server_location = await fetch_server_location()

    return {
        "success": True,
        "playground": "http://82.180.131.185:5000",
        "endpoint": "https://github.com/Snowball-01/OpenSubtitles-API",
        "developer": "https://t.me/Snowball_Official",
        "date": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "rss": f"{rss:.2f} MB",
        "heap": f"{vms:.2f} MB",
        "server": server_location,
        "version": "1.0.0",
    }


@app.get("/search")
async def get_query_results(query: Union[str, None] = None):
    if query:
        return await fetch_query(query)
    else:
        raise HTTPException(status_code=400, detail="Neither query nor id provided")


@app.get("/get")
async def get_subtitles_by_id(id: Union[str, None] = None):
    if id:
        return await fetch_subtitles(OPENSUBTITLE_URL + "/" + id)
    else:
        raise HTTPException(status_code=400, detail="Neither query nor id provided")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="OpenSubtitle API",
        version="1.0.0",
        description='Welcome to the **OpenSubtitles API**, a simple and powerful API to fetch subtitles and information about [OpenSubtitle.org](https://www.opensubtitles.org). This API is built with FastAPI and provides endpoints to fetch subtitles and query information.',
        contact={
        "name": "Snowball",
        "url": "http://t.me/Snowball_Official",
    },
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
