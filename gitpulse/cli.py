import argparse
import sys

from gitpulse.git_log import GitLogError, get_commits, is_git_repo
from gitpulse.render import (
    render_bar_chart,
    render_csv,
    render_json,
    render_markdown,
    render_table,
)
from gitpulse.stats import activity_by_weekday, author_summary, overview, top_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gitpulse", description="Git repository analytics.")
    parser.add_argument("path", nargs="?", default=".", help="Path to a git repository.")
    parser.add_argument("--since", default=None, help="Only include commits after this date.")
    parser.add_argument("--until", default=None, help="Only include commits before this date.")
    parser.add_argument("--author", default=None, help="Filter commits by author.")
    parser.add_argument(
        "--format",
        choices=["table", "json", "markdown", "csv"],
        default="table",
        help="Output format.",
    )
    parser.add_argument("--top-files", type=int, default=5, help="Number of top files to show.")
    parser.add_argument(
        "--no-activity", action="store_true", help="Hide the weekday activity chart."
    )
    parser.add_argument(
        "-o", "--output", default=None, help="Write output to a file instead of stdout."
    )
    return parser


def run(args: argparse.Namespace) -> str:
    if not is_git_repo(args.path):
        raise GitLogError(f"{args.path} is not a git repository")

    commits = get_commits(args.path, since=args.since, until=args.until, author=args.author)
    stats_overview = overview(commits)
    authors = author_summary(commits)

    if args.format == "json":
        output = render_json(stats_overview, authors)
    elif args.format == "markdown":
        output = render_markdown(stats_overview, authors)
    elif args.format == "csv":
        output = render_csv(stats_overview, authors)
    else:
        output = render_table(stats_overview, authors)
        if not args.no_activity:
            weekday_counts = activity_by_weekday(commits)
            output += "\n\nActivity by weekday\n" + "-" * 40 + "\n"
            output += render_bar_chart(weekday_counts)
        files = top_files(commits, limit=args.top_files)
        if files:
            output += "\n\nTop changed files\n" + "-" * 40 + "\n"
            output += "\n".join(f"{count:>4}  {path}" for path, count in files)

    return output


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except GitLogError as exc:
        print(f"gitpulse: error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w") as handle:
            handle.write(result + "\n")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
