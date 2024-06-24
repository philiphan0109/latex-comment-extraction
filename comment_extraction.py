import os
import re
import nltk
from nltk.tokenize import word_tokenize
import cProfile
import pstats
import io

# Download NLTK data files (only need to do this once)
nltk.download('punkt')

dir_path = "paper/"

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

def debug(path, context=5):
    comment_indices = extract_comment_indices(path)
    
    with open(path, "r", encoding="utf-8") as file:
        full_paper = file.read()
    
    comments_with_stats = {}
    
    for start, end in comment_indices:
        start_context = max(0, start - context)
        end_context = min(len(full_paper), end + context)
        comment_text_with_context = full_paper[start_context:end_context]
        comment_text = full_paper[start:end]
        
        char_length = len(comment_text)
        words = word_tokenize(comment_text)
        words = [word for word in words if word.isalnum()]
        word_count = len(words)
        
        comments_with_stats[(start, end)] = {
            'text_with_context': comment_text_with_context,
            'char_length': char_length,
            'word_count': word_count
        }
    
    return comments_with_stats

all_comments_with_stats = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_comments_with_stats[filename] = debug(file_path)
    
for file, comments in all_comments_with_stats.items():
    print(f"Comments and statistics from {file}")
    for (start, end), stats in comments.items():
        print(f"Start: {start}, End: {end}")
        print(f"Text with context: {stats['text_with_context']}")
        print(f"Character length: {stats['char_length']}")
        print(f"Word count: {stats['word_count']}")
        print("\n")
