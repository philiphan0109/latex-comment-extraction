import json
import os

def load_all_metadata(directory_path):
    metadata_list = []
    for paper_id in os.listdir(directory_path):
        paper_folder = os.path.join(directory_path, paper_id)
        if os.path.isdir(paper_folder):
            metadata_file = os.path.join(paper_folder, 'metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as file:
                    metadata_list.append(json.load(file))
    return metadata_list

def query_by_year(metadata, year):
    results = [paper for paper in metadata if paper['published'].startswith(str(year))]
    return results

def query_by_category(metadata, category):
    results = [paper for paper in metadata if category in paper['categories']]
    return results

def query_by_author(metadata, author):
    results = [paper for paper in metadata if author in paper['authors']]
    return results

def query_by_version(metadata, version):
    results = [paper for paper in metadata if paper['url'].endswith(f'v{version}')]
    return results

metadata = load_all_metadata('test_set/')
papers_2017 = query_by_year(metadata, 2017)
print(papers_2017)

"""
How to use the functions:

1. Load all metadata from the test_set directory:
   metadata = load_all_metadata('test_set/')

2. Query papers published in a specific year:
   year = 2017
   papers_2017 = query_by_year(metadata, year)

3. Query papers from a certain category:
   category = 'math.CO'
   papers_category = query_by_category(metadata, category)

4. Query papers by a specific author:
   author = 'Oliver Pechenik'
   papers_author = query_by_author(metadata, author)

5. Query papers by version:
   version = 3
   papers_version = query_by_version(metadata, version)
"""


if __name__ == "__main__":
    pass