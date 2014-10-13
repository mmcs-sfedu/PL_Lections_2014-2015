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
#!/usr/bin/python

import os
import re
import glob

#============================================ Global vars ==============================================

src_dir = './'
src_file_name_template = src_dir + 'lecture*.md'
der_dir_name = 'der'
der_dir = './' + der_dir_name
der_file_name_template = der_dir + '/lecture*.md'

#============================================= Functions ===============================================

#def make_index():
	#index_file = open('index.md', 'w')
	
	#index_file.write('---\n')
	#index_file.write('layout: default\n')
	#index_file.write('title: Лекции по курсу «Языки программирования» 2014, ФИИТ на Мехмате ЮФУ\n')
	#index_file.write('---\n\n')
	#index_file.write('Конспект лекций по курсу ЯП\n=====================\n\n')
	
	
	#i = 0
	#for lect_file_name in sorted(glob.glob( src_file_name_template )):
	  #lect_file = open(lect_file_name, 'r')
	  #link_file_name = lect_file_name.replace(src_dir, '').replace('.md', '.html')
	  #for line in lect_file:
	    #prep_line = line.replace('# ', '').replace('#', '').replace(' C', '-c').replace('++', '-1').replace(' ', '-').replace('\n', '')
	    #if line.startswith('# '):
	      #i = i+1
	      #index_file.write(line.replace('# ', '\n' + str(i) + '. [').replace('\n', '') + '](' + 
			      #link_file_name + ')\n'
			      #) 
	    #if line.startswith('## '):
	      #index_file.write(line.replace('## ', '\t* [').replace('`', '').replace('\n', '](') + 
			      #link_file_name + '#' +
			      #urllib.parse.quote( prep_line.replace('## ', '') ) + ')\n'
			      #)
	    #if line.startswith('### '):
	      #index_file.write(line.replace('### ', '\t\t* [').replace('`', '').replace('\n', '](') + 
			      #link_file_name + '#' +
			      #urllib.parse.quote( prep_line.replace('### ', '') ) + ')\n'
			      #)
	  #index_file.write('\n\n')

#==============================================

def make_index():
	index_file = open('index.md', 'w')
	
	index_file.write('---\n')
	index_file.write('layout: default\n')
	index_file.write('title: Лекции по курсу «Языки программирования» 2014, ФИИТ на Мехмате ЮФУ\n')
	index_file.write('---\n\n')
	index_file.write('Конспект лекций по курсу ЯП\n=====================\n\n')
	
	i = 0
	regex_parts_tag = re.compile('.*<a name="|">.*\n')
	regex_link_text = re.compile('.*#')
	pre_line = ''
	
	for der_file_name in sorted(glob.glob( der_file_name_template )):
	  der_file = open(der_file_name, 'r')
	  link_file_name = der_file_name.replace(der_dir + '/', '').replace('.md', '.html')
	  for line in der_file:
	    if line.startswith('# '):
	      i=i+1
	      index_file.write(str(i) + '. [ ' + line.replace('`', '').replace('# ', '').replace('\n', '') + ' ] (' + der_dir_name + '/' + link_file_name + ')\n')
	    if line.startswith('## '):
	      index_file.write('\t*')
	    if line.startswith('### '):
	      index_file.write('\t\t*')
	    
	    if line.startswith('## ') or line.startswith('### '):
	      index_file.write(' [' + regex_link_text.sub('', line).replace('`', '').replace('\n', '') + ' ] (' + der_dir_name + '/' + link_file_name + '#' + regex_parts_tag.sub('', pre_line) + ')\n')
	    pre_line = line
	      
	    
	    
	  index_file.write('\n\n')
	index_file.close()

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
	      der_file.write('\n\n<a name="' + str(i) + '">\n')
	      der_file.write(line)
	      der_file.write('</a>\n\n ')
	    else:
	      der_file.write(line)
	  
	  der_file.close()
	  lect_file.close()

#========================================== Executable code ============================================

make_der_files()
make_index()

#=======================================================================================================
make_der_files()
make_index()

#=======================================================================================================