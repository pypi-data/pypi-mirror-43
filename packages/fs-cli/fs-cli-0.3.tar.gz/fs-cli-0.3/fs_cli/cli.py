import click

from fs_cli.commands import InitprojectCommand
from fs_cli.config import TEMPLATES


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_code', required=True)
@click.argument('project_name', required=True)
@click.option('--ssh', '-s', is_flag=True, help='Connect to git via SSH')
@click.option('--directory', '-d', help='Project directory path')
@click.option('--repo', '-r', help='Template repository')
def initproject(project_name, project_code, ssh, directory, repo):
    if repo:
        template = repo
    else:
        template = TEMPLATES[project_code].get('ssh' if ssh else 'http')

    InitprojectCommand(
        git_url=template,
        project_name=project_name,
        dist_dir=directory,
    ).run()


def main():
    cli()
