# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import os
from StringIO import StringIO
import gzip

#Should get series title, series url, chapters to download

#Return a hash of all series titles and the corresponding url on eatmanga
def get_title_url(title):

  url      = "http://www.mangahere.co/mangalist/"
  temp     = urllib2.urlopen(url)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  for link in links:
    if link.text == title:
      return link['href']
  return None

def check_title_url(title):
  base_url = 'http://www.mangahere.co/manga/'

  lower_title = title.lower()
  lower_title = lower_title.replace (" ", "_")

  try:
    temp     = urllib2.urlopen(base_url + lower_title)
    soup     = BeautifulSoup(temp.read(), 'html.parser')
    
    return base_url + lower_title
  except urllib2.HTTPError:
    return None
  


#Takes in title url and gives latest chapter number released
def get_latest_released(series_title, url):
  temp     = urllib2.urlopen(url)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  max_chap = 0

  for link in links:
    try:
      link_chap_num   = re.sub(series_title, "", link.text)

      if max_chap < int(re.sub(series_title, "", link.text)):
        max_chap = int(re.sub(series_title, "", link.text))
    except ValueError:
      # Chapter name most likely has a non numberic value like, 1b, 1c or Special Omake
      pass
  max_chap -= 1
  return max_chap

#Download a single image form eatmanga
def download_image(url, img_name):
  time.sleep(2)

  response = urllib2.urlopen(url)

  if response.info().get('Content-Encoding') == 'gzip':
    buf = StringIO(response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
  else:
    data = response.read()

  soup = BeautifulSoup(data, 'html.parser')

  img = soup.find("img", { "id" : "image" })
  src = img['src'].strip('amp;')

  #f = open(img_name + str(img['src'][-4:]), 'wb')
  f = open(img_name + '.png', 'wb')
  f.write(urllib2.urlopen(src).read())
  f.close()


#http://www.mangareader.net/dolly-kill-kill/1
#Find all of the image pages for a single chapter on eatmanga
def single_chap_walkthrough(chap_url, chap_title, series_local_path):
  print "Downloading " + chap_title
  time.sleep(2)
  temp = urllib2.urlopen(chap_url)
  soup = BeautifulSoup(temp.read(), 'html.parser')
  #Get all chapters from the select drop-down
  selects = soup.find_all('select')

  released = False

  select = soup.find("select", { "onchange" : "change_page(this)" })

  if select is not None:
    try:
      #Only make the chapter directory if it has been released.
      os.chdir(series_local_path)
      os.mkdir(chap_title)
      os.chdir(series_local_path+"/"+chap_title)

      pages = select.find_all('option')
      for page_urls in pages:
        download_image(page_urls['value'], chap_title + "_" + page_urls.text)
      released = True
    except OSError:
      print 'Already downloaded. skippping...'
      pass
  return released

#Downloads all chapters for series
def download_chap(series_title, url, chap_num, series_local_path):
  print 'MangaHere: Downloading ' + series_title
  time.sleep(2)
  temp     = urllib2.urlopen(url)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')

  success = False

  for link in links:
    try:
      if series_title in link.text:
      
        chap_title = link.text
        chap_url   = link['href']
        #Proect against titles with numerics
        link_chap_num   = re.sub(series_title, "", link.text)

        if int(re.sub("[^0-9]", "", link_chap_num)) == int(chap_num):
          success = single_chap_walkthrough(chap_url, chap_title.lstrip(), series_local_path)
    except:
      pass
  return success





