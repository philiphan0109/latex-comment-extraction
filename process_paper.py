import os
import re
import nltk
from nltk.tokenize import word_tokenize
import cProfile
import pstats
import io
from stitch import stitch_tex_files

# given a directory of .tex files this function will:
# 1) generate a new .tex file named FULL_PAPER.tex
# 2) extract the comments from the full paper
def process_paper(path):
    full_paper = stitch_tex_files(path)
    with open(os.path.join(path, 'FULL_PAPER.tex'), 'w') as output_file:
        output_file.write(full_paper)
    