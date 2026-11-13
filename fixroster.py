#!/usr/bin/env python3  
""" fixroster: take the roster from Club Central and create a new spreadsheet with 
               names and phone number formatting fixed """
import sys
import os.path
import csv
import re


def fixname(name):
    specials = {'SUNIL MENON': 'Sunil Menon',
                'Alexander Bandel': 'Alex Bandel', 
                'May-Chen Martin-Kuo': 'May Martin-Kuo',
                'SHU ZHANG': 'Shu Zhang'}    
        
    # Suppress middle initials
    newname = re.sub(r'^\s*(\w*)\s*(?:[A-Z]\.?)?\s+(\w*)$', r'\1 \2', name)
    if newname in specials:
        newname = specials[newname]
        
    return newname

def fixphone(num):
    # Converts 10-digit phone numbers or numbers starting with "+1" to npa-nnn-xxxx format.
    innum = num
    if num.startswith('+1'):
        num = num[2:]  # Strip +1
    elif num.startswith('1'):
        num = num[1:]
    num = re.sub(r'[^0-9]','', num)
    if len(num) == 10:
        return num[0:3] + '-' + num[3:6] + '-' + num[6:]
    else:
        return innum
        
    
if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = 'members.tsv'                
    with open(infile, newline='') as csvfile:
        outcols = ['Name', 'Email', 'Home Phone', 'Mobile Phone', 'Additional Phone']
        phonecols = ['Home Phone', 'Mobile Phone', 'Additional Phone']
        outrows = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Status (*)'].lower().startswith('unpaid'):
                continue
            if row['Name']:
                row['Name'] = fixname(row['Name'])
                for c in phonecols:
                    row[c] = fixphone(row[c])
                outrows.append(list([row[n] for n in outcols]))
        with open(outfile, 'w', newline='') as out:
            writer = csv.writer(out, delimiter='\t')
            writer.writerows(sorted(outrows))


            
