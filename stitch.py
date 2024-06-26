import os
import re

dir_path = "paper/"

def read_tex_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def find_includes(tex_content):
    pattern = r'(?<!%)\\(input|include){([^}]+)}'
    return re.findall(pattern, tex_content)

def find_commented_includes(tex_content):
    pattern = r'(%.*\\(input|include){([^}]+)})'
    return re.findall(pattern, tex_content)

def convert_to_comment(content):
    lines = content.splitlines()
    commented_content = '\n'.join([f'% {line}' for line in lines])
    return commented_content

def stitch_tex_files(path):
    main_file_path = None
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                content = read_tex_file(file_path)
                if '\\begin{document}' in content:
                    main_file_path = file_path
    if not main_file_path:
        raise FileNotFoundError("Main .tex file not found in the directory")
    
    main_content = read_tex_file(main_file_path)
    includes = find_includes(main_content)
    commented_includes = find_commented_includes(main_content)
    
    for command, include_file in includes:
        if not include_file.endswith('.tex'):
            include_file += '.tex'
        include_path = os.path.join(dir_path, include_file)
        if os.path.exists(include_path):
            include_content = read_tex_file(include_path)
            main_content = main_content.replace(f'\\{command}{{{include_file[:-4]}}}', include_content)
        else:
            print(f"File not found: {include_path}")
    
    for comment, command, include_file in commented_includes:
        if not include_file.endswith('.tex'):
            include_file += '.tex'
        include_path = os.path.join(dir_path, include_file)
        if os.path.exists(include_path):
            include_content = read_tex_file(include_path)
            commented_content = convert_to_comment(include_content)
            main_content = main_content.replace(comment, f'% {include_file[:-4]}\n{commented_content}')
        else:
            print(f"File not found: {include_path}")
    
    return main_content

