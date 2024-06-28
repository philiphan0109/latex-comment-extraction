import os
from stitch import stitch_tex_files, identify_main_tex, is_standalone, get_included_files
from comment_extraction import extract_comments

# given a directory of .tex files this function will:
# 1) generate a new .tex file named FULL_PAPER.tex
# 2) extract the comments from the full paper

# path = "test_set/2010.04425/"

def read_tex_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def process_paper(path):
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

if __name__ == '__main__':
    test_path = "test_set"
    process_paper(test_path)
    
    
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

# process_paper(path)