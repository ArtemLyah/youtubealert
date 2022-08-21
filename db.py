import psycopg2
from youtubeapi import *

connection = psycopg2.connect(
    host = "ec2-44-206-137-96.compute-1.amazonaws.com",
    database = "d19bl2hpivscjk",
    user="gmjsofhzlwhkig",
    password="88f8d1e2dde1740481b28077fc401873054f8f852c77b8726fc467f2c039bbcb"
)
cursor = connection.cursor()
def add_new_channel(user_id, channel_link:str):
    cursor.execute(f"SELECT id FROM channels WHERE link = '{channel_link}'")
    channel_id = cursor.fetchone()
    # If the channel wasn't added
    # insert the channel into table "channels" 
    # get channel id and create user-channel relation
    if not channel_id:
        chl_name, pl_id = get_channel_info(channel_link)
        cursor.execute(f"INSERT INTO channels(name, link, playlist_id) VALUES('{chl_name}', '{channel_link}', '{pl_id}')")
        cursor.execute(f"SELECT id FROM channels WHERE link = '{channel_link}'")
        channel_id = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO user_channel_relations(user_id, channel_id) VALUES('{user_id}', '{channel_id}')")
        connection.commit()
        return 1, chl_name
    # If the channle is exist check on user-channel relations
    else:
        channel_id = channel_id[0]
        cursor.execute(f"SELECT id FROM user_channel_relations WHERE user_id = '{user_id}' AND channel_id = {channel_id}")
        # if user_channel relations exist return channel name and status 0 - relation hasn't added
        res = cursor.fetchone()
        if res:
            cursor.execute(f"SELECT name FROM channels WHERE id = {channel_id}")
            return 0, cursor.fetchone()[0]
        # relations don't exist create relation and return channel name and status 1 - relation has been added
        else:
            cursor.execute(f"INSERT INTO user_channel_relations(user_id, channel_id) VALUES('{user_id}', '{channel_id}')")
            connection.commit()
            cursor.execute(f"SELECT name FROM channels WHERE id = {channel_id}")
            return 1, cursor.fetchone()[0]
def view_channels(user_id):
    cursor.execute(f"""SELECT channels.name, channels.link FROM user_channel_relations 
                INNER JOIN channels ON user_channel_relations.channel_id=channels.id 
                WHERE user_id='{user_id}'""")
    return cursor.fetchall()
def delete_channel(user_id, channel_link=None, channel_name=None):
    if channel_link:
        cursor.execute(f"SELECT id FROM channels WHERE link = '{channel_link}'")
        channel_id = cursor.fetchone() 
    elif channel_name:
        cursor.execute(f"SELECT id FROM channels WHERE name = '{channel_name}'")
        channel_id = cursor.fetchone()
    if not channel_id:
        return 0
    else:
        cursor.execute(f"SELECT id FROM user_channel_relations WHERE user_id = '{user_id}' AND channel_id = '{channel_id[0]}'")
        if cursor.fetchone():
            cursor.execute(f"DELETE FROM user_channel_relations WHERE user_id = '{user_id}' AND channel_id = '{channel_id[0]}'")
            connection.commit()
            return 1
        else:
            return 0

def add_user_settings(user_id):
    cursor.execute(f"SELECT id FROM user_settings WHERE user_id='{user_id}'")
    if not cursor.fetchone():
        cursor.execute(f"INSERT INTO user_settings(user_id) VALUES('{user_id}')")
        connection.commit()
    return 1
def get_user_settings(user_id, args:list):
    rows = ",".join(args)
    cursor.execute(F"SELECT {rows} FROM user_settings WHERE user_id='{user_id}'")
    return cursor.fetchone()
def set_user_settings(user_id, **kwargs):
    s = ""
    for item in kwargs.items():
        s += f"{item[0]}={bool(item[1])},"
    cursor.execute(f"UPDATE user_settings SET {s[:-1]} WHERE user_id='{user_id}'")
    connection.commit()
    return 1

def get_new_video(time):
    cursor.execute("""SELECT chl.id, chl.link, chl.playlist_id, chl.name 
                    FROM channels as chl
                    INNER JOIN user_channel_relations as ucr ON chl.id=ucr.channel_id""")
    channels = cursor.fetchall()
    if not channels:
        return []
    for chl in channels:
        new_videos = check_on_new_video(chl[2], time)
        if new_videos:
            cursor.execute(f"SELECT user_id FROM user_channel_relations WHERE channel_id={chl[0]}")
            yield [chl, cursor.fetchall(), new_videos]
    return []



    

