import click


@click.command()
def pull():
    """Pull all repos"""
    from octohot.cli.config import repositories
    for repo in repositories:
        click.echo(repo.pprint("Pull"))
        repo.pull()
