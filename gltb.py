import pandas as pd
import os
import glob

for fname in glob.glob ('*_*.csv'):
    os.remove(fname)
    print('Just deleted all files', fname)
# Prompts the user for file name
for fname in glob.glob ('*.csv'):
# This brings in the new file into a DataFrame df1
    df1=pd.read_csv(fname, encoding='iso-8859-1', header=None)
# extracts the file extension ".csv"
    fname = fname.rsplit('.', 1)[0]
# brings in the new file
    df1.columns=['ABLOC', 'ABGL#', 'ABYR', 'ABCORP', 'ABTYPE', 'ABBBAL', 'ABM01', 'ABM02', 'ABM03', 'ABM04', 'ABM05', 'ABM06', 'ABM07', 'ABM08', 'ABM09', 'ABM10', 'ABM11', 'ABM12', 'ABS01', 'ABS02', 'ABS03', 'ABS04', 'ABS05', 'ABS06', 'ABS07', 'ABS08', 'ABS09', 'ABS10', 'ABS11', 'ABS12']
# removed unnecessary columns
    df1 = df1.drop(['ABS01', 'ABS02', 'ABS03', 'ABS04', 'ABS05', 'ABS06', 'ABS07', 'ABS08', 'ABS09', 'ABS10', 'ABS11', 'ABS12'],  axis=1)
# adds the leading '0's' to the location
    df1['ABLOC'] = df1['ABLOC'].apply(lambda x: '{0:0>3}'.format(x))
# Merges the ABCORP column with the ABCLOC field and the ABGL# no, ie. 100-100-1000
    df1['ACTNO'] = df1['ABCORP'].map(str) + '-' + df1['ABLOC'].map(str) + '-' + df1['ABGL#'].map(str)
# group by year
    df1 = df1.sort_values(by = ['ABCORP', 'ABLOC'])
# print(df1)
    df1.to_csv(fname + '-ready.csv', index=False)  
    print('Completed Successfully' + " " + fname)