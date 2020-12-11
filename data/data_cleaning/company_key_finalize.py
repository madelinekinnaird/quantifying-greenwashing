import pandas as pd
import os
import glob


df = pd.read_csv('..\company_key_verified.csv')
len(df)
## only verified accounts
df = df.loc[df['verified'] == 'Verified']

## drop any usernames that are actually hashtags
df['new_col'] = df['username'].astype(str).str[0]
df = df.loc[df['new_col'] != '#']

## drop an usernames that are more than 1 words
def count_words(row):
    if type(row.username) == str:
        return len(row.username.lower().split())
    elif np.isnan(row.username):
        return 0
    else:
        pass

df['words_in_username'] = df.apply(count_words, axis=1)
df = df.loc[(df['words_in_username'] <= 1)]

df = df.drop(['new_col', 'words_in_username'], axis=1)
df
path = '../../data'
df.to_csv(os.path.join(path,r'company_key.csv'))
