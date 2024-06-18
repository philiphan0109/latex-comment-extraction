import os
import re
from comment_extraction import extract_title, extract_abstract, extract_comments, extract_authors

dir_path = "paper/"

# Title
title = ""
for filename in os.listdir(dir_path):
    if filename.endswith('.tex'):
        file_path = os.path.join(dir_path, filename)
        temp_title = extract_title(file_path)
        if temp_title!= "No title found": 
            title = temp_title
print(title)

# Abstract
abstract = ""
for filename in os.listdir(dir_path):
    if filename.endswith('.tex'):
        file_path = os.path.join(dir_path, filename)
        temp_abstract = extract_abstract(file_path)
        if temp_abstract!= "No abstract found": 
            abstract = temp_abstract
print(abstract)

all_comments = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_comments[filename] = extract_comments(file_path)

for file, comments in all_comments.items():
    print(f"Comments from {file}")
    for comment in comments:
        print(f"- {comment}")
    print("\n")

all_authors = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_authors[filename] = extract_authors(file_path)

for file, authors in all_authors.items():
    print(f"File: {file}")
    for author in authors:
        print(f"Author: {author}")
    print("\n")