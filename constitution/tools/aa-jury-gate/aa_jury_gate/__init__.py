"""aa-jury-gate — multi-cognition jury gate enforcement CLI."""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("aa-jury-gate")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
