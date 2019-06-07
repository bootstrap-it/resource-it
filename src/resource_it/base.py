from typing import Any, Generic
from dataclasses import dataclass, asdict
from contextlib import suppress
from urllib.parse import urlparse

import log_it
log = log_it.logger(__name__)

class ResourceNotFoundError(Exception):
    pass

@dataclass
class ResourceUrl:
    scheme: str = ""
    netloc: str = ""
    path: str = ""
    params: str = ""
    query: str = ""
    fragment: str = ""

    def __repr__(self):
        url = [f"{self.scheme}://"]
        if self.netloc:
            url.append({self.netloc})
        if self.path:
            url.append(self.path)
        return "".join(url)

    @staticmethod
    def from_str(url):
        return ResourceUrl(**urlparse(url)._asdict())


class Resource:
    url: ResourceUrl
    data: Any = None
    data_cls: Generic = None

    def __init__(self, url):
        self.url = url
        self.init()
        with suppress(ResourceNotFoundError):
            self.read()

    def init(self):
        pass

    @property
    def exists(self):
        return self.data

    def create(self, data=None):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def update(self, data=None):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return repr(self.url)

    def diff(self, data):
        def calculate_diff(data):
            for field_name, field_value in data.items():
                res_data_value = getattr(self.data, field_name)
                if field_value and res_data_value != field_value:
                    yield field_name, field_value

        return dict(calculate_diff(data))