'''preprocess data'''
import pandas as pd
import argparse

def clean_data(country):
    '''function to load, process and save data'''
    abs_path = 'C:/Users/colli/Documents/dareData/assignments/life_expectancy/'
    df = pd.read_csv(abs_path + 'data/eu_life_expectancy_raw.tsv', sep='\t')
    df[['unit','sex','age','region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df.drop(columns='unit,sex,age,geo\\time', inplace=True)
    long_df = pd.melt(df,
                      id_vars=['unit','sex','age','region'],
                      var_name='year',
                      value_name='value')
    long_df['year'] = long_df.year.str.strip().astype(int)
    long_df['value'] = long_df.value.str.split(expand=True)[0]
    long_df['value'] = pd.to_numeric(long_df.value, errors='coerce')
    long_df.dropna(inplace=True)
    long_df.reset_index(inplace=True, drop=True)
    pt_df = long_df[long_df['region']==country].reset_index(drop=True)
    pt_df.to_csv(abs_path + f'data/{country}_life_expectancy.csv', index=False)
    print(f'clean and filtered file for {country} saved to data folder')

if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description='country filter for life expectancy data')
    parser.add_argument('--country', default='PT', help='select country for filter in ISO2 format eg FR')
    args = parser.parse_args()                
    clean_data(args.country)
