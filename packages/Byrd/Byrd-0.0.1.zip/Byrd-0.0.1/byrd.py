from contextlib import contextmanager
from getpass import getpass
from hashlib import md5
from itertools import chain
from collections import ChainMap, OrderedDict, defaultdict
from itertools import islice
from string import Formatter
import argparse
import io
import logging
import os
import posixpath
import subprocess
import sys
import threading

try:
    # This file is imported by setup.py at install time
    import keyring
    import paramiko
    import yaml
except ImportError:
    pass

__version__ = '0.0.1'


log_fmt = '%(levelname)s:%(asctime).19s: %(message)s'
logger = logging.getLogger('byrd')
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter(log_fmt))
logger.addHandler(log_handler)

basedir, _ = os.path.split(__file__)
PKG_DIR = os.path.join(basedir, 'pkg')
TAB = '\n    '

class ByrdException(Exception):
    pass

class FmtException(ByrdException):
    pass

class ExecutionException(ByrdException):
    pass

class RemoteException(ExecutionException):
    pass

class LocalException(ExecutionException):
    pass

def enable_logging_color():
    try:
        import colorama
    except ImportError:
        return

    colorama.init()
    MAGENTA = colorama.Fore.MAGENTA
    RED = colorama.Fore.RED
    RESET = colorama.Style.RESET_ALL

    # We define custom handler ..
    class Handler(logging.StreamHandler):
        def format(self, record):
            if record.levelname == 'INFO':
                record.msg = MAGENTA + record.msg + RESET
            elif record.levelname in ('WARNING', 'ERROR', 'CRITICAL'):
                record.msg = RED + record.msg + RESET
            return super(Handler, self).format(record)

    #  .. and plug it
    logger.removeHandler(log_handler)
    handler = Handler()
    handler.setFormatter(logging.Formatter(log_fmt))
    logger.addHandler(handler)
    logger.propagate = 0


def yaml_load(stream):
    class OrderedLoader(yaml.Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def edits(word):
    yield word
    splits = ((word[:i], word[i:]) for i in range(len(word) + 1))
    for left, right in splits:
        if right:
            yield left + right[1:]


def gen_candidates(wordlist):
    candidates = defaultdict(set)
    for word in wordlist:
        for ed1 in edits(word):
            for ed2 in edits(ed1):
                candidates[ed2].add(word)
    return candidates


def spell(candidates,  word):
    matches = set(chain.from_iterable(
        candidates[ed] for ed in edits(word) if ed in candidates
    ))
    return matches


def spellcheck(objdict, word):
    if word in objdict:
        return

    candidates = objdict.get('_candidates')
    if not candidates:
        candidates = gen_candidates(list(objdict))
        objdict._candidates = candidates

    msg = '"%s" not found in %s' % (word, objdict._path)
    matches = spell(candidates, word)
    if matches:
        msg += ', try: %s' % ' or '.join(matches)
    raise ByrdException(msg)


class ObjectDict(dict):
    """
    Simple objet sub-class that allows to transform a dict into an
    object, like: `ObjectDict({'ham': 'spam'}).ham == 'spam'`
    """

    # Meta allows to hide all the keys starting with an '_'
    _meta = {}

    def copy(self):
        res = ObjectDict(super().copy())
        ObjectDict._meta[id(res)] = ObjectDict._meta.get(id(self), {}).copy()
        return res

    def __getattr__(self, key):
        if key.startswith('_'):
            return ObjectDict._meta[id(self), key]

        if key in self:
            return self[key]
        else:
            return None

    def __setattr__(self, key, value):
        if key.startswith('_'):
            ObjectDict._meta[id(self), key] = value
        else:
            self[key] = value

class Node:

    @staticmethod
    def fail(path, kind):
        msg = 'Error while parsing config: expecting "%s" while parsing "%s"'
        raise ByrdException(msg % (kind, '->'.join(path)))

    @classmethod
    def parse(cls, cfg, path=tuple()):
        children = getattr(cls, '_children', None)
        type_name = children and type(children).__name__ \
                    or ' or '.join((c.__name__ for c in cls._type))
        res = None
        if type_name == 'dict':
            if not isinstance(cfg, dict):
                cls.fail(path, type_name)
            res = ObjectDict()

            if '*' in children:
                assert len(children) == 1, "Don't mix '*' and other keys"
                child_class = children['*']
                for name, value in cfg.items():
                    res[name] = child_class.parse(value, path + (name,))
            else:
                # Enforce known pre-defined
                for key in cfg:
                    if key not in children:
                        path = ' -> '.join(path)
                        if path:
                            msg = 'Attribute "%s" not understood in %s' % (
                                key, path)
                        else:
                            msg = 'Top-level attribute "%s" not understood' % (
                                key)
                        candidates = gen_candidates(children.keys())
                        matches = spell(candidates, key)
                        if matches:
                            msg += ', try: %s' % ' or '.join(matches)
                        raise ByrdException(msg)

                for name, child_class in children.items():
                    if name not in cfg:
                        continue
                    res[name] = child_class.parse(cfg[name], path + (name,))

        elif type_name == 'list':
            if not isinstance(cfg, list):
                cls.fail(path, type_name)
            child_class = children[0]
            res = [child_class.parse(c, path+ ('[%s]' % pos,))
                   for pos, c in enumerate(cfg)]

        else:
            if not isinstance(cfg, cls._type):
                cls.fail(path, type_name)
            res = cfg

        return cls.setup(res, path)

    @classmethod
    def setup(cls, values, path):
        if isinstance(values, ObjectDict):
            values._path = '->'.join(path)
        return values


class Atom(Node):
    _type = (str, bool)

class AtomList(Node):
    _children = [Atom]

class Hosts(Node):
    _children = [Atom]

class Auth(Node):
    _children = {'*': Atom}

class EnvNode(Node):
    _children = {'*': Atom}

class HostGroup(Node):
    _children = {
        'hosts': Hosts,
    }

class Network(Node):
    _children = {
        '*': HostGroup,
    }

class Multi(Node):
    _children = {
        'task': Atom,
        'export': Atom,
        'network': Atom,
    }

class MultiList(Node):
    _children = [Multi]

class Task(Node):
    _children = {
        'desc': Atom,
        'local': Atom,
        'python': Atom,
        'once': Atom,
        'run': Atom,
        'sudo': Atom,
        'send': Atom,
        'to': Atom,
        'assert': Atom,
        'env': EnvNode,
        'multi': MultiList,
        'fmt': Atom,
    }

    @classmethod
    def setup(cls, values, path):
        values['name'] = path and path[-1] or ''
        if 'desc' not in values:
            values['desc'] = values.get('name', '')
        super().setup(values, path)
        return values

# Multi can also accept any task attribute:
Multi._children.update(Task._children)


class TaskGroup(Node):
    _children = {
        '*': Task,
    }

class LoadNode(Node):
    _children = {
        'file': Atom,
        'pkg': Atom,
        'as': Atom,
    }

class LoadList(Node):
    _children = [LoadNode]

class ConfigRoot(Node):
    _children = {
        'networks': Network,
        'tasks': TaskGroup,
        'auth': Auth,
        'env': EnvNode,
        'load': LoadList,
    }


class Env(ChainMap):

    def __init__(self, *dicts):
        self.fmt_kind = 'new'
        return super().__init__(*filter(lambda x: x is not None, dicts))

    def fmt_env(self, child_env, kind=None):
        new_env = {}
        for key, val in child_env.items():
            # env wrap-around!
            new_val = self.fmt(val, kind=kind)
            if new_val == val:
                continue
            new_env[key] = new_val
        return Env(new_env, child_env)

    def fmt_string(self, string, kind=None):
        fmt_kind = kind or self.fmt_kind
        try:
            if fmt_kind == 'old':
                return string % self
            else:
                return string.format(**self)
        except KeyError as exc:
            msg = 'Unable to format "%s" (missing: "%s")'% (string, exc.args[0])
            candidates = gen_candidates(self.keys())
            key = exc.args[0]
            matches = spell(candidates, key)
            if matches:
                msg += ', try: %s' % ' or '.join(matches)
            raise FmtException(msg )
        except IndexError as exc:
            msg = 'Unable to format "%s", positional argument not supported'
            raise FmtException(msg)

    def fmt(self, what, kind=None):
        if isinstance(what, str):
            return self.fmt_string(what, kind=kind)
        return self.fmt_env(what, kind=kind)


class DummyClient:
    '''
    Dummy Paramiko client, mainly usefull for testing & dry runs
    '''

    @contextmanager
    def open_sftp(self):
        yield None


def get_secret(service, resource, resource_id=None):
    resource_id = resource_id or resource
    secret = keyring.get_password(service, resource_id)
    if not secret:
        secret = getpass('Password for %s: ' % resource)
        keyring.set_password(service, resource_id, secret)
    return secret


def get_passphrase(key_path):
    service = 'SSH private key'
    csum = md5(open(key_path, 'rb').read()).digest().hex()
    return get_secret(service, key_path, csum)


def get_password(host):
    service = 'SSH password'
    return get_secret(service, host)


def get_sudo_passwd():
    service = "Sudo password"
    return get_secret(service, 'sudo')


CONNECTION_CACHE = {}
def connect(host, auth):
    if host in CONNECTION_CACHE:
        return CONNECTION_CACHE[host]

    private_key_file = password = None
    if auth and auth.get('ssh_private_key'):
        private_key_file = auth.ssh_private_key
        if not os.path.exists(auth.ssh_private_key):
            msg = 'Private key file "%s" not found' % auth.ssh_private_key
            raise ByrdException(msg)
        password = get_passphrase(auth.ssh_private_key)
    else:
        password = get_password(host)

    username, hostname = host.split('@', 1)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password,
                   key_filename=private_key_file,
    )
    CONNECTION_CACHE[host] = client
    return client


def run_local(cmd, env, cli):
    # Run local task
    cmd = env.fmt(cmd)
    logger.info(env.fmt('{task_desc}', kind='new'))
    if cli.dry_run:
        logger.info('[dry-run] ' + cmd)
        return None
    logger.debug(TAB + TAB.join(cmd.splitlines()))
    process = subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    stdout, stderr = process.communicate()
    success = process.returncode == 0
    if stdout:
        logger.debug(TAB + TAB.join(stdout.decode().splitlines()))
    if not success:
        raise LocalException(stdout, stderr)
    return ObjectDict(stdout=stdout, stderr=stderr)


def run_python(task, env, cli):
    # Execute a piece of python localy
    code = task.python
    logger.info(env.fmt('{task_desc}', kind='new'))
    if cli.dry_run:
        logger.info('[dry-run] ' + code)
        return None
    logger.debug(TAB + TAB.join(code.splitlines()))
    cmd = ['python', '-c', 'import sys;exec(sys.stdin.read())']
    if task.sudo:
        user = 'root' if task.sudo is True else task.sudo
        cmd = 'sudo -u {} -- {}'.format(user, cmd)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        env=env,
    )

    # Plug io
    out_buff = io.StringIO()
    err_buff = io.StringIO()
    log_stream(process.stdout, out_buff)
    log_stream(process.stderr, err_buff)
    process.stdin.write(code.encode())
    process.stdin.flush()
    process.stdin.close()
    success = process.wait() == 0
    process.stdout.close()
    process.stderr.close()
    out = out_buff.getvalue()
    if out:
        logger.debug(TAB + TAB.join(out.splitlines()))
    if not success:
        raise LocalException(out + err_buff.getvalue())
    return ObjectDict(stdout=out, stderr=err_buff.getvalue())


def log_stream(stream, buff):
    def _log():
        try:
            for chunk in iter(lambda: stream.readline(2048), ""):
                if isinstance(chunk, bytes):
                    chunk = chunk.decode()
                buff.write(chunk)
        except ValueError:
            # read raises a ValueError on closed stream
            pass

    t = threading.Thread(target=_log)
    t.start()
    return t


def run_helper(client, cmd, env=None, in_buff=None, sudo=False):
    '''
    Helper function to run `cmd` command on remote host
    '''
    chan = client.get_transport().open_session()
    if env:
        chan.update_environment(env)

    stdin = chan.makefile('wb')
    stdout = chan.makefile('r')
    stderr = chan.makefile_stderr('r')
    out_buff = io.StringIO()
    err_buff = io.StringIO()
    out_thread = log_stream(stdout, out_buff)
    err_thread = log_stream(stderr, err_buff)

    if sudo:
        assert not in_buff, 'in_buff and sudo can not be combined'
        if isinstance(sudo, str):
            sudo_cmd = 'sudo -u %s -s' % sudo
        else:
            sudo_cmd = 'sudo -s'
        chan.exec_command(sudo_cmd)
        in_buff = cmd
    else:
        chan.exec_command(cmd)
    if in_buff:
        # XXX use a real buff (not a simple str) ?
        stdin.write(in_buff)
        stdin.flush()
        stdin.close()
        chan.shutdown_write()

    success = chan.recv_exit_status() == 0
    out_thread.join()
    err_thread.join()

    if not success:
        raise RemoteException(out_buff.getvalue() + err_buff.getvalue())

    res = ObjectDict(
        stdout = out_buff.getvalue(),
        stderr = err_buff.getvalue(),
    )
    return res


def run_remote(task, host, env, cli):
    res = None
    host = env.fmt(host)
    env.update({
        'host': extract_host(host),
    })
    if cli.dry_run:
        client = DummyClient()
    else:
        client = connect(host, cli.cfg.auth)

    if task.run:
        cmd = env.fmt(task.run)
        prefix = ''
        if task.sudo:
            if task.sudo is True:
                prefix = '[sudo] '
            else:
                 prefix = '[sudo as %s] ' % task.sudo
        msg = prefix + '{host}: {task_desc}'
        logger.info(env.fmt(msg, kind='new'))
        logger.debug(TAB + TAB.join(cmd.splitlines()))
        if cli.dry_run:
            logger.info('[dry-run] ' + cmd)
        else:
            res = run_helper(client, cmd, env=env, sudo=task.sudo)

    elif task.send:
        local_path = env.fmt(task.send)
        remote_path = env.fmt(task.to)
        if not os.path.exists(local_path):
            raise ByrdException('Path "%s" not found'  % local_path)
        else:
            send(client, env, cli, task)

    else:
        raise ByrdException('Unable to run task "%s"' % task.name)

    if res and res.stdout:
        logger.debug(TAB + TAB.join(res.stdout.splitlines()))

    return res

def send(client, env, cli, task):
    fmt = task.fmt and Env(env, {'fmt': 'new'}).fmt(task.fmt) or None
    local_path = env.fmt(task.send)
    remote_path = env.fmt(task.to)
    dry_run = cli.dry_run
    with client.open_sftp() as sftp:
        if os.path.isfile(local_path):
            send_file(sftp, os.path.abspath(local_path), remote_path, env,
                      dry_run=dry_run, fmt=fmt)
        elif os.path.isdir(local_path):
            for root, subdirs, files in os.walk(local_path):
                rel_dir = os.path.relpath(root, local_path)
                rel_dirs = os.path.split(rel_dir)
                rem_dir = posixpath.join(remote_path, *rel_dirs)
                run_helper(client, 'mkdir -p {}'.format(rem_dir))
                for f in files:
                    rel_f = os.path.join(root, f)
                    rem_file = posixpath.join(rem_dir, f)
                    send_file(sftp, os.path.abspath(rel_f), rem_file, env,
                              dry_run=dry_run, fmt=fmt)
        else:
            msg = 'Unexpected path "%s" (not a file, not a directory)'
            raise ByrdException(msg % local_path)


def send_file(sftp, local_path, remote_path, env, dry_run=False, fmt=None):
    if not fmt:
        logger.info(f'[send] {local_path} -> {remote_path}')
        lines = islice(open(local_path), 30)
        logger.debug('File head:' + TAB.join(lines))
        if not dry_run:
            sftp.put(local_path, remote_path)
        return
    # Format file content and save it on remote
    logger.info(f'[fmt] {local_path} -> {remote_path}')
    content = env.fmt(open(local_path).read(), kind=fmt)
    lines = islice(content.splitlines(), 30)
    logger.debug('File head:' + TAB.join(lines))
    if not dry_run:
        fh = sftp.open(remote_path, mode='w')
        fh.write(content)
        fh.close()


def run_task(task, host, cli, env=None):
    '''
    Execute one task on one host (or locally)
    '''
    if task.local:
        res = run_local(task.local, env, cli)
    elif task.python:
        res = run_python(task, env, cli)
    else:
        res = run_remote(task, host, env, cli)

    if task.get('assert'):
        eval_env = {
            'stdout': res.stdout.strip(),
            'stderr': res.stderr.strip(),
        }
        assert_ = env.fmt(task['assert'])
        ok = eval(assert_, eval_env)
        if ok:
            logger.info('Assert ok')
        else:
            raise ByrdException('Assert "%s" failed!' % assert_)
    return res


def run_batch(task, hosts, cli, global_env=None):
    '''
    Run one task on a list of hosts
    '''
    out = None
    export_env = {}
    task_env = global_env.fmt(task.get('env', {}))
    if task.get('multi'):
        parent_env = Env(export_env, task_env, global_env)
        parent_sudo = task.sudo
        for pos, step in enumerate(task.multi):
            task_name = step.task
            if task_name:
                # _cfg contain "local" config wrt the task
                siblings = task._cfg.tasks
                spellcheck(siblings, task_name)
                sub_task = siblings[task_name]
                sudo = step.sudo or sub_task.sudo or parent_sudo
            else:
                # reify a task out of attributes
                sub_task = Task.parse(step)
                sub_task._path = '%s->[%s]' % (task._path, pos)
                sudo = sub_task.sudo or parent_sudo

            sub_task.sudo = sudo
            network = step.get('network')
            if network:
                spellcheck(cli.cfg.networks, network)
                hosts = cli.cfg.networks[network].hosts
            child_env = step.get('env', {})
            child_env = parent_env.fmt(child_env)
            out = run_batch(sub_task, hosts, cli, Env(child_env, parent_env))
            out = out.decode() if isinstance(out, bytes) else out
            export_env['_'] = out
            if step.export:
                export_env[step.export] = out

    else:
        task_env.update({
            'task_desc': global_env.fmt(task.desc),
            'task_name': task.name,
        })
        parent_env = Env(task_env, global_env)
        if task.get('fmt'):
            parent_env.fmt_kind = task.fmt

        res = None
        if task.once and (task.local or task.python):
            res = run_task(task, None, cli, parent_env)
        elif hosts:
            for host in hosts:
                env_host = extract_host(host)
                parent_env.update({
                    'host': env_host,
                })
                res = run_task(task, host, cli, parent_env)
                if task.once:
                    break
        else:
            logger.warning('Nothing to do for task "%s"' % task._path)
        out = res and res.stdout.strip() or ''
    return out


def extract_host(host_string):
    return host_string and host_string.split('@')[-1] or ''


def abort(msg):
    logger.error(msg)
    sys.exit(1)


def load_cfg(path, prefix=None):
    load_sections = ('networks', 'tasks', 'auth', 'env')

    if os.path.isfile(path):
        logger.debug('Load config %s' % path)
        cfg = yaml_load(open(path))
        cfg = ConfigRoot.parse(cfg)
    else:
        raise ByrdException('Config file "%s" not found' % path)

    # Define useful defaults
    cfg.networks = cfg.networks or ObjectDict()
    cfg.tasks = cfg.tasks or ObjectDict()

    # Create backrefs between tasks to the local config
    if cfg.get('tasks'):
        cfg_cp = cfg.copy()
        for k, v in cfg['tasks'].items():
            v._cfg = cfg_cp


    # Recursive load
    if cfg.load:
        cfg_path = os.path.dirname(path)
        for item in cfg.load:
            if item.get('file'):
                rel_path = item.file
                child_path = os.path.join(cfg_path, item.file)
            elif item.get('pkg'):
                rel_path = item.pkg
                child_path = os.path.join(PKG_DIR, item.pkg)

            if item.get('as'):
                child_prefix = item['as']
            else:
                child_prefix, _ = os.path.splitext(rel_path)

            child_cfg = load_cfg(child_path, child_prefix)
            key_fn = lambda x: '/'.join([child_prefix, x])
            for section in load_sections:
                if not section in child_cfg:
                    continue
                items = {key_fn(k): v for k, v in child_cfg[section].items()}
                cfg[section].update(items)
    return cfg


def load_cli(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('names',  nargs='*',
                        help='Hosts and commands to run them on')
    parser.add_argument('-c', '--config', default='bd.yaml',
                        help='Config file')
    parser.add_argument('-R', '--run', nargs='*', default=[],
                        help='Run remote task')
    parser.add_argument('-L', '--run-local', nargs='*', default=[],
                        help='Run local task')
    parser.add_argument('-P', '--run-python', nargs='*', default=[],
                        help='Run python task')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Do not run actual tasks, just print them')
    parser.add_argument('-e', '--env', nargs='*', default=[],
                        help='Add value to execution environment '
                        '(ex: -e foo=bar "name=John Doe")')
    parser.add_argument('-s', '--sudo', default='auto',
                        help='Enable sudo (auto|yes|no')
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='Increase verbosity')
    parser.add_argument('-q', '--quiet', action='count',
                        default=0, help='Decrease verbosity')
    parser.add_argument('-n', '--no-color', action='store_true',
                        help='Disable colored logs')
    parser.add_argument('-i', '--info', action='store_true',
                        help='Print info')
    cli = parser.parse_args(args=args)
    cli = ObjectDict(vars(cli))

    # Load config
    cfg = load_cfg(cli.config)
    cli.cfg = cfg
    cli.update(get_hosts_and_tasks(cli, cfg))

    # Transformt env string into dict
    cli.env = dict(e.split('=') for e in cli.env)
    return cli

def get_hosts_and_tasks(cli, cfg):
    # Make sure we don't have overlap between hosts and tasks
    items = list(cfg.networks) + list(cfg.tasks)
    msg = 'Name collision between tasks and networks'
    assert len(set(items)) == len(items), msg

    # Build task list
    tasks = []
    networks = []
    for name in cli.names:
        if name in cfg.networks:
            host = cfg.networks[name]
            networks.append(host)
        elif name in cfg.tasks:
            task = cfg.tasks[name]
            tasks.append(task)
        else:
            msg = 'Name "%s" not understood' % name
            matches = spell(cfg.networks, name) | spell(cfg.tasks, name)
            if matches:
                msg += ', try: %s' % ' or '.join(matches)
            raise ByrdException (msg)

    # Collect custom tasks from cli
    customs = []
    for cli_key in ('run', 'run_local', 'run_python'):
        cmd_key = cli_key.rsplit('_', 1)[-1]
        customs.extend('%s: %s' % (cmd_key, ck) for ck in cli[cli_key])
    for custom_task in customs:
        task = Task.parse(yaml_load(custom_task))
        task.desc = 'Custom command'
        tasks.append(task)

    hosts = list(chain.from_iterable(n.hosts for n in networks))

    return dict(hosts=hosts, tasks=tasks)


def info(cli):
    formatter = Formatter()
    for name, attr in cli.cfg.tasks.items():
        kind = 'remote'
        if attr.python:
            kind = 'python'
        elif attr.local:
            kind = 'local'
        elif attr.multi:
            kind = 'multi'
        elif attr.send:
            kind = 'send file'

        print(f'{name} [{kind}]:\n\tDescription: {attr.desc}')

        values = []
        for v in attr.values():
            if isinstance(v, list):
                values.extend(v)
            elif isinstance(v, dict):
                values.extend(v.values())
            else:
                values.append(v)
        values = filter(lambda x: isinstance(x, str), values)
        fmt_fields = [i[1] for v in values for i in formatter.parse(v) if i[1]]
        if fmt_fields:
            variables = ', '.join(sorted(set(fmt_fields)))
        else:
            variables = None

        if variables:
            print(f'\tVariables: {variables}')


def main():
    cli = None
    try:
        cli = load_cli()
        if not cli.no_color:
            enable_logging_color()
        cli.verbose = max(0, 1 + cli.verbose - cli.quiet)
        level = ['WARNING', 'INFO', 'DEBUG'][min(cli.verbose, 2)]
        log_handler.setLevel(level)
        logger.setLevel(level)

        if cli.info:
            info(cli)
            return

        base_env = Env(
            cli.env, # Highest-priority
            cli.cfg.get('env'),
            os.environ, # Lowest
        )
        for task in cli.tasks:
            run_batch(task, cli.hosts, cli, base_env)
    except ByrdException as e:
        if cli and cli.verbose > 2:
            raise
        abort(str(e))


if __name__ == '__main__':
    main()
