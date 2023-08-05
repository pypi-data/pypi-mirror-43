# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import io
import shutil
import subprocess
import tarfile
from tempfile import NamedTemporaryFile, mkdtemp
from zipfile import ZipFile

import os
import pytest
from testfixtures import LogCapture

from gcdt import utils


# http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/?in=user-97991
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def create_tempfile(contents, dir=None, suffix=""):
    """Helper to create a named temporary file with contents.
    Note: caller has responsibility to clean up the temp file!

    :param contents: define the contents of the temporary file
    :param dir: as for mkstemp
    :param suffix: as for mkstemp
    :return: filename of the temporary file
    """

    # helper to create a named temp file
    tf = NamedTemporaryFile(delete=False, dir=dir, suffix=suffix)
    with open(tf.name, 'w') as tfile:
        tfile.write(contents)

    return tf.name


def get_size(start_path='.'):
    """Accumulate the size of the files in the folder.

    :param start_path:
    :return: size
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


# TODO find out how to automatically load the gcdt_testtools fixtures
@pytest.fixture(scope='module')  # 'function' or 'module'
def cleanup_tempfiles():
    items = []
    yield items
    # cleanup
    for i in items:
        os.unlink(i)


@pytest.fixture(scope='function')  # 'function' or 'module'
def temp_folder():
    # provide a temp folder and cleanup after test
    # this also changes into the folder and back to cwd during cleanup
    cwd = (os.getcwd())
    folder = mkdtemp()
    os.chdir(folder)
    yield folder, cwd
    # cleanup
    os.chdir(cwd)  # cd to original folder
    shutil.rmtree(folder)


@pytest.fixture(scope='function')  # 'function' or 'module'
def random_file():
    # provide a named file with some random content
    # we use random_string so it is reproducible
    filename = create_tempfile(utils.random_string())
    yield filename
    # cleanup
    os.unlink(filename)


def _dot_check():
    # Make sure the dot / graphviz tool is installed.
    # returns false if missing
    try:
        subprocess.call(["dot", "-V"])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return True
        else:
            # Something else went wrong while trying to run `npm`
            raise
    return False


# skipif helper check_preconditions
check_dot_precondition = pytest.mark.skipif(
    _dot_check(),
    reason="You need to install dot / graphviz (see gcdt docs)."
)


@pytest.fixture(scope='function')  # 'function' or 'module'
def preserve_env():
    env = os.environ['ENV']
    yield
    # cleanup
    os.environ['ENV'] = env


# pytest_vts
# python has many mocking tools for requests, we use pytest_vts because:
# * pytest
# * uses responses under the hood (good alternative would be requests-mock)
# * implementation is straight forward
@pytest.fixture
def vts(request, vts_recorder):
    """transform vts_recorder into a fixture by applying setup/teardown
    phases. If a file is there it goes into playback state."""
    def there(p):
        return os.path.abspath(os.path.join(
            os.path.dirname(request.module.__file__), p))

    # in order to avoid setting basedir for every test I patch it in
    param = getattr(request, 'param',
                    {'basedir': there('./resources/vts_cassettes'),
                     'strict_body': True})
    if param and not isinstance(param, dict):
        raise Exception('pytest-vts configuration error! Currently you can'
                        ' configure pytest-vts\'s fixtures with dicts objects')
    vts_recorder.setup(**param)
    request.addfinalizer(vts_recorder.teardown)
    return vts_recorder


def list_zip(input_zip):
    """list zip_bytes content."""
    # use string as buffer
    input_zip = ZipFile(io.BytesIO(input_zip))
    for name in input_zip.namelist():
        yield name


def read_file_from_zip(input_zip, name):
    """Read file contents of a single file from zip_bytes content."""
    # use string as buffer
    input_zip = ZipFile(io.BytesIO(input_zip))
    if name in input_zip.namelist():
        with input_zip.open(name) as zfile:
            return zfile.read()


def list_tarfile(tarfile_name):
    """list tarfile content."""
    tfile = tarfile.open(tarfile_name)
    return [t.name for t in tfile.getmembers()]


def read_file_from_tarfile(tarfile_name, name):
    """Read file contents of a single file from tarfile."""
    tfile = tarfile.open(tarfile_name)
    if name in [t.name for t in tfile.getmembers()]:
        return tfile.extractfile(name).read()


@pytest.fixture(scope='function')
def logcapture():
    """Access and control log capturing.
    """
    # http://testfixtures.readthedocs.io/en/latest/logging.html
    with LogCapture() as l:
        yield l
