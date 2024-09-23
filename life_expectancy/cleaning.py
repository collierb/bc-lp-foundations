import pandas as pd

def clean_data():
    df = pd.read_csv('data/eu_life_expectancy_raw.tsv', sep='\t')
    df[['unit','sex','age','region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df.drop(columns='unit,sex,age,geo\\time', inplace=True)
    long_df = pd.melt(df, id_vars=['unit','sex','age','region'], var_name='year', value_name='value')
    long_df['year'] = long_df.year.str.strip().astype(int)
    long_df['value'] = long_df.value.str.split(expand=True)[0]
    long_df['value'] = pd.to_numeric(long_df.value, errors='coerce')
    long_df.dropna(inplace=True)
    long_df.reset_index(inplace=True, drop=True)
    long_df[long_df['region']=='PT'].reset_index(drop=True).to_csv('data/pt_life_expectancy.csv', index=False)
    print('clean and filtered file saved to data folder')

clean_data()