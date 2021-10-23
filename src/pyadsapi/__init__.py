from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyadsapi")
except PackageNotFoundError:
    # package is not installed
    pass
