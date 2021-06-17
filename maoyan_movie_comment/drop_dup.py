import pandas as pd
import os

for fn in os.listdir('datas/'):
    mdata = pd.read_csv('datas/' + fn)
    #print(mdata[mdata.duplicated()])
    print(mdata.shape[0],end='\t')
    mdata.drop_duplicates(inplace=True)
    print(mdata.shape[0])
    mdata.to_csv('datas/{}'.format(fn),index=False)