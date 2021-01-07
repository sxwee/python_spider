import pandas as pd

mdata = pd.read_csv('mobile_info.csv')
#print(mdata[mdata.duplicated()])
mdata.drop_duplicates(inplace=True)
mdata.to_csv('mobile_info_drop_dup.csv',index=False)