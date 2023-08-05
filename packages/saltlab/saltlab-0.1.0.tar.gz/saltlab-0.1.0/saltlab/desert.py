import camel
import docker
from pathlib import Path
from .cluster import Cluster
from .client import Container, MasterContainer
from .di import registry

FILENAME = '.saltlab'

cregistry = camel.CamelRegistry()


@cregistry.dumper(Container, 'container', version=1)
@cregistry.dumper(MasterContainer, 'master', version=1)
@cregistry.dumper(docker.models.containers.Container, 'container', version=1)
def _dump_container(cont):
    return cont.id


@cregistry.loader('container', version=1)
def _load_container(data, version):
    return Container.get(data)


@cregistry.loader('master', version=1)
def _load_master(data, version):
    return MasterContainer.get(data)


@cregistry.dumper(docker.models.networks.Network, 'network', version=1)
def _dump_network(net):
    return net.id


@cregistry.loader('network', version=1)
def _load_network(data, version):
    client = registry['DockerClient']
    return client.networks.get(data)


@cregistry.dumper(docker.models.images.Image, 'image', version=1)
def _dump_image(img):
    return img.id


@cregistry.loader('image', version=1)
def _load_image(data, version):
    client = registry['DockerClient']
    return client.images.get(data)


@cregistry.dumper(Cluster, 'cluster', version=1)
def _dump_cluster(obj):
    return {
        'master': obj.master,
        'network': obj.network,
        'minions': obj.minions,
    }


@cregistry.loader('cluster', version=1)
def _load_cluster(data, version):
    return Cluster(data['master'], data['network'], data['minions'])


def find_savefile():
    # For now, only one per user
    return Path.home() / FILENAME


def load_savefile():
    fn = find_savefile()
    camel = registry['Camel']
    if fn.exists():
        return camel.load(fn.read_text())


def save_savefile(obj):
    fn = find_savefile()
    camel = registry['Camel']
    fn.write_text(camel.dump(obj))


def clear_savefile():
    fn = find_savefile()
    if fn.exists():
        fn.unlink()
