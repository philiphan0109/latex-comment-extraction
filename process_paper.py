import os
import random
from stitch import stitch_tex_files
from comment_extraction import extract_comments
import time
import multiprocessing as mp
import json
import argparse

def process_paper(paper_file: str, output_path: str) -> None:
    paper_id = os.path.basename(paper_file)
    
    full_text = stitch_tex_files(paper_file)
    full_text_path = os.path.join(output_path, paper_id, "full_text.tex")
    os.makedirs(os.path.dirname(full_text_path), exist_ok=True)
    with open(full_text_path, "w") as file:
        file.write(full_text)

    comments = extract_comments(full_text)
    comments_path = os.path.join(output_path, paper_id, "comments.json")
    with open(comments_path, "w") as file:
        json.dump(comments, file)

def wrapper(args):
    path, output_path = args
    try:
        process_paper(path, output_path)
        return None
    except Exception as e:
        return path

def main(input_path: str, output_path: str, num_processes: int, num_papers: int):
    start_time = time.time()
    paper_files = [
        os.path.join(input_path, paper_file) for paper_file in os.listdir(input_path)
    ]
    random.shuffle(paper_files)
    paper_files = paper_files[:num_papers]

    with mp.Pool(num_processes) as pool:
        results = pool.map(wrapper, [(paper, output_path) for paper in paper_files])

    failed_paper_files = [paper_file for paper_file in results if paper_file is not None]
    for paper in failed_paper_files:
        print(paper)
    print(
        f"Processed: {len(paper_files) - len(failed_paper_files)} / {len(paper_files)} papers."
    )
    print(f"This took: {time.time() - start_time} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process arXiv LaTeX papers to extract comments.")
    parser.add_argument("--input", type=str, default="test_set/", help="Input directory containing LaTeX files")
    parser.add_argument("--output", type=str, default="test_set/", help="Output directory for processed files")
    parser.add_argument("--processes", type=int, default=16, help="Number of processes to use for multiprocessing")
    parser.add_argument("--papers", type=int, default=1000, help="Number of papers to process")
    
    args = parser.parse_args()
    
    main(args.input, args.output, args.processes, args.papers)