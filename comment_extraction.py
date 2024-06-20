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
        if line.startswith('%'): # This means that the line is a full line comment
            if not current_comment:
                comment_start_index = current_index
            current_comment.append(line.strip())
        else: # If it's not a full line comment, it can mean two things
            
            # 1) there is a comment at the END of the line (this excludes any \%s)
            end_of_line_comment = re.search(r'(?<!\\)%.*$', line)
            if end_of_line_comment:
                comment_start_index = current_index + end_of_line_comment.start()
                comments[comment_start_index] = [end_of_line_comment.group()]
            
            if current_comment: # 2) this line is not a part of a block comment anymore, so save the previous block comment to the dictionary
                comments[comment_start_index] = current_comment
                current_comment = []
                
                
        current_index += len(line) + 1
    
    # one last save
    if current_comment: 
                comments[comment_start_index] = current_comment
                current_comment = []
    
    return comments

def extract_comment_length(path):
    comments = extract_comments(path)
    comment_lengths = {index: len(" ".join(comment)) for index, comment in comments.items()}
    return comment_lengths

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
    
# To test your code, uncomment (with command + /) and run this
# This should work... if not it shouldn't be easy to fix :D

comment_lengths = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        comment_lengths[filename] = extract_comment_length(file_path)

for file, comments in comment_lengths.items():
    print(f"Comments from {file}")
    for char, length in comments.items():
        print(f"{char}: {length}")
    print("\n")

    