import pandas as pd

# Create a sample DataFrame
data = {'score_1': [0.1, 0.25, 0.05, 0.15, 0.9],
        'score_2': [0.2, 0.3, 0.8, 0.1, 0.7]}
df = pd.DataFrame(data)

# Create the highlighted column
df['highlighted'] = ((df['score_1'] < 0.35) & (df['score_2'] < 0.35)) | \
                    ((df['score_1'] < 0.20) & (df['score_2'] < 0.90)) | \
                    ((df['score_1'] < 0.15) & (df['score_2'] < 0.80))

# Create the risk_1_group column
def score1_group(score):
    if score < 0.10:
        return 'Very Low'
    elif 0.10 <= score < 0.30:
        return 'Medium'
    elif 0.30 <= score < 0.80:
        return 'High'
    else:
        return 'Very High'

df['risk_1_group'] = df['score_1'].apply(score1_group)

print(df)