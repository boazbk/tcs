import shutil, os

#Collect important markdown files from root directory (index.md and lectures), then place them within the content folder. This is the directory structure that the makefile expects.

#files = ['index.md'] #first file is index.md - we know this file will need to be rendered, next we'll add all the lectures

files = [file for file in os.listdir('.') if os.path.isfile(file)] #all files in root folder

dir_path = os.path.dirname(os.path.realpath(__file__))[:-len("scripts")]  #get os-specific path to the root folder
dest = dir_path + "scripts\\content"
print(dir_path)
print(dest)
content = []

for file in files:
    if(file == "index.md" or file=="metadata.yaml" or file =="introtcs.bib" or file.startswith("lec_")):
        content.append(file)
    
for file in content:
    shutil.copy(dir_path+file,dest)
