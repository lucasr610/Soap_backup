import os
from pathlib import Path


def get_soap_root() -> Path:
    """Return the Soap root directory honoring $SOAP_ROOT."""
    env = os.getenv("SOAP_ROOT")
    return Path(env).expanduser() if env else Path.home() / "Soap"
