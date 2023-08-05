import contextlib
import sys
from .di import registry

__version__ = '0.1.0'
__all__ = ()


@registry.register('DockerClient')
def client():
    import docker
    return docker.from_env()


@registry.register('Camel')
def init_camel():
    import camel
    from .desert import cregistry

    return camel.Camel([cregistry, camel.PYTHON_TYPES])


@contextlib.contextmanager
def load_cluster():
    from .desert import load_savefile, save_savefile
    cluster = load_savefile()
    if cluster is None:
        sys.exit("No cluster found")
    try:
        yield cluster
    finally:
        save_savefile(cluster)
