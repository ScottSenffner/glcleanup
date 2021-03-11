#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
import datetime
import glob
from pandas.tseries.offsets import MonthEnd

# Prompts the user for file name
for fname in glob.glob ('*.csv'):
# This brings in the new file into a DataFrame df1
    df1=pd.read_csv(fname, encoding='iso-8859-1', header=None)
# extracts the file extension ".csv"
    fname = fname.rsplit('.', 1)[0]
# (was the old test file location - df1=pd.read_excel("C:\\Users\\ssenffner\\AS400 Export\\GLACT100T-test.xlsx", header=None)
    df1.columns=['JDCORP','JDYM','JDGC','JDLOC','JDGL#','JDSR','JDBAT','JDSEQ','JDLN','JHMC','JDRDT','JHDES','JHDBF','JHDBN','JHREF','JDDES','JDAMT','JDCKNO','JDCKDT','JDDBF','JDDBN','JDRGRP','JDRSTS','JDRB','JDICT','JDCKT','JHSTS','JDSTS']
# Creates a copy of the old date for creating a batch number
    df1['JDYM-O'] = df1['JDYM']
# This validates the check date column to make sure it is more than 0
    df1['JDCKDT'] = np.where(df1['JDCKDT']==0, df1['JDRDT'], df1['JDCKDT'])
# print(df1[0:3]) Test to see if it works.
# This takes the raw date format in the Journal Accounting period (i.e. 200012) and changes it to date format and it adds the last day of the month to each one, ie. 2000-12-31.
    df1['JDYM'] = pd.to_datetime(df1['JDYM'], format='%Y%m') + MonthEnd(1)
    df2=pd.to_datetime(df1['JDYM'], format='%Y%m')
# Converts the date from 19960731 to an actual date of
    df1['JDCKDT'] = pd.to_datetime(df1['JDCKDT'], format='%Y%m%d')
# merges the GL_Corp column with the Dept_Loc_PC field and the GL_Acc no, ie. 100-100-1000
    df1['JDGC'] = df1['JDGC'].map(str) + '-' + df1['JDLOC'].map(str) + '-' + df1['JDGL#'].map(str)
# Creates a batch number from the original Journal Period, Journal Source and Journal Batch No.
    df1['JDSR1'] = df1['JDYM-O'].map(str) + '-' + df1['JDSR'].map(str) + '-' + df1['JDBAT'].map(str)
# Inserts a column at the begining with the new batch number above.
    df1.insert(0, 'Batch', df1['JDSR1'])
# converts the JDSR field from a Base64 to str to add different source codes.
    df1['JDSR'] = df1['JDSR'].astype(str)
# replaces as400 source code with Dynamics source code.
    df1 = df1.replace({'JDSR':{'100' : 'GJ', '5' : 'SJ' , '10' : 'POIVC' , '11' : 'PMPAY' , '13' : 'CRJ' , '15' : 'CMDEP' , '16' : 'CMTRX' , '17' : 'CMXFR' , '20' : 'PA' , '21' : 'PAFNG' , '22' : 'PAACR' , '23' : 'PAREVACR' , '25' : 'PACOC' , '160' : 'RJEGLAMT' , '165' : 'RJECLAMT'}})
# removed unnecessary columns
    df1 = df1.drop(['JDCORP', 'JDLOC', 'JDGL#', 'JDBAT', 'JDSEQ', 'JDLN', 'JHMC', 'JDRDT', 'JHDBF', 'JHDBN', 'JHREF', 'JDYM-O', 'JDSR1', 'JDCKT', 'JDRB', 'JDRGRP', 'JHSTS', 'JDRSTS', 'JDICT', 'JDDBF', 'JDSTS'],  axis=1)
# renames column headers
    df1 = df1.rename(columns={'JDYM': 'Period ID', 'JDSR': 'SourceDoc', 'JDGC': 'Account', 'JHDES': 'Reference', 'JDDES': 'Description', 'JDAMT': 'Amount', 'JDCKNO': 'Check No', 'JDCKDT': 'Transaction Date', 'JDDBN':'Vendor No', 'JDCK': 'Check Type' })
# inserts column for currency
    df1.insert(6, 'CurrencyID', 'Z-US$')
    df1.to_csv(fname + '-ready.csv', index=False)  #'C:\\Users\\Scott\\Desktop\\as400 exports\\' +
    print('Completed Successfully' + " " + fname)
print('Completed Successfully')
