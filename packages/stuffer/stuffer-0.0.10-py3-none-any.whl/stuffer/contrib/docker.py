from stuffer import apt
from stuffer import content
from stuffer.core import Group


class Docker(Group):
    def children(self):
        return [apt.Install(["apt-transport-https", "ca-certificates"]),
                apt.KeyAdd("https://download.docker.com/linux/ubuntu/gpg"),
                apt.Install('lsb-release'),
                apt.SourceList("docker",
                               content.OutputOf(
                                   'echo "deb https://apt.dockerproject.org/repo ubuntu-$(lsb_release -c -s) main"'))
                ]
