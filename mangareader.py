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

  url      = "http://www.mangareader.net/alphabetical"
  base_url = "http://www.mangareader.net"
  temp     = urllib2.urlopen(url)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')
  for link in links:
    if link.text == title:
      return base_url + link['href']
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

  return max_chap

#Download a single image form eatmanga
def download_image(url, img_name):
  time.sleep(2)
  base_url = "http://www.mangareader.net"
  temp = urllib2.urlopen(base_url + url)
  soup = BeautifulSoup(temp.read(), 'html.parser')

  imgs = soup.find_all('img')

  for img in imgs:
    if img.has_attr('id'):
      if img['id'] == 'img':
        #urllib.urlretrieve(img['src'], img_name + str(img['src'][-4:]))
        f = open(img_name + str(img['src'][-4:]), 'wb')
        f.write(urllib2.urlopen(img['src']).read())
        f.close()


#http://www.mangareader.net/dolly-kill-kill/1
#Find all of the image pages for a single chapter on eatmanga
def single_chap_walkthrough(chap_url, chap_title, series_local_path):
  print "Downloading " + chap_title
  time.sleep(2)

  released = False

  try:
    temp = urllib2.urlopen(chap_url)
    soup = BeautifulSoup(temp.read(), 'html.parser')
    #Get all chapters from the select drop-down
    selects = soup.find_all('select')

    select = soup.find("select", { "id" : "pageMenu" })


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
  except urllib2.HTTPError, e:
    print "ERROR: " + str(e.code)
    pass
  return released

#Downloads all chapters for series
def download_chap(series_title, url, chap_num, series_local_path):
  print 'MangaReader: Downloading ' + series_title
  time.sleep(2)
  base_url = "http://www.mangareader.net"
  temp     = urllib2.urlopen(url)
  soup     = BeautifulSoup(temp.read(), 'html.parser')

  links = soup.find_all('a')

  success = False

  for link in links:
    if series_title in link.text:
    
      chap_title = link.text
      chap_url   = base_url + link['href']
      #Proect against titles with numerics
      link_chap_num   = re.sub(series_title, "", link.text)

      if int(re.sub("[^0-9]", "", link_chap_num)) == int(chap_num):
        success = single_chap_walkthrough(chap_url, chap_title, series_local_path)
  return success





