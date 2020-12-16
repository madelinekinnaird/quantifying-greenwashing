import instaloader
import argparse
import pathlib
import sys
import csv
import time
import emoji
import os
import csv
from glob import glob
from os.path import expanduser
from sqlite3 import connect
import os.path
import pandas as pd
from datetime import datetime
from itertools import dropwhile, takewhile

## initiating instaloader
instagram = instaloader.Instaloader(download_comments=False, download_pictures=False, download_videos=False,

									download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)

## gtown_datascraper (Dec 12 Morning)
## gtown_datascraper1 (dec 10 morning)
## gtown_datascraper2 ( dec 11 evening)
## gtown_datascraper3 (dec 12)
## gtown_datascraper4 (Dec 12 morning)
## aggie_datascraper (Dec 10 mid morning)
## aggie_datascraper1 (Dec 12 Morning)

## aggie_datascraper3 (Dec 12 morning)
# aggie_datascraper4 (Dec 12 morning)
## datascraper1234 (Dec. 12 morning)
## ivakinnaird (Dec 10, evening) (12 morning)
## taylorkinnaird13
#taylor_rose_kinnaird13
## daisykinnaird
## jameskinnaird13
## emilyrananana
## jamesbethany13
## lilyswift26
## rexrexrexroth
## jamestkinnaird


## load your username session, initiatied in ig_login
instagram.load_session_from_file('jamestkinnaird')

## COMPANIES TO REDO
## burberry
## hyundai
## heineken
## gucci
## clinique
## espn
## ebay
## docusign
## corteva
## corona
## bakerhughesco
## nivea
## att
## bookingcom
##
## ikea
## interpublicipg
## japanair
## kochindustriesinc
## kohls
## krogerco
## victoriasecret
## libean
## levis
## nokia
## rei
## redbull
## tollbrothers
## universalstandard
## zentihbankplc


## 'nivea'
## bakerhughesco

companies = ['zenithbankplc']


def add_more_posts(companies, addDirection, addDate):
    for company in companies:
        ## import company csv as dataframe
        csvName = company + '.csv'
        output_path = pathlib.Path('../../../data/all_instagram_posts')
        df = pd.read_csv(output_path.joinpath(csvName))

        ## get earliest and latest date
        oldestDate = pd.to_datetime(df['date_utc'].min()) ## earliest date in data
        recentDate = pd.to_datetime(df['date_utc'].max()) ## most recent date in data

        if addDirection == 'beginning':
            SINCE = oldestDate
            UNTIL = addDate

        if addDirection == 'end':
            SINCE = addDate
            UNTIL = recentDate

        posts = instaloader.Profile.from_username(instagram.context, company).get_posts()

        processed = 1
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):

            print(post.date)
            print("...scraping info for post %i, %s" % (processed, company))


            post_info = {
                "shortcode": post.shortcode,
                "username": company,
                "date_utc": post.date_utc.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "is_video": "yes" if post.is_video else "no",
                "is_sponsored": post.is_sponsored,
                "hashtags": (",".join(post.caption_hashtags)).encode('utf-8', errors='ignore'),
                "mentions": (",".join(post.caption_mentions)).encode('utf-8', errors='ignore'),
                "caption": (emoji.demojize(post.caption)).encode('utf-8', errors='ignore') if post.caption else "",
                "video_view_count": post.video_view_count if post.is_video else 0,
                "video_length": post.video_duration if post.is_video else 0,
                "likes": post.likes,
                "comments": post.comments,
                "location_name": (post.location.name).encode('utf-8', errors='ignore') if post.location else "",
                "location_latlong": " ".join((str(post.location.lat), str(post.location.lng))) if post.location else ""
                }

            processed += 1


            file_path = os.path.join(output_path, csvName)

            fieldnames=["shortcode", "username", "date_utc", "is_video",
             "is_sponsored", "hashtags", "mentions", "caption", "video_view_count",
             "video_length", "likes", "comments", "location_name", "location_latlong"]



            #bigdict = {'column_1': 1, 'column_2': 2, 'column_3': 3}

            with open(file_path, 'a+') as csv_file:
                #fieldnames = ['column_1', 'column_2', 'column_3']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
                #if '\n' not in csv_file.readlines()[-1]:
                #    csv_file.write("\n")
                writer.writerow(post_info)





        print("...scraped %i posts for %s" % (processed - 1, company))
    print("Done scraping!")

## choose your cutoffdate
cutoffDate = datetime(2020, 1, 1)

## run for your list of companies, choice of direction, and cutoff date
add_more_posts(companies, 'beginning', cutoffDate)
