#!/usr/bin/env python
# coding: utf-8

import xlrd
import pandas as pd

def format_path(file_path):
    return '/'.join(file_path.split('\\'))

def excel_to_csv(input_path,output_path,input_enc='gb18030',output_enc='utf-8'):
    df=pd.read_excel(format_path(input_path),encoding=input_enc,dtype=object)
    df.to_csv(format_path(output_path),encoding=output_enc,index=False)

fp=format_path
etc=excel_to_csv
