from pathlib import Path
from subprocess import run, PIPE

from stuffer.core import Action


class Terraform(Action):
    """Install Terraform."""

    def __init__(self, version):
        super().__init__()
        self.version = version

    @staticmethod
    def _dst():
        return Path("/usr/local/bin/terraform")


    @classmethod
    def _installed_version(cls):
        if cls._dst().exists():
            return run([str(cls._dst()), '--version'], stdout=PIPE, universal_newlines=True
                       ).stdout.splitlines()[0].replace('Terraform v', '')

    def run(self):
        if not self._installed_version() == self.version:
            self._extract_net_archive(
                "https://releases.hashicorp.com/terraform/{}/terraform_{}_linux_amd64.zip".format(
                    self.version, self.version),
                self._dst().parent)
