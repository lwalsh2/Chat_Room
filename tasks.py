"""
Tasks to run through invoke
"""

from invoke import task, context

# The Sort Methods that can be called:
sort_methods = ['bubble', 'heap', 'merge', 'quick', 'tree']

@task()
def clean(cmd: context.Context) -> None:
    """Cleans artifacts from the project. Can be called with `invoke clean`.
    Args:
        cmd (context.Context): Context invoke passes to run commands
    Returns:
        None
    """
    cmd.run('rm -rf bin')


@task(clean)
def build(cmd: context.Context) -> None:
    """Builds the project. Can be called with `invoke build`.
    Args:
        cmd (context.Context): Context invoke passes to run commands
    Returns:
        None
    """
    cmd.run('mkdir bin;cmake -B bin -S c_implementation;cd bin;make')

