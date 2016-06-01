import os
from invoke import task, run

WHEELHOUSE_PATH = os.environ.get('WHEELHOUSE')

@task
def install(develop=False):
    run('python setup.py develop')
    cmd = 'pip install --upgrade -r {}'.format('requirements.txt')

    if WHEELHOUSE_PATH:
        cmd += ' --no-index --find-links={}'.format(WHEELHOUSE_PATH)
    run(cmd, pty=True)

@task
def flake():
    run('flake8 .', pty=True)

@task
def test(verbose=False):
    flake()
    cmd = 'py.test --cov-report term-missing --cov pyerman tests'
    if verbose:
        cmd += ' -v'
    run(cmd, pty=True)

@task
def clean():
    run('find . | grep -E "(__pycache__|\.pyc|\.pyo|\.pyx|\.c|\.cx$)" | xargs rm -rf')
