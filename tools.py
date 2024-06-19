import os
import re

def extract_title(file_path):
    title = "No title found"
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('\\title{'):
                end_pos = line.find('}', 7)
                if end_pos != -1:
                    title = line[7:end_pos].strip()
                    break
    return title

def extract_abstract(file_path):
    abstract = ""
    inside_abstract = False
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file: 
            line = line.strip()
            if line.startswith('\\begin{abstract}'):
                inside_abstract = True
                continue
            if line.startswith('\\end{abstract}'):
                inside_abstract = False
                break
            if inside_abstract and not line.startswith('%'):
                abstract += line + ' '
                
    if not abstract:
        abstract = "No abstract found"
        
    return abstract.strip()

def extract_comments(path):
    comments = {}
    current_comment = []
    current_index = 0

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith('%'):
                if not current_comment:
                    start_index = current_index + line.find('%')
                current_comment.append(stripped_line[1:].strip())
            else:
                if current_comment:
                    comments[start_index] = " ".join(current_comment)
                    current_comment = []
            current_index += len(line) + 1  # +1 for the newline character
        if current_comment:
            comments[start_index] = " ".join(current_comment)

    return comments

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
            # Remove affiliations and emails after the author's name
            clean_author = re.split(r'\\\\|\\texttt', clean_author)[0]
            # Clean up the author string
            clean_author = clean_author.strip().replace('\n', ' ').replace('\t', ' ')
            # Append to the list if not empty
            if clean_author:
                authors.append(clean_author)
    
    return authors