import subprocess
from unittest.mock import patch

import pytest
from git_metainfo.core import GitMetaInfoError
from git_metainfo.core import GitNotInstalledError
from git_metainfo.core import NotGitRepositoryError
from git_metainfo.core import get_git_data


def test_git_not_installed():
    with patch(
        "git_metainfo.core.shutil.which",
        return_value=None,
    ):
        with pytest.raises(GitNotInstalledError):
            get_git_data()


def test_not_git_repository():
    error = subprocess.CalledProcessError(
        128,
        ["git"],
        output=b"fatal: not a git repository",
    )

    with patch(
        "git_metainfo.core.shutil.which",
        return_value="/usr/bin/git",
    ):
        with patch(
            "git_metainfo.core.subprocess.check_output",
            side_effect=error,
        ):
            with pytest.raises(NotGitRepositoryError):
                get_git_data()


def test_detached_head():
    responses = [
        b"HEAD",
        b"abc123",
        b"abc123",
        b"John",
        b"john@john.com",
        b"2026-01-01 00:00:00 +0000",
        b"2026-01-01T00:00:00Z",
        b"John",
        b"john@john.com",
        b"2026-01-01 00:00:00 +0000",
        b"2026-01-01T00:00:00Z",
        b"test commit",
    ]

    with patch(
        "git_metainfo.core.shutil.which",
        return_value="/usr/bin/git",
    ):
        with patch(
            "git_metainfo.core.subprocess.check_output",
            side_effect=responses,
        ):
            data = get_git_data()
            print(data)

    assert data["detached_head"] is True
    assert data["branch"] is None


def test_normal_branch():
    responses = [
        b"master",
        b"abc123",
        b"abc123",
        b"John",
        b"john@john.com",
        b"2026-01-01 00:00:00 +0000",
        b"2026-01-01T00:00:00Z",
        b"John",
        b"john@john.com",
        b"2026-01-01 00:00:00 +0000",
        b"2026-01-01T00:00:00Z",
        b"test commit",
    ]

    with patch(
        "git_metainfo.core.shutil.which",
        return_value="/usr/bin/git",
    ):
        with patch(
            "git_metainfo.core.subprocess.check_output",
            side_effect=responses,
        ):
            data = get_git_data()

    assert data["detached_head"] is False
    assert data["branch"] == "master"


def test_unknown_git_error():
    error = subprocess.CalledProcessError(
        1,
        ["git"],
        output=b"some other git error",
    )

    with patch(
        "git_metainfo.core.shutil.which",
        return_value="/usr/bin/git",
    ):
        with patch(
            "git_metainfo.core.subprocess.check_output",
            side_effect=error,
        ):
            with pytest.raises(GitMetaInfoError):
                get_git_data()
