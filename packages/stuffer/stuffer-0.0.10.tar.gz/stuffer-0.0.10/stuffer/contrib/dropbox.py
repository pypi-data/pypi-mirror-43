from typing import List

from stuffer import apt
from stuffer import files
from stuffer.core import Group, Action


class DropboxClient(Group):
    def children(self) -> List[Action]:
        return [
            apt.KeyRecv('keyserver.ubuntu.com', '1C61A2656FB57B7E4DE0F4C1FC918B335044912E'),
            apt.SourceList('dropbox', "deb http://linux.dropbox.com/ubuntu/ xenial main"),
            apt.Install('python-gpg'),  # For verification of proprietary daemon package.
            apt.Install('dropbox'),
            files.SysctlConf('50-dropbox-watches', 'fs.inotify.max_user_watches', 524288)
        ]
