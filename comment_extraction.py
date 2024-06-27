import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data files (only need to do this once)
nltk.download('punkt')

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
        if line.lstrip().startswith("%"):
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

        section_match = re.match(r'\\section{(.+?)}', line)
        if section_match:
            current_section = section_match.group(1)
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

        current_index += len(line) + 1

    if current_comment:
        comments_by_section[current_section].append((comment_start_index, comment_end_index))

    return comments_by_section

if __name__ == "__main__":
    print("hello")
    path_to_main_tex = "paper/main.tex"
    output_path = "paper/a.txt"
    
    results = extract_comments(path_to_main_tex)
    
    with open(output_path, "w", encoding="utf-8") as file:
        for section, comments in results.items():
            file.write(f"Section: {section}\n")
            print(f"Section: {section}")
            for start_idx, end_idx in comments:

                with open(path_to_main_tex, "r", encoding="utf-8") as text_file:
                    text_file.seek(start_idx)
                    comment_text = text_file.read(end_idx - start_idx)
                
                file.write(f"  Comment Indices: ({start_idx}, {end_idx})\n")
                file.write(f"  Comment Text: {comment_text.strip()}\n\n")
                
                print(f"  Comment Indices: ({start_idx}, {end_idx})")
                print(f"  Comment Text: {comment_text.strip()}\n")
