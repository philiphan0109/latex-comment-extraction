import os
import re

dir_path = "paper/"

def read_tex_file(file_path):
    with open(file_path, 'r') as file:
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

# tex_content = """
# \\input{file1}
# % \\include{file2}
# %    \\input{file3}
# \\include{file4}
# % some comment \\input{file5}
# """

# print("Includes:", find_includes(tex_content))
# print("Commented Includes:", find_commented_includes(tex_content))