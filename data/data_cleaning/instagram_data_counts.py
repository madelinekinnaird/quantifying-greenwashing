import pandas as pd
import numpy as np
import os
import glob

## get back up to data directory
os.chdir("../")
df = pd.read_csv('master_data_postlevel_clean.csv')

################################### GREEN WORDS ####################################################

## GREEN WORDS
text_file = open("../greenwords.txt", "r")
green_words = text_file.read().split(',')


def green_words_count(column):
    '''
    Function which creates new column count of green words
    '''
    for word in green_words:
        df[column+'_'+word] = df[column].str.count(word)


################################### DATE_UTC ####################################################

## turn to datetime
df['date_utc'] = pd.to_datetime(df['date_utc'])

## if posted exactly on the 00
df['likely_automated'] = df['date_utc'].dt.strftime('%S') == '00'
df['likely_automated'].value_counts()

## frequency of posting, for now this range is Jan1 to Dec5 (338 days)
df['posts_per_day'] =
df.groupby('company').size()
df['posts_per_month'] =
df['posts_per_year'] =

## number of posts each month
## hypothesis that less posts in june of 2020 corresponds with better ESG score


################################### IS_VIDEO ####################################################

yn_map = {'yes': 1, 'no': 0}
df['is_video'] = df['is_video'].map(yn_map)

################################### IS_SPONSORED ####################################################

yn_map = {'TRUE': 1, 'FALSE': 0}
df['is_sponsored'] = df['is_sponsored'].map(yn_map)

################################### HASHTAGS ####################################################

## number of hashtags per post
def count_hashtags(row):
    if type(row.hashtags) == str:
        return len(row.hashtags.split(','))
    elif np.isnan(row.hashtags):
        return 0
    else:
        pass

df['hashtag_counts'] = df.apply(count_hashtags, axis=1)


## green words in hashtags
green_words_count('hashtags')

################################### MENTIONS ####################################################

## number of mentions per post
def count_mentions(row):
    if type(row.mentions) == str:
        return len(row.mentions.split(','))
    elif np.isnan(row.mentions):
        return 0
    else:
        pass

df['mention_counts'] = df.apply(count_mentions, axis=1)

## green words in mentions
green_words_count('mentions')

################################### CAPTIONS ####################################################

## total words
def count_words(row):
    if type(row.caption) == str:
        return len(row.caption.lower().split())
    elif np.isnan(row.caption):
        return 0
    else:
        pass

df['caption_num_words'] = df.apply(count_words, axis=1)


## unique words
def count_uwords(row):
    if type(row.caption) == str:
        return len(set(row.caption.lower().split()))
    elif np.isnan(row.caption):
        return 0
    else:
        pass

df['caption_unique_words'] = df.apply(count_uwords, axis=1)


## green words in mentions
green_words_count('caption')
####### EMOJIS ########

## new column where :emoji: -> X and type string, to more accurately count character and words later
df['caption_for_counts'] = df['caption'].str.replace(r':[^:\s]*(?:::[^:\s]*)*:', "X")

## create column for caption lengeth in characters
df['caption_length'] = df['caption_for_counts'].str.len()


## number of emojis
X_counts = df['caption'].str.count('X')
X_emoji_counts = df['caption_for_counts'].str.count('X')
df['emoji_counts'] = X_emoji_counts - X_counts


################################### LOCATION ####################################################

## has a location or not
col = df['location_name'].notnull()
df['has_location'] = col.astype(int)
df['has_location'].value_counts()

############################################ EXPORT TO CSV ######################################################

## export csv to data folder
df.to_csv( "master_data_postlevel_counts.csv", index=False, encoding='utf-8-sig')
