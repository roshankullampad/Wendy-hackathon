"""Package marker for event planner."""

import os
import sys

# Ensure workspace root is in sys.path when this module is imported
_WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)
