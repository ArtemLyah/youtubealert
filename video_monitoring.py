from db import get_new_video
from dispatcher import bot
from aiogram import asyncio

async def video_alarm(time):
    while True:
        channels = get_new_video(time)
        for channel in channels:
            for user in channel[1]:
                for video in channel[2]:
                    text = f"New video was uploaded on {channel[0][3]}\nhttps://www.youtube.com/watch?v={video[0]}"
                    await bot.send_message(user[0], text)
        await asyncio.sleep(time*60-2)



# [
#   (   
#       82, 
#       'https://www.youtube.com/channel/UCvUNLcyWgJMmv51rz8Sbg4Q', 
#       'UUvUNLcyWgJMmv51rz8Sbg4Q', 
#       'uzumaki uchiha'
#   ), 
#   [('905143300',)], 
#   [['M-ZBD093u-o', 25]]
# ]
