from aiogram import executor
from dispatcher import dp
from video_monitoring import video_alarm
import handlers

if __name__ == "__main__":
    dp.loop.create_task(video_alarm(10))
    print("OK")
    executor.start_polling(dp, skip_updates=True)
