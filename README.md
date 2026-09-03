# gitpulse

Command-line analytics for any git repository. Point it at a repo and get commit
counts, insertions/deletions per author, activity heatmaps, longest contribution
streaks, and the files that change the most — all from local git history, no
network access or third-party services required.

## Install

```bash
pip install -e .
```

Requires Python 3.10+ and git available on your `PATH`.

## Usage

```bash
gitpulse                          # analyze the current directory
gitpulse /path/to/repo            # analyze a specific repo
gitpulse --since "2024-01-01"     # only commits after a date
gitpulse --author "Jane Doe"      # filter by author
gitpulse --format json            # json / table / markdown
gitpulse --top-files 10           # show more hot files
gitpulse -o report.md --format markdown   # write a markdown report to a file
```

### Example output

```
gitpulse summary
----------------------------------------
Total commits:     128
Total authors:     4
Total insertions:  5321
Total deletions:   1904
Longest streak:    9 day(s)

By author
----------------------------------------
Author              Commits    Insert    Delete
Alice                    64      3012      1100
Bob                      40      1600       500
...

Activity by weekday
----------------------------------------
Mon  | ################## 18
Tue  | ###################### 22
Wed  | ############# 13
...

Top changed files
----------------------------------------
  42  gitpulse/cli.py
  31  gitpulse/stats.py
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap

- [ ] CSV export (`--format csv`) for spreadsheet-friendly reports
- [ ] Per-file contributor breakdown
- [ ] Configurable date bucketing for the activity chart (daily/weekly/monthly)

## License

MIT
