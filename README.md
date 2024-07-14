# music-pack-generator-coop
Converts yt-dlp playlist URLs into randomly generated music packs for sm64ex-coop

### Example of use on Android
```
pkg install git python-pip
git clone https://www.github.com/robertkirkman/music-pack-generator-coop.git
cd music-pack-generator-coop
pip install -r requirements.txt
mkdir -p /storage/emulated/0/com.owokitty.sm64excoop/user/mods
./music-pack-generator.py https://www.youtube.com/playlist?list=PLp_G0HWfCo5raQSCb_BxY6oA1OVnNBolc
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