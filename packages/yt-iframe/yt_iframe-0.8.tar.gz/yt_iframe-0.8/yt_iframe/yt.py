from bs4 import BeautifulSoup as bs
import requests
from time import sleep


def video(link):
    # link = youtube video url. Return iframe as string
    string = ''     # iframe string

    try:
        link = link.split('watch?v=')[1]
        string = '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + link + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    except:
        print('yt.video - Error! Not a valid link.')

    return string


def channel(link):
    # link = youtube channel url. Return iframes in list
    iframes = []       # list of iframes
    links = []      # list of video links

    # Inner methods for finding RSS URL
    def userURL(link):
        user = requests.get(link).text
        soup = bs(user, 'lxml')
        link = soup.find("link", {"rel":"canonical"})
        return channelURL(link['href'])
    def channelURL(link):
        link = link.split('/channel/')[1]
        link = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + link
        return link

    # Get RSS URL from channel URL
    if '/channel/' in link:
        xml = channelURL(link)
    elif '/user/' in link:
        xml = userURL(link)
    else:
        print('yt.channel - Error! Not a valid link')

    # Get RSS feed
    feed = requests.get(xml).text
    xmlsoup = bs(feed, "lxml")

    # Add video links to links list
    for entry in xmlsoup.findAll('link'):
        if '/watch?v=' in entry['href']:
            links.append(entry['href'])
    return links


def channelDict(link):
    # Alternate version of channel() that returns a dictionary
    # Key = title of video
    # Value = video link
    links = {}

    def userURL(link):
        user = requests.get(link).text
        soup = bs(user, 'lxml')
        link = soup.find("link", {"rel":"canonical"})
        return channelURL(link['href'])
    def channelURL(link):
        link = link.split('/channel/')[1]
        link = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + link
        return link

    # Get RSS URL from channel URL
    if '/channel/' in link:
        xml = channelURL(link)
    elif '/user/' in link:
        xml = userURL(link)
    else:
        print('yt.channel - Error! Not a valid link')

    # Get RSS feed
    feed = requests.get(xml).text
    xmlsoup = bs(feed, "lxml")

    # Create dictionary entries
    for entry in xmlsoup.findAll('entry'):
        ytlink = entry.find('link')
        if '/watch?v=' in ytlink['href']:
            title = entry.find('title').text
            ytlink = ytlink['href']
            links[title] = ytlink
        else:
            continue
    return links


def getFrames(links):
    # Convert links list to iframes list
    iframes = []
    for vid in links:
        frame = video(vid)
        iframes.append(frame)
    return iframes
