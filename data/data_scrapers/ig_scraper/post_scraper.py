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


## python post_scraper.py --batchfile batch.txt

config_path = pathlib.Path(__file__, "..","config.py").resolve()
if not config_path.exists():
	print("No config.py file found. You can create it by copying or renaming")
	print("config.py-example and editing the values in it.")
	sys.exit(1)

import config


## command line stuff to collect bathc
cli = argparse.ArgumentParser()
cli.add_argument("--batchfile", "-b", required=True, help="File containing entities to scrape, one per line")
cli.add_argument("--output", "-o",
				 help="Location to create result files in. If left empty, the working directory is used.")
cli.add_argument("--timestamp", "-t",
				 help="Appends a timestamp to the resulting filenames. Useful for scheduled scraping.")
args = cli.parse_args()



## collecting info from batch file
batch_file = pathlib.Path(args.batchfile).resolve()
if not batch_file.exists():
	print("Batch file ('%s') not found." % str(batch_file))
	sys.exit(1)




## where to put the output files
output_path = pathlib.Path(args.output).resolve() if args.output else pathlib.Path(__file__, "..").resolve()
if not output_path.exists() or not output_path.is_dir():
	print("Given output path (%s) is not a valid directory." % str(output_path))
	sys.exit(1)





## initiating instaloader
instagram = instaloader.Instaloader(download_comments=False, download_pictures=False, download_videos=False,
									download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)


## loading the session
instagram.load_session_from_file(config.USERNAME)



## turn batch usernames into a set
usernames = set()
with batch_file.open() as input:
	for username in input:
		if not username.strip():
			continue
		usernames.add(username.strip())



# initialise result variables and files
# user and post data is written to a CSV file directly, followers/followees are
# kept in memory until the end to write one big graph file


if args.timestamp:
	timestr = time.strftime("%Y%m%d%H%M%S")+"_"
else:
	timestr = ""



## CSV Option
post_file = output_path.joinpath(timestr+"posts.csv").open("w")
post_writer = csv.DictWriter(post_file, fieldnames=["shortcode", "username", "date_utc", "url_thumbnail", "url_media",
													"is_video", "is_sponsored", "hashtags", "mentions", "caption",
													"video_view_count", "video_length", "likes",
													"comments", "likes+comments", "location_name", "location_latlong"])
post_writer.writeheader()


## get stuff prepared
user_ids = {}


# start scraping
print("Scraping %i usernames, %i posts per user." % (len(usernames), config.POSTS_PER_USERNAME))
for username in usernames:
	print("Scraping %s..." % username)


	profile = instaloader.Profile.from_username(instagram.context, username)
	print(profile)


	user_ids[username] = profile.userid



	processed = 1
	for post in profile.get_posts():
		if processed > config.POSTS_PER_USERNAME:
			break

		print("...scraping info for post %s" % post.shortcode)

		post_info = {
			"shortcode": post.shortcode,
			"username": username,
			"date_utc": post.date_utc.strftime("%Y-%m-%d %H:%M"),
			"url_thumbnail": post.url,
			"url_media": post.video_url if post.is_video else post.url,
			"is_video": "yes" if post.is_video else "no",
			"is_sponsored": post.is_sponsored,
			"hashtags": ",".join(post.caption_hashtags),
			"mentions": ",".join(post.caption_mentions),
			"caption": emoji.demojize(post.caption),
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

	print("...scraped %i posts for %s" % (processed - 1, username))

#user_file.close()
post_file.close()

print("Done scraping!")
