import git
import pandas as pd
import sys
import os
import subprocess
import time
import shutil
from pdb import set_trace

class THA:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.save_to = "../../"+repo_url.split("/")[-1].split('.')[0]
        if os.path.isdir(self.save_to):
            shutil.rmtree(self.save_to)
        self.repo = git.Repo.clone_from(repo_url, self.save_to)

    def get_diffs(self, diff):
        file_changed = []
        for diff_item in diff:
            if diff_item.change_type == "M" or diff_item.change_type == "D" or diff_item.change_type == "T" or diff_item.change_type == "R":
                name = diff_item.a_blob.path
            elif diff_item.change_type == "A":
                name = diff_item.b_blob.path
            else:
                raise Exception("Unknown Change Type.")
            if name.split(".")[-1] == "py" and not name.split(".")[-2].split("/")[-1].startswith("test_"):
                file_changed.append(name)
        return ";".join(file_changed)

    def analyze(self):
        current = self.repo.head.commit
        latest = current.hexsha
        store_dict = {"commit_id":[], "diffs":[], "test_failures":[]}
        while True:
            parents = current.parents
            if len(parents)>0:
                prev = parents[0]
            else:
                subprocess.Popen(["git","reset", "--hard", latest], cwd=self.save_to)
                df = pd.DataFrame(store_dict, columns = ["commit_id", "diffs", "test_failures"])
                print(df)
                df.to_csv("../output/"+self.save_to.split("/")[-1]+".csv", index=False)
                return
            # Get diffs
            diff = prev.diff(current)
            file_changed = self.get_diffs(diff)
            store_dict["commit_id"].append(current.hexsha)
            store_dict["diffs"].append(file_changed)

            # Get test failures
            subprocess.run(["git","reset", "--hard", current.hexsha], cwd=self.save_to)
            time.sleep(1)
            result = subprocess.run([sys.executable, "./single_pytest.py", self.save_to], capture_output=True, text=True)
            failures = ";".join([x.split(self.save_to.split('/')[-1])[-1][1:] for x in set(result.stdout.split())])

            store_dict["test_failures"].append(failures)

            current = prev


if __name__ == "__main__":
    repo = sys.argv[1]
    analyzer = THA(repo)
    analyzer.analyze()
