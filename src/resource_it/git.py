from pathlib import Path
import shutil
from dataclasses import dataclass, field

from resource_it import resource, ensure
from resource_it.base import Resource, ResourceNotFoundError
from resource_it.filesystem import Dir
from resource_it.os_utils import run, run_output

from typing import Callable

import cfg_it
import log_it
log = log_it.logger(__name__)


@cfg_it.props
class cfg:
    git_ssh_key_file: str = ""


class Repo(Resource):
    @dataclass
    class meta_cls:
        dir: Dir
        run_git: Callable

    @dataclass
    class data_cls:
        origin: str
        branch: str
        synced: bool
        dir: Dir

    def init(self):
        git_ssh_opts = [
                f"ssh",
                f"-o UserKnownHostsFile=/dev/null",
                f"-o StrictHostKeyChecking=no",
        ]

        if cfg.git_ssh_key_file:
            git_ssh_opts.append(f"-i {cfg.git_ssh_key_file}")

        git_env = {"GIT_SSH_COMMAND": " ".join(git_ssh_opts)}

        self.meta = Repo.meta_cls(
            dir=resource(f"dir://{self.url.path}"),
            run_git=lambda params: run(
                f"git {params}",
                cwd=self.url.path,
                env=git_env),
        )

    def read(self):
        # if cfg.GIT_SSH_KEY_FILE and cfg.GIT_SSH_KEY_FORCE_PERMISSIONS:
        #     os.chmod(cfg.GIT_SSH_KEY_FILE, 400)
        if not self.meta.dir.exists:
            raise ResourceNotFoundError("repo dir doesn't exist")
        run_git = lambda params: run_output(self.meta.run_git(params))

        branch         = run_git(f"rev-parse --abbrev-ref HEAD")
        commits_behind = int(run_git(f"rev-list HEAD...origin/{branch} --count"))

        self.data = Repo.data_cls(
            origin=run_git(f"remote get-url origin"),
            branch=branch,
            synced=(commits_behind == 0),
            dir=self.meta.dir,
        )

    def create(self, **data):
        self.meta.dir | ensure
        origin = data["origin"]
        branch = data.get("branch")

        opts = [
            # "--depth 1",
        ]

        if branch:
            opts.append(f"--branch {branch}")

        self.meta.run_git(f"clone {' '.join(opts)} {origin} .")
        self.read()

    def update(self, **diff):
        if "origin" in diff:
            self.meta.run_git(f"remote set-url origin {diff['origin']}")
        if "branch" in diff:
            self.meta.run_git(f"fetch origin {diff['branch']}")
            self.meta.run_git(f"checkout {diff['branch']}")
            self.meta.run_git(f"pull")
        if "synced" in diff:
            self.meta.run_git(f"pull")
        self.read()

    def delete(self):
        self.data.dir.delete()
        self.read()