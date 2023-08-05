from noora.io.File import File
from noora.io.Files import Files
from noora.version.Version import Version


class VersionLoader(object):
    def __init__(self, versions):
        self.__versions = versions

    def load(self, properties):
        alter = File(properties.get("alter.dir"))
        if alter.exists():
            files = Files()
            for version in files.list(alter):
                self.__versions.add(Version(version.tail()))

        create = File(properties.get("create.dir"))
        if create.exists():
            self.__versions.add(Version(properties.get("default_version")))
