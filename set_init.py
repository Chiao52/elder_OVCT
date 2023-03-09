import os

def init_file_name():
    dirPath = r'./functions'
    file_list = os.listdir(dirPath)
    file_name = []
    for i in file_list:
      j = i.strip('.py')
      file_name.append(j)

    #write ./function/__init__.py
    file = open('./functions/__init__.py', 'w')
    file.write("__all__ = ")
    file.write(str(file_name))
    file.close()
