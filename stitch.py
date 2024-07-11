import os
import re

def read_tex_file(tex_file: str) -> str:
    with open(tex_file, "r", errors="replace") as file:
        return file.read()


def find_include_tag(line: str) -> str | None:
    pattern = r"\\(input|include)\{([^}]+)\}"
    match = re.search(pattern, line)
    return match.groups()[1] if match else None


def convert_to_comment(text: str) -> str:
    lines = text.splitlines()
    return "\n".join([f"% {line}" for line in lines])


def process_line(line, tex_dir) -> str:
    include_path = find_include_tag(line)
    if not include_path:
        return line

    if not include_path.endswith(".tex"):
        include_path += ".tex"
    include_path = os.path.join(tex_dir, include_path)

    if os.path.exists(include_path):
        include_text = read_tex_file(include_path)
        if line.strip().startswith("%"):
            return convert_to_comment(process_file(include_path, tex_dir))
        else:
            return process_file(include_path, tex_dir)
    else:
        if line.strip().startswith("%"):
            return line
        else:
            # print(f"RAW FILE NOT FOUND: {raw_file_path}")
            return line


def is_document(text: str) -> bool:
    return bool(re.search(r"\\begin *{document}", text)) and bool(
        re.search(r"\\end *{document}", text)
    )


def contains_main_document_elements(text: str) -> bool:
    return any(
        cmd in text.lower()
        for cmd in [
            "\\title",
            "\\author",
            "\\maketitle",
            "\\tableofcontents",
            "\\begin{abstract}",
        ]
    )


def identify_main_tex(tex_files: list, debug: bool = False) -> str | None:
    main_candidates = []

    if debug and not tex_files:
        print("No .tex files")

    for tex_file in tex_files:
        with open(tex_file, "r", errors="replace") as file:
            text = file.read()

        if is_document(text):
            main_candidates.append(tex_file)
            if contains_main_document_elements(text):
                return tex_file

    if not main_candidates and len(tex_files) == 1:
        return tex_files[0]

    if debug and not main_candidates:
        print("No main candidates")

    return main_candidates[0] if main_candidates else None


def process_file(tex_file: str, tex_dir: str) -> str:
    text = read_tex_file(tex_file)
    return "\n".join([process_line(line, tex_dir) for line in text.splitlines()])


def stitch_tex_files(tex_dir: str, debug: bool = False) -> str:
    if debug:
        print(os.path.basename(tex_dir))
    tex_files = []
    for root, _, files in os.walk(tex_dir):
        for file in files:
            if (file.lower().endswith(".tex") or file.lower().endswith("...")) and file.lower().find("full_text") == -1:
                # if(file.lower().endswith("...")):
                #     print("Weird File Extension: ", tex_dir)
                tex_files.append(os.path.join(root, file))

    main_file = identify_main_tex(tex_files, debug)
    if not main_file:
        if len(tex_files) == 1:
            return read_tex_file(tex_files[0])
        else:
            raise FileNotFoundError("No main.tex file")

    return process_file(main_file, tex_dir)
