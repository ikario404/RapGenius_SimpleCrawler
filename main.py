#!/usr/lib/python2.7
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests, csv, lxml, string, sys
# UTF-8 for all
reload(sys)
sys.setdefaultencoding('utf8')
# Helpfull color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## Downloader
def download(url):
    print(bcolors.WARNING + bcolors.BOLD + 'GO download on : ' + bcolors.FAIL + url + bcolors.ENDC)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        sys.exit(bcolors.FAIL + bcolors.BOLD + 'nothing here')

## First Crawl
def extract_url(html):
    # print(bcolors.WARNING + bcolors.BOLD + 'GO extraction data from : '+ bcolors.FAIL + artist_name + bcolors.ENDC)
    soup = BeautifulSoup(html, 'lxml')
    next_link = soup.find('a', {'class' : 'next_page'})
    listLink = soup.find('section', {'class':'all_songs'})
    link = listLink.find_all('a', {'class' : 'song_name'})
    all_link = []

    for x in link:
        title_Song = x.get('title')
        url_Song = x.get('href')
        listeA = [title_Song, url_Song]                
        all_link.append(listeA)

    if (next_link is None):
        print 'ONLY ONE PAGE'
        for x in link:
            title_Song = x.get('title')
            url_Song = x.get('href')
            listeA = [title_Song, url_Song]
            all_link.append(listeA)
    else:
        print 'MULTIPLE PAGES'
        next_link_URL = host + next_link.get('href')
        while (next_link is not None):        
            try:
                next_to_list = download(next_link_URL)
                soup = BeautifulSoup(next_to_list, 'lxml')
                next_link = soup.find('a', {'class' : 'next_page'}).get('href')
                linkList = soup.find_all('a', {'class' : 'song_name'})
                next_link_URL = host + next_link
                for x in linkList:
                    title_Song = x.get('title')
                    url_Song = x.get('href')
                    listeA = [title_Song, url_Song]                
                    all_link.append(listeA)
            except AttributeError:
                print('Fin de boucle !')
                break

        return all_link

## Second Crawl
def extract_lyrics(html):
    soup = BeautifulSoup(html, 'lxml')
    divLyrics = soup.find('div', {'class':'lyrics'})
    divLyrics = divLyrics.find_all('p')
    return divLyrics

# Extract CSV
def write_csv(filename, data):
    with open('corpus/' + filename + '.csv', 'a') as csvfile:        
        dataWriter = csv.writer(csvfile, delimiter=';')
        dataWriter.writerows(all_songs)
        return

if len(sys.argv) > 1:
    artist_name = str(sys.argv[1])
else:
    sys.exit(bcolors.FAIL + bcolors.BOLD + 'Please pass one argument as an artist_name seen on RapGenius')

## Used on debug
# artist_name = 'East'
# artist_name = urlparse(ArtistURL).path.split('/artists/',1)[-1]

host = 'http://genius.com'
ArtistURL = host + '/artists/' + artist_name
get = download(ArtistURL)
songListURL = extract_url(get)
all_songs = []

if (songListURL is None):
    sys.exit(bcolors.FAIL + bcolors.BOLD + 'nothing here')
else:
    for x in songListURL:
        title_Song = x[0]
        url_Song = x[1]
        print url_Song
        getTracks = download(url_Song)
        lyricsData = extract_lyrics(getTracks)
        for y in lyricsData:
            text = y.getText().encode('utf8')
            listeB = [title_Song,url_Song,artist_name,text]
            all_songs.append(listeB)

    print 'nombre pistes : ' + len(all_songs)
    for song in all_songs:
        print song[0]

    write_csv(artist_name, song)
