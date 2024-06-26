import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data files (only need to do this once)
nltk.download('punkt')

dir_path = "paper/"

def extract_comments(path):
    comments_by_section = {}

    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()
    
    current_index = 0
    comment_start_index = -1
    comment_end_index = -1
    current_comment = False
    current_section = "Other"
    
    lines = full_paper.split("\n")
    for line in lines:
        if line.startswith("\\section{"):
            current_section = line.strip()[9:-1]
            if current_comment not in comments_by_section:
                comments_by_section[current_comment] = []
            
        if "\\begin{abstract}" in line:
            current_section = "Abstract"
            if current_section not in comments_by_section:
                comments_by_section[current_section] = []
        elif "\\end{abstract}" in line:
            current_section = "Other"
        
        if line.startswith("%"):
            if not current_comment:
                comment_start_index = current_index
                current_comment = True
            comment_end_index = current_index + len(line)
        else:
            end_of_line_comment = re.search(r'(?<!\\)%.*$', line)
            if end_of_line_comment:
                comment_start_index = current_index + end_of_line_comment.start()
                comment_end_index = current_index + len(line)
                comments_by_section[current_section].append((comment_start_index, comment_end_index))
            if current_comment:
                comments_by_section[current_section].append((comment_start_index, comment_end_index))
                current_comment = False
        current_index += len(line) + 1
        
    if current_comment: 
        comments_by_section[current_section].append((comment_start_index, comment_end_index))
        current_comment = False
        
    return comments_by_section

def extract_comment_indices(path):
    comment_indices = []

    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()
    
    current_index = 0
    comment_start_index = -1
    comment_end_index = -1
    current_comment = False
    
    lines = full_paper.split("\n")
    for line in lines:
        if line.startswith("%"):
            if not current_comment:
                comment_start_index = current_index
                current_comment = True
            comment_end_index = current_index + len(line)
        else:
            end_of_line_comment = re.search(r'(?<!\\)%.*$', line)
            if end_of_line_comment:
                comment_start_index = current_index + end_of_line_comment.start()
                comment_end_index = current_index + len(line)
                comment_indices.append((comment_start_index, comment_end_index))
            if current_comment:
                comment_indices.append((comment_start_index, comment_end_index))
                current_comment = False
        current_index += len(line) + 1
        
    if current_comment: 
        comment_indices.append((comment_start_index, comment_end_index))
        current_comment = False
        
    return comment_indices

def extract_comment_statistics(path):
    comment_indices = extract_comment_indices(path)
    comments = {}
    
    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()
    
    for start, end in comment_indices:
        comment = full_paper[start: end]
        comment = comment.split("\n")
        comments[start] = comment
    
    comment_statistics = {}
    for index, comment in comments.items():
        for i in range(len(comment)):
            comment[i] = comment[i][1:].strip()
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

