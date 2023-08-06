import os
from pathlib import Path
from shutil import copyfile
from .base import BaseRemote

__author__ = 'Akshat Bajaj'
__date__ = '2019/02/18'

class Local(BaseRemote):
    def __init__(self):
        self.messages = []

    def add(self, add_to, key):
        project_name = self.read_from_local_config("project-info", "project-name")
        if project_name is None:
            return "error: project name not present in config"

        path_to_local_file = Path(os.path.join(add_to, key))
        path_to_remote = self.read_from_config("remote", add_to)
        if path_to_remote:
            # Append filename
            path_to_remote_file = os.path.join(path_to_remote, project_name, key)
            if Path(path_to_local_file).is_file() or Path(path_to_remote_file).is_file():
                self.write_config(add_to, ".surround/config.yaml", key)
                return "info: file added successfully"
            return "error: " + key + " not found."
        return "error: no remote named " + add_to

    def pull(self, what_to_pull, key=None):
        if key:
            project_name = self.read_from_local_config("project-info", "project-name")
            if project_name is None:
                self.messages.append("error: project name not present in config")
                return "error: project name not present in config"

            path_to_remote = self.read_from_config("remote", what_to_pull)
            file_to_pull = os.path.join(path_to_remote, project_name, key)
            if Path(os.path.join(what_to_pull, key)).exists():
                self.messages.append("info: " + os.path.join(what_to_pull, key) + " already exists")
                return "info: " + os.path.join(what_to_pull, key) + " already exists"

            os.makedirs(what_to_pull, exist_ok=True)
            if Path(file_to_pull).exists():
                copyfile(file_to_pull, os.path.join(what_to_pull, key))
                self.messages.append("info: " + key + " pulled successfully")
                return "info: " + key + " pulled successfully"
            self.messages.append("error: file does not exist")
            return "error: file does not exist"

        files_to_pull = self.read_all_from_local_config(what_to_pull)
        self.messages = []
        if files_to_pull:
            for file_to_pull in files_to_pull:
                self.pull(what_to_pull, file_to_pull)
            return self.messages
        self.messages.append("error: No file added to " + what_to_pull)
        return self.messages

    def push(self, what_to_push, key=None):
        if key:
            project_name = self.read_from_local_config("project-info", "project-name")
            if project_name is None:
                self.messages.append("error: project name not present in config")
                return "error: project name not present in config"

            path_to_remote = self.read_from_config("remote", what_to_push)
            path_to_remote_file = os.path.join(path_to_remote, project_name, key)
            if Path(path_to_remote_file).exists():
                self.messages.append("info: " + path_to_remote_file + " already exists")
                return "info: " + path_to_remote_file + " already exists"

            os.makedirs(os.path.dirname(path_to_remote_file), exist_ok=True)
            if path_to_remote_file and Path(os.path.join(what_to_push, key)).exists():
                copyfile(os.path.join(what_to_push, key), path_to_remote_file)
                self.messages.append("info: " + key + " pushed successfully")
                return "info: " + key + " pushed successfully"
            self.messages.append("error: file does not exist")
            return "error: file does not exist"

        files_to_push = self.read_all_from_local_config(what_to_push)
        self.messages = []
        if files_to_push:
            for file_to_push in files_to_push:
                self.push(what_to_push, file_to_push)
            return self.messages
        self.messages.append("error: No file added to " + what_to_push)
        return self.messages
