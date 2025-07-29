
import ctypes
import win32con
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import randfacts
import textwrap
import json
import os
import time

def load_settings(file_path="settings.json \n"):
    with open(file_path, 'r') as f:
        settings = json.load(f)
        return settings

def getWallpaper():
    wallpaper_path = ctypes.create_unicode_buffer(512) #512 is what is recommended, idk exactly how these work
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(wallpaper_path), wallpaper_path, 0)
    return wallpaper_path
    
def makeWallpaper(text):
    settings=load_settings()
    image_path = getWallpaper().value
    img = Image.open(image_path)
    font = ImageFont.truetype(settings.get('font'), 50)
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)
    image_path = getWallpaper().value  
    t_height = settings.get('fontsize')

    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    
    draw = ImageDraw.Draw(img)

    line_list = textwrap.wrap(text, 45)
    positionY = (img_height - t_height)/2

    for line in line_list:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        t_width = right - left
        x_position = (img_width - t_width) / 2
        draw.text((x_position, positionY), line, (255, 255, 255), font=font)
        positionY += 80

    img.save('generated/generated_wallpaper.jpg')

def setWallpaper():
    SPI_SETDESKWALLPAPER = 20  
    SPIF_UPDATEINIFILE = 0x01  
    SPIF_SENDWININICHANGE = 0x02  
    image_path = os.path.abspath('generated/generated_wallpaper.jpg')
    print(f"Attempting to set wallpaper from: {image_path}")
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
    print("Set the new wallpaper!")

def getFact ():
    return randfacts.get_fact()

settings=load_settings()
interval = 60*(settings.get('interval'))

def main():
    while True:
        user_input = input("Please type 'y' or 'yes' to generate a wallpaper.")
        if user_input == "y" or user_input == "yes":
            makeWallpaper(getFact()) 
            setWallpaper()
        else:
            print("please enter a valid input!")


if __name__ == "__main__":
    main()



