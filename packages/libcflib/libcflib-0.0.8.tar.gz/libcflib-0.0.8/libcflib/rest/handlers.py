"""REST Specification request handlers."""
from libcflib import __version__ as VERSION
from libcflib.rest.request_handler import RequestHandler


NON_EMPTY_STR = {"type": "string", "empty": False, "required": True}


class Artifact(RequestHandler):
    """Gets an artifact's data"""

    route = "/artifact"
    schema = {
        "pkg": NON_EMPTY_STR.copy(),
        "channel": NON_EMPTY_STR.copy(),
        "arch": NON_EMPTY_STR.copy(),
        "name": NON_EMPTY_STR.copy(),
    }

    def get(self, *args, **kwargs):
        """GETs an artifact."""
        a = self.db.get_artifact(**self.data)
        self.write(a)


class Packages(RequestHandler):
    """Gets the packages dictionary"""

    route = "/packages"
    schema = {}

    def get(self, *args, **kwargs):
        """GETs the packages dict"""
        self.write(self.db.packages)


class Package(RequestHandler):
    """Gets the packages dictionary"""

    route = "/package"
    schema = {"pkg": NON_EMPTY_STR.copy()}

    def get(self, *args, **kwargs):
        """GETs the packages dict"""
        self.write(self.db.packages[self.data("pkg")])


class Search(RequestHandler):
    """Performs a database search"""
    route = "/search"
    schema = {
        "query": NON_EMPTY_STR.copy(),
        "page_num": {"type": "integer", "required": False, 'min': 1},
        "page_size": {"type": "integer", "required": False, 'min': 1},
    }
    defaults = {
        "page_num": 1,
        "page_size": 10,
    }
    converters = {
        "page_num": int,
        "page_size": int,
    }

    def get(self, *args, **kwargs):
        res = {"results": list(self.db.search(**self.data))}
        res.update(self.data)
        self.write(res)


class Version(RequestHandler):
    """Gets the version of libcflib"""

    route = "/version"
    schema = {}

    def get(self, *args, **kwargs):
        """GETs the libcflib version"""
        self.write({"version": VERSION})
