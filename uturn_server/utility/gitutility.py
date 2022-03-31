import subprocess
import os
import json
from git import GitCommandError
import pydriller

from . import server_dir
from . import exceptions


class Project:
    with open(server_dir + "/config.json", 'r') as file:
        config = json.loads(file.read())
    
    mainbranch = config.get("branch")
    def __init__(self, name):
        self.name = name
        self.projectconfig = self.config.get("projects").get(self.name)
        self.projectpath = self.projectconfig.get("path")
        if not os.path.isdir(self.projectpath):
            raise exceptions.ProjectDoesntExistError("Invalid Path.")

        self.start_command = self.projectconfig.get("start")
        self.stop_command = self.projectconfig.get("stop")

        self.repo = pydriller.Repository(
            self.projectpath, 
            only_in_branch=self.mainbranch,
            order="reverse"
        )
        self.git = pydriller.Git(self.projectpath)
    
    def commits(self):
        commits_from_start = self.repo.traverse_commits()
        for commit in commits_from_start:
            yield commit
    
    def rollback(self, hashsha: str):
        """
            Creates another branch with is equivalent to that commit.
        """
        try:
            with open(os.devnull, 'wb') as devnull:
                subprocess.check_call(
                    self.stop_command.split(),
                    stdout=devnull,
                    stderr=subprocess.STDOUT,
                    cwd=self.projectpath
                )
                self.git.checkout(hashsha)
                subprocess.check_call(
                    self.start_command.split(),
                    stdout=devnull,
                    stderr=subprocess.STDOUT,
                    cwd=self.projectpath
                )
        except GitCommandError:
            raise GitCommandError("Invalid Hash")
    
    def all_branches(self) -> list:
        return os.listdir(self.projectpath+".git/refs/heads")