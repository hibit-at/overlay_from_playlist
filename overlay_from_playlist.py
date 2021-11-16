import json
import requests
import io
from PIL import Image, ImageDraw, ImageFont

file_path = 'xxxxxxxxx.json'  # path of the playlist(*.json, *.bplist)

j = json.loads(open(file_path).read())


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


def image_make(cover_url, title, author, mapper, diff, bpm):
    canvasSize = (1920, 300)
    backgroundRGB = (0, 0, 0, 0)
    img = Image.new('RGBA', canvasSize, backgroundRGB)
    cover_img = Image.open(io.BytesIO(requests.get(cover_url).content))
    img.paste(cover_img, (25, 25))
    img = text_over(img, title, 50)
    img = text_over(img, author, 100)
    img = text_over(img, mapper, 150)
    img = text_over(img, diff, 200)
    img.save(f"{title}.png")


for song in j['songs']:
    hash = song['hash']
    diff = song['difficulties'][0]['name'].replace('Plus', '+')
    url = f'https://api.beatsaver.com/maps/hash/{hash}'
    res = requests.get(url).json()
    print(hash, diff)
    title = res['metadata']['songName']
    author = res['metadata']['songAuthorName']
    mapper = res['metadata']['levelAuthorName']
    bpm = res['metadata']['bpm']
    cover_url = res['versions'][0]['coverURL']
    image_make(cover_url, title, author, mapper, diff, bpm)
