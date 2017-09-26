#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import json
from collections import Counter

DEV_KEY = "{YOUR_API_KEY}"

# Execute an HTTP GET request with the search term asked.
def youtube_search(search_term):

  videos = []
  words = []
  daily_time = list(get_daily_time())

  # Save GET response
  rqst_videos = requests.get(url='https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&type=video&maxResults=50&key=%s' % (search_term, DEV_KEY))
  jsget = rqst_videos.json()

  # For each title and description found in the JSON response, insert them in the respective list.
  for titles_or_description in jsget['items']:
    tmp_list = []

    # Get each Title, description and ID from each Video
    each_title = (titles_or_description["snippet"]['title'])
    each_description = (titles_or_description["snippet"]['description'])
    each_video_id = (titles_or_description["id"]['videoId'])

    # Populate temporary list and then append it to permanent list.
    tmp_list.extend((each_title, each_description, each_video_id, each_video_id, get_n_convert_videos_lenght(each_video_id)))
    videos.append(tmp_list)

    # Insert every title and description to the list to count them later on.
    words.append(each_title)
    words.append(each_description)

  
  show_videos_found(videos)
  # List of capitalized words and number of words to show
  show_most_used_words(capitalize_words(words), 5)  
  calculate_days_needed(videos, daily_time)

def capitalize_words(list_of_words):
  # List containing possible unwated words, for finer usage, insert more of them here.
  list_of_unwanted_words = ['A','E','I','O','U']
  tmp_list = []
  for each_word in list_of_words:
    # Get and capitalize each word inside list_of_words
    each_capd_words = [word.upper() for word in re.findall(r'\w+', each_word)]
    for w in each_capd_words:
      if w not in list_of_unwanted_words:
        tmp_list.append(w)

  return tmp_list


def calculate_days_needed(total_videos_time, daily_time_list):
  lenght_list = [item[4] for item in total_videos_time]
  days_passed = 0
  # For each dayily time, try to squeeze as much videos as possible
  # If a video is watched, it is removed from the video's list.
  # If a video cannot be watched, it will try again on the next day, incrementing the passing day.
  for daily_time in daily_time_list:
    while((int)(len(lenght_list)) > 0):
      if lenght_list[0] <= daily_time:
        daily_time = daily_time - lenght_list[0]
        lenght_list.pop(0)
      else:
        days_passed += 1
        break
  print("")
  print("Days needed to watch all videos: \n%s" % (days_passed))
  print("")




def show_videos_found(list_of_videos):
  # Google's maximum results is 50.
  # Print the whole list of Video Titles found.
  print ("\n50 First videos found: ")
  tmp_list = [item[0] for item in list_of_videos]
  for p in tmp_list: print (p)
  print ("")


def show_most_used_words(list_of_words, num_words):
  # Count all equal words are ordenate them by most repeated(used).
  # Num of words is equals to the desired amount of 'Most Used Words' to be shown 
  c = Counter(list_of_words)
  print ((str)(num_words) + " most used words in titles and descriptions combined: ")
  print ([x[0] for x in c.most_common(num_words)])


def get_search_term():
  # Get user input on the search term.
  return input("Insert search term: ")


def get_daily_time():
  # Get user input on each daily time and converts to seconds.
  daily_time = []
  print("\nPlease insert time in minutes")
  monday = (int)(input("Insert time for Monday: "))*60
  tuesday = (int)(input("Insert time for Tuesday: "))*60
  wednesday = (int)(input("Insert time for Wednesday: "))*60
  thursday = (int)(input("Insert time for Thursday: "))*60
  friday = (int)(input("Insert time for Friday: "))*60
  saturday = (int)(input("Insert time for Saturday: "))*60
  sunday = (int)(input("Insert time for Sunday: "))*60
  print("")


  daily_time.extend((monday,tuesday,wednesday,thursday,
    friday,saturday,sunday))
  return daily_time


def get_n_convert_videos_lenght(each_video_id):
    rqst_lenght = requests.get(url='https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=%s&key=%s' % (each_video_id, DEV_KEY))
    jslenght = rqst_lenght.json()
    video_lenght = jslenght['items'][0]['contentDetails']['duration']
    # Remove unneeded strings, replace needed strings for mathematical functions.
    video_lenght = video_lenght.replace('PT', '')
    video_lenght = video_lenght.replace('H', '*3600+')
    video_lenght = video_lenght.replace('M', '*60+')
    video_lenght = video_lenght.replace('S', '')
    # Calculate remaning math function.
    video_lenght_secs = eval('%s' % (video_lenght))
    print("Processing video lenghts...")
    return video_lenght_secs


if __name__ == "__main__":
  youtube_search(get_search_term())