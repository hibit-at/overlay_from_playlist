import json
from tkinter import Canvas
import requests
import io
import os
import re
from PIL import Image, ImageDraw, ImageFont
import sys


def text_over(img, text, height, fontsize, isLeft):
    ttfontname = "C:\\Windows\\Fonts\\meiryob.ttc"
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
    if isLeft:
        textPos = (50, height)
        draw.text(textPos, text, fill=textRGB, anchor="la", font=font)
    else:
        textPos = (960-50, height)
        draw.text(textPos, text, fill=textRGB, anchor="ra", font=font)

    return img


def make_image(title, player, isLeft):
    standing = player['standing']
    sid = player['sid']
    name = player['name']
    canvasSize = (960, 1200)
    backgroundRGB = (0, 0, 0, 0)
    img = Image.new('RGBA', canvasSize, backgroundRGB)
    profile_url = f'https://cdn.scoresaber.com/avatars/{sid}.jpg'
    cover_img = Image.open(io.BytesIO(requests.get(profile_url).content))
    scoresaber_url = f'https://scoresaber.com/api/player/{sid}/full'
    res = requests.get(scoresaber_url).json()
    pp = res['pp']
    global_rank = res['rank']
    local_rank = res['countryRank']
    total_score = res['scoreStats']['totalScore']
    total_ranked_score = res['scoreStats']['totalRankedScore']
    average_ranked_accuracy = res['scoreStats']['averageRankedAccuracy']
    total_play_count = res['scoreStats']['totalPlayCount']
    ranked_play_count = res['scoreStats']['rankedPlayCount']
    if isLeft:
        pos = (25,25)
    else:
        pos = (900-25-128,25)
    img.paste(cover_img, pos)
    texts = []
    texts.append(name)
    texts.append(f'pp : {pp:,.2f}')
    texts.append(f'JP rank : # {local_rank} (# {global_rank:,})')
    texts.append(f'TotalScore : {total_score:,}')
    texts.append(f'RankedScore : {total_ranked_score:,}')
    texts.append(f'RankedAccuracy : {average_ranked_accuracy:,.2f}')
    texts.append(f'TotalPlayCount : {total_play_count:,}')
    texts.append(f'RankedPlayCount : {ranked_play_count:,}')
    texts.append(f'{title} # {standing}')
    height = 250
    for text in texts:
        img = text_over(img, text, height, 36, isLeft)
        height += 50
    if not os.path.exists(title):
        os.mkdir(title)
    if isLeft:
        suffix = 'left'
    else:
        suffix = 'right'
    img.save(f'{title}/{name}_{suffix}.png')


def search_league(league_id):
    url = f'https://jbsl-web.herokuapp.com/leaderboard/api/{league_id}'
    res = requests.get(url).json()
    title = res['league_title']
    top8 = res['total_rank'][:8]
    for player in top8:
        print(f'start {player}')
        make_image(title, player, True)
        make_image(title, player, False)
        print(f'done {player}')


if __name__ == "__main__":
    league_id = sys.argv[1]
    # print(league_id)
    search_league(league_id)
