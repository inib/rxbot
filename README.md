
# **RXBot**

Hi, thank you for choosing RXBot! This documentation serves to help you understand what the bot is, what it can do, and how to use it, with the instructions being as simple and clear as possible.

RXBot is a song request bot for Twitch streamers: viewers can request songs in chat, and they will be added to a queue for the streamer to listen to while they stream. What makes RXBot unique is that it supports not only YouTube, but Google Play Music as well (though you must have a subscription to use that functionality). It's also very lightweight, so it will have virtually no impact on system performance.

⚠️ This project is still in early development, so despite pre-release testing, it may not function as expected. Please report bugs using Github's *Issues* tab, or in the [Rxbots Discord](https://discord.gg/8FRQBJy). ⚠️

*(Readme last updated for v3.2.3)*

-----

## Requirements

Once you download the bot, make sure you have all the requirements installed before running it:

• [**Python 3.7.0**](https://www.python.org/downloads/release/python-370/) is what the bot runs off of. If you have an older Python version like 2.7.9, and you don't need that specific version, uninstall it *before* installing 3.7.0. Will potentially save headaches in the future.

• [**VLC Media Player**](https://www.videolan.org/vlc/index.html) needs to be *installed*, but it does not need to actually be *running* alongside the bot for it to work.

• [**Git**](https://git-scm.com/downloads) is required to install and update some requirements.

• Finally, run **Install_Requirements.bat** in the bot's folder. If you wish, you can delete this file and **requirements.txt** afterwards, as they are no longer needed.

## First-Time Setup

*(Make sure you read this section and the* ***Settings*** *section before attempting to use your bot.)*

Before doing anything, you need to create a Twitch account for your bot to use. Don't use the account you'll actually be streaming from. It would probably be a good idea to make your bot a chat moderator. And if you use the BetterTTV extension, make sure to [add your new bot.](https://betterttv.com/dashboard/bots)

Next, if you *don't* want to use Google Play Music, open **Settings.py** in any text editor, such as Notepad++. Change `GPM_ENABLE` to False, this will disable GPM functionality. Now, run the bot by opening **RUN.bat** in the bot's folder. If you disabled GPM, skip the next paragraph.

The first time you run it, the bot will tell you to go to [this page](https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fskyjam&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&client_id=228293309116.apps.googleusercontent.com&access_type=offline) to generate an oauth link. You need a Google Play Music subscription to use its functionality— if you don't have one, please read the previous paragraph and skip this one. Log in with your Google Play Account and follow all the prompts until it gives you a code. Copy that code, paste it in the bot window, and press Enter. If you entered it correctly, the bot will tell you that your backup playlist is empty. Close the bot so we can fix that.

If there are no song requests in the queue, the bot will play songs from your backup playlist. Since this is your first time using the bot, your backup playlist is empty. Open **Run_PlaylistEditor.bat**, and it will present you with four options: `1. Fill Playlist || 2. Update Playlist || 3. Shuffle Playlist || 4. View Playlist || 5. Clear Playlist` To add songs, type 1 and hit enter. The bot will then detect all playlists on your Google Play Music account (only playlists you've created, not ones you follow). Type the number of the playlist you wish to import and hit enter. Once the bot is finished importing (it should take less than a second), it will close itself, but you can re-open it and add import more playlists if you wish. Note that song files you've *uploaded* to your GPM account will not work, but you can add those songs to the bot via Youtube or uploaded files (more on that later). For now, it's time to adjust your settings.

## Settings

The **Settings.py** file is where you can adjust your personal settings for the bot. Make sure you read this section completely, as you *need* to change some of these for the bot to work in your channel. To edit this file, use a program such as IDLE or Notepad++.

##### BOT

`PORT = 80` || The bot connects to Twitch through this port. 80 will already be open on most networks, so that is the default setting. If 80 doesn't work, try 6667. If you want an SSL connection, use 443 or 6697.

`BOT_OAUTH = ""` || This is your bot's Twitch OAuth token. To put it simply, it's a password that only *this bot* can use to sign into your bot's Twitch account. [Click here to generate your oauth token](https://twitchapps.com/tmi/) (make sure you sign in with ***your bot's account,*** not your own). Once it's generated, copy it and paste it between the quotes.

`BOT_NAME = ""` || Your bot's Twitch username. Put it between the quotes.

`CHANNEL = ""` || Your Twitch username. Put it between the quotes.

`GPM_ENABLE = True` || Turn Google Play Music integration on or off. This *must* be set to `False` if you do not have a Google Play Music subscription.

##### SONGREQUEST

`MAX_DUPLICATE_SONGS = 1` || The same song cannot be in the queue more than this many times. Most sane users will want to keep this set to 1.

`MAX_REQUESTS_USER = 5` || This is the maximum number of songs a single user can have in the queue at a time.

`SHUFFLE_ON_START = True`| If set to true, the bot will automatically shuffle your backup playlist every time you open it. If set to false, your songs will play in the same order every time.

`DELAY_BETWEEN_SONGS = 0.5` || This is the number of seconds between the current song ending, and the next song beginning. 0.5 should be fine for most users.

`VOL_INCREMENT = 5` || Adjusts how much the volume will change when using a volume hotkey, or `!volumeup`/`volumedown`. For example: if you have this set to 5, and your volume is at 50, hitting your volume up hotkey will change the volume to 55.

`MAXTIME = 10` || This is the maximum song length, in minutes. If a user tries to request a song that exceeds this length, it will be rejected, and not added to the queue.

`YT_IF_NO_RESULT = True` || If a user's request is not found on Google Play Music, the bot will search the request on Youtube instead, and add the top result to the list. If you don't want that feature, change this setting to `False`.

`MEDIA_FILE_ENABLE = True` || Sets whether or not users are allowed to request uploaded music file links. Enabling this gives users more options, but can also be easily abused. Use with caution.

`QUEUE_LINK = ""` || There is  a file called **SongQueue.xlsx** in the bot's Resources folder, which contains the whole queue in a readable format. We recommend using something like [Google Drive]([https://www.google.com/drive/download/backup-and-sync/](https://www.google.com/drive/download/backup-and-sync/)) to upload the file every time it updates. Get the shareable link to the uploaded file, and paste it between the quotes to set your queue link, which users can view with `!queue`.

`DEFAULT_SR_MSG = ""` || The message that will show up if a user types `!sr` or `!songrequest` by itself. Put your message between the quotes.

`GPM_PLAYLIST = ""` || This is the name of your main Google Play Music playlist. When you choose `2. Update Playlist` in the playlist editor, the bot will check this playlist for any new songs, and add them to your bot's backup playlist. Put your playlist name between the quotes.

##### TITLE BLACKLIST FILTER

`SONGBLSIZE = 8` || When a user requests a song via searching, the song they typed is searched on Google Play Music, and the bot picks the top result. However, the top result is sometimes a cover, remix, live performance, etc. which the user will probably not want. If this setting is above 1, the bot will take that many results, and sort through them using your blacklisted terms. So for example, if you have the word "remix" set as a blacklisted term, the bot will prioritize search results *without* the word "remix" in them. The higher this number is set, the more accurate your search results will be, but the slower the bot will respond to them. We recommend a setting between 3 and 8.

`BLACKLISTED_SONG_TITLE_CONTENTS` || These are terms blacklisted from GPM search results. There are a few terms already blacklisted by default, but you can remove them if you wish, and of course add new ones. Each blacklisted term should be on its own line— just make sure the formatting matches that of the terms that are there by default.  
Note that the terms are in order from most-hated to least-hated. For example: If "remix" is at the top of the list, and "live" is at the bottom, the bot would prioritize adding a song with "live" in the title over one with  "remix".

##### GENERAL

`MODERATORS` || A list of users that have moderator permissions inside the bot, letting them use bot-only commands. Chat moderators will be added to this list automatically once the bot detects them in the viewer list (this can take a few minutes), but you can also manually add users if you want them to have moderator permissions in the bot, but not in your chat. Each user should be on its own line.

##### HOTKEYS

`ENABLE_HOTKEYS = False` || Enable or disable hotkeys for pausing, adjusting the volume, skipping songs, or removing the last song added to the queue.  If this is set to `True` and you do not have a key binding for *all* of the hotkey functions, the bot will throw an error on startup, but the hotkeys you *have* bound will still function.  
Formatting for a keybinding is `('modifier', 'key')`, where the modifier can be `control`, `shift`, or `alt`. If you don't want a modifier, format it like `('key',),`. [List of all key IDs here.](http://bit.ly/2HfPiSZ)
Note that you can make a hotkey for *any* command, not just the ones listed here by default. Just make sure to format custom hotkeys correctly, one hotkey on each line. And if you don't want any of the default hotkeys listed, you can simply delete the ones you don't want.

`!togglepause` || Pause/play the music.

`!veto` || Skips the current song.

`!clearsong` || Removes the last song added to the queue.

`!vu` || Turns the volume up.

`!vd` || Turns the volume down.

`OUTPUT_HOTKEYS` || Normally when a command is executed via hotkey, it will not output anything to chat. If you make a hotkey of a command that you *want* to output to chat (for example, `!queue`), add that command to this list, one per line.

## Updating to a Newer Version

If a new update releases for RXBot, that likely means bugs have been fixed and/or new features have been added. Here's a short guide on updating:

1. Backup your current bot installation! Simply copy the folder, and keep it to the side just in case you need to roll back or bring over any files.  
2. Download the zip of the new version from GitHub, and while you're here, look at the version number written next to the **Settings.py** file. Is it older than the version you're updating to? If so, that's good.  
3. Overwrite your old files with the new files. If **Settings.py** is still for an older version, you don't need to overwrite your current one. If you *do* need to update the file, then you will have to manually copy over your settings from your old file to the new one.

## Commands

This is a list of commands for the bot, which users will type into Twitch chat. Alternatively, you can type them directly into the bot console. Whenever you wish to close the bot, enter `quit` into the console window to properly clear some files (this will **not** clear the song request queue, don't worry).

##### SONGREQUEST

`!sr` or `!songrequest` || This is the command users will type to request songs. They type the command, then the song they want to request.  
**Google Play Music:** Following the command with a search term will add the song from Google Play Music. For example:`!sr Ginuwine Pony` will search "Ginuwine Pony" on Google Play Music, and add the best result. Users can also add their own blacklisted terms to their search by putting a hyphen before the word they wish to exclude. For example: `!sr Ginuwine Pony -remix` will look up "Ginuwine Pony" on Google Play Music, but will exclude all search results containing the word "Remix" in the title.   
**Youtube:** Instead of looking up a song, users can instead paste a Youtube link. For example: `!sr https://www.youtube.com/watch?v=lbnoG2dsUk0` 
**Uploaded Music File:** If you upload a music file (.mp3, .wav, etc.) to the internet and can get a direct streaming link to it, you can request that as well. For example: You can upload your song file to a website like [Instaudio](https://instaud.io/), then request the song with the direct streaming link, like so: `!sr https://instaud.io/_/3nOe.mp3`  

Note that every song in the queue has an ID, which can be used in other commands. This ID is *not* based on the song's current position in the queue, and does not change. The ID is shown when the song is requested.

`!np` or `!nowplaying` || Displays the currently-playing song in chat. Note: the current song is saved to the **nowplaying.txt** file in the bot's Output folder, so you can add this as a text source in OBS (or your streaming program of choice) to display the current song on screen.  
The bot will also output the current song's album art to **albumart.jpg** in the bot's Output folder. If a song does not have album art (ex. if it's a Youtube request), the file will be generic album art. You can set your generic album art by editing **generic_art.jpg** in the bot's Resources folder, just make sure to keep the resolution 512x512.

`!q` or `!queue` || Displays the link to your uploaded song queue in chat. Set this link in the **Settings.py** file with the `QUEUE_LINK` setting.

`!tl` or `!timeleft` || Displays how much time is left on the current song. Putting a song ID after the command will display the combined length of all songs leading up to that one, i.e. how long until that song begins playing (assuming no pausing or skipping, of course).

`!ws` or `!wrongsong` || If a user requests a song, but the search does not yield the correct song, the user can type this command to remove the last song they requested from the queue. They can also add a song ID after the command, if they wish to remove one of their requests that isn't the most recent one. For example, `!wrongsong 7` will remove song 7 from the queue, assuming the same user requested it.

`!cs` or `!clearsong` **(Mod Only)** || Removes the last song added to the queue, regardless of who requested it. Can also add a song ID after the command, if they wish to remove a song besides the most recent one. For example: `!clearsong 7` will remove song 7 from the queue.

`!plsr` **(Mod Only)** || Functions like `!sr`, but adds the song to the backup playlist rather than the song request queue.

`!plclearsong` **(Mod Only)** || Functions like `!clearsong`, but removes the most recent song added via `!plsr`.

`!volume` or `!v` **(Mod Only)** || Doing the command by itself will display the current music volume in chat. Adding a number after the command will set the volume to that number. For example: `!volume 75` will set the volume to 75 (out of 100).

`!volumeup` or `!vu`/`!volumedown` or `!vd` **(Mod Only))** || Turn the music volume up or down. Doing the command by itself will adjust the volume based on your `VOL_INCREMENT` setting, but adding a number after the command will adjust the volume by that increment. For example: if your volume is at 50, `!volumeup 20` will change the volume to 70.

`!veto` **(Mod Only)** || Skip the current song.

`!pause` **(Mod Only)** || Pause the music.

`!play` **Mod Only)** || Play the music.

`!p` or `!togglepause` **(Mod Only)** || Plays the music if it's paused, or pauses the music if it's playing. Mainly used for a hotkey.

`!clearqueue` **(Mod Only)** || Removes all songs from the queue (this will not skip the current song).

`!clearplaylist` **(Mod Only)** || Removes all songs from the backup playlist.

##### MISC

`!ping` || Makes the bot respond with "Pong." Use to test if your bot is still connected.

`!uptime` || Display in chat how long the current stream has been live.

`!roll` || Have the bot roll some dice— any amount of dice, any number of sides, and any modifier(s). For example, `!roll 3d20+9` will roll three 20-sided dice, and add nine to the result. Supported modifiers are add (+), subtract (-), multiply (*), and divide (/). Can only use one modifier per command.

## FAQ/Troubleshooting

If you wish, you can join the [Rxbots Discord](https://discord.gg/8FRQBJy) for help with the bot. Use the **#dev-chat** channel to ask questions, report bugs, or suggest new features.

**Q:** My bot crashes on startup!  
**A:** Reinstall Python 3.7.0. If that doesn't work, please contact us in the Discord.

**Q:** The bot outputs this error when a song starts: `prefetch stream error: unimplemented query (264) in control`  
**A:** This error is 100% harmless, and can safely be ignored. It seems to just be an output error within VLC, nothing we can fix.

**Q:** The bot outputs a *bunch* of `main libvlc error`s when a song is requested, but still seems to work.  
**A:** Try re-installing VLC, that seems to fix it. These errors *also* seem to be completely harmless, as we've yet to encounter any actual problems with them, but better safe than sorry. 

**Q:** The bot gives an error when attempting to play age-restriced Youtube videos! 
**A:** This is most likely a problem with pafy, one of the bot's dependencies. Run **FixAgeRestrict.bat**. If that doesn't fix it, contact us.

**Q:** I'm receiving an error that begins with `Unhandled exception in thread started by <bound method SystemHotkey._nt_wait`  
**A:** This is caused by another program using the same hotkeys you have set in RXBot. Either close the program(s) with the shared hotkeys, or rebind them.

**Q:** I get an error that has a bunch of URLs, and says "Error saving album art. Try removing and re-adding your backup playlist." 
**A:** Google Play Music will occasionally delete and re-add songs to give albums different names, album art, etc. When it does this, it changes the ID of the song (which is what's stored in your backup playlist). If you're seeing a few of these errors popping up, just clear your backup playlist and re-import it using **PlaylistEditor.py**.

**Q:** Hotkeys don't work while I'm in certain programs!  
**A:** This is usually because the program is being run as admin, not much we can do there. If you want to try running the bot as admin, you must first edit **RUN.bat** and replace `Run.py` with the full file directory, [like this.](https://i.imgur.com/kcu4Grv.png) Then, right click **Run.bat** and select "Run as Administrator".

**Q:** Is this bot purely for song requests?  
**A:** At the moment, song requests are the main priority for RXBot. We do plan to add normal commands later on though, so stay tuned!

**Q:** Why use Google Play Music instead of the more popular Spotify?  
**A:** A while back, Spotify removed their public API, meaning that Spotify integration in any unauthorized program is impossible. Google Play Music, on the other hand, does *not* suck, and has a free-to-use public API.

## Credits and Stuff
Grant Fowler, aka [**Rxbots**](https://www.twitch.tv/rxbots) - Sole creator of the bot.

Michael Balas, aka [**iCeCoCaCoLa64**](https://www.twitch.tv/icecocacola64) - Ideas, motivation, testing, and documentation (hi there 👋🏻).

[**kc0zhq**](https://www.twitch.tv/kc0zhq) - Coding help and motivation.

[**Grrenix**](https://www.twitch.tv/Grrenix) - Coding help and motivation.

**StreamLabs Chatbot** - For becoming such ungodly amounts of terrible that you inspired a random college student to become a coding God.

If you wish to donate to this project, go to [the Rxbots Twitch channel](https://www.twitch.tv/rxbots) and click the "Donations" panel below the stream. It's absolutely not necessary, but know that we really appreciate it!
