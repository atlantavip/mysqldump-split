# -*- coding: utf-8 -*-
import os, re

temp_path       = 'sql_split'
load_file_name  = 'sql_split.test.sql'

re_new_line             = '[\n\r\s]{1,}'
re_new_line_hyphen      = '[\n\r\s]{0,}--\s'
re_table_name_template  = '[`]{0,1}(?P<table_name>[a-zA-Z\_\-\d]+)[`]{0,1}'
re_content_template     = '(?P<content>[\w\W]+)'

re_split_text      = r"{nrh}{nrh}Table structure for table {table_name}{nrh}{nr}".format(
                        table_name = re_table_name_template, nr = re_new_line, nrh = re_new_line_hyphen)

re_table_name      = r"{nrh}Table structure for table {table_name}{nrh}{nr}".format(
                        table_name = re_table_name_template, nr = re_new_line, nrh = re_new_line_hyphen)
re_table_structure = r"{nrh}Table structure for table {table_name}{nrh}{nr}{content}{nrh}{nrh}Dumping data".format(
                        table_name = re_table_name_template, nr = re_new_line, nrh = re_new_line_hyphen, content = re_content_template)
re_table_data      = r"{nrh}Dumping data for table {table_name}{nrh}{nr}{content}".format(
                        table_name = re_table_name_template, nr = re_new_line, nrh = re_new_line_hyphen, content = re_content_template)


def file_open(filename):
  ret = ''
  filehandle = open(filename, encoding="utf8")
  ret = filehandle.read()
  filehandle.close()
  return ret
  
def file_write(filename, content):
  file = os.path.normpath(os.path.join(os.getcwd(), 'sql_split', filename))
  with open(file, "w", encoding="utf8") as text_file:
    print(f"{content}", file=text_file)

  
def dump2file(table_dump):
  #table name search
  table_name_matches  = re.search(re_table_name, table_dump)
  if (table_name_matches == None):
    return
    
  table_name          = table_name_matches.group('table_name')
  print ('export: {table_name}'.format(table_name = table_name))
  
  #table structure search
  table_structure_matches = re.search(re_table_structure, table_dump)
  table_structure         = table_structure_matches.group('content')
  file_write('{table_name}_structure.sql'.format(table_name = table_name), table_structure)
  
  #table data search
  table_data_matches  = re.search(re_table_data, table_dump)
  table_data          = table_data_matches.group('content')
  file_write('{table_name}_data.sql'.format(table_name = table_name), table_data)

  
def get_content():

  content = file_open(load_file_name)
  iter = re.finditer(re_split_text, content)
  indices = [m.start(0) for m in iter]

  last_index = -1
  for index in indices:
    if (last_index == -1):
      last_index = index
      continue
      
    table_dump = content[last_index:index]
    dump2file(table_dump)
    
    last_index = index
  
  table_dump = content[last_index:len(content)]
  dump2file(table_dump)

if __name__ == '__main__':
  get_content()

