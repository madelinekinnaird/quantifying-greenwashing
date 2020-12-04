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


## initiating instaloader
instagram = instaloader.Instaloader(download_comments=False, download_pictures=False, download_videos=False,
									download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)
## loading the session
instagram.load_session_from_file('datascraper1234')

## where to put the output files
output_path = pathlib.Path('../../../data/all_instagram_posts')

## list of companies to scrape
companies = open("batch.txt", "r")


## LOOP THROUGH COMPANIES
for company in companies:
	company = company.strip()

	## check if csv already exists
	csvName = company + '.csv'
	if os.path.exists(output_path.joinpath(csvName)):
		print("Already finished %s csv!" % company)
		continue
	else:
		print("Scraping %s ..." % company)


		## CSV
		post_file = output_path.joinpath(csvName).open("w")
		post_writer = csv.DictWriter(post_file, fieldnames=["shortcode", "username", "date_utc",
															"is_video", "is_sponsored", "hashtags", "mentions", "caption",
															"video_view_count", "video_length", "likes",
															"comments", "likes+comments", "location_name", "location_latlong"])


		post_writer.writeheader()

		## load company profile
		profile = instaloader.Profile.from_username(instagram.context, company)


		processed = 1
		for post in profile.get_posts():
			if processed > 100:
				break

			print("...scraping info for post %s" % post.shortcode)

			post_info = {
				"shortcode": post.shortcode,
				"username": company,
				"date_utc": post.date_utc.strftime("%Y-%m-%d %H:%M"),
				"is_video": "yes" if post.is_video else "no",
				"is_sponsored": post.is_sponsored,
				"hashtags": ",".join(post.caption_hashtags),
				"mentions": ",".join(post.caption_mentions),
				"caption": (emoji.demojize(post.caption)).encode('utf-8')if post.caption else "",
				"video_view_count": post.video_view_count if post.is_video else 0,
				"video_length": post.video_duration if post.is_video else 0,
				"likes": post.likes,
				"comments": post.comments,
				"likes+comments": (post.likes + post.comments),
				"location_name": post.location.name if post.location else "",
				"location_latlong": " ".join((str(post.location.lat), str(post.location.lng))) if post.location else ""
				}

			processed += 1

			post_writer.writerow(post_info)

		print("...scraped %i posts for %s" % (processed - 1, company))

		#user_file.close()
		post_file.close()

print("Done scraping!")
