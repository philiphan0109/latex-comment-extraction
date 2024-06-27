import os
import re

dir_path = "paper/"

def read_tex_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def find_includes(tex_content):
    pattern = r'(?<!%)^[^%]*\\(input|include)\{([^}]+)\}'
    return re.findall(pattern, tex_content, re.MULTILINE)

def find_commented_includes(tex_content):
    pattern = r'^\s*%\s*\\(input|include)\{([^}]+)\}'
    return re.findall(pattern, tex_content, re.MULTILINE)

def convert_to_comment(content):
    lines = content.splitlines()
    commented_content = '\n'.join([f'% {line}' for line in lines])
    return commented_content

def is_standalone(file):
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
        return '\\begin{document}' in content and '\\end{document}' in content

def contains_main_document_elements(content):
    return any(cmd in content for cmd in ['\\title', '\\author', '\\maketitle', '\\tableofcontents', '\\begin{abstract}'])

def identify_main_tex(files):
    main_candidates = []
    supplement_files = []

    for file in files:
        if is_standalone(file):
            with open(file, 'r', encoding="utf-8") as f:
                content = f.read()
                if re.search(r'\bsupplement\b', file.lower()):  
                    supplement_files.append(file)
                else:
                    main_candidates.append(file)
    
    if main_candidates:
        for file in main_candidates:
            with open(file, 'r', encoding="utf-8") as f:
                content = f.read()
                if contains_main_document_elements(content):
                    return file
    
    return main_candidates[0] if main_candidates else None



def get_included_files(main_file):
    included_files = []
    if main_file:
        with open(main_file, 'r', encoding="utf-8") as f:
            content = f.read()
            # Look for \include or \input commands
            included_files = re.findall(r'\\(?:include|input)\{([^}]+)\}', content)
    return included_files

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
    includes = find_includes(main_content)
    commented_includes = find_commented_includes(main_content)
    
    for command, include_file in includes:
        raw_include_file = include_file
        if not include_file.endswith('.tex'):
            include_file += '.tex'
        include_path = os.path.join(path, include_file)
        raw_include_path = os.path.join(path, raw_include_file)
        if os.path.exists(include_path):
            include_content = read_tex_file(include_path)
            main_content = main_content.replace(f'\\{command}{{{include_file[:-4]}}}', include_content)
        elif os.path.exists(raw_include_path):
            include_content = read_tex_file(include_path)
            main_content = main_content.replace(f'\\{command}{{{include_file[:-4]}}}', include_content)
        else:
            print(f"RAW FILE NOT FOUND: {raw_include_path}")
            # print(f"File not found: {include_path}")
            
    for comment, command, include_file in commented_includes:
        raw_include_file = include_file
        if not include_file.endswith('.tex'):
            include_file += '.tex'
        include_path = os.path.join(path, include_file)
        if os.path.exists(include_path):
            include_content = read_tex_file(include_path)
            commented_content = convert_to_comment(include_content)
            main_content = main_content.replace(comment, f'% {include_file[:-4]}\n{commented_content}')
        elif os.path.exists(raw_include_file):
            include_content = read_tex_file(include_path)
            main_content = main_content.replace(f'\\{command}{{{include_file[:-4]}}}', include_content)
        # else:
        #     print(f"File not found: {include_path}")
    
    return main_content


#test