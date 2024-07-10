import os
import json

def get_versions(dir_path: str) -> dict:
    versions = {}
    for paper in os.listdir(dir_path):
        paper_path = os.path.join(dir_path, paper)
        metadata_path = os.path.join(paper_path, "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            url = metadata["url"]
            if url[-2] != 'v':
                print("no version")
            elif (url[-2:] not in versions.keys()):
                versions[url[-2:]] = 1
            else: 
                versions[url[-2:]] += 1
    return versions


if __name__ == "__main__":
    path = "test_set/"
    versions = get_versions(path)
    for version in versions.items():
        print(version)
    