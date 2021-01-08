import logging
import os
from io import BytesIO
from typing import List

import requests
from googleapiclient.discovery import build
from PIL import Image

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

logger = logging.getLogger(__name__)


def google_links(search_term, count=5) -> List:
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = (
        service.cse()
        .list(q=search_term, cx=GOOGLE_CSE_ID, searchType="image")
        .execute()
    )
    items = result.get("items", [])
    return [item["link"] for item in items][:count]


def google_images(search_term, count) -> List[bytes]:
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = (
        service.cse()
        .list(q=search_term, cx=GOOGLE_CSE_ID, searchType="image")
        .execute()
    )
    items = result.get("items", [])
    logger.debug(f"Got links: {[item['link'] for item in items]}")
    images = []

    for link in [item["link"] for item in items][:count]:
        try:
            response = requests.get(link, allow_redirects=True)
        except Exception as error:
            logger.error(f"Error: {error}")
            continue
        if response.ok:
            try:
                Image.open(BytesIO(response.content))
                images.append(response.content)
            except Exception as error:
                logger.error(f"Error: {error}")
                continue
        else:
            logger.error(f"Bad response: {response.status_code}")
            continue
    return images
