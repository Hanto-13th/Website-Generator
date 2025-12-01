import os
import shutil
import sys

from functions import copy_files_recursive, generate_pages_recursive

#All path we use to generate the website :

#dir_path_static >> all static files like CSS files or images for aesthetic website
#dir_path_docs >> the final directory with all markdown file copied and converted into html file, this is directory Github will use to deploy the website
#dir_path_content >> the directory contains all markdown files with the structure of our final website, to convert after into a HTML website
#template_path >> the model of HTMl page we use to generate the website 

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

"""The main func which copy and transform all markdown file of 'content' into the 'docs' dir depending on 'template.html' and using all files
for aesthetic (images, css files) from 'static' """

def main():
    #check if a arg is passed, to create the URL base path else '/' is used
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    #delete the destination directory to clean it, recreate him and copy all files from static into directory
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    #generate all pages from the content dir into the docs dir using template html model
    print("Generating page...")
    generate_pages_recursive(dir_path_content,template_path,dir_path_docs,basepath)


main()