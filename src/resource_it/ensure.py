from typing import Any
from . import pipe

from mock.log import logger
log = logger(__name__)

@pipe
class attr:
    attr_name: str

    def pipe_it(self, obj: Any) -> Any:
        log.info(f"select: {repr(obj)}")
        return getattr(obj, self.attr_name)
