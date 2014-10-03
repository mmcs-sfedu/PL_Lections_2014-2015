#!/usr/bin/python

import glob
import urllib.parse

index_file = open('index.md', 'w')

index_file.write('---\n')
index_file.write('layout: default\n')
index_file.write('title: Лекции по курсу «Языки программирования» 2014, ФИИТ на Мехмате ЮФУ\n')
index_file.write('---\n\n')
index_file.write('Конспект лекций по курсу ЯП\n=====================\n\n')



i = 0
for lect_file_name in sorted(glob.glob('./lecture*.md')):
  lect_file = open(lect_file_name, 'r')
  for line in lect_file:
    if line.startswith('# '):
      i = i+1
      index_file.write(line.replace('# ', '\n' + str(i) + '. [').replace('\n', '') + '](' + 
		       lect_file_name.replace('./', '').replace('.md', '.html)\n')
		       ) 
    if line.startswith('## '):
      index_file.write(line.replace('## ', '\t* [').replace('\n', '](') + 
		       lect_file_name.replace('./', '').replace('.md', '.html#') + 
		       urllib.parse.quote( line.replace('## ', '').replace('\n', '').encode('utf8') ) + ')\n'
		       )
    if line.startswith('### '):
      index_file.write(line.replace('### ', '\t\t* [').replace('\n', '](') + 
		       lect_file_name.replace('./', '').replace('.md', '.html#') + 
		       urllib.parse.quote( line.replace('### ', '').replace('\n', '').encode('utf8') ) + ')\n'
		       )
  index_file.write('\n\n')
      