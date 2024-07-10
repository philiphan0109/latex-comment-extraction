import os
import random
from stitch import stitch_tex_files
from comment_extraction import extract_comments
import time
import multiprocessing as mp
import json

INPUT_PATH = "test_set/"
OUTPUT_PATH = "test_set/"
NUM_PROCESSES = 16

def process_paper(paper_file: str) -> None:
    paper_id = os.path.basename(paper_file)
    
    full_text = stitch_tex_files(paper_file)
    full_text_path = os.path.join(OUTPUT_PATH, paper_id, "full_text.tex")
    with open(full_text_path, "w") as file:
        file.write(full_text)

    comments = extract_comments(full_text)
    comments_path = os.path.join(OUTPUT_PATH, paper_id, "comments.json")
    with open(comments_path, "w") as file:
        json.dump(comments, file)

    # with open(output_path, "w", encoding="utf-8") as file:
    #     for section, comments in results.items():
    #         file.write(f"Section: {section}\n")
    #         for start_idx, end_idx in comments:
    #             context = 0
    #             start_context_idx = max(start_idx - context, 0)
    #             end_context_idx = min(end_idx + context, len(text))
    #             comment_text = text[start_context_idx:end_context_idx]
    #             file.write(
    #                 f"  Comment Indices: ({start_context_idx}, {end_context_idx})\n"
    #             )
    #             file.write(f"  Comment Text: \n {comment_text.strip()}\n\n")


def wrapper(path) -> str | None:
    try:
        process_paper(path)
        return None
    except Exception as e:
        return path


if __name__ == "__main__":
    # MP Testing
    start_time = time.time()
    paper_files = [
        os.path.join(INPUT_PATH, paper_file) for paper_file in os.listdir(INPUT_PATH)
    ]
    random.shuffle(paper_files)
    paper_files = paper_files[:1000]

    with mp.Pool(NUM_PROCESSES) as pool:
        results = pool.map(wrapper, paper_files)

    failed_paper_files = [paper_file for paper_file in results if paper_file != None]
    for paper in failed_paper_files:
        print(paper)
    print(
        f"Processed: {len(paper_files) - len(failed_paper_files)} / {len(paper_files)} papers."
    )
    print(f"This took: {time.time() - start_time} seconds.")

    # Local Testing
    # starttime = time.time()
    # test_path = "test_set/"
    # counter = 1000
    # incorrect_papers = []
    # for paper_path in os.listdir(test_path):
    #     try:
    #         paper_path = os.path.join(test_path, paper_path)
    #         process_paper(paper_path)
    #     except Exception as e:
    #         incorrect_papers.append(paper_path)
    #         counter -= 1
    # print(incorrect_papers)
    # print(f"This took: {time.time() - starttime} seconds | Papers correct: {counter}")
