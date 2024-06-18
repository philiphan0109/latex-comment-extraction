import os
import re

dir_path = "paper/"

def extract_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to match authors
    author_pattern = re.compile(
        r'\\author{(.*?)}', re.DOTALL
    )
    author_block = re.search(author_pattern, content)

    if not author_block:
        return []

    author_block_content = author_block.group(1)

    # Regular expression to match individual authors
    individual_author_pattern = re.compile(
        r'\\(?:And|AND)?\s*'
        r'([^\\]+?)\s*'
        r'(\\thanks\{.*?\})?\s*'
        r'(\\footnotemark\[\d+\])?\s*'
        r'(\\hspace\{.*?\})?'
        r'\\\\\s*'
        r'([^\\]+?)\s*'
        r'\\\\\s*'
        r'\\texttt\{.*?\}',
        re.DOTALL
    )

    authors = []
    for match in re.finditer(individual_author_pattern, author_block_content):
        name, thanks, footnotemark, hspace, affiliation = match.groups()
        author_info = {
            'name': name.strip(),
            'affiliation': affiliation.strip()
        }
        if thanks:
            author_info['thanks'] = thanks.strip()
        if footnotemark:
            author_info['footnotemark'] = footnotemark.strip()
        if hspace:
            author_info['hspace'] = hspace.strip()
        authors.append(author_info)

    return authors

all_authors = {}

for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_authors[filename] = extract_authors(file_path)

for file, authors in all_authors.items():
    print(f"Authors from {file}")
    for author in authors:
        print(f"- Name: {author['name']}")
        print(f"  Affiliation: {author['affiliation']}")
        if 'thanks' in author:
            print(f"  Thanks: {author['thanks']}")
        if 'footnotemark' in author:
            print(f"  Footnote: {author['footnotemark']}")
        if 'hspace' in author:
            print(f"  Hspace: {author['hspace']}")
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