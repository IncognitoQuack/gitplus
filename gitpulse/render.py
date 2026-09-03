import csv
import io
import json


def render_bar_chart(data: dict, width: int = 30) -> str:
    if not data:
        return ""
    max_value = max(data.values()) or 1
    lines = []
    for label, value in data.items():
        bar_len = int((value / max_value) * width)
        bar = "#" * bar_len
        lines.append(f"{str(label):>4} | {bar} {value}")
    return "\n".join(lines)


def render_table(overview: dict, authors: dict) -> str:
    lines = [
        "gitpulse summary",
        "-" * 40,
        f"Total commits:     {overview['total_commits']}",
        f"Total authors:     {overview['total_authors']}",
        f"Total insertions:  {overview['total_insertions']}",
        f"Total deletions:   {overview['total_deletions']}",
        f"Longest streak:    {overview['longest_streak_days']} day(s)",
        "",
        "By author",
        "-" * 40,
    ]
    header = f"{'Author':<20}{'Commits':>10}{'Insert':>10}{'Delete':>10}"
    lines.append(header)
    for author, data in sorted(authors.items(), key=lambda kv: kv[1]["commits"], reverse=True):
        lines.append(
            f"{author:<20}{data['commits']:>10}{data['insertions']:>10}{data['deletions']:>10}"
        )
    return "\n".join(lines)


def render_markdown(overview: dict, authors: dict) -> str:
    lines = [
        "# gitpulse summary",
        "",
        f"- **Total commits:** {overview['total_commits']}",
        f"- **Total authors:** {overview['total_authors']}",
        f"- **Total insertions:** {overview['total_insertions']}",
        f"- **Total deletions:** {overview['total_deletions']}",
        f"- **Longest streak:** {overview['longest_streak_days']} day(s)",
        "",
        "## By author",
        "",
        "| Author | Commits | Insertions | Deletions |",
        "|---|---|---|---|",
    ]
    for author, data in sorted(authors.items(), key=lambda kv: kv[1]["commits"], reverse=True):
        row = f"| {author} | {data['commits']} | {data['insertions']} | {data['deletions']} |"
        lines.append(row)
    return "\n".join(lines)


def render_csv(overview: dict, authors: dict) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["author", "commits", "insertions", "deletions", "files_touched"])
    for author, data in sorted(authors.items(), key=lambda kv: kv[1]["commits"], reverse=True):
        writer.writerow(
            [author, data["commits"], data["insertions"], data["deletions"], len(data["files"])]
        )
    writer.writerow([])
    writer.writerow(["total_commits", overview["total_commits"]])
    writer.writerow(["total_authors", overview["total_authors"]])
    writer.writerow(["total_insertions", overview["total_insertions"]])
    writer.writerow(["total_deletions", overview["total_deletions"]])
    writer.writerow(["longest_streak_days", overview["longest_streak_days"]])
    return buffer.getvalue().strip("\n")


def render_json(overview: dict, authors: dict) -> str:
    payload = {
        "overview": overview,
        "authors": {
            name: {**data, "files": sorted(data["files"])}
            for name, data in authors.items()
        },
    }
    return json.dumps(payload, indent=2)
