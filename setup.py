from setuptools import setup, find_packages

setup(
    author="Tanish",
    author_email="sharmatanish097654@gmail.com",
    description="Torrscraper is a command line tool to search and download torrents from the command line.",
    long_description_content_type='text/markdown',
    long_description='''##How to Use 

Installation
pip install Torrscrape

1)Install docker 
  mac:https://docs.docker.com/desktop/install/mac-install/<br>
  win:https://docs.docker.com/desktop/install/windows-install/<br>
  linux:https://docs.docker.com/desktop/install/linux-install/<br>
2)setup jackett:

docker run -d \
  --name=jackett \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e AUTO_UPDATE=true `#optional` \
  -e RUN_OPTS= `#optional` \
  -p 9117:9117 \
  -v /path/to/data:/config \
  -v /path/to/blackhole:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/jackett:latest

3)setup qbit web(docker):

docker run -d \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e WEBUI_PORT=8080 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v /path/to/appdata/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/qbittorrent:latest

##Usage
torrscrape --api "jackett_apikey" --search "search_term" --catagory "catagory"
catagories: TV,TV/Anime,Other,Movies,PC/Games''',
    name="Torrscrape",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "qbittorrent-api",
        "pandas",
        "tabulate",
        "click",        
    ],
    entry_points={
        "console_scripts": [
            "torrscrape=Torrscrape.main:main",
        ],
    },
)
