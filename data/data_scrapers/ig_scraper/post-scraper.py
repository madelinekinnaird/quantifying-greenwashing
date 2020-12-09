import instaloader
import argparse
import pathlib
import sys
import csv
import time
import emoji
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
## loading the session created from ig_login.py!
## gtown_datascraper
## gtown_datascraper1
## gtown_datascraper2 (Dec 7 evening)
## gtown_datascraper3 (Dec 8 midday)
## aggie_datascraper
## aggie_datascraper1 (Dec 7 evening)
## aggie_datascraper2 (Dec 8 evening) DONT USE
## datascraper1234
## ivakinnaird

instagram.load_session_from_file('aggie_datascraper3')

## where to put the output files
output_path = pathlib.Path('../../../data/all_instagram_posts')

## list of instagram usernames to scrape
df = pd.read_csv('../../../data/company_key.csv')
column = 'username'
companies = df[column]

## LOOP THROUGH COMPANIES
for company in companies:
	## check if csv already exists
	csvName = company + '.csv'
	if os.path.exists(output_path.joinpath(csvName)):
		print("Already finished %s csv!" % company)
		## open the file
		## pull id of first post of 2020
		## if id is in csv, then continue
		## else:
		## loop through posts like below, add line saying if post id in csv then continue to next post
		continue
	else:
		print("Scraping %s .................." % company)


		## CSV
		post_file = output_path.joinpath(csvName).open("w")
		post_writer = csv.DictWriter(post_file, fieldnames=["shortcode", "username", "date_utc",
															"is_video", "is_sponsored", "hashtags", "mentions", "caption",
															"video_view_count", "video_length", "likes",
															"comments", "likes+comments", "location_name", "location_latlong"])


		post_writer.writeheader()

		## load company profile
		posts = instaloader.Profile.from_username(instagram.context, company).get_posts()


		SINCE = datetime(2020, 12, 5)
		UNTIL = datetime(2020, 1, 1)

		processed = 1
		for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):

			print(post.date)
			print("...scraping info for post %s, %s" % (post.shortcode, company))




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
			post_writer.writerow(post_info)

		print("...scraped %i posts for %s" % (processed - 1, company))

		#user_file.close()
		post_file.close()


print("Done scraping!")
