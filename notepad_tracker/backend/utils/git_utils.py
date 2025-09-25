# backend/utils/git_utils.py
import os
import git
from backend.config import AUTO_COMMIT_MESSAGE

def commit_file(filepath):
    repo_path = os.path.dirname(filepath)

    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        repo = git.Repo.init(repo_path)

    rel_path = os.path.relpath(filepath, repo.working_tree_dir)
    repo.index.add([rel_path])
    repo.index.commit(AUTO_COMMIT_MESSAGE)
