import pandas as pd
import numpy as np
import os
import glob

## get back up to data directory
os.chdir("data/")

df = pd.read_csv('instagram_data_raw.csv')
df.dtypes

## change to binary
yn_map = {'yes': 1, 'no': 0}

## is_video
df['is_video'] = df['is_video'].map(yn_map)




## new column where :emoji: -> X and type string, to more accurately count character and words later
df['caption_for_counts'] = df['caption'].str.replace(r':[^:\s]*(?:::[^:\s]*)*:', "X")

## create column for caption lengeth in characters
df['caption_length'] = df['caption_for_counts'].str.len()



## total words
def count_thing1(row):
    if type(row.caption) == str:
        return len(row.caption.lower().split())
    elif np.isnan(row.caption):
        return 0
    else:
        pass

df['caption_num_words'] = df.apply(count_thing1, axis=1)


## unique words
def count_thing2(row):
    if type(row.caption) == str:
        return len(set(row.caption.lower().split()))
    elif np.isnan(row.caption):
        return 0
    else:
        pass

df['caption_unique_words'] = df.apply(count_thing2, axis=1)


## number of mentions per post
def count_thing3(row):
    if type(row.mentions) == str:
        return len(row.mentions.split(','))
    elif np.isnan(row.mentions):
        return 0
    else:
        pass

df['mention_counts'] = df.apply(count_thing3, axis=1)


## number of hashtags per post
def count_thing4(row):
    if type(row.hashtags) == str:
        return len(row.hashtags.split(','))
    elif np.isnan(row.hashtags):
        return 0
    else:
        pass

df['hashtag_counts'] = df.apply(count_thing4, axis=1)


## number of emojis
df['X_counts'] = df['caption'].str.count('X')
df['X_emoji_counts'] = df['caption_for_counts'].str.count('X')
df['emoji_counts'] = df['X_emoji_counts'] - df['X_counts']



##########################################################################################################################

## GREEN WORDS
green_words = ["eco", "eco-friendly","green", "organic", "clean", "sustainable", "sustainability", "carbon", "emissions"]



def green_words_count(column):
    '''
    Function which creates new column count of green words
    '''
    for word in green_words:
        df[column+'_'+word] = df[column].str.count(word)




## green words in mentions
green_words_count('mentions')

## green words in hashtags
green_words_count('hashtags')

## green words in captions
green_words_count('caption')



## column for likely automated post
## posts that are made exactly on the hour are often pre-scheduled
df['date_utc'] = pd.to_datetime(df['date_utc'])
df['likely_automated'] = df['date_utc'].dt.strftime('%M') == '00'


## column for certain emojis(LATER)

df.dtypes

## explort csv to data folder
df.to_csv( "instagram_data.csv", index=False, encoding='utf-8-sig')

## new columns for each word in the list of "green words"
## df = df.join(df.caption.str.findall('|'.join(["eco", "eco-friendly", "green", "organic", "clean", "sustainable", "sustainability", "carbon", "emissions"])).explode().str.get_dummies().sum(level=0))
