import sqlite3
import json

import nextcord


# Create Banner from a picture and a text
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def create_banner(text):
    background = Image.open("./images/Banner.png")
    draw = ImageDraw.Draw(background)
    # get perfect font size
    font = ImageFont.truetype("./arial.ttf", size=int(background.size[1] / 2))
    # get text size
    text_size = draw.textsize(text, font=font)
    # get the middle of the image
    w, h = background.size
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (w - text_width) / 2
    text_y = (h - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    text = text.replace("#", "")
    text = text.replace(" ", "_")
    
    background.save(f"./images/Banner_{text}.png")
    return f"./images/Banner_{text}.png"
