import os
import re

dir_path = "paper/"

def read_tex_file(file_path):
    with open(file_path, 'r', encoding="utf-8", errors="replace") as file:
        return file.read()

def find_include_tag(line):
    """Find \input or \include tags within a line."""
    pattern = r'\\(input|include)\{([^}]+)\}'
    match = re.search(pattern, line)
    return match.groups() if match else None

def convert_to_comment(content):
    lines = content.splitlines()
    commented_content = '\n'.join([f'% {line}' for line in lines])
    return commented_content

def process_include_tag(line, path):
    tag, filename = find_include_tag(line)
    raw_file_path = filename
    if not filename.endswith('.tex'):
        filename += '.tex'
    file_path = os.path.join(path, filename)
    raw_file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
        content = read_tex_file(file_path)
        if line.strip().startswith('%'):
            return convert_to_comment(content)
        else:
            return content
    elif os.path.exists(raw_file_path):
        content = read_tex_file(raw_file_path)
        if line.strip().startswith('%'):
            return convert_to_comment(content)
        else:
            return content
    else:
        if not line.strip().startswith('%'):
            print(f"RAW FILE NOT FOUND: {raw_file_path}")
        return line

def is_standalone(file):
    with open(file, 'r', encoding="utf-8", errors="replace") as f:
        content = f.read()
        return '\\begin{document}' in content and '\\end{document}' in content

def contains_main_document_elements(content):
    return any(cmd in content for cmd in ['\\title', '\\author', '\\maketitle', '\\tableofcontents', '\\begin{abstract}'])

def identify_main_tex(files):
    main_candidates = []
    supplement_files = []

    for file in files:
        if is_standalone(file):
            with open(file, 'r', encoding="utf-8", errors="replace") as f:
                content = f.read()
                if re.search(r'\bsupplement\b', file.lower()):  
                    supplement_files.append(file)
                else:
                    main_candidates.append(file)
    
    if main_candidates:
        for file in main_candidates:
            with open(file, 'r', encoding="utf-8", errors="replace") as f:
                content = f.read()
                if contains_main_document_elements(content):
                    return file
    return main_candidates[0] if main_candidates else None

def stitch_tex_files(path):
    tex_files = []
    for root, _, files in os.walk(path):

        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    # Identify the main .tex file
    main_file_path = identify_main_tex(tex_files)
    if not main_file_path:
        raise FileNotFoundError("Main .tex file not found in the directory")

    main_content = read_tex_file(main_file_path)
    processed_lines = []

    for line in main_content.splitlines():
        if find_include_tag(line):
            processed_lines.append(process_include_tag(line, path))
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)