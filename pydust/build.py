"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pathlib import Path
import sys

from pydust import buildzig
import subprocess


def build():
    """The main entry point from Poetry's build script."""
    buildzig.zig_build(["install", f"-Dpython-exe={sys.executable}", "-Doptimize=ReleaseSafe"])

def build_uv():
    """The main entry point from Poetry's build script."""

    sync_output = subprocess.run(["uv", "sync", "--no-install-projects"], check=False, capture_output=True, text=True)
    if sync_output.returncode != 0:
        print(f"Error running 'uv sync':\nstderr: {sync_output.stderr}\nstdout: {sync_output.stdout}", file=sys.stderr)
        sys.exit(1)
    output = subprocess.run(["uv", "python", "find"], check=True, capture_output=True, text=True)
    python_exe = Path(output.stdout.strip()).as_posix()
    buildzig.zig_build(["install", f"-Dpython-exe={python_exe}", "-Doptimize=ReleaseSafe"])
