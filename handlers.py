from aiogram import filters, types
from dispatcher import dp
import db 

KEYBOARD = types.ReplyKeyboardMarkup([
        [types.KeyboardButton("Add a channel")], 
        [types.KeyboardButton("View channels")], 
        [types.KeyboardButton("Delete a channel")]
    ], resize_keyboard=True)

@dp.message_handler(filters.Command("start"))
async def start(message:types.Message):
    db.add_user_settings(message.chat.id)
    await message.answer("Hello I am YouTube Bell bot.\nI am following new videos of YouTube channels. ",
                        reply_markup=KEYBOARD)
# manage channels
@dp.message_handler(filters.Text("Add a channel") | filters.Command("add"))
async def add_channel(message:types.Message):
    db.set_user_settings(message.chat.id, is_add_channel=1)
    await message.answer("Add a new channel.\nWrite a link of a channel.")

@dp.message_handler(filters.Text("View channels") | filters.Command("view"))
async def view_channels(message:types.Message):
    channels = db.view_channels(message.chat.id)
    s = "YouTube notifications of channels.\n"
    entities = []
    for channel in channels:
        s += channel[0]+"\n"
        entities.append(types.MessageEntity(type="text_link", offset=len(s)-len(channel[0])-1, length=len(channel[0]), url=channel[1]))
    await message.answer(s, entities=entities, reply_markup=KEYBOARD)

@dp.message_handler(filters.Text("Delete a channel") | filters.Command("delete"))
async def delete_channels(message:types.Message):
    db.set_user_settings(message.chat.id, is_delete_channel=1)
    await message.answer("Delete a channel.\nWrite a name or link of a channel.")
#=============================================================================================
async def add_channel(message, chn_link):
    status, chl_name = db.add_new_channel(message.chat.id, chn_link)
    if status:
        await message.answer(f"Channel {chl_name} was successfully added.\nNow wait for new videos...", reply_markup=KEYBOARD)
    else:
        await message.answer(f"You already have the channel {chl_name}", reply_markup=KEYBOARD)
async def delete_channel(message, chn_link):
    res = db.delete_channel(message.chat.id, channel_link=chn_link)
    if res:
        await message.answer("Channel was successfully deleted", reply_markup=KEYBOARD)
    else:
        await message.answer("You don't have the channel", reply_markup=KEYBOARD)
#=============================================================================================
@dp.message_handler(filters.Text)
async def get_text(message:types.Message):
    if "https://www.youtube.com/" in message.text or "https://youtube.com/" in message.text:
        if "https://www.youtube.com/watch?" in message.text:
            await message.answer("This is YouTube video. Write here link of the channel.", reply_markup=KEYBOARD)
        chn_link_details = message.text.removeprefix("https://www.youtube.com/").split("/")
        if not chn_link_details:
            chn_link_details = message.text.removeprefix("https://youtube.com/").split("/") 
        if chn_link_details[0] in ["c", "channel", "user"]:
            try:
                chn_link = "https://www.youtube.com/"+chn_link_details[0]+"/"+chn_link_details[1]
                if db.get_user_settings(message.chat.id, ["is_add_channel"])[0]:
                    await add_channel(message, chn_link)
                elif db.get_user_settings(message.chat.id, ["is_delete_channel"])[0]:
                    await delete_channel(message, chn_link)
                db.set_user_settings(message.chat.id, is_add_channel=0)
                db.set_user_settings(message.chat.id, is_delete_channel=0)
            except Exception as ex:
                await message.answer("Oops... Something goes wrong. Try to repeat later.")
                print(ex.with_traceback())
        else:
            await message.answer("It isn't channel's link. Please go to the channel and write here its link")
    else:
        await message.answer("It isn't channel's link. Please go to the channel and write here its link")
    
    