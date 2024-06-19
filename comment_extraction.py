import os
import re
from comment_extraction import extract_title, extract_abstract, extract_comments, extract_authors

dir_path = "paper/"

all_comments = {}
for filename in os.listdir(dir_path):
    if filename.endswith(".tex"):
        file_path = os.path.join(dir_path, filename)
        all_comments[filename] = extract_comments(file_path)

for file, comments in all_comments.items():
    print(f"Comments from {file}")
    for comment in comments:
        print(f"- {comment}")
    print("\n")