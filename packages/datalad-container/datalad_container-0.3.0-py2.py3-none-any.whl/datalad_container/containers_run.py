"""Drop-in replacement for `datalad run` for command execution in a container"""

__docformat__ = 'restructuredtext'

import logging
import os.path as op

from datalad.interface.base import Interface
from datalad.interface.base import build_doc
from datalad.support.param import Parameter
from datalad.distribution.dataset import datasetmethod
from datalad.distribution.dataset import require_dataset
from datalad.interface.utils import eval_results

from datalad.interface.run import Run
from datalad.interface.run import get_command_pwds
from datalad.interface.run import normalize_command
from datalad_container.find_container import find_container

lgr = logging.getLogger("datalad.containers.containers_run")


_run_params = dict(
    Run._params_,
    container_name=Parameter(
        args=('-n', '--container-name',),
        metavar="NAME",
        doc="""Specify the name of or a path to a known container to use 
        for execution, in case multiple containers are configured."""),
)


@build_doc
# all commands must be derived from Interface
class ContainersRun(Interface):
    # first docstring line is used a short description in the cmdline help
    # the rest is put in the verbose help and manpage
    """Drop-in replacement of 'run' to perform containerized command execution

    Container(s) need to be configured beforehand (see containers-add). If no
    container is specified and only one container is configured in the current
    dataset, it will be selected automatically. If more than one container is
    registered in the current dataset or to access containers from subdatasets,
    the container has to be specified.

    A command is generated based on the input arguments such that the
    container image itself will be recorded as an input dependency of
    the command execution in the `run` record in the git history.
    """

    _params_ = _run_params

    @staticmethod
    @datasetmethod(name='containers_run')
    @eval_results
    def __call__(cmd, container_name=None, dataset=None,
                 inputs=None, outputs=None, message=None, expand=None,
                 explicit=False, sidecar=None):
        pwd, _ = get_command_pwds(dataset)
        ds = require_dataset(dataset, check_installed=True,
                             purpose='run a containerized command execution')

        container = find_container(ds, container_name)
        image_path = op.relpath(container["path"], pwd)

        # sure we could check whether the container image is present,
        # but it might live in a subdataset that isn't even installed yet
        # let's leave all this business to `get` that is called by `run`

        cmd = normalize_command(cmd)
        # expand the command with container execution
        if 'cmdexec' in container:
            callspec = container['cmdexec']

            # Temporary kludge to give a more helpful message
            if callspec.startswith("["):
                import simplejson
                try:
                    simplejson.loads(callspec)
                except simplejson.errors.JSONDecodeError:
                    pass  # Never mind, false positive.
                else:
                    raise ValueError(
                        'cmdexe {!r} is in an old, unsupported format. '
                        'Convert it to a plain string.'.format(callspec))

            cmd = callspec.format(img=image_path, cmd=cmd)
        else:
            # just prepend and pray
            cmd = container['path'] + ' ' + cmd

        # with amend inputs to also include the container image
        inputs = (inputs or []) + [image_path]

        # fire!
        for r in Run.__call__(
                cmd=cmd,
                dataset=ds,
                inputs=inputs,
                outputs=outputs,
                message=message,
                expand=expand,
                explicit=explicit,
                sidecar=sidecar,
                on_failure="ignore",
                return_type='generator'):
            yield r
