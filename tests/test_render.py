import json

from gitpulse.render import (
    render_bar_chart,
    render_csv,
    render_json,
    render_markdown,
    render_table,
)

OVERVIEW = {
    "total_commits": 2,
    "total_authors": 1,
    "total_insertions": 10,
    "total_deletions": 2,
    "longest_streak_days": 2,
}
AUTHORS = {
    "Alice": {"commits": 2, "insertions": 10, "deletions": 2, "files": {"a.txt"}},
}


def test_render_table_contains_key_figures():
    output = render_table(OVERVIEW, AUTHORS)
    assert "Total commits:     2" in output
    assert "Alice" in output


def test_render_markdown_has_table_header():
    output = render_markdown(OVERVIEW, AUTHORS)
    assert "| Author | Commits | Insertions | Deletions |" in output
    assert "Alice" in output


def test_render_json_round_trips():
    output = render_json(OVERVIEW, AUTHORS)
    parsed = json.loads(output)
    assert parsed["overview"]["total_commits"] == 2
    assert parsed["authors"]["Alice"]["files"] == ["a.txt"]


def test_render_bar_chart_scales_to_width():
    chart = render_bar_chart({"Mon": 5, "Tue": 10}, width=10)
    lines = chart.split("\n")
    assert lines[1].count("#") == 10
    assert lines[0].count("#") == 5


def test_render_bar_chart_empty():
    assert render_bar_chart({}) == ""


def test_render_csv_has_header_and_author_row():
    output = render_csv(OVERVIEW, AUTHORS)
    lines = output.split("\r\n")
    assert lines[0] == "author,commits,insertions,deletions,files_touched"
    assert lines[1] == "Alice,2,10,2,1"


def test_render_csv_includes_totals_footer():
    output = render_csv(OVERVIEW, AUTHORS)
    assert "total_commits,2" in output
    assert "longest_streak_days,2" in output
