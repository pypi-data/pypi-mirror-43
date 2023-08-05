from typing import List

from stuffer.core import Group, Action

from stuffer import apt


class SpotifyClient(Group):
    def children(self) -> List[Action]:
        return [
            apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "931FF8E79F0876134EDDBDCCA87FF9DF48BF1C90"),
            apt.SourceList("spotify", "deb http://repository.spotify.com stable non-free"),
            apt.Install("spotify-client")
        ]
