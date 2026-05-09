# git-metainfo

## Generate git metadata JSON

Output git metadata:

```bash
$ git-metainfo
{
  "hash": "40b71138b4ef89496645e377008e11eedbe207d6",
  "short_hash": "40b7113",
  "author_name": "Kevin Tran",
  "author_email": "151680+orientalperil@users.noreply.github.com",
  "author_date": "2026-05-08 22:06:47 -0700",
  "author_date_iso": "2026-05-08T22:06:47-07:00",
  "committer_name": "Kevin Tran",
  "committer_email": "151680+orientalperil@users.noreply.github.com",
  "committer_date": "2026-05-08 22:06:47 -0700",
  "committer_date_iso": "2026-05-08T22:06:47-07:00",
  "message": "Code",
  "branch": "master",
  "detached_head": false
}
```

Output to a file:

`git-metainfo --output file.json`

Use as library:

```python
from git_metainfo.core import get_git_data

data = get_git_data()
```

## Development

### Install

`poetry install`

### Install pre-commit

`pre-commit install`

### Lint and format

`ruff format && isort .`

## See also:

[Typescript version](https://github.com/orientalperil/git-metainfo-typescript)
