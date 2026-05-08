import json
import shutil
import subprocess
from pathlib import Path


class GitMetaInfoError(Exception):
    pass


class GitNotInstalledError(GitMetaInfoError):
    pass


class NotGitRepositoryError(GitMetaInfoError):
    pass


def _run_git_command(args):
    if shutil.which("git") is None:
        raise GitNotInstalledError(
            "git executable was not found in PATH"
        )

    try:
        return (
            subprocess.check_output(
                ["git", *args],
                stderr=subprocess.STDOUT,
            )
            .decode()
            .strip()
        )

    except subprocess.CalledProcessError as e:
        output = e.output.decode().lower()

        if "not a git repository" in output:
            raise NotGitRepositoryError(
                "current directory is not a git repository"
            ) from e

        raise GitMetaInfoError(output) from e


def get_git_data():
    branch = _run_git_command(
        ["rev-parse", "--abbrev-ref", "HEAD"]
    )

    detached = branch == "HEAD"

    return {
        "hash": _run_git_command(
            ["rev-parse", "HEAD"]
        ),
        "short_hash": _run_git_command(
            ["rev-parse", "--short", "HEAD"]
        ),
        "author_name": _run_git_command(
            ["log", "-1", "--pretty=%an"]
        ),
        "author_email": _run_git_command(
            ["log", "-1", "--pretty=%ae"]
        ),
        "author_date": _run_git_command(
            ["log", "-1", "--pretty=%ai"]
        ),
        "author_date_iso": _run_git_command(
            ["log", "-1", "--pretty=%aI"]
        ),
        "committer_name": _run_git_command(
            ["log", "-1", "--pretty=%cn"]
        ),
        "committer_email": _run_git_command(
            ["log", "-1", "--pretty=%ce"]
        ),
        "committer_date": _run_git_command(
            ["log", "-1", "--pretty=%ci"]
        ),
        "committer_date_iso": _run_git_command(
            ["log", "-1", "--pretty=%cI"]
        ),
        "message": _run_git_command(
            ["log", "-1", "--pretty=%B"]
        ),
        "branch": None if detached else branch,
        "detached_head": detached,
    }


def write_git_metainfo(output="git-metainfo.json"):
    data = get_git_data()

    output_path = Path(output)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    return output_path
