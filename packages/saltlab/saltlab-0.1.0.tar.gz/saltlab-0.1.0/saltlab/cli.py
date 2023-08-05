"""
saltlab CLI tool
"""
import click
import itertools
from .di import registry
from .cluster import Cluster
from .desert import save_savefile, clear_savefile
from . import load_cluster


@click.group()
def saltlab():
    """
    saltlab tool
    """
    pass


@saltlab.command()
@click.option('--image', default='debian:stable-slim')
def init(image):
    """
    Creates a salt cluster, spawning the master.
    """
    cluster = Cluster.create_new(image)
    save_savefile(cluster)


@saltlab.command()
def nuke():
    """
    Destroys a whole cluster, including master and all minions
    """
    with load_cluster() as cluster:
        cluster.destroy()
    clear_savefile()


def _fix_stats(val):
    """
    Deals with the incredible inconsistency that is the prune commands.
    """
    if 'ContainersDeleted' in val:
        if val['ContainersDeleted'] is None:
            return 0, val['SpaceReclaimed']
        else:
            return len(val['ContainersDeleted']), val['SpaceReclaimed']
    elif 'ImagesDeleted' in val:
        if val['ImagesDeleted'] is None:
            return 0, val['SpaceReclaimed']
        else:
            return len(val['ImagesDeleted']), val['SpaceReclaimed']
    elif 'NetworksDeleted' in val:
        if val['NetworksDeleted'] is None:
            return 0, 0
        else:
            return len(val['NetworksDeleted']), 0
    else:
        print(val)
        return 0, 0


@saltlab.command()
def megaprune():
    """
    Prunes everything
    """
    docker = registry['DockerClient']
    c_count, c_size = _fix_stats(docker.containers.prune())
    print(f"Pruned {c_count} containers freeing {c_size} bytes")
    i_count, i_size = _fix_stats(docker.images.prune())
    print(f"Pruned {i_count} images freeing {i_size} bytes")
    n_count, n_size = _fix_stats(docker.networks.prune())
    print(f"Pruned {n_count} networks")

    total = c_size + i_size + n_size
    mb = round(total / 1024 / 1024)
    print(f"Freed {mb}MB total")


@saltlab.command()
@click.argument('name')
@click.option('--image', default='debian:stable-slim')
def spawn(name, image):
    """
    Spawns a new minion and enrolls it to the master.
    """
    with load_cluster() as cluster:
        cluster.spawn_minion(name, image)


@saltlab.command()
def ls():
    """
    List minions.
    """
    with load_cluster() as cluster:
        for mid in cluster.minions.keys():
            print(mid)


@saltlab.command()
@click.argument('name')
def terminate(name):
    """
    Destroys a minion
    """
    with load_cluster() as cluster:
        cluster.terminate_minion(name)


@saltlab.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.argument('target')
def mount(source, target):
    """
    Mount a directory into the salt filesystem.
    """
    with load_cluster() as cluster:
        cluster.add_fs_mount(source, target)


@saltlab.command()
@click.argument('target')
def unmount(target):
    """
    Unmount a directory from the salt filesystem.
    """
    with load_cluster() as cluster:
        cluster.remove_fs_mount(target=target)


@saltlab.command()
def kickall():
    """
    Reboot all servers
    """
    with load_cluster() as cluster:
        print("Restarting master...")
        cluster.master.restart()
        for m in cluster.minions.values():
            print(f"Restarting {m.name}...")
            m.restart()


@saltlab.command()
@click.argument('server')
def kick(server):
    """
    Reboot a given server (master accepted).
    """
    with load_cluster() as cluster:
        container = cluster.get(server)
        container.restart()


@saltlab.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('salt_args', nargs=-1, type=click.UNPROCESSED)
def call(salt_args):
    """
    Performs a salt minion call. See https://docs.saltstack.com/en/latest/ref/cli/salt.html
    for usage.
    """
    with load_cluster() as cluster:
        cluster.master.piped_call(['salt'] + list(salt_args))


@saltlab.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('salt_args', nargs=-1, type=click.UNPROCESSED)
def run(salt_args):
    """
    Performs a salt runner call. See https://docs.saltstack.com/en/latest/ref/cli/salt-run.html
    for usage.
    """
    with load_cluster() as cluster:
        cluster.master.piped_call(['salt-run'] + list(salt_args))


# TODO (in the order I thought of them):
#  * Port exposing (master and minions)
#  * Config editing (master and minions)
#  * Multi-master configurations
#  * Keys (proxy for salt-key)
#  * Pillar
#  * Pip Install Editable (PIE)
