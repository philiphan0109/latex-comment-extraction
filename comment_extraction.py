import re
# from nltk.tokenize import word_tokenize


def extract_comments(full_text: str) -> dict:
    comments = {}

    current_index = 0
    current_section = "None"
    current_subsection = "None"
    current_subsubsection = "None"
    comments[current_section] = {}
    comments[current_section][current_subsection] = {}
    comments[current_section][current_subsection][current_subsubsection] = []
    is_comment = False
    current_comment = ""
    start_index = end_index = -1

    def change_section(new_section: str) -> None:
        nonlocal current_section, current_subsection, current_subsubsection, comments, is_comment
        current_section = new_section
        current_subsection = "None"
        current_subsubsection = "None"
        if current_section not in comments:
            comments[current_section] = {}
        if current_subsection not in comments[current_section]:
            comments[current_section][current_subsection] = {}
        if current_subsubsection not in comments[current_section][current_subsection]:
            comments[current_section][current_subsection][current_subsubsection] = []
        is_comment = False
        current_comment = ""

    def change_subsection(new_subsection: str) -> None:
        nonlocal current_subsection, current_subsubsection, is_comment
        current_subsection = new_subsection
        current_subsubsection = "None"
        if current_subsection not in comments[current_section]:
            comments[current_section][current_subsection] = {}
        if current_subsubsection not in comments[current_section][current_subsection]:
            comments[current_section][current_subsection][current_subsubsection] = []
        is_comment = False

    def change_subsubsection(new_subsubsection: str) -> None:
        nonlocal current_subsubsection, is_comment
        current_subsubsection = new_subsubsection
        if current_subsubsection not in comments[current_section][current_subsection]:
            comments[current_section][current_subsection][current_subsubsection] = []
        is_comment = False

    lines = full_text.split("\n")
    for line in lines:
        # Comment
        if line.lstrip().startswith("%"):
            if not is_comment:
                start_index = current_index + line.find("%")
                is_comment = True
                current_comment = line[line.find("%") + 1 :]
            else:
                current_comment += "\n" + line[line.find("%") + 1 :]
            end_index = current_index + len(line)
            continue
        else:
            if is_comment:
                comments[current_section][current_subsection][
                    current_subsubsection
                ].append((start_index, end_index, current_comment))
                is_comment = False
                
            end_of_line_comment = re.search(r"(?<!\\)%.*$", line)
            if end_of_line_comment:
                start_index = current_index + end_of_line_comment.start()
                end_index = current_index + len(line)
                current_comment = line[end_of_line_comment.start() + 1 :]
                comments[current_section][current_subsection][current_subsubsection].append(
                    (start_index, end_index, current_comment)
                )
                is_comment = False
                
        # Section
        match = re.search(r"\\section\*? *\{(.+?)\}", line)
        if match:
            change_section(match.group(1))
        elif re.search(r"\\begin *{abstract}", line):
            change_section("Abstract")
        elif re.search(r"\\end *{abstract}", line):
            change_section("None")

        # Subsection
        match = re.search(r"\\subsection\*? *\{(.+?)\}", line)
        if match:
            change_subsection(match.group(1))

        # Subsubsection
        match = re.search(r"\\subsubsection\*? *\{(.+?)\}", line)
        if match:
            change_subsubsection(match.group(1))

        current_index += len(line) + 1

    if is_comment:
        comments[current_section][current_subsection][current_subsubsection].append(
            (start_index, end_index, current_comment)
        )

    return comments


# def extract_comment_indices(path):
#     comment_indices = []
#
#     with open(path, "r", errors="replace") as file:
#         full_text = file.read()
#
#     current_index = 0
#     comment_start_index = -1
#     comment_end_index = -1
#     is_current_comment = False
#     current_comment = ""
#
#     lines = full_text.split("\n")
#     for line in lines:
#         if line.lstrip().startswith("%"):
#             if not is_current_comment:
#                 comment_start_index = current_index + line.find("%")
#                 comment_end_index = current_index + len(line)
#                 is_current_comment = True
#                 current_comment = line[line.find("%") + 1 :]
#             else:
#                 comment_end_index = current_index + len(line)
#                 current_comment += "\n" + line[line.find("%") + 1 :]
#         else:
#             end_of_line_comment = re.search(r"(?<!\\)%.*$", line)
#             if end_of_line_comment:
#                 if is_current_comment:
#                     comment_indices.append(
#                         (comment_start_index, comment_end_index, current_comment)
#                     )
#                     is_current_comment = False
#                     current_comment = ""
#                 comment_start_index = current_index + end_of_line_comment.start()
#                 comment_end_index = current_index + len(line)
#                 is_current_comment = True
#                 current_comment = line[end_of_line_comment.start() + 1 :]
#             elif is_current_comment:
#                 comment_indices.append(
#                     (comment_start_index, comment_end_index, current_comment)
#                 )
#                 is_current_comment = False
#                 current_comment = ""
#         current_index += len(line) + 1
#
#     if is_current_comment:
#         comment_indices.append(
#             (
#                 comment_start_index,
#                 comment_end_index,
#                 full_text[comment_start_index:comment_end_index],
#             )
#         )
#         is_current_comment = False
#
#     return comment_indices
#
#
# def extract_comment_statistics(path):
#     comment_indices = extract_comment_indices(path)
#     comments = {}

#     with open(path, "r", errors="replace") as file:
#         full_paper = file.read()

#     for start, end in comment_indices:
#         comment = full_paper[start:end]
#         comment = comment.split("\n")
#         comments[start] = comment

#     comment_statistics = {}
#     for index, comment in comments.items():
#         for i in range(len(comment)):
#             comment[i] = comment[i][1:].strip()
#         comment_text = " ".join(comment)
#         char_length = len(comment_text)
#         words = word_tokenize(comment_text)
#         words = [word for word in words if word.isalnum()]
#         word_count = len(words)
#         comment_statistics[index] = {
#             "char_length": char_length,
#             "word_count": word_count,
#         }

#     return comment_statistics


# if __name__ == "__main__":
#     print("hello")
#     path_to_main_tex = "paper/main.tex"
#     output_path = "paper/a.txt"

#     results = extract_comments(path_to_main_tex)

#     with open(output_path, "w", encoding="utf-8") as file:
#         for section, comments in results.items():
#             file.write(f"Section: {section}\n")
#             print(f"Section: {section}")
#             for start_idx, end_idx in comments:
#                 # Extract the actual comment text from the document
#                 with open(path_to_main_tex, "r", encoding="utf-8") as text_file:
#                     text_file.seek(start_idx)
#                     comment_text = text_file.read(end_idx - start_idx)

#                 file.write(f"  Comment Indices: ({start_idx}, {end_idx})\n")
#                 file.write(f"  Comment Text: {comment_text.strip()}\n\n")

#                 # Print to console as well
#                 print(f"  Comment Indices: ({start_idx}, {end_idx})")
#                 print(f"  Comment Text: {comment_text.strip()}\n")
