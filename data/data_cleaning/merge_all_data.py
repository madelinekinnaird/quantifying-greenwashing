import pandas as pd
import os
import glob

################################## COMBINE ALL USERNAMES INSTAGRAM POSTS #############################################
## set directory for data intake
os.chdir("../all_instagram_posts")

## import
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
df = pd.concat([pd.read_csv(f, sep=",", encoding = "ISO-8859-1") for f in all_filenames])

## set directory to data
os.chdir("../")

#export combined csv
df.to_csv( "all_instagram_posts.csv", index=False, encoding='utf-8-sig')

################################## CREATE RAW MASTER DATASET (ESG + FORTUNE 2000) #############################################
## key to instagram posts for company names to merge
dfKey = pd.read_csv('company_key.csv')
df1 = pd.merge(dfKey,df, on='username',how='left')
len(df1)

## merge ESG scores
dfESG = pd.read_csv('esg_ratings.csv')
df1 = pd.merge(df1,dfESG, left_on='esg_company', right_on = 'company',how='left')
df1 = df1.drop(columns=['company_y'])
df1 = df1.rename(columns={"company_x": "company"})
len(df1)

## merge in global2000
df2000 = pd.read_csv('global2000.csv')
df1 = pd.merge(df1, df2000, left_on='company', right_on = 'Company',how='left')
len(df1)
df1.dtypes
##
df1.to_csv( "master_data.csv", index=False, encoding='utf-8-sig')

################################## CREATE MASTER DATASET (ESG + FORTUNE 2000) #############################################

## key to instagram posts for company names to merge
df2 = pd.merge(dfKey,df, on='username',how='left')
len(df2)

## merge ESG scores, only where company has ESGscore
df2 = pd.merge(df2,dfESG, left_on='esg_company', right_on = 'company',how='inner')
df2 = df2.drop(columns=['company_y'])
df2 = df2.rename(columns={"company_x": "company"})
len(df2)

## merge in global2000
df2 = pd.merge(df2, df2000, left_on='company', right_on = 'Company',how='inner')
len(df2)

##
df2.to_csv( "master_data.csv", index=False, encoding='utf-8-sig')
