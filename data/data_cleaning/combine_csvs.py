import pandas as pd
import os
import glob

## set directory for data intake
os.chdir("../data/all_instagram_posts")

## import
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
df = pd.concat([pd.read_csv(f, sep=",", encoding = "ISO-8859-1") for f in all_filenames])

## set directory back to data
os.chdir("../")

#export combined csv
df.to_csv( "instagram_data_raw.csv", index=False, encoding='utf-8-sig')
