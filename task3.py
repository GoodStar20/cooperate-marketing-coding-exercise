import pandas as pd

df = pd.read_csv('task3_dateset.csv')

df['Date'] = pd.to_datetime(df['Date'])

df = df.sort_values(by=['Site', 'Date'])

def correct_ads_run(group):
    first_nonzero_index = group['Ads_Run'].ne(0).idxmax()
    group['Corrected_Ads_Run'] = group.loc[first_nonzero_index, 'Ads_Run']
    for i in range(first_nonzero_index + 1, len(group)):
        if group.loc[i, 'Ads_Run'] == 0:
            group.loc[i, 'Corrected_Ads_Run'] = max(0, group.loc[i - 1, 'Corrected_Ads_Run'] - 1)
        else:
            group.loc[i, 'Corrected_Ads_Run'] = group.loc[i, 'Ads_Run']

    return group

corrected_df = df.groupby('Site').apply(correct_ads_run)

corrected_df.to_csv('corrected_task3_dataset.csv', index=False)
