"""Process control: the app ends only its own process, never by port."""

import os
import signal


def shutdown() -> None:
    """Send SIGTERM to this process (the server running the app)."""
    os.kill(os.getpid(), signal.SIGTERM)
