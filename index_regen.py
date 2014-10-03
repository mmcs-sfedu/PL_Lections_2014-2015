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
  link_file_name = lect_file_name.replace('./', '').replace('.md', '.html')
  for line in lect_file:
    prep_line = line.replace('# ', '').replace('#', '').replace(' C', '-c').replace('++', '-1').replace(' ', '-').replace('\n', '')
    if line.startswith('# '):
      i = i+1
      index_file.write(line.replace('# ', '\n' + str(i) + '. [').replace('\n', '') + '](' + 
		       link_file_name + ')\n'
		       ) 
    if line.startswith('## '):
      index_file.write(line.replace('## ', '\t* [').replace('`', '').replace('\n', '](') + 
		       link_file_name + '#' +
		       urllib.parse.quote( prep_line.replace('## ', '') ) + ')\n'
		       )
      #print(  line.replace('## ', '').replace('\n', '')  )
      #print(  urllib.parse.quote( line.replace('## ', '').replace('\n', '') )  )
    if line.startswith('### '):
      index_file.write(line.replace('### ', '\t\t* [').replace('`', '').replace('\n', '](') + 
		       link_file_name + '#' +
		       urllib.parse.quote( prep_line.replace('### ', '') ) + ')\n'
		       )
  index_file.write('\n\n')
      