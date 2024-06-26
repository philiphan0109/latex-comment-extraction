import os
from stitch import stitch_tex_files
from comment_extraction import extract_comments

# given a directory of .tex files this function will:
# 1) generate a new .tex file named FULL_PAPER.tex
# 2) extract the comments from the full paper

def process_paper(path):
    full_paper = stitch_tex_files(path)
    with open(os.path.join(path, 'FULL_PAPER.tex'), 'w') as output_file:
        output_file.write(full_paper)
    
    full_paper_path = os.path.join(path, 'FULL_PAPER.tex')
    output_path = "paper/a.txt"
    results = extract_comments(full_paper_path)
    
    with open(output_path, "w", encoding="utf-8") as file:
        for section, comments in results.items():
            file.write(f"Section: {section}\n")
            for start_idx, end_idx in comments:
                with open(full_paper_path, "r", encoding="utf-8") as text_file:
                    text_file.seek(start_idx)
                    comment_text = text_file.read(end_idx - start_idx)
                
                file.write(f"  Comment Indices: ({start_idx}, {end_idx})\n")
                file.write(f"  Comment Text: {comment_text.strip()}\n\n")
                # print(f"  Comment Indices: ({start_idx}, {end_idx})")
                # print(f"  Comment Text: {comment_text.strip()}\n")

if __name__ == "__main__":
    path = "paper/"
    print("hello")
    process_paper(path)