# -*- coding: utf-8 -*-
import sys
import os
import bakaupdate
import eatmanga
import mangareader
import mangahere
import time

def find_max(hash, key, chap_num):
  try:
    return chap_num > hash[key]
  except KeyError:
    return True

def remove_key(hash, key):
  try:
    del hash[key]
  except KeyError:
    pass

#Download all missing chapters of a single title
def download_chap_loop(chap_nums, title, module, url, local_path):
  try:
    for chap_num in chap_nums:
        module.download_chap(title, url, chap_num, local_path)
  except KeyError:
    print title + ' not found in Baka list.'

def get_download_list(base_dir):

  to_download = bakaupdate.login(base_dir)

  blacklist = ['Kyochuu Rettou',
    'T REX Na Kanojo',
    'Suicide Island',
    'Gakkou Gurashi!',
    'Monster Musume no Iru Nichijou']

  for title in to_download.keys():
    if title in blacklist:
      del to_download[title]

  return to_download


if len(sys.argv) <= 1:
  print 'No command found, exiting...'
  sys.exit()


base_dir = os.getcwd()
to_download = get_download_list(base_dir)



if sys.argv[1] == '-single':
  title      = ' '.join(sys.argv[2:])
  local_path = base_dir + '/' + title

  print 'Downloading all chapters for '+ title + '...'

  eatmanga_url      = eatmanga.get_title_url(title)
  mangareader_url   = mangareader.get_title_url(title)
  mangahere_url     = mangahere.check_title_url(title)

  eatmanga_chap_num    = eatmanga.get_latest_released(title, eatmanga_url)       if eatmanga_url    is not None else -1
  mangareader_chap_num = mangareader.get_latest_released(title, mangareader_url) if mangareader_url is not None else -1
  mangahere_chap_num   = mangahere.get_latest_released(title, mangahere_url)     if mangahere_url   is not None else -1


#TODO: Don't check directories that have already been downlaoded.
#  if os.path.exists("/home/el/myfile.txt")

  if   eatmanga_chap_num    >= mangahere_chap_num and eatmanga_chap_num   >= mangareader_chap_num:
    print 'Downloading from EatManga'
    download_chap_loop(to_download[title], title, eatmanga, eatmanga_url, local_path)

  elif mangareader_chap_num > eatmanga_chap_num  and mangareader_chap_num > mangahere_chap_num:
    print 'Downloading from MangaReader'
    download_chap_loop(to_download[title], title, mangareader, mangareader_url, local_path)

  elif mangahere_chap_num   > eatmanga_chap_num  and mangahere_chap_num   > mangareader_chap_num:
    print 'Downloading from MangaHere'
    download_chap_loop(to_download[title], title, mangahere, mangahere_url, local_path)
  else:
    print 'I have no idea what to do with my life...'



elif sys.argv[1] == "-update":
  print 'Downloading all titles latests updates'

  for title in to_download.keys():
    if len(to_download[title]) > 1:
      print 'Downloading: ' + title
      local_path = base_dir + '/' + title

      eatmanga_url      = eatmanga.get_title_url(title)
      mangareader_url   = mangareader.get_title_url(title)
      mangahere_url     = mangahere.check_title_url(title)

      eatmanga_chap_num    = eatmanga.get_latest_released(title, eatmanga_url)       if eatmanga_url    is not None else -1
      mangareader_chap_num = mangareader.get_latest_released(title, mangareader_url) if mangareader_url is not None else -1
      mangahere_chap_num   = mangahere.get_latest_released(title, mangahere_url)     if mangahere_url   is not None else -1

      if   eatmanga_chap_num    >= mangahere_chap_num and eatmanga_chap_num   >= mangareader_chap_num and eatmanga_chap_num > 0:
        print 'Downloading from EatManga'
        eatmanga.download_chap(title, eatmanga_url, to_download[title][-1], local_path)

      elif mangareader_chap_num > eatmanga_chap_num  and mangareader_chap_num > mangahere_chap_num:
        print 'Downloading from MangaReader'
        mangareader.download_chap(title, mangareader_url, to_download[title][-1], local_path)

      elif mangahere_chap_num   > eatmanga_chap_num  and mangahere_chap_num   > mangareader_chap_num:
        print 'Downloading from MangaHere'
        mangahere.download_chap(title, mangahere_url, to_download[title][-1], local_path)

      else:
        print 'I have no idea what to do with my life...'

else:
  print 'Downloading all titles all chapters.'











