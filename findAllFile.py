import os


g=os.walk(r"C:\Users\PharmaOryx-YJ\Desktop\pubchemdata\pubchem1~100w\XML\XML")

for path,dir_list,file_list in g:
    for file_name in file_list:
        print(file_name)