"""List known container environments of a dataset"""

__docformat__ = 'restructuredtext'

import logging
import os.path as op

from datalad.interface.base import Interface
from datalad.interface.base import build_doc
from datalad.interface.common_opts import recursion_flag
from datalad.support.param import Parameter
from datalad.distribution.dataset import datasetmethod, EnsureDataset, Dataset
from datalad.distribution.dataset import require_dataset
from datalad.interface.utils import eval_results
from datalad.support.constraints import EnsureNone
from datalad.interface.results import get_status_dict
from datalad.coreapi import subdatasets

lgr = logging.getLogger("datalad.containers.containers_list")


@build_doc
# all commands must be derived from Interface
class ContainersList(Interface):
    # first docstring line is used a short description in the cmdline help
    # the rest is put in the verbose help and manpage
    """List containers known to a dataset
    """

    # parameters of the command, must be exhaustive
    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc="""specify the dataset to query. If no dataset is given, an
            attempt is made to identify the dataset based on the current
            working directory""",
            constraints=EnsureDataset() | EnsureNone()),
        recursive=recursion_flag,
    )

    @staticmethod
    @datasetmethod(name='containers_list')
    @eval_results
    def __call__(dataset=None, recursive=False):
        ds = require_dataset(dataset, check_installed=True,
                             purpose='list containers')

        if recursive:
            for sub in ds.subdatasets(return_type='generator'):
                subds = Dataset(sub['path'])
                if subds.is_installed():
                    for c in subds.containers_list():
                        c['name'] = sub['gitmodule_name'] + '/' + c['name']
                        yield c

        # all info is in the dataset config!
        var_prefix = 'datalad.containers.'
        containers = {}
        for var, value in ds.config.items():
            if not var.startswith(var_prefix):
                # not an interesting variable
                continue
            var_comps = var[len(var_prefix):].split('.')
            cname = var_comps[0]
            ccfgname = '.'.join(var_comps[1:])
            if not ccfgname:
                continue

            cinfo = containers.get(cname, {})
            cinfo[ccfgname] = value

            containers[cname] = cinfo

        for k, v in containers.items():
            if 'image' not in v:
                # there is no container location configured
                continue
            res = get_status_dict(
                status='ok',
                action='containers',
                name=k,
                type='file',
                path=op.join(ds.path, v.pop('image')),
                # TODO
                #state='absent' if ... else 'present'
                **v)
            yield res
