
from Initialize import joinRoom, initsqlite, socket
from Settings import SHUFFLE_ON_START
from SongRequest import *
import string
import vlc
from threading import Thread
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


global nowplaying, paused
nowplaying = False
paused = False



if SHUFFLE_ON_START == True:
    from random import shuffle
    import sqlite3

    db = sqlite3.connect('songqueue.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM playlist ORDER BY RANDOM()''')
    listSongs = cursor.fetchall()
    shuffle(listSongs)
    sqlcommand = '''DELETE FROM playlist'''
    cursor.execute(sqlcommand)
    for item in listSongs:
        sqlcommand = '''
                        INSERT INTO playlist(song, key)
                        VALUES("{song_name}", "{key}");'''.format(song_name=item[1], key=item[2])
        cursor.execute(sqlcommand)
    db.commit()
    db.close()
    print(">> Backup Playlist has been shuffled.")






#>>>>COMMANDS
def test():
    print "WEIIIIIIINER"






def getUser(line):
    seperate = line.split(":", 2)
    user = seperate[1].split("!", 1)[0]
    return user



def getMessage(line):
    seperate = line.split(":", 2)
    message = seperate[2]
    return message





def getint(cmdarguments):
    import re
    try:
        out = int(re.search(r'\d+', cmdarguments).group())
        return out
    except:
        return None

def PONG():
    import threading
    s.send(bytes('PONG :tmi.twitch.tv\r\n'))
    threading.Timer(240, PONG).start()
PONG()

p = vlc.MediaPlayer()
initsqlite()


def main():
    global nowplaying, paused
    s = openSocket()
    joinRoom(s)
    readbuffer = ""


    while True:
        try:
            readbuffer = readbuffer + s.recv(1024)
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()




            for line in temp:

                if "PING" in line: #PING detection from twitch. Immediately sends a PONG back with the same content as the line. The PONG() Function is backup.
                    s.send("PONG %s\r\n" % line[1])

                else:
                    global user #All these things break apart the given chat message to make things easier to work with.
                    user = getUser(line)
                    message = str(getMessage(line))
                    command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                    cmdarguments = message.replace(command or "\r" or "\n", "")
                    getint(cmdarguments)

                    print(">> " + user + ": " + message)

                    if ("!sr" == command):
                        sr_getsong(cmdarguments, user)

                    if ("!addsong" == command):
                        sr_addsongtoplaylist(cmdarguments)


                    if ("!pause" in command):
                        p.set_pause(True)
                        nowplaying = False
                        paused = True

                    if ("!play" == command):
                        p.set_pause(False)
                        nowplaying = True
                        paused = False

                    if ("!clearqueue" == command):
                        sendMessage(s, "Cleared the song request queue.")
                        dosqlite('''DELETE FROM songs''')

                    if ("!veto" in command):
                        sendMessage(s, "Song Vetoed.")
                        p.stop()
                        paused = False
                        nowplaying = False

                    if ("!wrongsong" == command):
                        wrongsong(getint(cmdarguments), user)


                    if ("!clearsong" == command):
                        clearsong(getint(cmdarguments), user)

                    if ("!test" == command):
                        nptime = int(p.get_time())
                        nplength = int(p.get_length())
                        sendMessage(s, (str(nplength) + " - " + str(nptime)))


                    if ("!volume" == command):
                        volume(p, getint(cmdarguments))


                    if ("!volumeup" == command):
                        volumeup(p, getint(cmdarguments))


                    if ("!volumedown" == command):
                        volumedown(p, getint(cmdarguments))

                    if ("!nowplaying" == command):
                        with open("nowplaying.txt", "r") as f:
                            returnnp = f.readlines()
                            if not returnnp:
                                sendMessage(s, (user + " >> The music is currently paused."))
                            else:
                                sendMessage(s, (user + " >> " + returnnp[0]))








        except socket.error:
            print("Socket died")



def tick():
    import time
    global nowplaying, paused
    songtitle = ""
    while True:
        time.sleep(0.3) #Slow down the stupidly fast loop for the sake of CPU




        import sqlite3 #Open the db, get the song out
        from sqlite3 import Error
        db = sqlite3.connect('songqueue.db')
        cursor = db.cursor()
        cursor.execute('''SELECT id, name, song, key FROM songs ORDER BY id ASC''') #Pick the top song
        row = cursor.fetchone()
        db.close()
        if row == None: #>>>>>> DO THIS STUFF IF THE LIST IS EMPTY!
            playfromplaylist()





        if (paused == True or nowplaying == False):
            writenowplaying(False, "")

        if (nowplaying == True and paused == False):#Detect when a song is over
            writenowplaying(True, songtitle)
            time.sleep(0.3)
            nptime = int(p.get_time())
            nplength = int(p.get_length())

            if (nptime + 2300) > nplength: #Do this stuff when a song is over
                time.sleep(1.6)
                print("Song is over!")
                p.stop()
                global nowplaying
                nowplaying = False




        elif paused == False: # When a song is over, start a new song

            db = sqlite3.connect('songqueue.db')
            cursor = db.cursor()
            cursor.execute('''SELECT id, name, song, key FROM songs ORDER BY id ASC''') #Pick the top song
            row = cursor.fetchone()

            try:
                songtitle = row[2]
                songkey = row[3]
            except:
                print(">>>>>>BACKUP PLAYLIST IS EMPTY! ADD SOME SONGS TO IT WITH FillPlaylist.py or !addsong !!!! <<<<<<<<<<<<<<<<")
                return

            cursor.execute('SELECT id FROM songs ORDER BY id ASC LIMIT 1')
            row = cursor.fetchone()
            cursor.execute(('''DELETE FROM songs WHERE id={0}''').format(int(row[0]))) #Delete the top song
            db.commit()
            db.close()



            try:
                if validators.url(songtitle) == True: #TEST IF THE REQUEST IS A LINK
                    if "youtu" in songtitle: #IS IT A YOUTUBE LINK?
                        playurl = YouTube(songtitle).streams.filter(only_audio=True).order_by('abr').first().url #If it is, get the link with the best sound quality thats only audio
                        songtitle = YouTube(songtitle).title
                        writenowplaying(True, songtitle)
                    else:
                        playurl = songtitle
                        songtitle = "Online Music File"
                        writenowplaying(True, songtitle)
                else:
                    playurl = sr_geturl(songkey)
                    writenowplaying(True, songtitle)

                global p
                p = vlc.MediaPlayer(playurl)
                p.play()
                nowplaying = True


            except Exception as e:
                print e








t1 = Thread(target = main)
t2 = Thread(target = tick)


t1.start()
t2.start()