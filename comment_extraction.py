import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data files (only need to do this once)
# nltk.download('punkt')

dir_path = "paper/"

import re

def extract_comments(path):
    comments_by_section = {}

    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()

    current_index = 0
    current_section = "Other"
    comments_by_section[current_section] = []
    current_comment = False
    comment_start_index = 0

    lines = full_paper.split("\n")
    for line in lines:
        # Comment
        if line.lstrip().startswith("%"):
            if not current_comment:
                comment_start_index = current_index
                current_comment = True
            comment_end_index = current_index + len(line)
        else:
            if current_comment:
                comments_by_section[current_section].append((comment_start_index, comment_end_index))
                current_comment = False
        
            end_of_line_comment = re.search(r'(?<!\\)%.*$', line)
            if end_of_line_comment:
                comment_start_index = current_index + end_of_line_comment.start()
                comment_end_index = current_index + len(line)
                comments_by_section[current_section].append((comment_start_index, comment_end_index))
            
        current_index += len(line) + 1
        #Section
        section_match = re.match(r'\\(section|subsection|subsubsection|section*|subsection*|subsubsection*){(.+?)}', line)
        if section_match:
            # print(section_match.group(1))
            current_section = f"{section_match.group(1)}:{section_match.group(2)}"
            if current_section not in comments_by_section:
                comments_by_section[current_section] = []
            current_comment = False
        if "\\begin{abstract}" in line:
            current_section = "Abstract"
            if current_section not in comments_by_section:
                comments_by_section[current_section] = []
            current_comment = False
        elif "\\end{abstract}" in line:
            current_section = "Other"
            current_comment = False

    if current_comment:
        comments_by_section[current_section].append((comment_start_index, comment_end_index))

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

# if __name__ == "__main__":
#     print("hello")
#     path_to_main_tex = "paper/main.tex"
#     output_path = "paper/a.txt"
    
#     results = extract_comments(path_to_main_tex)
    
#     with open(output_path, "w", encoding="utf-8") as file:
#         for section, comments in results.items():
#             file.write(f"Section: {section}\n")
#             print(f"Section: {section}")
#             for start_idx, end_idx in comments:
#                 # Extract the actual comment text from the document
#                 with open(path_to_main_tex, "r", encoding="utf-8") as text_file:
#                     text_file.seek(start_idx)
#                     comment_text = text_file.read(end_idx - start_idx)
                
#                 file.write(f"  Comment Indices: ({start_idx}, {end_idx})\n")
#                 file.write(f"  Comment Text: {comment_text.strip()}\n\n")
                
#                 # Print to console as well
#                 print(f"  Comment Indices: ({start_idx}, {end_idx})")
#                 print(f"  Comment Text: {comment_text.strip()}\n")