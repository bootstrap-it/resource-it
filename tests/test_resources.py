from resource_it.filesystem import Dir, File, glob
from resource_it import ensure
from pipe_it import first, tee_log, drain, where, apply
import log_it
log = log_it.logger(__name__)

# def test_consul_kv():
#     [1, 3, 4] | consul_kv("some-kv-path")
#     {"p":1, "t":2, "e":3} | consul_kv("pte-kv-path")

def test_files():
    pass

def test_dirs():
    (Dir(".")
    | glob("**/*.py")
    | where(lambda it: it.url.startswith("cfg-it"))
    | apply(lambda it: it.data.content)
    | tee_log
    | drain
    )

def test_file_creation():
    file_data = File.data_cls(content="tt1t")
    File(
        url="tes11t_file.txt",
        data={"content":"tt2t"}
    )


if __name__ == "__main__":
    # test_dirs()
    test_file_creation()