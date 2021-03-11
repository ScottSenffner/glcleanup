import os
import glob
import pandas as pd
os.chdir("C:\\temp\\2019 GL History")
extension = 'csv'
for fname in glob.glob ('*_*.csv'):
    os.remove(fname)
    print('Just deleted all files', fname)
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, encoding='iso-8859-1', header=None) for f in all_filenames ])
fname = 'GL todays date'
#export to csv
combined_csv.to_csv(fname + '-combined-ready.csv', index=False, encoding='utf-8')
print('Completed Successfully' + " " + fname)
