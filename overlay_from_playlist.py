import json
import requests
import io
import os
import re
from PIL import Image, ImageDraw, ImageFont


def text_over(img, text, height):
    ttfontname = "C:\\Windows\\Fonts\\meiryob.ttc"
    fontsize = 36
    textRGB = (255, 255, 255, 255)
    if text == 'Easy':
        textRGB = (0, 255, 255, 255)
    if text == 'Normal':
        textRGB = (0, 255, 0, 255)
    if text == 'Hard':
        textRGB = (255, 255, 0, 255)
    if text == 'Expert':
        textRGB = (255, 127, 0, 255)
    if text == 'Expert+':
        textRGB = (255, 0, 127, 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ttfontname, fontsize)
    textTopLeft = (300, height)
    draw.text(textTopLeft, text, fill=textRGB, font=font)
    return img


def process_playlist(playlist_name, playlist):
    for song in playlist['songs']:
        hash = song['hash']
        diff = song['difficulties'][0]['name'].replace('Plus', '+')
        diff = diff.capitalize()
        url = f'https://api.beatsaver.com/maps/hash/{hash}'
        res = requests.get(url).json()
        print(hash, diff)
        title = res['metadata']['songName']
        title = re.sub(r'[\\/:*?"<>|]+', '', title)
        author = res['metadata']['songAuthorName']
        mapper = res['metadata']['levelAuthorName']
        bpm = res['metadata']['bpm']
        cover_url = res['versions'][0]['coverURL']
        canvasSize = (1920, 300)
        backgroundRGB = (0, 0, 0, 0)
        img = Image.new('RGBA', canvasSize, backgroundRGB)
        cover_img = Image.open(io.BytesIO(requests.get(cover_url).content))
        img.paste(cover_img, (25, 25))
        img = text_over(img, title, 50)
        img = text_over(img, author, 100)
        img = text_over(img, mapper, 150)
        img = text_over(img, diff, 200)
        if not os.path.exists(playlist_name):
            os.mkdir(playlist_name)
        img.save(f"{playlist_name}/{title}.png")


for file_path in os.listdir():
    extension = file_path.split('.')[-1]
    if extension == 'json' or extension == 'bplist':
        playlist_name = file_path.split('.')[0]
        playlist = json.loads(open(file_path).read())
        process_playlist(playlist_name, playlist)
