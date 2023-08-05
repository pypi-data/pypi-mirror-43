import os
import shutil
import stat
from abc import abstractmethod
from tempfile import TemporaryDirectory

import click
from git import Git, Repo
from jinja2 import Template


class BaseCommand:
    @abstractmethod
    def run(self):
        pass


class InitprojectCommand(BaseCommand):

    PROJECT_KEY_NAME = 'project_name'

    def __init__(self, git_url=None, project_name=None,
                 project_key_name=None, dist_dir=None) -> None:
        self.project_key_name = project_key_name or self.PROJECT_KEY_NAME
        self.project_name = project_name
        self.git_url = git_url
        self.dist_dir = dist_dir or os.path.join(os.getcwd(), project_name)

    def generate_by_template(self, template_dir):
        if not os.path.exists(self.dist_dir):
            os.mkdir(self.dist_dir)
        base_path = template_dir
        for root, dirs, files in os.walk(template_dir):
            path_rest = os.path.relpath(root, base_path)
            relative_dir = path_rest.replace(self.project_key_name, self.project_name)
            if relative_dir:
                target_dir = os.path.join(self.dist_dir, relative_dir)
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)
            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = os.path.join(root, filename)
                new_path = os.path.join(self.dist_dir, relative_dir,
                                        filename.replace(self.project_key_name, self.project_name))
                if os.path.exists(new_path):
                    raise OSError(
                        'File exists: {}'.format(os.path.normpath(new_path))
                    )
                with open(old_path, 'r', encoding='utf-8') as template_file:
                    content = template_file.read()
                template = Template(content)
                content = template.render(**{self.project_key_name: self.project_name})
                with open(new_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(content)
                shutil.copymode(old_path, new_path)
                try:

                    self.make_writeable(new_path)
                except OSError:
                    click.echo(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path)

    def make_writeable(self, filename):
        if not os.access(filename, os.W_OK):
            st = os.stat(filename)
            new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
            os.chmod(filename, new_permissions)

    def run(self):
        with TemporaryDirectory() as tmpdir:
            Git(tmpdir).clone(self.git_url)
            repo_dir_name, _ = os.path.splitext(self.git_url)
            self.generate_by_template(os.path.join(tmpdir, os.path.basename(repo_dir_name)))
            Repo.init(self.dist_dir)
