try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

try:
    __version__ = metadata.version("pyadsapi")
except metadata.PackageNotFoundError:
    # package is not installed
    pass
