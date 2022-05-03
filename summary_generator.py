import json
from tkinter import Canvas
import requests
import io
import os
import re
from PIL import Image, ImageDraw, ImageFont
import sys


def text_over(img, text, textPos, fontsize, anchor='la'):
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
    draw.text(textPos, text, fill=textRGB, anchor=anchor, font=font)
    return img


def add_player_info(img, title, player, h_base, v_base):
    standing = player['standing']
    sid = player['sid']
    name = player['name']
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
    pos = list(map(int, [h_base, v_base]))
    print(pos)
    img.paste(cover_img, pos)
    pos[1] += 200
    for text in texts:
        img = text_over(img, text, pos, 25)
        pos[1] += 30
    return img


def search_league(league_id):
    url = f'https://jbsl-web.herokuapp.com/leaderboard/api/{league_id}'
    res = requests.get(url).json()
    title = res['league_title']
    canvasSize = (1920, 1200)
    backgroundRGB = (0, 0, 0, 0)
    img = Image.new('RGBA', canvasSize, backgroundRGB)
    text_over(img, f'{title} 本戦出場選手一覧', (1920/2, 50), 50, 'ma')
    top8 = res['total_rank'][:8]
    h_base = 50
    v_base = 150
    for i, player in enumerate(top8):
        if i == 4:
            h_base = 50
            v_base += 500
        print(f'start {player}')
        img = add_player_info(img, title, player, h_base, v_base)
        h_base += 1920/4

    if not os.path.exists(title):
        os.mkdir(title)

    img.save(f'{title}/summary.png')


if __name__ == "__main__":
    league_id = sys.argv[1]
    # print(league_id)
    search_league(league_id)
