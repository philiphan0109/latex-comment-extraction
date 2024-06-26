import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data files (only need to do this once)
nltk.download('punkt')

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
        if line.strip().startswith('%'): # This means that the line is a full line comment
            if not current_comment:
                comment_start_index = current_index
            current_comment.append(line.strip()[1:].strip())  # Remove the leading % and strip leading/trailing spaces
        else: # If it's not a full line comment, it can mean two things
            
            # 1) there is a comment at the END of the line (this excludes any \%s)
            end_of_line_comment = re.search(r'(?<!\\)%.*$', line)
            if end_of_line_comment:
                comment_text = end_of_line_comment.group()[1:].strip()  # Remove the leading % and strip spaces
                comment_start_index = current_index + end_of_line_comment.start()
                comments[comment_start_index] = [comment_text]
            
            if current_comment: # 2) this line is not a part of a block comment anymore, so save the previous block comment to the dictionary
                comments[comment_start_index] = current_comment
                current_comment = []
                
        current_index += len(line) + 1
    
    # one last save
    if current_comment: 
        comments[comment_start_index] = current_comment
        current_comment = []
    
    return comments

def extract_comment_statistics(path):
    comments = extract_comments(path)
    comment_statistics = {}

    for index, comment in comments.items():
        comment_text = " ".join(comment)
        char_length = len(comment_text)
        words = word_tokenize(comment_text)
        words = [word for word in words if word.isalnum()]
        word_count = len(words)
        comment_statistics[index] = {
            'char_length': char_length,
            'word_count': word_count
        }
    
    return comment_statistics

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

comment_statistics = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        comment_statistics[filename] = extract_comment_statistics(file_path)

for file, statistics in comment_statistics.items():
    print(f"Statistics from {file}")
    for char, stats in statistics.items():
        print(f"{char}: {stats}")
    print("\n")
