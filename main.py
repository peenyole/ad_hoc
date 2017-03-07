# -*- coding: utf-8 -*-
import sys
import os
import bakaupdate
import eatmanga
import mangareader
import mangahere
import time

base_dir = os.getcwd()
to_download = bakaupdate.login(base_dir)

blacklist = ['Kyochuu Rettou', 'T REX Na Kanojo', 'Suicide Island', 'Gakkou Gurashi!', 'Monster Musume no Iru Nichijou']

for title in to_download.keys():
  if title in blacklist:
    del to_download[title]

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

if len(sys.argv) > 1 and sys.argv[1] == "-single":
  title = ' '.join(sys.argv[2:])
  print 'Downloading all ' + title + ' chapters.'

  #TODO: This is a hurried mess
  eatmanga_url      = eatmanga.get_title_url(title)
  eatmanga_chap_num = -1
  if eatmanga_url is not None:
    eatmanga_chap_num    = eatmanga.get_latest_released(title, eatmanga_url)

  mangareader_url      = mangareader.get_title_url(title)
  mangareader_chap_num = -1
  if mangareader_url is not None:
    mangareader_chap_num = mangareader.get_latest_released(title, mangareader_url)

  mangahere_url      = mangahere.check_title_url(title)
  mangahere_chap_num = -1
  if mangahere_url is not None:
    mangahere_chap_num   = mangahere.get_latest_released(title, mangahere_url)

  which = -1

  if eatmanga_chap_num > mangareader_chap_num and eatmanga_chap_num > mangahere_chap_num:
    which = 0
  elif mangareader_chap_num > eatmanga_chap_num and mangareader_chap_num > mangahere_chap_num:
    which = 1
  elif mangahere_chap_num >= mangareader_chap_num and mangahere_chap_num >= eatmanga_chap_num:
    which = 2

  local_path = base_dir + '/' + title

  try:
    for chap_num in to_download[title]:
      success = False

      if which == 0:
        eatmanga.download_chap(title, eatmanga_url, chap_num, local_path)
      elif which == 1:
        mangareader.download_chap(title, mangareader_url, chap_num, local_path)
      elif which == 2:
        mangahere.download_chap(title, mangahere_url, chap_num, local_path)

  except KeyError:
    print title + ' not found in Baka list.'

elif len(sys.argv) > 1 and sys.argv[1] == "-update":
  print 'Downloading all titles latests updates'
  # Title : url
  eatmanga_hash    = {}
  mangareader_hash = {}
  mangahere_hash   = {}

  total_hashed = 0

  print 'Titles: ' + str(len(to_download))

  for title in to_download.keys():
    print 'Hashing: ' + title

    eatmanga_url         = eatmanga.get_title_url(title)
    if eatmanga_url is not None:
      eatmanga_chap_num    = eatmanga.get_latest_released(title, eatmanga_url)
      eatmanga_hash[title] = eatmanga_url

    mangareader_url      = mangareader.get_title_url(title)
    if mangareader_url is not None:
      mangareader_chap_num = mangareader.get_latest_released(title, mangareader_url)
      if find_max(eatmanga_hash, title, mangareader_chap_num):
        remove_key(eatmanga_hash, title)
        mangareader_hash[title] = mangareader_url

    mangahere_url        = mangahere.check_title_url(title)
    if mangahere_url is not None:
      mangahere_chap_num   = mangahere.get_latest_released(title, mangahere_url)
      if find_max(eatmanga_hash, title, mangahere_chap_num) and find_max(mangareader_hash, title, mangahere_chap_num):
        remove_key(eatmanga_hash, title)
        remove_key(mangareader_hash, title)
        mangahere_hash[title] = mangahere_url

  total_hashed += len(eatmanga_hash) + len(mangareader_hash) + len(mangahere_hash)

  for title in eatmanga_hash.keys():
    try:
      local_path   = base_dir + '/' + title
      chap_num     = to_download[title][-1]

      eatmanga.download_chap(title, eatmanga_hash[title], chap_num, local_path)

    #Title downloads are all caught up
    except IndexError:
      pass

  for title in mangareader_hash.keys():
    try:
      local_path   = base_dir + '/' + title
      chap_num     = to_download[title][-1]

      mangareader.download_chap(title, mangareader_hash[title], chap_num, local_path)

    #Title downloads are all caught up
    except IndexError:
      pass

  for title in mangahere_hash.keys():
    try:
      local_path   = base_dir + '/' + title
      chap_num     = to_download[title][-1]

      mangahere.download_chap(title, mangahere_hash[title], chap_num, local_path)

    #Title downloads are all caught up
    except IndexError:
      pass


else:
  print 'Downloading all titles all chapters.'

