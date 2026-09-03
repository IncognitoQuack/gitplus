import subprocess
from pathlib import Path

import pytest


def _run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "sample_repo"
    repo.mkdir()
    _run(["git", "init"], cwd=repo)
    _run(["git", "config", "user.name", "Alice"], cwd=repo)
    _run(["git", "config", "user.email", "alice@example.com"], cwd=repo)

    (repo / "a.txt").write_text("hello\n")
    _run(["git", "add", "a.txt"], cwd=repo)
    _run(
        [
            "git",
            "-c",
            "user.name=Alice",
            "-c",
            "user.email=alice@example.com",
            "commit",
            "-m",
            "add a.txt",
            "--date=2024-01-01T09:00:00",
        ],
        cwd=repo,
    )

    (repo / "b.txt").write_text("world\n")
    _run(["git", "add", "b.txt"], cwd=repo)
    _run(
        [
            "git",
            "-c",
            "user.name=Bob",
            "-c",
            "user.email=bob@example.com",
            "commit",
            "-m",
            "add b.txt",
            "--date=2024-01-02T14:30:00",
        ],
        cwd=repo,
    )

    (repo / "a.txt").write_text("hello again\n")
    _run(["git", "add", "a.txt"], cwd=repo)
    _run(
        [
            "git",
            "-c",
            "user.name=Alice",
            "-c",
            "user.email=alice@example.com",
            "commit",
            "-m",
            "update a.txt",
            "--date=2024-01-03T10:15:00",
        ],
        cwd=repo,
    )

    return repo
