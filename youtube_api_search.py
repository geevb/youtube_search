#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import json
from collections import Counter

# Execute an HTTP GET request with the search term asked.
def youtube_search(search_term):
  videos_titles = []
  words = []
  most_used_words = []

  get = requests.get(url='https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&type=video&maxResults=50&key=AIzaSyB1AjbGz_Xvq5TDxKZK0UoQABpqDlBh6Sk' % (search_term))
  jsget = get.json()

  # For each title and description found in the JSON response, insert them in the respective list.
  for titles_or_description in jsget['items']:
    each_title = (titles_or_description["snippet"]['title'])
    each_description = (titles_or_description["snippet"]['description'])
    videos_titles.append(each_title)
    words.append(each_title)
    words.append(each_description)

  # Capitalize all letters to make an appropriate counting and insert them in a new list.
  for each_word in words:
    each_caps_words = [word.upper() for word in re.findall(r'\w+', each_word)]
    for w in each_caps_words:
      most_used_words.append(w)

  show_videos_found(videos_titles)
  show_most_used_words(most_used_words, 5)


def show_videos_found(list_of_videos):
  # Google's maximum results is 50.
  # Print the whole list of Video Titles found.
  print ("50 Videos found: ")
  for p in list_of_videos: print (p)
  print ("")


def show_most_used_words(list_of_words, num_words):
  # Count all equal words are ordenate them by most repeated(used).
  c = Counter(list_of_words)
  print ((str)(num_words) + " most used words in titles and descriptions: ")
  print ([x[0] for x in c.most_common(num_words)])


def get_search_term():
  # Get user input on the search term.
  return input("Insert search term: ")


if __name__ == "__main__":
  youtube_search(get_search_term())