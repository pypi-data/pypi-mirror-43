import click


@click.command()
def clone():
    """Clone all repos"""
    from octohot.cli.config import repositories
    for repo in repositories:
        click.echo(repo.pprint("Clone"))
        repo.clone()
