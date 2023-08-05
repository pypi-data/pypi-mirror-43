"""
Functions to load/save cluster information.
"""
import pkg_resources
import tarfile
import io
import sys
import secrets
import os.path
import yaml
import itertools
from .di import inject
from .client import Container, MasterContainer


class Cluster:
    client = inject('DockerClient')

    def __init__(self, master, network, minions):
        self.master = master or None
        self.network = network or None
        self.minions = minions or {}

        if master is not None:
            for container in itertools.chain((master,), self.minions.values()):
                container.start()

    @classmethod
    def create_new(cls, image):
        """
        Create a new cluster and save the information.
        """
        # We actually need the instance around to perform some of the initialization
        self = cls(None, None, None)
        self.network = cls.client.networks.create(
            name='saltlab',
        )

        self.master = MasterContainer(self._spawn_container(
            name='saltlab-master',
            image=image,
            network=self.network.id,
            hostname='master',
            command=['salt-master'],
            bootstrap_args=['-M', '-i', 'master', '-A', 'localhost'],
        ))
        return self

    def destroy(self):
        """
        Destroy the entire cluster, including master and minions.
        """
        print(f"Destroying container {self.master.name}...")
        self.master.remove(force=True)
        self.master = None

        for minion in self.minions.values():
            print(f"Destroying container {minion.name}...")
            minion.remove(force=True)
        self.minions = None

        print("Destroying network...")
        self.network.remove()
        self.network = None

        print("Pruning containers...")
        self.client.containers.prune()

        print("Pruning images...")
        self.client.images.prune()

    def spawn_minion(self, minionid, image):
        print("Generating keys")
        pub, priv = self.master.generate_minion_keys(minionid)
        print("Spawning container")
        minion = self._spawn_container(
            name=minionid,
            hostname=minionid,
            image=image,
            network=self.network.id,
            command=['salt-minion'],
            minion_keys=(pub, priv),
            bootstrap_args=['-i', minionid, '-A', self.master.name],
        )
        self.minions[minionid] = minion
        while minion.status in ('created',):
            minion.reload()
        minion.reload()
        if minion.status != 'running':
            raise RuntimeError(f"Container failed to start, status={minion.status}")
        print(f"Minion {minionid} started")
        return minion

    def terminate_minion(self, minionid):
        print(f"Destroying {minionid}")
        self.minions[minionid].remove(force=True)
        del self.minions[minionid]

    def _spawn_container(self, *, image, minion_keys=None, bootstrap_args=None, **kwargs):
        """
        Spawn a salted container
        """
        salted_image = self._build_salted_image(
            image=image,
            minion_keys=minion_keys,
            bootstrap_args=bootstrap_args,
        )
        container = Container.run(
            image=salted_image,
            detach=True,
            init=True,
            auto_remove=False,
            **kwargs
        )
        return container

    def _build_salted_image(self, *, image, minion_keys=None, bootstrap_args=None):
        pulled = self.client.images.pull(image)

        temp_container = Container.create(
            image=image,
            command=[
                '/bin/sh', '/tmp/bootstrap-salt.sh', '-U', '-X', '-d', '-x', 'python3'
            ] + (bootstrap_args or []),
            # Don't worry about running an init; it's going to be destroyed in a moment
            auto_remove=False,
        )

        seedfiles = {
            '/tmp/bootstrap-salt.sh': pkg_resources.resource_stream(__name__, 'bootstrap-salt.sh'),
        }
        if minion_keys:
            pub_data, priv_data = minion_keys
            seedfiles['/etc/salt/pki/minion/minion.pub'] = pub_data
            seedfiles['/etc/salt/pki/minion/minion.pem'] = priv_data
        temp_container.inject_files(seedfiles)

        temp_container.start()
        for chunk in temp_container.attach(stream=True, logs=True):
            sys.stdout.write(chunk.decode('utf-8'))

        prepared_image = temp_container.commit()

        temp_container.reload()
        assert temp_container.status == 'exited'
        temp_container.remove()

        return prepared_image

    def _fspath2syspath(self, path):
        if ':' in path:
            env, path = path.split(':', 1)
        else:
            env = 'base'
        if path:
            return f'/srv/salt/{env}/{path}'
        else:
            return f'/srv/salt/{env}'

    def _gen_fs_config(self):
        envs = {'base'}
        for src, dest, mode in self.master.binds():
            if dest.startswith('/srv/salt'):
                rightbit = dest[len('/srv/salt'):].strip('/')
                midbit = rightbit.split('/', 1)[0]
                envs.add(midbit)
        return yaml.safe_dump({
            'file_roots': {
                env: [f'/srv/salt/{env}']
                for env in envs
            }
        })

    def add_fs_mount(self, source, target):
        """
        Add a bind mount into the salt fileserver.
        """
        tpath = self._fspath2syspath(target)
        self.master = self.master.add_mount(
            outside=source,
            inside=tpath,
            mode='r',
        )
        self.master.inject_files({
            '/etc/salt/master.d/fs.conf': self._gen_fs_config(),
        })
        self.master.restart()

    def remove_fs_mount(self, target):
        """
        Remove a bind mount from the salt fileserver.
        """
        tpath = self._fspath2syspath(target)
        self.master = self.master.remove_mount(
            inside=tpath,
        )
        self.master.inject_files({
            '/etc/salt/master.d/fs.conf': self._gen_fs_config(),
        })
        self.master.restart()

    def get(self, minionid):
        """
        Gets the container for the given minion.
        """
        if minionid == 'master':
            return self.master
        else:
            return self.minions[minionid]

    def servers(self):
        yield self.master
        yield from self.minions.values()
