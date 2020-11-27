import pandas as pd
import numpy as np
df = pd.read_csv('../data/IG/albertsons.csv', sep=",", encoding='cp1252')

## remove rows with errors
df = df.dropna(how='all')

##
df.dtypes

## original caption

## new column where :emoji: -> ^, to accurately count text later
df['caption_no_emoji'] = df['caption'].str.replace(r':[^:\s]*(?:::[^:\s]*)*:', "^")

## create column for caption lengeth in characters
df['caption_length'] = df['caption_no_emoji'].str.len()

## Split list into new series
captions = df['caption_no_emoji'].str.lower().str.split()

## Get amount of unique words
df['caption_unique_words'] = captions.apply(set).apply(len)

## Get amount of words
df['caption_word_count'] = captions.apply(len)

## number of hashtags




## number of mentions
mentions = df['mentions'].str.lower().str.split(',')
df['number_of_mentions'] = mentions.apply(sum)


## number of emojis



## column for each type of emoji (?)


## new columns for each word in the list of "green words"




df = df.join(df.caption.str.findall('|'.join(["eco", "eco-friendly", "green", "organic", "clean", "sustainable", "sustainability"])).explode().str.get_dummies().sum(level=0))
df.dtypes
