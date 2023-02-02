import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
import datetime
import streamlink

addon = xbmcaddon.Addon()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_video_links():
    video_titles = []
    video_links = []
    for i in range(1, 10):
        url = f"https://tviplayer.iol.pt/videos/ultimos/{i}/canal:"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        video_titles.extend([item.text for item in soup.find_all("span", class_="item-title")])
        video_links.extend([f"https://tviplayer.iol.pt{item['href']}" for item in soup.find_all("a", class_="item")])
    return video_titles, video_links

def list_videos(video_titles, video_links):
    for title, link in zip(video_titles, video_links):
        now = datetime.datetime.now()
        timestamp = now.strftime("%m%d%H%M%S")
        video_url = streamlink.streams(link)["best"].url if streamlink.streams(link) else None
        item = soup.find("a", class_="item", href=link)
        if item:
            image_url = item["style"].split("url(")[1].split(")")[0]
        else:
            image_url = "https://cdn.iol.pt/img/logostvi/branco/tviplayer.png"
        if video_url:
            li = xbmcgui.ListItem(label=title)
            li.setArt({'thumb': image_url, 'icon': image_url})
            li.setInfo(type='Video', infoLabels={'Title': title})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=video_url, listitem=li)

def run():
    video_titles, video_links = get_video_links()
    list_videos(video_titles, video_links)
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    run()
