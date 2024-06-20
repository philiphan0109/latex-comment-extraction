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

def extract_comment_text(path):
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
        comments[start] = comment
    
    comment_statistics = {}
    for index, comment in comments.items():
        char_length = len(comment)
        words = word_tokenize(comment)
        words = [word for word in words if word.isalnum()]
        word_count = len(words)
        comment_statistics[index] = {
            'char_length': char_length,
            'word_count': word_count
        }
    
    return comment_statistics



# all_comment_indices = {}
# for filename in os.listdir(dir_path):
#     if filename.endswith(".tex"):
#         file_path = os.path.join(dir_path, filename)
#         all_comment_indices[filename] = extract_comment_indices(file_path)

# for file, comment_indices in all_comment_indices.items():
#     print(f"Comments from {file}")
#     for comment in comment_indices:
#         print(f"start: {comment[0]} | stop: {comment[1]}")
#     print("\n")

def main():
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


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

    main()

    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())