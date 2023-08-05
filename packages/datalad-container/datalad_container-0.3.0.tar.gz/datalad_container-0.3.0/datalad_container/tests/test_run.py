import os.path as op

from six import text_type

from datalad.api import Dataset
from datalad.api import create
from datalad.api import containers_add
from datalad.api import containers_run
from datalad.api import containers_list

from datalad.tests.utils import ok_clean_git
from datalad.tests.utils import assert_in
from datalad.tests.utils import assert_result_count
from datalad.tests.utils import assert_raises
from datalad.tests.utils import with_tempfile
from datalad.tests.utils import with_tree
from datalad.tests.utils import skip_if_no_network
from datalad.utils import on_windows


testimg_url = 'shub://datalad/datalad-container:testhelper'


@with_tree(tree={"dummy0.img": "doesn't matter 0",
                 "dummy1.img": "doesn't matter 1"})
def test_run_mispecified(path):
    ds = Dataset(path).create(force=True)
    ds.save(path=["dummy0.img", "dummy1.img"])
    ok_clean_git(path)

    # Abort if no containers exist.
    with assert_raises(ValueError) as cm:
        ds.containers_run("doesn't matter")
    assert_in("No known containers", text_type(cm.exception))

    # Abort if more than one container exists but no container name is
    # specified.
    ds.containers_add("d0", image="dummy0.img")
    ds.containers_add("d1", image="dummy0.img")

    with assert_raises(ValueError) as cm:
        ds.containers_run("doesn't matter")
    assert_in("explicitly specify container", text_type(cm.exception))

    # Abort if unknown container is specified.
    with assert_raises(ValueError) as cm:
        ds.containers_run("doesn't matter", container_name="ghost")
    assert_in("Container selection impossible", text_type(cm.exception))


@skip_if_no_network
@with_tempfile
@with_tempfile
def test_container_files(path, super_path):
    ds = Dataset(path).create()
    cmd = ['dir'] if on_windows else ['ls']

    # plug in a proper singularity image
    ds.containers_add(
        'mycontainer',
        url=testimg_url,
        image='righthere',
        # the next one is auto-guessed
        #call_fmt='singularity exec {img} {cmd}'
    )
    assert_result_count(
        ds.containers_list(), 1,
        path=op.join(ds.path, 'righthere'),
        name='mycontainer',
        updateurl=testimg_url)
    ok_clean_git(path)

    # now we can run stuff in the container
    # and because there is just one, we don't even have to name the container
    res = ds.containers_run(cmd)
    # container becomes an 'input' for `run` -> get request, but "notneeded"
    assert_result_count(
        res, 1, action='get', status='notneeded',
        path=op.join(ds.path, 'righthere'), type='file')
    # this command changed nothing
    assert_result_count(
        res, 1, action='add', status='notneeded', path=ds.path, type='dataset')

    # same thing as we specify the container by its name:
    res = ds.containers_run(cmd,
                            container_name='mycontainer')
    # container becomes an 'input' for `run` -> get request, but "notneeded"
    assert_result_count(
        res, 1, action='get', status='notneeded',
        path=op.join(ds.path, 'righthere'), type='file')
    # this command changed nothing
    assert_result_count(
        res, 1, action='add', status='notneeded', path=ds.path, type='dataset')

    # we can also specify the container by its path:
    res = ds.containers_run(cmd,
                            container_name=op.join(ds.path, 'righthere'))
    # container becomes an 'input' for `run` -> get request, but "notneeded"
    assert_result_count(
        res, 1, action='get', status='notneeded',
        path=op.join(ds.path, 'righthere'), type='file')
    # this command changed nothing
    assert_result_count(
        res, 1, action='add', status='notneeded', path=ds.path, type='dataset')

    # Now, test the same thing, but with this dataset being a subdataset of
    # another one:

    super_ds = Dataset(super_path).create()
    super_ds.install("sub", source=path)

    # When running, we don't discover containers in subdatasets
    with assert_raises(ValueError) as cm:
        super_ds.containers_run(cmd)
    assert_in("No known containers", text_type(cm.exception))
    # ... unless we need to specify the name
    res = super_ds.containers_run(cmd, container_name="sub/mycontainer")
    # container becomes an 'input' for `run` -> get request (needed this time)
    assert_result_count(
        res, 1, action='get', status='ok',
        path=op.join(super_ds.path, 'sub', 'righthere'), type='file')
    # this command changed nothing
    assert_result_count(
        res, 1, action='add', status='notneeded', path=super_ds.path, type='dataset')

