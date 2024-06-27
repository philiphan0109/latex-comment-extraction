import os
from stitch import stitch_tex_files, identify_main_tex, is_standalone, get_included_files
from comment_extraction import extract_comments

# given a directory of .tex files this function will:
# 1) generate a new .tex file named FULL_PAPER.tex
# 2) extract the comments from the full paper

path = "test_set/"

def read_tex_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def process_paper(path):
    tex_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    
    main_file_path = identify_main_tex(tex_files)
    if not main_file_path:
        raise FileNotFoundError("Main .tex file not found in the directory")

    main_content = read_tex_file(main_file_path)
    includes = get_included_files(main_file_path)
    included_files = set(os.path.join(path, f"{include_file}.tex") for include_file in includes)

    full_paper = stitch_tex_files(path)
    full_paper_path = os.path.join(path, 'FULL_PAPER.tex')
    with open(full_paper_path, 'w', encoding="utf-8") as output_file:
        output_file.write(full_paper)

    with open(full_paper_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()
    
    results = extract_comments(full_paper_path)
    output_path = os.path.join(path, "a.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        for section, comments in results.items():
            file.write(f"Section: {section}\n")
            for start_idx, end_idx in comments:
                context = 0
                start_context_idx = max(start_idx - context, 0)
                end_context_idx = min(end_idx + context, len(text))
                comment_text = text[start_context_idx:end_context_idx]
                file.write(f"  Comment Indices: ({start_context_idx}, {end_context_idx})\n")
                file.write(f"  Comment Text: \n {comment_text.strip()}\n\n")

        file.write("\nPotential Supplemental Files:\n")
        for tex_file in tex_files:
            if is_standalone(tex_file) and tex_file not in included_files and tex_file != main_file_path:
                file.write(f"{tex_file}\n")

if __name__ == '__main__':
    test_path = "test_set"
    counter = 1000
    incorrect_papers = []
    for paper_path in os.listdir(test_path):
        try:
            paper_path = os.path.join(test_path, paper_path)
            process_paper(paper_path)
        except Exception as e:
            incorrect_papers.append(paper_path)
            counter -= 1
    print(incorrect_papers)
