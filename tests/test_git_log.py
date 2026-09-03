import pytest

from gitpulse.git_log import GitLogError, get_commits, is_git_repo, parse_log_output


def test_is_git_repo_true(sample_repo):
    assert is_git_repo(str(sample_repo)) is True


def test_is_git_repo_false(tmp_path):
    assert is_git_repo(str(tmp_path)) is False


def test_get_commits_returns_all_commits_in_order(sample_repo):
    commits = get_commits(str(sample_repo))
    subjects = [c.subject for c in commits]
    assert subjects == ["update a.txt", "add b.txt", "add a.txt"]


def test_get_commits_filters_by_author(sample_repo):
    commits = get_commits(str(sample_repo), author="Bob")
    assert len(commits) == 1
    assert commits[0].author == "Bob"


def test_commit_insertions_and_deletions(sample_repo):
    commits = get_commits(str(sample_repo))
    update_commit = next(c for c in commits if c.subject == "update a.txt")
    assert update_commit.insertions == 1
    assert update_commit.deletions == 1


def test_get_commits_raises_on_non_repo(tmp_path):
    with pytest.raises(GitLogError):
        get_commits(str(tmp_path))


def test_parse_log_output_empty_string():
    assert parse_log_output("") == []


def test_parse_log_output_ignores_malformed_chunk():
    raw = "\x02badheader\x03\n"
    assert parse_log_output(raw) == []
