"""
Tasks to run through invoke
"""

from invoke import task, context

@task()
def clean(cmd: context.Context) -> None:
    """Cleans artifacts from the project. Can be called with `invoke clean`.
    Args:
        cmd (context.Context): Context invoke passes to run commands
    Returns:
        None
    """
    cmd.run('rm -rf bin build client server Definitely_Not_the_Key')


@task(clean)
def build(cmd: context.Context) -> None:
    """Builds the project. Can be called with `invoke build`.
    Args:
        cmd (context.Context): Context invoke passes to run commands
    Returns:
        None
    """
    # Build the binaries
    cmd.run('mkdir bin build;cmake -B build -S c_implementation;cd build;make')
    # Move the binaries to the project directory
    cmd.run('cp build/src/client bin/;cp build/src/server bin/')
