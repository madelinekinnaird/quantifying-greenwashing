import pandas as pd
import numpy as np
import os
import copy


## import instagram csvs
df = pd.read_csv('..\master_data_postlevel_counts.csv')
df = df.drop(columns=['Unnamed: 0'])

##################################### GENERAL AGGREGATIONS #############################################

## dictionary for each columns aggregation
aggregations = {'shortcode' :'count',
                'is_video' : np.mean,
                'is_sponsored': np.mean,
                'caption' : 'count',
                'video_view_count' : np.mean,
                'video_length': np.mean,
                'likes' : np.mean,
                'comments' : np.mean,
                'caption_num_words' : np.mean,
                'caption_unique_words': np.mean,
                'mention_counts': np.mean,
                'hashtag_counts' : np.mean,
                'emoji_counts' : np.mean,
                'mentions_eco' : np.mean,
                'mentions_eco-friendly': np.mean,
                'mentions_green': np.mean,
                'mentions_organic' : np.mean,
                'mentions_clean' : np.mean,
                'mentions_sustainable' : np.mean,
                'mentions_sustainability' : np.mean,
                'mentions_carbon' : np.mean,
                'mentions_emissions' : np.mean,
                'hashtags_eco' : np.mean,
                'hashtags_eco-friendly' : np.mean,
                'hashtags_green' : np.mean,
                'hashtags_organic' : np.mean,
                'hashtags_clean' : np.mean,
                'hashtags_sustainable' : np.mean,
                'hashtags_sustainability' : np.mean,
                'hashtags_carbon' : np.mean,
                'hashtags_emissions' : np.mean,
                'caption_eco' : np.mean,
                'caption_eco-friendly' : np.mean,
                'caption_green' : np.mean,
                'caption_organic' : np.mean,
                'caption_clean' : np.mean,
                'caption_sustainable' : np.mean,
                'caption_sustainability' : np.mean,
                'caption_carbon' : np.mean,
                'caption_emissions' : np.mean,
                'likely_automated' : np.mean,
                'has_location' : np.mean
    }


## aggregate averages by company
company_info = ['company','environment_rating', 'environment_percentage', 'Country', 'Sales', 'Profits', 'Assets', 'Market Value']
df_agg = df.groupby(company_info, as_index = False).agg(aggregations)


####################################### AVERAGES CONTAINING GREEN WORDS ###########################################
## create a binary column for if any greenwords are present in the caption
colList = ['caption_eco', 'caption_eco-friendly','caption_green', 'caption_organic', 'caption_clean', 'caption_sustainable', 'caption_sustainability', 'caption_carbon', 'caption_emissions', 'likely_automated']
df["greenTrue"] = df[colList].any(1).astype(int)

## set aggregations
greenAggregations = {'is_video' : np.mean,
                'is_sponsored': np.mean,
                'video_length': np.mean,
                'likes' : np.mean,
                'comments' : np.mean,
                'caption_num_words' : np.mean,
                'caption_unique_words': np.mean,
                'mention_counts': np.mean,
                'hashtag_counts' : np.mean,
                'emoji_counts' : np.mean,
}


values = ['is_video', 'is_sponsored', 'video_length', 'likes', 'comments', 'caption_num_words', 'caption_unique_words', 'mention_counts','hashtag_counts', 'emoji_counts']

## group by if green or not
green_agg = df.groupby(['company', 'greenTrue'], as_index = False).agg(greenAggregations)
green_agg = green_agg.pivot(index='company', columns='greenTrue', values=values)
green_agg = green_agg.reset_index()

## make a copy for different manipulations
green_aggs_diffs = copy.deepcopy(green_agg)

## get rid of the double index and make column names more legible
a = green_agg.columns
ind = pd.Index([e[0] + '_' + str(e[1]) for e in a.tolist()])
green_agg.columns = ind
green_agg = green_agg.rename(columns={"company_": "company"})

## calculate difference between averages with and without green_words
for column in values:
    green_aggs_diffs[column+'_green_diff'] = green_aggs_diffs[column][1] - green_aggs_diffs[column][0]
## drop extra index
green_aggs_diffs.columns = green_aggs_diffs.columns.droplevel(-1)


green_aggs_complete = green_agg.merge(green_aggs_diffs, on='company')

####################################### MERGE ##########################################################
## merge green ags
company_level_data = df_agg.merge(green_aggs_complete, on='company')


####################################### POST FREQUENCY ##########################################################
## posts per year
company_level_data = company_level_data.rename(columns={"shortcode": "posts_per_year"})

## posts per day, currently data goes through dec 5th so only 39 days.
company_level_data['posts_per_day'] = company_level_data['posts_per_year']/339

## not all posts have a caption, captions per year
company_level_data['captions_per_year'] = company_level_data['caption']/company_level_data['posts_per_year']


####################################### EXPORT TO CSV ##########################################################
company_level_data.to_csv( "master_data_companylevel_counts.csv", index=False, encoding='utf-8-sig')

#output.to_csv("path_to_file, index = False, encoding="utf-8")
