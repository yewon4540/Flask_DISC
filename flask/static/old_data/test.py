import pandas as pd

df = pd.DataFrame(columns=['D','I','S','C'])

df.loc[0] = [0,0,0,0]
# df['D'].loc[0] += 1
df.to_csv('./PM8_all.csv', index=False)
