from __future__ import unicode_literals
from Initialize import *
api = initSetup()  # Run init setup to make sure everything is working before importing stuff
import time
import urllib.request, urllib.parse, urllib.error
from shutil import copyfile
import sqlite3
from sqlite3 import Error
import logging
import sys
import codecs
from Initialize import settings

logging.disable(sys.maxsize)

commands_SongRequest = {

    # Public SR Commands
    "!sr": ('sr.songrequest', 'cmdarguments', 'user'),
    "!songrequest": ('sr.songrequest', 'cmdarguments', 'user'),  # Alias
    "!wrongsong": ('sr.wrongsong', 'getint(cmdarguments)', 'user'),
    "!ws": ('sr.wrongsong', 'getint(cmdarguments)', 'user'),  # Alias
    "!nowplaying": ('sr.getnowplaying', 'None', 'user'),
    "!np": ('sr.getnowplaying', 'None', 'user'),  # Alias
    "!timeleft": ('sr.queuetime', 'getint(cmdarguments)', 'user'),
    "!tl": ('sr.queuetime', 'getint(cmdarguments)', 'user'),  # Alias
    "!queue": ('sr.queuelink', 'user', 'None'),
    "!q": ('sr.queuelink', 'user', 'None'),  # Alias
    "!songlist": ('sr.queuelink', 'user', 'None'),  # Alias

    # Showtime
    "!showtime": ("STREAMER", 'startsong', 'None', 'None'),  # Alias

    # NowPlaying Control
    "!play": ("MOD", 'play', 'None', 'None'),
    "!togglepause": ("MOD", 'togglepause', 'None', 'None'),
    "!p": ("MOD", 'togglepause', 'None', 'None'),
    "!pause": ("MOD", 'pause', 'None', 'None'),
    "!veto": ("MOD", 'veto', 'None', 'None'),

    # Volume Control
    "!volume": ("MOD", 'srcontrol.volume', 'getint(cmdarguments)', 'user'),
    "!v": ("MOD", 'srcontrol.volume', 'getint(cmdarguments)', 'user'),  # Alias
    "!volumeup": ("MOD", 'srcontrol.volumeup', 'getint(cmdarguments)', 'user'),
    "!vu": ("MOD", 'srcontrol.volumeup', 'getint(cmdarguments)', 'user'),  # Alias
    "!volumedown": ("MOD", 'srcontrol.volumedown', 'getint(cmdarguments)', 'user'),
    "!vd": ("MOD", 'srcontrol.volumedown', 'getint(cmdarguments)', 'user'),  # Alias

    # Playlist Control
    "!clearsong": ("MOD", 'sr.clearsong', 'getint(cmdarguments)', 'user'),
    "!cs": ("MOD", 'sr.clearsong', 'getint(cmdarguments)', 'user'),  # Alias
    "!plsr": ("MOD", 'sr.plsongrequest', 'cmdarguments', 'user'),
    "!plclearsong": ("MOD", 'sr.plclearsong', 'cmdarguments', 'user'),
    "!plcs": ("MOD", 'sr.plclearsong', 'cmdarguments', 'user'),  # Alias
    "!clearqueue": ("MOD", 'sr.clearqueue', 'None', 'None'),
    "!cq": ("MOD", 'sr.clearqueue', 'None', 'None'),  # Alias
}


def writenowplaying(isPlaying, song_name):
    with codecs.open("../Output/nowplaying.txt", "w", "utf-8") as f:
        if isPlaying == True:
            f.write(('{song_name}').format(song_name=song_name))
        else:
            f.truncate()


def getytkey(url):
    if "youtube" in url.lower():
        return (url.split("=")[1][:11])
    elif "youtu.be" in url.lower():
        return (url.split("e/")[1][:11])
    else:
        return None


def songtitlefilter(song_name, redo):
    blacklist = settings['BLACKLISTED TITLE CONTENTS'][:]
    results = api.search(song_name, settings['SONG BL SIZE'])['song_hits']
    songs = []
    for item in results:
        songs.append(item['track'])

    # Remove things from the blacklist if theyre explicitly requested
    for term in blacklist:
        if term.lower() in song_name.lower():
            blacklist.remove(term)

    # Iterate through the blacklisted contents, then the songs. Last song standing wins.
    for term in blacklist:
        if len(songs) == 1:
            break
        for song in reversed(songs):
            if len(songs) == 1:
                break
            if term.lower() in song['title'].lower():
                print((">Removed: " + song['title']))
                songs.remove(song)

    for item in songs:
        print((">Allowed: " + item['title']))
    print((">>>Playing: " + songs[0]['title']))
    return songs[redo]


def sr_geturl(songkey):
    try:
        stream_url = api.get_stream_url(songkey)
        return (stream_url)
    except Exception as e:
        print(e)


def saveAlbumArt(songkey):
    try:
        if (songkey[0] == "T") and len(songkey) > 20:  # If the key is from GPM - all GPM keys start with T.
            songinfo = api.get_track_info(songkey)
            imgLink = songinfo['albumArtRef'][0]['url']
            f = open('../Output/albumart.jpg', 'wb')
            f.write(urllib.request.urlopen(imgLink).read())
            f.close()
        else:  # Otherwise just use the generic image.
            copyfile('../Config/generic_art.jpg', '../Output/albumart.jpg')
    except TypeError:
        pass
    except:
        print("Error saving album art. Try removing and re-adding your backup playlist. SONGKEY = " + songkey)


def removetopqueue():
    if sqliteread('''SELECT count(*) from queue''')[0] > 0:
        row = sqliteread('''SELECT id, name, song, key FROM queue ORDER BY id ASC''')  # Pick the top song
        if row[1] == "BotPlaylist":  # If the list is empty but a song is loaded from playlist
            sqlitewrite(('''DELETE FROM queue WHERE id={0}''').format(int(row[0])))  # Delete the top song
        return False
    else:
        print("Nothing in backup playlist")


def getnewentry():
    if sqliteread('''SELECT count(*) from queue''')[0] > 0:
        result = sqliteread('SELECT id FROM queue ORDER BY id DESC LIMIT 1')
        return (str(result[0]))
    else:
        return ("Err")


def playfromplaylist():
    row = sqliteread('''SELECT id, song, key FROM playlist ORDER BY id ASC''')  # Pick the top song
    if row == None:  # >>>>>> DO THIS STUFF IF THE LIST IS EMPTY!
        return
    try:
        songtitle = row[1]
        songkey = row[2]
    except:
        return

    # Delete the top result
    row = sqliteread('SELECT id FROM playlist ORDER BY id ASC LIMIT 1')
    sqlitewrite(('''DELETE FROM playlist WHERE id={0}''').format(int(row[0])))  # Delete the top song
    sqlitewrite(('''INSERT INTO playlist(song, key) VALUES("{song_name}", "{key}");''').format(song_name=songtitle,
                                                                                               key=songkey))
    sqlitewrite(('''INSERT INTO queue(name, song, key) VALUES("BotPlaylist", "{song_name}", "{key}");''').format(
        song_name=songtitle, key=songkey))


class SRcontrol:  # Class for controlling currently playing audio
    def __init__(self):
        self.msg = ""
        self.songtitle = ""
        self.songkey = ""
        self.playurl = ""
        self.cachedVol = 85 # need variable for that
        self.isNotGPM = False


    def ps_youtube(self, yt):
        try:
            yturl = "http://youtube.com/watch?v=" + yt.videoid

            ydl_opts = {  # Set options for youtube-dl, these can be edited later.
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '320',  # Lower this if you have garbage internet
                }],
                'outtmpl': '%(title)s.%(etx)s',
                'quiet': True  # Set to false for troubleshooting
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(yturl, download=False)
            try:
                url = info['formats'][0]['url']
                if url.startswith("https://manifest.googlevideo.com"):
                    url = info['formats'][0]['fragment_base_url']
            except KeyError as e:
                sendMessage("Error getting Youtube song to play.[189]")
                print(e)
                return

            self.playurl = url
            self.isNotGPM = True
        except Error as e:  # Catch pafy errors
            sendMessage("Error getting Youtube song to play. [209]")
            print("Error likely with Pafy / YtDL. Error below.")
            print(e)
            return

    def playsong(self):
        row = sqliteread('''SELECT id, name, song, key FROM queue ORDER BY id ASC''')  # Pick the top song
        if row and len(row) > 2:
            self.songtitle = row[2]
            self.songkey = row[3]
        else:
            time.sleep(0.4)
            return
        sqlitewrite(('''DELETE FROM queue WHERE id={0}''').format(row[0]))  # Delete the top song

        try:  # Try Youtube
            self.ps_youtube(pafy.new(self.songkey, basic=True, size=False))
            self.isNotGPM = True

        except ValueError:  # Not Yt, try online and GPM

            # ONLINE
            if validators.url(self.songkey):
                self.playurl = self.songkey
                self.isNotGPM = True

            # GPM
            else:
                self.playurl = sr_geturl(self.songkey)


        self.instance = vlc.Instance()
        self.p = self.instance.media_player_new(self.playurl)
        self.p.audio_set_volume(self.cachedVol)
        self.p.play()
        saveAlbumArt(self.songkey)
        writenowplaying(True, self.songtitle)
        createsongqueue()
        return True

    # start intermission track at lower volume
    def startintermission(self):
        print("Starting intermission track")
        try:
            self.playurl = settings['ENABLE HOTKEYS']
            self.instance = vlc.Instance()
            self.p = self.instance.media_player_new("/Resources/intermission.mp3")
            self.p.audio_set_volume(40) #add intermission volume variable to cfg
            self.p.play()

        except:
            print("Starting intermission track failed")

        return True

    # stop intermission track
    # need to add ~2 sec volume fadeout
    def stopintermission(self):
        print("Stopping intermission track")
        try:
            self.p.stop()
        except:
            print("Stopping intermission track failed")

        return False

    def songover(self):
        print("Song is over!")
        # why and why here
        #time.sleep(settings['DELAY BETWEEN SONGS'])
        try:
            # Check if it should reset the volume to the cached volume
            if settings["YT VOL RESET"] and self.isNotGPM and (self.cachedVol != self.p.audio_get_volume()):
                print("Reset audio to cached volume of %s." % self.cachedVol)
                self.p.audio_set_volume(self.cachedVol)
            self.cachedVol = self.p.audio_get_volume()
            self.p.stop()
            self.isNotGPM = False
            time.sleep(settings['DELAY BETWEEN SONGS'])

        except AttributeError:
            print("Nothing is playing")

        return False

    def gettime(self):
        try:
            return int(self.p.get_time())
        except AttributeError:
            print("Nothing is playing")

    # -------------------------SONG REQUEST COMMANDS----------------------------------

    def volume(self, vol, user):
        try:
            if vol == None:
                return "Current volume: " + str(self.p.audio_get_volume())
            if (vol > 100) or (vol < 0):
                return "Invalid volume level. Must be between 0-100."
            self.p.audio_set_volume(vol)
            return "Music volume set to: " + str(vol)
        except AttributeError:
            return "Music needs to be playing before adjusting the volume."

    def volumeup(self, vol, user):
        try:
            if not vol:
                vol = settings['VOL INCREMENT']
            currentvolume = self.p.audio_get_volume()
            if (currentvolume + vol) > 100:
                self.p.audio_set_volume(100)
                print("Raised the volume to: 100")
                return "Raised the volume to: 100"
            self.p.audio_set_volume(currentvolume + vol)
            self.msg = "Raised the volume to: " + str(currentvolume + vol)
            return self.msg
        except AttributeError:
            return "Music needs to be playing before adjusting the volume."

    def volumedown(self, vol, user):
        try:
            if not vol:
                vol = settings['VOL INCREMENT']
            currentvolume = self.p.audio_get_volume()
            if (currentvolume - vol) < 0:
                self.p.audio_set_volume(0)
                print("Lowered the volume to: 0")
                return "Lowered the volume to: 0"
            self.p.audio_set_volume(currentvolume - vol)
            self.msg = "Lowered the volume to: " + str(currentvolume - vol)
            return self.msg
        except AttributeError:
            return "Music needs to be playing before adjusting the volume."

    def play(self):
        try:
            #writenowplaying(True, self.songtitle)
            self.p.set_pause(False)
            return "Resumed the music"
        except AttributeError:
            print("Nothing is playing")

    def pause(self):
        try:
            #writenowplaying(False, "")
            self.p.set_pause(True)
            return "Paused the music"
        except AttributeError:
            print("Nothing is playing")


class SRcommands:
    def __init__(self):
        self.db = None
        self.video = None
        global skiprequests, skipusers
        skiprequests = 0
        skipusers = []

    def requestChecks(self, user, songtime, key):
        self.db = sqliteread('''SELECT id, count(*) FROM queue WHERE key="%s" AND name!="BotPlaylist"''' % key)
        if self.db[1] > (settings['MAX DUPLICATE SONGS'] - 1):
            return user + " >> That song is already in the queue."
        if songtime > (settings['MAX SONG LENGTH'] * 60000):
            return user + " >> That song exceeds the maximum length of " + str(settings['MAX SONG LENGTH']) + " minutes."

    '''--------------------SONG REQUEST--------------------'''

    def songrequest(self, request, user):
        if request == "\r" or not request:  # Send a message if they request nothing
            return user + " >> " + settings['DEFAULT SR MSG']
        # Get the first argument for links
        requestArgs = (request.split())
        # Check for songs already in the queue
        if sqliteread('''SELECT count(*) FROM queue WHERE name="{0}"'''.format(user))[0] > (settings['MAX USER REQUESTS'] - 1):
            return user + " >> You already have " + str(settings['MAX USER REQUESTS']) + " songs in the queue."

        request = request.replace("\r", "")[1:]

        # YouTube
        try:
            yt = pafy.new(requestArgs[0], basic=True, size=False)
            songtime = int(yt.length) * 1000

            returnMsg = self.requestChecks(user, songtime, yt.videoid)
            if returnMsg:
                return returnMsg

            if settings['YT ENABLE']:
                # Add to queue
                removetopqueue()
                sqlitewrite(
                    '''INSERT INTO queue(name, song, key, time) VALUES("{user}", "{request}", "{key}", "{time}");'''.format(
                        user=user, request=(yt.title.replace('"', "'")), key=(yt.videoid.replace('"', "'")), time=songtime))
                return user + " >> Added: " + yt.title + " to the queue (YT). ID: " + getnewentry()
            else:
                return user + " >> Requests from youtube are disabled by the streamer, try !sr artist song"

        except:

            # Online
            if validators.url(requestArgs[0]):
                if not settings['MEDIA FILES ENABLE']:
                    return user + " >> Online Media Links are disabled by the streamer, you'll need to request something else."

                songtime = self.getsongtime("Online", requestArgs[0])
                returnMsg = self.requestChecks(user, songtime, requestArgs[0])
                if returnMsg:
                    return returnMsg

                # Get Title
                if len(requestArgs) > 1:
                    title = request.replace(requestArgs[0], '')[1:]
                else:
                    title = "Online Music File"
                # Add to queue
                removetopqueue()
                sqlitewrite(
                    '''INSERT INTO queue(name, song, key, time) VALUES("{user}", "{title}", "{request}", "{time}");'''.format(
                        user=user, title=title, request=(requestArgs[0].replace('"', "'")), time=songtime))
                return user + " >> Added " + title + " to the queue. ID: " + getnewentry()

            # GPM
            if settings['GPM ENABLE']:
                try:
                    top_song_result = songtitlefilter(request, 0)
                    key = top_song_result['storeId']
                    songtitle = str(top_song_result['artist'] + " - " + top_song_result['title'])
                # Unable to find song
                except IndexError:
                    if settings['YT IF NO RESULT']:
                        return self.youtubesr(request, user)
                    else:
                        return user + " >> No results found for that song. Please try a different one."
                else:
                    # Test if the song is already in the queue
                    songtime = int(api.get_track_info(key)['durationMillis'])
                    returnMsg = self.requestChecks(user, songtime, key)
                    if returnMsg:
                        return returnMsg


                    # Add song to the queue
                    removetopqueue()
                    sqlitewrite(
                        '''INSERT INTO queue(name, song, key, time) VALUES("{user}", "{request}", "{key}", "{time}");'''.format(
                            user=user, request=(songtitle.replace('"', "'")), key=(key.replace('"', "'")),
                            time=songtime))
                    return user + " >> Added: " + songtitle + " to the queue. ID: " + getnewentry()
            else:
                return self.youtubesr(request, user)

    def youtubesr(self, request, user):
        # Search YT
        try:
            ydl = youtube_dl.YoutubeDL({"default_search": "auto", "noplaylist": True, "quiet": True})
            ydlresult = ydl.extract_info(request, download=False)['entries'][0]
            key = ydlresult['id']
            songtime = ydlresult['duration'] * 1000
            title = ydlresult['title']
        except youtube_dl.utils.DownloadError:
            return ("No results for that request, try a different one.")

        returnMsg = self.requestChecks(user, songtime, key)
        if returnMsg:
            return returnMsg

        removetopqueue()
        sqlitewrite(
            '''INSERT INTO queue(name, song, key, time) VALUES("{user}", "{request}", "{key}", "{time}");'''.format(
                user=user, request=(title.replace('"', "'")), key=(key.replace('"', "'")), time=songtime))
        return user + " >> Added: " + title + " to the queue (YT). ID: " + getnewentry()

    '''--------------------QUEUE CONTROL--------------------'''

    def wrongsong(self, songid, user):
        if not songid:
            try:
                result = sqliteread(
                    'SELECT id, song FROM queue WHERE name="{0}"  ORDER BY id DESC LIMIT 1'.format(user))
                sqlitewrite('DELETE FROM queue WHERE id={0}'.format(str(result[0])))
                return user + ' >> Removed your request: "' + str(result[1]) + '" from the queue.'
            except Error as e:
                raise e
            except:
                return user + " >> Couldn't find your most recent request."
        else:
            try:
                result = sqliteread('SELECT song, name FROM queue WHERE id={0}'.format(songid))
                if user in result[1]:
                    sqlitewrite('DELETE FROM queue WHERE id={0}'.format(songid))
                    return user + ' >> Removed your request: "' + str(result[0]) + '" from the queue.'
                else:
                    return user + " >> You didn't request that song, you can't delete it!"
            except Error as e:
                raise e
            except:
                return user + " >> Couldn't find that request."

    def clearsong(self, songid, user):
        if not songid:
            try:
                result = sqliteread('SELECT id, song, name FROM queue ORDER BY id DESC LIMIT 1')
                sqlitewrite('DELETE FROM queue WHERE id={0}'.format(str(result[0])))
                return user + ' >> Removed the request: "' + str(result[1]) + '" requested by ' + str(
                    result[2]) + " from the queue."
            except Error as e:
                raise e
            except:
                return "Something messed up. Is the queue empty?"
        else:
            try:
                result = sqliteread('SELECT song, name FROM queue WHERE id={0}'.format(songid))
                sqlitewrite('DELETE FROM queue WHERE id={0}'.format(songid))
                return user + ' >> Removed the request: "' + str(result[0]) + '" requested by ' + str(
                    result[1]) + " from the queue."
            except Error as e:
                raise e
            except:
                return user + " >> Couldn't find that request."

    def queuetime(self, id, user):
        if not id:  # If there's no ID, get the total song
            data = sqliteFetchAll('''SELECT time FROM queue''')
        else:  # Get up to that song
            data = sqliteFetchAll('''SELECT time FROM queue WHERE id < {0}'''.format(id))

        if not data or not data[0][0]:
            if id:
                return user + " >> That ID is not in the queue."
            else:
                return user + " >> There are currently no songs in the queue."
        totaltime = 0
        for item in data:
            totaltime += int(item[0])
        seconds = round((totaltime / 1000) % 60)
        minutes = round((totaltime / (1000 * 60)) % 60)
        hours = round((totaltime / (1000 * 60 * 60)) % 24)
        return user + " >> There is about " + str(hours) + "h " + str(minutes) + "m " + str(
            seconds) + "s of songs in the queue."

    '''--------------------BACKUP PL CONTROL--------------------'''

    def plsongrequest(self, request, user):
        if request == "\r":  # Send a message if they request nothing
            return user + " >> " + " plsr functions just like !sr but adds songs to your playlist, not the queue."
        request = request.replace("\r", "")[1:]
        requestArgs = (request.split())

        # YouTube
        try:
            try:
                yt = pafy.new(requestArgs[0], basic=True, size=False)
            except OSError:
                return user + " >> That video is unavailable, or the bot cannot access it."
            # Duplicate
            self.db = sqliteread('''SELECT id, count(*) FROM playlist WHERE key="{0}"'''.format(yt.videoid))
            if self.db[1] > (settings['MAX DUPLICATE SONGS'] - 1):
                return user + " >> That song is already in the playlist. ID: " + str(self.db[0])
            # Add to queue
            sqlitewrite('''INSERT INTO playlist(song, key) VALUES("{request}", "{key}");'''.format(
                request=(yt.title.replace('"', "'")), key=(yt.videoid.replace('"', "'"))))
            return user + " >> Added: " + yt.title + " to the playlist (YT). ID: " + str(
                sqliteread('SELECT id FROM playlist ORDER BY id DESC LIMIT 1')[0])
        except ValueError:
            # Request is not a YT request, check for other URL

            # Online
            if validators.url(requestArgs[0]):
                # Duplicate
                self.db = sqliteread('''SELECT id, count(*) FROM playlist WHERE key="{0}"'''.format(requestArgs[0]))
                if self.db[1] > (settings['MAX DUPLICATE SONGS'] - 1):
                    return user + " >> That song is already in the playlist. ID: " + str(self.db[0])
                # Get Title
                if len(requestArgs) > 1:
                    title = request.replace(requestArgs[0], '')[1:]
                else:
                    title = "Online Music File"
                # Add to queue
                sqlitewrite('''INSERT INTO playlist(song, key) VALUES("{title}", "{request}");'''.format(title=title,
                                                                                                         request=(requestArgs[0].replace('"',"'"))))
                return user + " >> Added " + title + " to the queue. ID: " + str(
                    sqliteread('SELECT id FROM playlist ORDER BY id DESC LIMIT 1')[0])

            # GPM
            if settings['GPM ENABLE']:
                try:
                    top_song_result = songtitlefilter(request, 0)
                    key = top_song_result['storeId']
                    songtitle = str(top_song_result['artist'] + " - " + top_song_result['title'])
                # Unable to find song
                except IndexError:
                    if settings['YT IF NO RESULT']:
                        return self.plyoutubesr(request, user)
                    else:
                        return user + " >> No results found for that song. Please try a different one."
                    # Test if the song is already in the queue
                self.db = sqliteread('''SELECT id, count(*) FROM playlist WHERE key="{0}"'''.format(key))
                if self.db[1] > (settings['MAX DUPLICATE SONGS'] - 1):
                    return user + " >> That song is already in the playlist. ID: " + str(self.db[0])

                # Add song to the queue
                sqlitewrite('''INSERT INTO playlist(song, key) VALUES("{request}", "{key}");'''.format(
                    request=(songtitle.replace('"', "'")), key=(key.replace('"', "'"))))
                return user + " >> Added: " + songtitle + " to the playlist. ID: " + str(
                    sqliteread('SELECT id FROM playlist ORDER BY id DESC LIMIT 1')[0])
            else:
                return self.plyoutubesr(request, user)

    def plyoutubesr(self, request, user):
        try:
            ydl = youtube_dl.YoutubeDL({"default_search": "auto", "noplaylist": True, "quiet": True})
            ydlresult = ydl.extract_info(request, download=False)['entries'][0]
            key = ydlresult['id']
            title = ydlresult['title']
        except youtube_dl.utils.DownloadError:
            return ("No results for that request, try a different one.")

        # Check the queue to see if the song is already in there.
        self.db = sqliteread('''SELECT id, count(*) FROM playlist WHERE key="{0}"'''.format(key))
        if self.db[1] > (settings['MAX DUPLICATE SONGS'] - 1):
            return user + " >> That song is already in the playlist. ID: " + str(self.db[0])

        sqlitewrite('''INSERT INTO playlist(song, key) VALUES("{request}", "{key}");'''.format(
            request=(title.replace('"', "'")), key=(key.replace('"', "'"))))
        return user + " >> Added: " + title + " to the playlist (YT). ID: " + str(
            sqliteread('SELECT id FROM playlist ORDER BY id DESC LIMIT 1')[0])

    def plclearsong(self, songid, user):
        if not songid:
            try:
                result = sqliteread('SELECT id, song FROM playlist ORDER BY id DESC LIMIT 1')
                sqlitewrite('DELETE FROM playlist WHERE id={0}'.format(str(result[0])))
                return user + ' >> Removed your request: "' + str(result[1]) + '" from the backup playlist.'
            except Exception as e:
                print(e)
                return user + " >> Couldn't find the most recent request."
        else:
            try:
                result = sqliteread('SELECT song FROM playlist WHERE id={0}'.format(songid))
                sqlitewrite('DELETE FROM playlist WHERE id={0}'.format(songid))
                return user + ' >> Removed the song: "' + str(result[0]) + " from the queue."
            except Error as e:
                raise e
            except:
                return user + " >> Couldn't find that request."

    '''--------------------MISC--------------------'''

    def getnowplaying(self, x, user):
        with open("../Output/nowplaying.txt", "r", encoding="utf-8") as f:
            returnnp = f.readlines()
        if not returnnp:
            return user + " >> The music is currently paused."
        else:
            return user + " >> " + returnnp[0]

    def clearqueue(self, x, y):
        try:
            sqlitewrite('DELETE FROM queue')
            return "Cleared the current songrequest queue"
        except:
            return "There was some sort of issue clearing the queue."

    def queuelink(self, user, x):
        return user + " >> " + settings['QUEUE LINK']

    def getsongtime(self, title, key):
        songtime = -1
        try:
            if title:
                songurl = key
            else:  # Otherwise it's GPM
                songurl = sr_geturl(key)
            instance = vlc.Instance()
            media = instance.media_new(songurl)
            player = instance.media_player_new()
            player.set_media(media)

            # Start the parser
            media.parse_with_options(1, 0)
            cycle = 0
            while str(media.get_parsed_status()) != 'MediaParsedStatus.done':
                cycle += 1
                if cycle > 999999:
                    print("CRITICAL ERROR - GETSONGTIME IS BROKEN!")
                    break
            songtime = media.get_duration()
        # Let it be known to whatever brave adventurer is exploring my code, that this is the place that
        # Grant's sanity died for nearly two weeks straight.
        except Exception as e:
            print("GETSONGTIME ISSUE")
            print(e)
            return
        return (songtime - 2000)  # Most songs have a short offset.
