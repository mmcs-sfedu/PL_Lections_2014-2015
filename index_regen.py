#!/usr/bin/python

import os
import re
import glob
import urllib.parse

#============================================ Global vars ==============================================

src_dir = './'
src_file_name_template = src_dir + 'lecture*.md'
der_dir = './der'

#============================================= Functions ===============================================

def make_index():
	index_file = open('index.md', 'w')
	
	index_file.write('---\n')
	index_file.write('layout: default\n')
	index_file.write('title: Лекции по курсу «Языки программирования» 2014, ФИИТ на Мехмате ЮФУ\n')
	index_file.write('---\n\n')
	index_file.write('Конспект лекций по курсу ЯП\n=====================\n\n')
	
	
	i = 0
	for lect_file_name in sorted(glob.glob( src_file_name_template )):
	  lect_file = open(lect_file_name, 'r')
	  link_file_name = lect_file_name.replace(src_dir, '').replace('.md', '.html')
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
	    if line.startswith('### '):
	      index_file.write(line.replace('### ', '\t\t* [').replace('`', '').replace('\n', '](') + 
			      link_file_name + '#' +
			      urllib.parse.quote( prep_line.replace('### ', '') ) + ')\n'
			      )
	  index_file.write('\n\n')

#==============================================

def make_der_files():
	try:
	   os.makedirs(der_dir)
	except OSError:
	  pass
	
	for lect_file_name in sorted(glob.glob( src_file_name_template )):
	  lect_file = open(lect_file_name, 'r')
	  der_file = open(der_dir + lect_file_name.replace(src_dir, '/'), 'w')
	  
	  der_file.write('---\n')
	  der_file.write('layout: default\n')
	  der_file.write('---\n\n')
	  
	  i = 0
	  for line in lect_file:
	    if line.startswith('## ') or line.startswith('### '):
	      i = i+1
	      der_file.write(line.replace('# ', '# <a name="' + str(i) + '"></a> '))
	    else:
	      der_file.write(line)
	  
	  der_file.close()
	  lect_file.close()

#========================================== Executable code ============================================

make_der_files()
make_index()

#=======================================================================================================