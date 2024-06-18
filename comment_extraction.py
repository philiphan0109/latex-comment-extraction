import os

dir_path = "paper/"

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