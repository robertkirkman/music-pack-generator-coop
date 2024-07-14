#!/usr/bin/env python3
import sys
import os
import shutil
import re
import random
import jinja2
import unicodedata
from yt_dlp import YoutubeDL

levels = {
    "9": "BobOmb",
    "5": "CoolCool",
    "6": "CastleWalls",
    "24": "ThwompFort",
    "10": "Snowman",
    "17": "Bowser1",
    "19": "Bowser2",
    "-2": "PowerUp",
    "26": "Courtyard",
    "11": "WetDry",
    "27": "Slide",
    "12": "JollyRoger",
    "23": "DireDireDocks",
    "20": "SecretWatter",
    "4": "BigBoo",
    "7": "HazyMaze",
    "22": "LethalLava",
    "8": "ShiftingSand",
    "36": "TallTallMountain",
    "13": "TinyHugeIsland",
    "14": "TickTockClock",
    "15": "RainbowRide",
    "21": "Bowser3",
}


def generate(playlistUrl, dest, interactive):
    # generate colors and pack name
    randomColor1 = randomcolor()
    randomColor2 = randomcolor()
    randomColor3 = randomcolor()
    randomColor4 = randomcolor()
    packName = "owokitty-generated-music-pack-" + randomColor1

    # set up sound folder
    if "http" in playlistUrl:
        sourceFolder = "downloads/"
    else:
        sourceFolder = playlistUrl + "/"
    trackFilenames = os.listdir(sourceFolder)
    trackFilenames = [file for file in trackFilenames if file[-4:] == ".mp3"]

    # generate sound folder
    tracks = generate_album(sourceFolder, trackFilenames, dest + packName + "/sound/")

    # in interactive mode, keep regenerating the sound folder until done
    if interactive:
        accept = False
        while not accept:
            print("Generated Tracklist:")
            for track in tracks:
                print(levels[track["levelNum"]].ljust(16, " ") + ": " + track["name"])
            if input("Is this acceptable? (yes/no): ") == "yes":
                accept = True
                break
            else:
                tracks = generate_album(
                    sourceFolder, trackFilenames, dest + packName + "/sound/"
                )

    # generate main.lua
    mainLua = (
        jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
        .get_template("template.lua.j2")
        .render(
            randomColor1=randomColor1,
            randomColor2=randomColor2,
            randomColor3=randomColor3,
            randomColor4=randomColor4,
            tracks=tracks,
            playlistUrl=playlistUrl,
        )
    )
    with open(dest + packName + "/main.lua", "w") as f:
        f.write(mainLua)


def generate_album(source, trackFilenames, dest):
    newFilenames = []
    newFilenames.extend(trackFilenames)
    random.shuffle(newFilenames)
    try:
        shutil.rmtree(dest)
    except Exception as e:
        pass
    os.makedirs(dest)
    tracks = []
    for level in levels:
        filename = newFilenames.pop(0)
        slugname = slugify(filename)
        sourceFile = source + filename
        destinationFile = dest + slugname
        shutil.copyfile(sourceFile, destinationFile)
        if len(tracks) < len(levels):
            tracks.append({"levelNum": level, "name": slugname})
        else:
            break
    return tracks


def download(args, all):
    ydl_opts = {
        "external_downloader": {"default": "ffmpeg"},
        "external_downloader_args": {"ffmpeg": ["-t", "90", "-b:a", "128k"]},
        "format": "mp3/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "outtmpl": "downloads/%(uploader)s-%(title)s.%(ext)s",
        "ignoreerrors": True,
    }

    if all:
        ydl_opts["playlist_items"] = "1:" + str(len(levels))

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(args)


# deterministically convert strings into readable equivalents that are filename-friendly
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s.]", "", value.lower())
    return re.sub(r"[.\s]+", ".", value).strip("._")


def randomcolor():
    return f"{random.randrange(0x1000000):06x}"


def main():
    if len(sys.argv) < 2:
        print(
            "usage: ./music-pack-generator.py [yt-dlp playlist url | local album directory] (--interactive)"
        )
        exit(1)

    destination = "./"
    android_destination = "/storage/emulated/0/com.owokitty.sm64excoop/user/mods/"
    interactiveFlag = "--interactive"
    allPlaylistTracksFlag = "--all"
    interactive = False
    allPlaylistTracks = False

    if os.getenv("TERMUX_VERSION"):
        if os.access(android_destination, os.W_OK | os.X_OK):
            destination = android_destination
        else:
            print("warning: Termux detected but no Termux storage access permission!")

    args = sys.argv[1:]

    if interactiveFlag in args:
        interactive = True

    if allPlaylistTracksFlag in args:
        allPlaylistTracks = True

    ytdlpArgs = [i for i in args if i != interactiveFlag and i != allPlaylistTracksFlag]

    # if someone has an edge case for having a folder named "http" they will figure it out
    if any("http" in x for x in ytdlpArgs):
        # Download music
        download(ytdlpArgs, allPlaylistTracks)

        # generate pack
        generate(", ".join(ytdlpArgs), destination, interactive)
    else:
        # generate pack
        generate(ytdlpArgs[0], destination, interactive)


if __name__ == "__main__":
    main()
