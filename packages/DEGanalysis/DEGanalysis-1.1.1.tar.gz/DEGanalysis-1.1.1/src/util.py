import os
import csv
from xlsxwriter.workbook import Workbook

def mkdir(dir,sampls):
    for n in sampls:
        d = os.path.join(dir,n)
        if not os.path.exists(d):
            os.makedirs(d)
        else:
            continue

def tab2xlsx(tab_files,xlsx_file,sheetnames):    
    workbook = Workbook(xlsx_file)
    sn = iter(sheetnames)
    sheet_num = 0 
    for f1 in [csv.reader(open(tab_file,"rb"),delimiter="\t") for tab_file in tab_files]:
      for r,row in enumerate(f1):
        if r%1048576 == 0:          
            sheet_num+=1
            worksheet = workbook.add_worksheet(name=sn.next())
        for c,col in enumerate(row):
            worksheet.write_string(r%1048576,c,col) 
    if sheet_num > len(tab_files): 
        print "Warning: Too large of the %s file, %d sheets in this file has 1048576 line"%(xlsx_file,sheet_num-1)
    workbook.close()
