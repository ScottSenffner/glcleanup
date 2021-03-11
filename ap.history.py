#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
import datetime
import glob
from pandas.tseries.offsets import MonthEnd
batchID = 0


# Prompts the user for file name
for fname in glob.glob ('*history.csv'):
# This brings in the new file into a DataFrame df1
    df1=pd.read_csv(fname, encoding='iso-8859-1', header=None )
# extracts the file extension ".csv"
    fname = fname.rsplit('.', 1)[0]
    df1.columns=['OPRCD','OPAPL','OPVEND','OPSEQ#','OPPF','OPMF','OPINV#','OPIDT','OPVINV','OPBAT#','OPSINV','OPDISF','OPDISC','OPDDT','OPCKT','OPVCK','OPAMT','OPCKNO','OPDIST','OPCKGL','OPPYM','OPPBAT','OPPSEQ','OPDYM','OPDBAT','OPDSEQ','OPDLN','OPDESC','OPCINV']
# Creates a copy of the old date for creating a batch number
    df1['OPPYM-O'] = df1['OPPYM']
    df1['OPDYM-O'] = df1['OPDYM']
    df1['OPIDT'] = np.where(df1['OPIDT']==0, df1['OPDDT'], df1['OPIDT'])
    df1['OPIDT-O'] = df1['OPIDT']
# Converts the date from 19960731 to an actual date of
    df1['OPIDT'] = pd.to_datetime(df1['OPIDT'], format='%Y%m%d')
    df1['OPDDT'] = pd.to_datetime(df1['OPDDT'], format='%Y%m%d')
# This takes the raw date format in the Journal Accounting period (i.e. 200012) and changes it to date format and it adds the last day of the month to each one, ie. 2000-12-31.
    df1['OPPYM-O']=pd.to_datetime(df1['OPPYM-O'], format='%Y%m') + MonthEnd(1)
    df1['OPDYM-O']=pd.to_datetime(df1['OPDYM-O'], format='%Y%m') + MonthEnd(1)
# Creates a batch ID 
    df1.insert(0, 'BatchID', 1)
    df1['BatchID'] = df1['BatchID'] + 1 
# removed unnecessary columns
    df1 = df1.drop(['OPRCD', 'OPSEQ#', 'OPPF', 'OPMF', 'OPVINV', 'OPDISF', 'OPPBAT', 'OPPSEQ','OPDBAT', 'OPDSEQ', 'OPDLN', 'OPCINV', 'OPPYM', 'OPDYM'],  axis=1)
# renames column headers
    df1 = df1.rename(columns={'OPAPL': 'DEPARTMENT', 'OPVEND': 'VENDORID', 'OPINV#': 'DOCNUMBR', 'OPIDT': 'DOCDATE', 'OPSINV': 'APPLDAMT', 'OPDISF': 'Discount_Flag', 'OPDISC': 'DISTAMNT', 'OPDDT': 'CHKDUEDT', 'OPCKT':'CHKTYPE', 'OPVCK': 'VOIDED', 'OPAMT': 'DOCAMNT', 'OPCKNO': 'CHKNO', 'OPDIST': 'DISTKNAM', 'OPCKGL': 'GLNUMBR', 'OPDESC': 'TRXDSCRN' })
# Creates a filename to export
    df1.to_csv(fname + '-ready2.csv', index=False) 
    print('Completed Successfully' + " " + fname)
print('Completed Successfully')
