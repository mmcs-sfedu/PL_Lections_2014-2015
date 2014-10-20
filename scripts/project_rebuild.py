#!/usr/bin/python
# coding: utf8

import os
import re
import sys
import glob
from translate import Translator

#============================================ Global vars ==============================================

src_dir_name = 'src'
src_dir = sys.path[0] + '/' + src_dir_name + '/'
src_file_name_template = src_dir + 'lecture*.md'
der_dir_name = 'lecture'
der_dir = sys.path[0] + '/' + der_dir_name
der_file_name_template = der_dir + '/*.md'
dictionary_name = 'dictionary'
dictionary = sys.path[0] + '/' + dictionary_name
dictionary_separator = ' : '
translator = Translator('en', 'ru')

#============================================= Functions ===============================================

def make_index():
	index_file = open('index.md', 'w', encoding='utf8')
	
	write_index_head(index_file)
	
	i = 0
	regex_parts_tag = re.compile('.*<a name="|">.*\n')
	regex_link_text = re.compile('.*#|`|\n')
	pre_line = ''
	
	for der_file_name in sorted(glob.glob( der_file_name_template )):
		der_file_name = der_file_name.replace('\\', '/')
		der_file = open(der_file_name, 'r', encoding='utf8')
		link_file_name = re.compile('.*/').sub('', der_file_name).replace('.md', '.html')
		for line in der_file:
			if line.startswith('# '):
				i=i+1
				index_file.write(str(i) + '. [' + line.replace('`', '').replace('# ', '').replace('\n', '') + '] (' + der_dir_name + '/' + link_file_name + ')\n')
			if line.startswith('## '):
				index_file.write('\t*')
			if line.startswith('### '):
				index_file.write('\t\t*')
			
			if line.startswith('## ') or line.startswith('### '):
				index_file.write(' [' + regex_link_text.sub('', line).strip() + '] (' + der_dir_name + '/' + link_file_name + '#' + regex_parts_tag.sub('', pre_line) + ')\n')
			pre_line = line
		
		index_file.write('\n\n')
		
	index_file.close()

#==============================================

def make_der_files(refresh_dict):
	try:
		os.makedirs(der_dir)
	except OSError:
		pass
	
	if refresh_dict:
		clean_dictionary()
	
	for lect_file_name in glob.glob( src_file_name_template ):
		lect_file = open(lect_file_name, 'r', encoding='utf8')
		der_file = open(lect_file_name.replace(src_dir_name, der_dir_name).
		  replace('lecture_', ''), 'w', encoding='utf8')
		
		write_der_head(der_file)
		
		regex_str_val = re.compile('.*# |`|\n')
		for line in lect_file:
			if line.startswith('## ') or line.startswith('### '):
				str_val = regex_str_val.sub('', line)
				lat_str_val = get_from_dictionary(str_val)
				
				if lat_str_val == '':
					lat_str_val = format_tag(cyr_to_lat(str_val))
					add_to_dictionary(str_val, lat_str_val)
					
				der_file.write('\n\n<a id="' + lat_str_val + '" ' + 'title="' + str_val + '" class="toc-item"></a>\n')
				
				der_file.write(line + '\n\n')
			else:
				der_file.write(line)
		
		der_file.close()
		lect_file.close()

#==============================================

def write_index_head(file_to_write):
	write_warning(file_to_write)
	file_to_write.write('---\n')
	file_to_write.write('layout: default\n')
	file_to_write.write('title: Лекции по курсу «Языки программирования» 2014, ФИИТ на Мехмате ЮФУ\n')
	file_to_write.write('---\n\n')
	file_to_write.write('Конспект лекций по курсу ЯП\n=====================\n\n')

#==============================================

def write_der_head(file_to_write):
	write_warning(file_to_write)
	file_to_write.write('---\n')
	file_to_write.write('layout: default\n')
	file_to_write.write('---\n\n')

#==============================================

def write_warning(file_to_write):
	file_to_write.write('<!--\n')
	file_to_write.write('WARNING!!!\n')
	file_to_write.write('This file was generated automatically.\n')
	file_to_write.write('All changes made here will be erased.\n')
	file_to_write.write('-->\n\n\n')

#==============================================

def cyr_to_lat(cyr_text):
	#return transletter(cyr_text)
	return translator.translate(cyr_text)

#==============================================

#def transletter(cyr_text):
	#chars = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
	   #'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
	   #'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
	   #'ц':'c','ч':'ch','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
	   #'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E',
	   #'Ё':'E', 'Ж':'Zh','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M',
	   #'Н':'N', 'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F',
	   #'х':'H', 'Ц':'C','Ч':'Ch','Ш':'Sh','Щ':'Scz','Ъ':'','Ы':'Y','Ь':'',
	   #'Э':'E', 'Ю':'Ju','Я':'Ya',',':'','?':'',' ':'_','~':'','!':'',
	   #'@':'','#':'', '$':'','%':'','^':'','&':'','*':'','(':'',')':'',
	   #'-':'_','=':'','+':'', ':':'',';':'','<':'','>':'','\'':'','"':'',
	   #'\\':'','/':'','№':'', '[':'',']':'','{':'','}':''}
	
	#for char in chars:
		 #cyr_text = cyr_text.replace(char, chars[char])
	#return cyr_text

#==============================================

def clean_dictionary():
	dict_lines = []
	
	dict_file = open(dictionary, 'r', encoding='utf8')
	for line in dict_file:
		if line.startswith('#'):
			dict_lines.append(line)
	dict_file.close()
	
	dict_file = open(dictionary, 'w', encoding='utf8')
	for line in dict_lines:
		dict_file.write(line)
	dict_file.close

#==============================================

def get_from_dictionary(key):
	regex_key = re.compile(dictionary_separator + '.*|#|\n')
	regex_val = re.compile('.*' + dictionary_separator + '|\n')
	val = ''
	try:
		dictionary_file = open(dictionary, 'r', encoding='utf8')
	except IOError:
		#print ("file not found")
		return val
	
	for line in dictionary_file:
		if regex_key.sub('', line) == key:
			val = regex_val.sub('', line)
	
	dictionary_file.close()
	return val

#==============================================

def add_to_dictionary(key, val):
	dictionary_file = open(dictionary, 'a', encoding='utf8')
	dictionary_file.write(key.replace('\n', '') + dictionary_separator + val.replace('\n', '') + '\n')
	dictionary_file.close()
	
#==============================================

def format_tag(tag):
	tag = tag.lower()
	
	tag = tag.replace('.net', 'dot_net')
	
	replaces = {'\n':'', '-':' ', '+':' plus ', '*':' asterisk ', '.':'', ',':'', '(':'', ')':''}
	for repl in replaces:
		tag = tag.replace(repl, replaces[repl])
	
	replaces = {' a ': ' ', 'an ': ' ','the ':' '}
	for repl in replaces:
		tag = tag.replace(repl, replaces[repl])
	
	tag = re.sub(r'\s+', '_', tag.strip())
	
	#print(tag)
	if len(tag) > 25:
		replaces = {'function': 'func', 'structure': 'struct', 'dynamic': 'dyn', 'two_dimensional':'2d',
			  'c_plus_plus':'cpp'}
		for repl in replaces:
			tag = tag.replace(repl, replaces[repl])
	
	#print(tag)
	return tag