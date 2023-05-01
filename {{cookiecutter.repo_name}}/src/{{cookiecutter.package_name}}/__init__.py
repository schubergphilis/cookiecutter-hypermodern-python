"""{{cookiecutter.friendly_name}}."""
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version


# This is a fallback for using `importlib.metadata`.
# DO NOT modify the version manually - it is updated by python-semantic-release
__static_version = "{{cookiecutter.version}}"

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = __static_version
