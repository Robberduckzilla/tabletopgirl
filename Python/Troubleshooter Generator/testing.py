import os

all_files = os.listdir()
txt_files = [x[:-4] for x in all_files if '.txt' in x]
print(txt_files)