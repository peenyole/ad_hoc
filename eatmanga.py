#python
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import os

#Should get series title, series url, chapters to download

#Return a hash of all series titles and the corresponding url on eatmanga
def get_title_url(title):

  url = "http://eatmanga.com/Manga-Scan/"
  base_url ="http://eatmanga.com"
  request = urllib2.Request(url)
  request.add_header('User-agent', 'Mozilla 5.10')
  temp = urllib2.urlopen(request)
  soup = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  for link in links:
    if link.text == title:
      return base_url + link['href']
  return None

#Return a hash of all series titles and the corresponding url on eatmanga
def get_eatmanga_urls(title_chap_info):
  time.sleep(2)
  hashy = {}
  url = "http://eatmanga.com/Manga-Scan/"
  base_url ="http://eatmanga.com"
  request = urllib2.Request(url)
  request.add_header('User-agent', 'Mozilla 5.10')

  temp = urllib2.urlopen(request)

  soup = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  for link in links:
    if link.text in title_chap_info:
      hashy[link.text] = base_url + link['href']
  return hashy

#Takes in title url and gives latest chapter number released
def get_latest_released(series_title, url):
  request = urllib2.Request(url)
  request.add_header('User-agent', 'Mozilla 5.10')

  temp     = urllib2.urlopen(request)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  max_chap = 0

  for a in links:
    try:
      link_chap_num   = re.sub(series_title, "", a.text)

      if max_chap < int(re.sub(series_title, "", a.text)):
        max_chap = int(re.sub(series_title, "", a.text))
    except ValueError:
      # Chapter name most likely has a non numberic value like, 1b, 1c or Special Omake
      pass
  max_chap -= 1
  return max_chap

#Download a single image form eatmanga
def download_image(url, img_name):
  time.sleep(2)
  base_url ="http://eatmanga.com"
  request = urllib2.Request(base_url + url)
  request.add_header('User-agent', 'Mozilla 5.10')
  temp = urllib2.urlopen(request)
  soup = BeautifulSoup(temp.read(), 'html.parser')

  imgs = soup.find_all('img')

  for img in imgs:
    if img.has_attr('id'):
      if img['id'] == 'eatmanga_image_big' or img['id'] == 'eatmanga_image':
        #urllib.urlretrieve(img['src'], img_name + str(img['src'][-4:]))
        f = open(img_name + str(img['src'][-4:]), 'wb')
        f.write(urllib2.urlopen(img['src']).read())
        f.close()

#Find all of the image pages for a single chapter on eatmanga
def single_chap_walkthrough(chap_url, chap_title, series_local_path):
  print "Downloading " + chap_title
  time.sleep(2)
  request = urllib2.Request(chap_url)
  request.add_header('User-agent', 'Mozilla 5.10')
  temp = urllib2.urlopen(request)
  soup = BeautifulSoup(temp.read(), 'html.parser')
  #Get all chapters from the select drop-down
  selects = soup.find_all('select')

  for select in selects:
    if select['id'] == 'pages':
      try:
        #Only make the chapter directory if it has been released.
        os.chdir(series_local_path)
        os.mkdir(chap_title)
        os.chdir(series_local_path+"/"+chap_title)

        pages = select.find_all('option')
        for page_urls in pages:
          download_image(page_urls['value'], chap_title + "_" + page_urls.text)
        return True
      except OSError:
        print 'Already downloaded. skippping...'
        pass

  return False

#Downloads all chapters for series
def download_chap(series_title, url, chap_num, series_local_path):
  print 'EatManga: Downloading ' + str(series_title) + ':' + str(chap_num) 
  time.sleep(2)
  base_url = "http://eatmanga.com"
  request  = urllib2.Request(url)
  request.add_header('User-agent', 'Mozilla 5.10')

  temp     = urllib2.urlopen(request)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')

  success = False

  for a in links:
    if series_title in a.text:
      chap_title = a.text
      # try:
      chap_url   = base_url + a['href']
      #Proect against titles with numerics
      link_chap_num   = re.sub(series_title, "", a.text)

      try:
        link_chap_num = int(re.sub("[^0-9]", "", link_chap_num))
      except ValueError:
        link_chap_num = -1

      if  link_chap_num == int(chap_num):
        success = single_chap_walkthrough(chap_url, chap_title, series_local_path)



  return success





