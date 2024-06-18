import os
import re

dir_path = "paper/"

def extract_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    authors = []
    
    # Define patterns to locate the \author section
    author_pattern = re.compile(r'\\author{', re.DOTALL)
    
    # Find the \author{...} section manually to handle nested braces
    author_match = author_pattern.search(content)
    
    if author_match:
        start = author_match.end()
        brace_count = 1
        end = start
        while brace_count > 0 and end < len(content):
            if content[end] == '{':
                brace_count += 1
            elif content[end] == '}':
                brace_count -= 1
            end += 1
        
        author_content = content[start:end-1]
        
        # Define patterns to split authors and clean up names
        and_split_pattern = r'\\(?:And|AND|and| )'
        footnote_pattern = r'\\thanks{.*?}'
        
        # Split authors using \And, \AND, or \and
        raw_authors = re.split(and_split_pattern, author_content)

        for raw_author in raw_authors:
            # Remove any \thanks footnotes
            clean_author = re.sub(footnote_pattern, '', raw_author)
            # Clean up the author string
            clean_author = clean_author.strip().replace('\n', ' ').replace('\t', ' ')
            # Append to the list if not empty
            if clean_author:
                authors.append(clean_author)
    
    return authors

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



def extract_comments(path):
    comments = []
    current_comment = []
    
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith('%'):
                current_comment.append(line[1:].strip())
            else: 
                if current_comment:
                    comments.append(" ".join(current_comment))
                    current_comment = []
    if current_comment:
        comments.append(" ".join(current_comment))
        current_comment = []
    
    return comments

# all_comments = {}

# for filename in os.listdir(dir_path):
#     if filename.endswith(".tex"):
#         file_path = os.path.join(dir_path, filename)
#         all_comments[filename] = extract_comments(file_path)

# for file, comments in all_comments.items():
#     print(f"Comments from {file}")
#     for comment in comments:
#         print(f"- {comment}")
#     print("\n")