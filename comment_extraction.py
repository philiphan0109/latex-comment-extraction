import os
import re

dir_path = "paper/"

def extract_comments(path):
    comments = {}

    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()
    
    current_index = 0
    comment_start_index = -1
    current_comment = []
    
    lines = full_paper.split("\n")
    for line in lines:
        stripped_line = line
        
        if line.startswith('%'):
            if not current_comment:
                comment_start_index = current_index
            current_comment.append(line.strip())
        else: 
            if current_comment:
                comments[comment_start_index] = current_comment
                current_comment = []
                
                
        current_index += len(line) + 1
        
    return comments

all_comments = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_comments[filename] = extract_comments(file_path)

for file, comments in all_comments.items():
    print(f"Comments from {file}")
    for char, comment in comments.items():
        print(f"{char}: {comment}")
    print("\n")