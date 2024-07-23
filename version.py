import os
import json
from collections import defaultdict

def get_versions(dir_path: str) -> dict:
    versions = defaultdict(list)
    for paper in os.listdir(dir_path):
        paper_path = os.path.join(dir_path, paper)
        metadata_path = os.path.join(paper_path, "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            url = metadata["url"]
            arxiv_id = metadata["id"]
            
            if url[-2] == 'v':
                version = url[-2:]
                versions[version].append(arxiv_id)
            else:
                print(f"No version found for paper with ID: {arxiv_id}")
    
    return versions

if __name__ == "__main__":
    path = "test_set/"
    versions = get_versions(path)
    for version, ids in versions.items():
        print(f"Version {version}: {len(ids)} papers")
        print(f"ArXiv IDs: {', '.join(ids)}")
        print()