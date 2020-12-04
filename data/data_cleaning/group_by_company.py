import pandas as pd
import numpy as np
import os

#path = os.getcwd()
#print(path)

## import both instagram and rating csvs
df = pd.read_csv('..\instagram_data.csv')
ratings = pd.read_csv('..\environment_ratings.csv')

df.dtypes
## aggregations for all of the green words
green_aggs = [np.sum, np.min, np.max, np.std, np.mean, np.median]

## dictionary for each columns aggregation
aggregations = {'shortcode' :'count',
                'is_video' : [np.sum, np.mean],
                'is_sponsored': [np.sum, np.mean],
                'caption' : 'count',
                'video_view_count' : [np.sum, np.mean],
                'likes' : [np.sum, np.mean],
                'comments' : [np.sum, np.mean],
                'likes+comments' : [np.sum, np.mean],
                'caption_num_words' : [np.sum, np.mean],
                'caption_unique_words': [np.sum, np.mean],
                'mention_counts': [np.sum, np.mean],
                'hashtag_counts' : [np.sum, np.mean],
                'emoji_counts' : [np.sum, np.mean],
                'mentions_eco' : green_aggs,
                'mentions_eco-friendly': green_aggs,
                'mentions_green': green_aggs,
                'mentions_organic' : green_aggs,
                'mentions_clean' : green_aggs,
                'mentions_sustainable' : green_aggs,
                'mentions_sustainability' : green_aggs,
                'mentions_carbon' : green_aggs,
                'mentions_emissions' : green_aggs,
                'hashtags_eco' : green_aggs,
                'hashtags_eco-friendly' : green_aggs,
                'hashtags_green' : green_aggs,
                'hashtags_organic' : green_aggs,
                'hashtags_clean' : green_aggs,
                'hashtags_sustainable' : green_aggs,
                'hashtags_sustainability' : green_aggs,
                'hashtags_carbon' : green_aggs,
                'hashtags_emissions' : green_aggs,
                'caption_eco' : green_aggs,
                'caption_eco-friendly' : green_aggs,
                'caption_green' : green_aggs,
                'caption_organic' : green_aggs,
                'caption_clean' : green_aggs,
                'caption_sustainable' : green_aggs,
                'caption_sustainability' : green_aggs,
                'caption_carbon' : green_aggs,
                'caption_emissions' : green_aggs,
                'likely_automated' : [np.sum, np.std, np.mean]
    }
df.dtypes

df_agg = df.groupby('username', as_index = False).agg(aggregations)


output = df_agg.merge(ratings,on=['username'], how='inner')

path_to_file = "../Data"
output.to_csv("path_to_file, index = False, encoding="utf-8")



import pandas as pd

read_file = pd.read_csv (r'C:/Users/madel/projects/quantifying-greenwashing/data/Data')
read_file.to_csv(r'C:/Users/madel/projects/quantifying-greenwashing/data/Data.csv', index=None)
