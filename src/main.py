import sys
import os
import shutil
from textnode import *
from markdown_blocks import *

def copy_tree(src,dst):
    os.makedirs(dst, exist_ok=True)
    for entry in os.listdir(src):
        src_path = os.path.join(src,entry)
        dst_path = os.path.join(dst,entry)
        
        if os.path.isdir(src_path):
            copy_tree(src_path,dst_path)
        else:
            shutil.copy2(src_path,dst_path)



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print ("cwd is:", os.getcwd())
    ##step 1. erase public if it exists and make a new one
    if os.path.exists('./public'):
        shutil.rmtree('./public')
    ##step 2. copy all files from static to public
    copy_tree('./static','./public')
    #generate_page('content/index.md', 'template.html', 'public/index.html' )
    generate_pages_recursive('./content', 'template.html', './public', basepath)

main ()