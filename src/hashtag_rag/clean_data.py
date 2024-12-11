import os
import pandas as pd
from ftlangdetect import detect 
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = os.getenv('BASE_PATH')

dev_file_path = f'{BASE_PATH}/dev.tsv'
train_file_path = f'{BASE_PATH}/train.tsv'
test_file_path = f'{BASE_PATH}/test.tsv'

dev_df = pd.read_csv(dev_file_path, sep='\t')
train_df = pd.read_csv(train_file_path, sep='\t')
test_df = pd.read_csv(test_file_path, sep='\t')

frames = [dev_df, train_df, test_df]

df_csv = pd.concat(frames)

df_csv['lang'] = df_csv['label'].apply(lambda x: detect(text=x, low_memory=False)['lang'])
df_csv['score'] = df_csv['label'].apply(lambda x: detect(text=x, low_memory=False)['score'])

df_csv_alt = df_csv[df_csv['lang'] == 'en']

# print(df_csv_alt.shape)
df_csv_alt.to_csv('~/handlo/data/hashtags/base.csv',index=False)