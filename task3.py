import pandas as pd

df = pd.read_csv("task3_dateset.csv")

df['Date'] = pd.to_datetime(df['Date'])

grouped = df.groupby('Site').apply(lambda x: x.sort_values('Date')).reset_index(drop=True)

# Iterate over each group
for name, group in grouped.groupby('Site'):
    try:
        first_non_zero_index = group['Ads_Run'].ne(0).idxmax()
    except ValueError:
        continue  # Skip this group if there are no non-zero values
    first_non_zero_value = group.loc[first_non_zero_index, 'Ads_Run']

    group.loc[first_non_zero_index:, 'Corrected_Ads_Run'] = first_non_zero_value

    prev_ads_run = first_non_zero_value
    for i, row in group.iloc[:first_non_zero_index].iterrows():
        if row['Ads_Run'] == 0:
            prev_ads_run -= 1
            grouped.at[i, 'Corrected_Ads_Run'] = max(0, prev_ads_run)
        else:
            break

    prev_ads_run = first_non_zero_value

    for i, row in group.iloc[first_non_zero_index + 1:].iterrows():
        if row['Ads_Run'] == 0:
            prev_ads_run += 1
            grouped.at[i, 'Corrected_Ads_Run'] = prev_ads_run


grouped.to_csv("corrected_task3_dataset.csv", index=False)