# music-pack-generator-coop
Converts yt-dlp playlist URLs or local albums into randomly generated music packs for sm64ex-coop

### Arguments

- `[yt-dlp URLs|local path]`: Either a local path to copy `.mp3` files from, or a space-separated list of [`yt-dlp` URLs](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- `--all`: (for download mode) Downloads the entire playlist instead of only the first 23 tracks
- `--interactive`: Choose to reshuffle the playlist before saving it

### Dependencies
- Python 3
- Pip
- FFmpeg

### Example of use on Android
```
termux-setup-storage
pkg install git python-pip ffmpeg
git clone https://www.github.com/robertkirkman/music-pack-generator-coop.git
cd music-pack-generator-coop
pip install -r requirements.txt
mkdir -p /storage/emulated/0/com.owokitty.sm64excoop/user/mods
./music-pack-generator.py https://www.youtube.com/playlist?list=PLp_G0HWfCo5raQSCb_BxY6oA1OVnNBolc --interactive
```


### Example of use on GNU/Linux
```
git clone https://www.github.com/robertkirkman/music-pack-generator-coop.git
cd music-pack-generator-coop
pip install -r requirements.txt # or find yt-dlp and jinja2 in your distro's package repositories and install them
./music-pack-generator.py https://www.youtube.com/playlist?list=PLp_G0HWfCo5raQSCb_BxY6oA1OVnNBolc
mkdir -p ~/.local/share/sm64ex-coop/mods
cp -r owokitty-generated-music-pack-* ~/.local/share/sm64ex-coop/mods/
```
