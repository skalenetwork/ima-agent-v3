# Brand new IMA Agent, in Python

## Development

### Dependencies

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install all dependencies:

```bash
uv sync --prerelease=allow --all-extras
```

### Linting and type checking

#### Check linting/formatting issues

```bash
uv run ruff check
```

#### Check type issues

```bash
uv run mypy .
```

#### Auto-fix ruff issues (linting + formatting)

```bash
uv run ruff check --fix
```

# Format code with ruff

```bash
uv run ruff format
```
