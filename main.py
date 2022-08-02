# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.oauth2.credentials
import googleapiclient.errors
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw, ImageFont

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def credentials_to_dict(credentials):
    """Return dictionary containing data from a Google Credentials object.

    Args:
        credentials (google.oauth2.credentials.Credentials): credentials object

    Returns:
        dict: dictionary containing data from a Google Credentials object
    """
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def create_thumbnail(text, path):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("UbuntuTitling-Bold.ttf", 100)
    text_w, text_h = draw.textsize(text, font=font)
    draw.text(
        ((width - text_w) / 2, (height - text_h) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center",
    )
    img.save(path)


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    # print(credentials_to_dict(credentials))
    # with open("credentials.json", "r") as f:
    #     credentials = google.oauth2.credentials.Credentials(**json.load(f))

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
    video_id = os.environ["VIDEO_ID"]
    request = youtube.videos().list(part="statistics", id=video_id)
    response = request.execute()
    print(response)
    view = response["items"][0]["statistics"]["viewCount"]
    title = f"Click on this video to increase this number {view}"
    request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "categoryId": "28",
                "title": title,
            },
        },
    )
    response = request.execute()
    thumbnail_path = "thumbnail.png"
    create_thumbnail(
        f"This video has {view} views\n\nat {datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H:%M')} UTC+0",
        thumbnail_path,
    )
    request = youtube.thumbnails().set(
        media_body=MediaFileUpload(thumbnail_path), videoId=video_id
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
