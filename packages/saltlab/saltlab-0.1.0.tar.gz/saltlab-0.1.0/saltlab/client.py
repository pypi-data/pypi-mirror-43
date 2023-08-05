import sys
import docker
import secrets
import os.path
import io
import tarfile
from .di import inject


def mktarinfo(data, **args):
    """
    Convenience function to synthesize a TarInfo
    """
    # If we got handed a stream instead of the data, read out the stream
    if hasattr(data, 'read'):
        data = data.read()
    if isinstance(data, str):
        data = data.encode('utf-8')

    ti = tarfile.TarInfo()
    ti.size = len(data)
    ti.type = tarfile.REGTYPE
    for name, value in args.items():
        setattr(ti, name, value)
    return ti, io.BytesIO(data)


class Container:
    _client = inject('DockerClient')

    def __init__(self, container):
        if isinstance(container, Container):
            self._backer = container._backer
        else:
            self._backer = container

    @classmethod
    def run(cls, *pargs, **kwargs):
        c = cls._client.containers.run(*pargs, **kwargs)
        return cls(c)

    @classmethod
    def create(cls, *pargs, **kwargs):
        c = cls._client.containers.create(*pargs, **kwargs)
        return cls(c)

    @classmethod
    def get(cls, *pargs, **kwargs):
        c = cls._client.containers.get(*pargs, **kwargs)
        return cls(c)

    @classmethod
    def list(cls, *pargs, **kwargs):
        for c in cls._client.containers.list(*pargs, **kwargs):
            yield cls(c)

    @classmethod
    def prune(cls, *pargs, **kwargs):
        return cls._client.containers.prune(*pargs, **kwargs)

    def __getattr__(self, name):
        return getattr(self._backer, name)

    def inject_files(self, files):
        """
        Inserts the given files into the container.

        The files are given as a dict, mapping names to data or streams.
        """
        with io.BytesIO() as buff:
            with tarfile.open(fileobj=buff, mode='w:') as tf:
                for name, stream in files.items():
                    tf.addfile(*mktarinfo(stream, name=name))

            self._backer.put_archive('/', buff.getvalue())

    def pull_files(self, path):
        """
        Pull the given directory, returning a TarFile
        """
        buff = io.BytesIO()
        data, stat = self._backer.get_archive(path)
        for chunk in data:
            buff.write(chunk)

        buff.seek(0)

        return tarfile.open(fileobj=buff, mode='r:')

    def network_args(self):
        for name, data in self.attrs['NetworkSettings']['Networks'].items():
            yield self._client.networks.get(data['NetworkID']), {
                'aliases': data['Aliases'],
                'links': data['Links'],
                'ipv4_address': data['IPAddress'],
                'ipv6_address': data['GlobalIPv6Address'],
            }

    def mutate(self, *, delete_old=True, **kwargs):
        """
        Replace this container with an equivalant one, updating the given args
        in the process.

        You may disable deleting the old container, but this may have unintended
        consequences.
        """
        self.stop()
        args = self.init_args()
        args.update(kwargs)
        args['image'] = self.commit()
        networks = list(self.network_args())
        if delete_old:
            self.remove()
        newc = type(self)(self._client.containers.create(**args))

        for network, args in networks:
            network.connect(newc.id, **args)

        newc.start()
        return newc

    def add_mount(self, *, outside, inside, mode='w'):
        """
        Rebuild the container with a new bind mount.
        """
        mounts = list(self._mount_args())
        mounts.append(docker.types.Mount(
            target=inside,
            source=outside,
            type='bind',
            read_only=True if mode == 'r' else False,
        ))
        return self.mutate(mounts=mounts)

    def remove_mount(self, *, inside):
        """
        Rebuild the container with a new bind mount.
        """
        mounts = [
            mount
            for mount in self._mount_args()
            if mount['Destination'] != inside
        ]

        return self.mutate(mounts=mounts)

    def binds(self):
        """
        Generate the bind mounts, as (source, destination, mode)
        """
        for mount in self.attrs['Mounts']:
            yield mount['Source'], mount['Destination'], 'w' if mount['RW'] else 'r'

    def _mount_args(self):
        for mount in self.attrs['Mounts']:
            m = docker.types.Mount(
                target=mount['Destination'],
                source=mount['Source'],
            )
            m.update(mount)
            yield m

    def init_args(self):
        """
        Return the arguments used to create this container.

        Networks are omitted, because proper cloning cannot happen from init
        args alone.
        """
        self.reload()
        return {
            'image': self.image,
            'command': self.attrs['Config']['Cmd'],
            'auto_remove': self.attrs['HostConfig']['AutoRemove'],
            'blkio_weight_device': self.attrs['HostConfig']['BlkioWeightDevice'],
            'blkio_weight': self.attrs['HostConfig']['BlkioWeight'],
            'cap_add': self.attrs['HostConfig']['CapAdd'],
            'cap_drop': self.attrs['HostConfig']['CapDrop'],
            'cpu_count': self.attrs['HostConfig']['CpuCount'],
            'cpu_percent': self.attrs['HostConfig']['CpuPercent'],
            'cpu_period': self.attrs['HostConfig']['CpuPeriod'],
            'cpu_quota': self.attrs['HostConfig']['CpuQuota'],
            'cpu_shares': self.attrs['HostConfig']['CpuShares'],
            'cpuset_cpus': self.attrs['HostConfig']['CpusetCpus'],
            'cpuset_mems': self.attrs['HostConfig']['CpusetMems'],
            'device_cgroup_rules': self.attrs['HostConfig']['DeviceCgroupRules'],
            'device_read_bps': self.attrs['HostConfig']['BlkioDeviceReadBps'],
            'device_read_iops': self.attrs['HostConfig']['BlkioDeviceReadIOps'],
            'device_write_bps': self.attrs['HostConfig']['BlkioDeviceWriteBps'],
            'device_write_iops': self.attrs['HostConfig'].get('BlkioDeviceWriteIops'),
            'devices': self.attrs['HostConfig']['Devices'],
            'dns': self.attrs['HostConfig']['Dns'],
            'dns_opt': self.attrs['HostConfig']['DnsOptions'],
            'dns_search': self.attrs['HostConfig']['DnsSearch'],
            'domainname': self.attrs['Config']['Domainname'],
            'entrypoint': self.attrs['Config']['Entrypoint'],
            'environment': self.attrs['Config']['Env'],
            'extra_hosts': self.attrs['HostConfig']['ExtraHosts'],
            'group_add': self.attrs['HostConfig']['GroupAdd'],
            # 'healthcheck': ...,
            'hostname': self.attrs['Config']['Hostname'],
            'init': self.attrs['HostConfig']['Init'],
            # 'init_path': ...,
            'ipc_mode': self.attrs['HostConfig']['IpcMode'],
            'isolation': self.attrs['HostConfig']['Isolation'],
            'labels': self.labels,
            'links': self.attrs['HostConfig']['Links'],
            'log_config': self.attrs['HostConfig']['LogConfig'],
            'mac_address': self.attrs['NetworkSettings']['MacAddress'],
            # 'mem_limit': ...,
            'mem_swappiness': self.attrs['HostConfig']['MemorySwappiness'],
            # 'memswap_limit': ...,
            'mounts': list(self._mount_args()),
            'name': self.name,
            'nano_cpus': self.attrs['HostConfig']['NanoCpus'],
            # 'network': self.attrs['NetworkSettings']['Networks'],
            # 'network_disabled': ...,
            # 'network_mode': self.attrs['HostConfig']['NetworkMode'],
            'oom_kill_disable': self.attrs['HostConfig']['OomKillDisable'],
            'oom_score_adj': self.attrs['HostConfig']['OomScoreAdj'],
            'pid_mode': self.attrs['HostConfig']['PidMode'],
            'pids_limit': self.attrs['HostConfig']['PidsLimit'],
            # 'platform': self.attrs['Platform'],  # FIXME: create() doesn't like this
            'ports': self.attrs['NetworkSettings']['Ports'],
            'privileged': self.attrs['HostConfig']['Privileged'],
            'publish_all_ports': self.attrs['HostConfig']['PublishAllPorts'],
            'read_only': self.attrs['HostConfig']['ReadonlyRootfs'],
            'restart_policy': self.attrs['HostConfig']['RestartPolicy'],
            'runtime': self.attrs['HostConfig']['Runtime'],
            'security_opt': self.attrs['HostConfig']['SecurityOpt'],
            'shm_size': self.attrs['HostConfig']['ShmSize'],
            'stdin_open': self.attrs['Config']['OpenStdin'],  #???
            # 'stdout': ...,
            # 'stderr': ...,
            # 'stop_signal': ...,
            # 'storage_opt': ...,
            # 'sysctls': ...,
            # 'tmpfs': ...,
            'tty': self.attrs['Config']['Tty'],
            'ulimits': self.attrs['HostConfig']['Ulimits'],
            # 'use_config_proxy': ...,
            'user': self.attrs['Config']['User'],
            'userns_mode': self.attrs['HostConfig']['UsernsMode'],
            # 'volume_driver': self.attrs['HostConfig']['VolumeDriver'],  # FIXME: create() doesn't like this
            # 'volumes': self.attrs['Config']['Volumes'],  # Use mounts instead
            'volumes_from': self.attrs['HostConfig']['VolumesFrom'],
            'working_dir': self.attrs['Config']['WorkingDir'],
        }

    def piped_call(self, command):
        """
        Make a call, piping the output

        Note: Does not distinguish between stdout and stderr, because complexity.
        """
        status, stream = self._backer.exec_run(
            cmd=command,
            stdin=False,
            stdout=True,
            stderr=True,
            demux=False,
            stream=True,
        )
        for chunk in stream:
            sys.stdout.write(chunk.decode('utf-8'))


class MasterContainer(Container):
    def generate_minion_keys(self, minionid):
        # Unfortunately, we can't get salt-key to spew keys directly; we'd have
        # to use the Python API
        tempdir = '/tmp/' + secrets.token_urlsafe()

        # Create staging directory
        self.exec_run(
            cmd=['mkdir', tempdir],
        )

        # Generate keys
        status, _ = self.exec_run(
            cmd=['salt-key', '--gen-keys='+minionid, '--gen-keys-dir='+tempdir],
        )

        # Pull out data
        ball = self.pull_files(tempdir)

        privkey_name = [name for name in ball.getnames() if os.path.splitext(name)[1] == '.pem'][0]
        pubkey_name = [name for name in ball.getnames() if os.path.splitext(name)[1] == '.pub'][0]

        with ball.extractfile(privkey_name) as f:
            privkey_data = f.read()

        with ball.extractfile(pubkey_name) as f:
            pubkey_data = f.read()

        # Remove staging directory
        self.exec_run(
            cmd=['rm', '-r', tempdir],
        )

        # Pre-accept the minion key
        self.inject_files({
            '/etc/salt/pki/master/minions/'+minionid: pubkey_data
        })

        return pubkey_data, privkey_data
