#python
import cred
import cookielib
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import os

normalized_hash = {
  'Jisatsutou':'Suicide Island',
  'T-REX na Kanojo':'T REX Na Kanojo',
  'Tonari no Kashiwagi-san':'Tonari no Kashiwagi san'
}

def login(base_dir):
  # Store the cookies and create an opener that will hold them
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

  # Add our headers
  opener.addheaders = [('User-agent', 'Mozilla-Firefox')]

  # Install our opener (note that this changes the global opener to the one
  # we just made, but you can also just call opener.open() if you want)
  urllib2.install_opener(opener)

  # The action/ target from the form
  authentication_url = 'https://www.mangaupdates.com/login.html'
  payload = cred.get_baka_creds()

  # Use urllib to encode the payload
  data = urllib.urlencode(payload)

  # Build our Request object (supplying 'data' makes it a POST)
  req = urllib2.Request(authentication_url, data)

  # Make the request and read the response
  resp = urllib2.urlopen(req)
  contents = resp.read()

  temp = urllib2.urlopen('https://www.mangaupdates.com/mylist.html')

  soup = BeautifulSoup(temp.read(), 'html.parser')
  return get_title_chaps_hash(base_dir, soup.find_all('tr'))

def normalize_title(input_title):
  if input_title in normalized_hash.keys():
    return normalized_hash[input_title]
  else:
    return input_title

def parse_titles(title, chapter_info):
  try:
   if title['title'] == 'Series Info':
    title = normalize_title(str(title.u.text))

    vol_chap = chapter_info.find_all('b')
    vol      = re.sub("[^0-9]", "", vol_chap[0].text)
    chap     = re.sub("[^0-9]", "", vol_chap[1].text)

    #manga = Manga(title, vol, chap)
    return title
  except KeyError:
    pass

def get_title_chaps_hash(base_dir, trs):
  to_download = {}
  for tr in trs:

    tds = tr.find_all('td')
    #Find the correct <td></td> from the html
    if len(tds) > 2 and len(tds[1].find_all('a')) > 1:

      last_release = re.sub("[^0-9]", "", tds[1].find_all('a')[1].text)

      #Get new manga titles
      title = parse_titles(tds[1].a, tds[2])
      if title is not None:    
        series_local_path = base_dir + "/" + str(title)
        #Hash 'title':[Chaps to download]
        to_download[title] = directories(base_dir, title, series_local_path, last_release)

  return to_download

  #returns array of chapter numbers to be downloaded
def directories(base_dir, series_title, series_path, last_release):
  chap_dirs = []

  if not os.path.isdir(series_path):
    os.mkdir(series_path)
    
  downloaded_chaps = os.listdir(series_path)
  
  downloaded_chapters = [] #Numeric chapter numbers

  #Get array of all chapter numbers that have been downloaded, accomodates missed downloads
  for folder in downloaded_chaps:
    if folder.startswith( '.' ):
      pass
    #Protect against titles with numerics
    temp = re.sub(series_title, "", folder)
    chap_num = re.sub("[^0-9]", "", temp)
    if len(chap_num) > 0:
      downloaded_chapters.append(int(chap_num))

  to_download = []

  for x in range(1, int(last_release)+1):
    if x not in downloaded_chapters:
      to_download.append(x)

  return to_download