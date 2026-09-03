import json

from gitpulse.cli import build_parser, main, run


def test_run_table_format(sample_repo, capsys):
    args = build_parser().parse_args([str(sample_repo)])
    output = run(args)
    assert "gitpulse summary" in output
    assert "Total commits:     3" in output


def test_run_json_format(sample_repo):
    args = build_parser().parse_args([str(sample_repo), "--format", "json"])
    output = run(args)
    parsed = json.loads(output)
    assert parsed["overview"]["total_commits"] == 3


def test_run_csv_format(sample_repo):
    args = build_parser().parse_args([str(sample_repo), "--format", "csv"])
    output = run(args)
    assert output.startswith("author,commits,insertions,deletions,files_touched")


def test_main_returns_error_code_for_non_repo(tmp_path, capsys):
    exit_code = main([str(tmp_path)])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not a git repository" in captured.err


def test_main_writes_to_output_file(sample_repo, tmp_path):
    out_file = tmp_path / "report.txt"
    exit_code = main([str(sample_repo), "-o", str(out_file)])
    assert exit_code == 0
    assert "gitpulse summary" in out_file.read_text()
