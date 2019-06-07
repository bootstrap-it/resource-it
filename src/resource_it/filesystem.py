from dataclasses import dataclass, field
from typing import List, Union, Callable, Iterable, Generator
from pathlib import Path
import shutil

from resource_it import resource, Resource, ResourceNotFoundError
from pipe_it import pipe

import log_it
log = log_it.logger(__name__)


class File(Resource):
    @dataclass
    class meta_cls:
        path: Path

    @dataclass
    class data_cls:
        size: int = 0
        name: str = None
        path: str = None
        content: str = None

        # def __hash__(self):
        #     import hashlib
        #     sha_hash = hashlib.sha256()
        #     for chunk in self.content:
        #         sha_hash.update(chunk)
        #     return sha_hash.digest()

    def init(self):
        self.meta = File.meta_cls(path=Path(self.url.path))

    def read(self):
        try:
            file_content = self.meta.path.read_text()
        except Exception as e:
            raise ResourceNotFoundError(e)
        else:
            self.data = File.data_cls(
                name=self.meta.path.name,
                path=str(self.meta.path.absolute()),
                content=file_content,
                )

    def create(self, data: data_cls):
        self.meta.path.parent.mkdir(parents=True, exist_ok=True)
        self.meta.path.write_text(data.content)

    def update(self, data: data_cls):
        self.meta.path.write_text(data.content)

    def delete(self):
        self.meta.path.unlink


class Dir(Resource):
    @dataclass
    class meta_cls:
        path: Path

    @dataclass
    class data_cls:
        content: Iterable[str]

    def init(self):
        self.meta = Dir.meta_cls(path=Path(self.url.path))

    def __iter__(self):
        for sub_path in self.meta.path.iterdir():
            abs_sub_path = sub_path.absolute()
            if abs_sub_path.is_dir():
                yield f"dir://{abs_sub_path}"
            else:
                yield f"file://{abs_sub_path}"

    def create(self):
        self.meta.path.mkdir(parents=True, exist_ok=True)
        self.read()

    def read(self):
        try:
            self.data = Dir.data_cls(content=list(self))
        except Exception as e:
            ResourceNotFoundError(e)

    def update(self):
        pass

    def delete(self):
        shutil.rmtree(self.meta.path)


@pipe
def glob(dir, pattern="**/*"):
    log.debug(f"glob: search '{pattern}' in dir: {dir.url.path}")
    for path in dir.meta.path.glob(pattern):
        yield resource(f"file://{path.absolute()}")
