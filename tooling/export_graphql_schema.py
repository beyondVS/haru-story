import argparse
from pathlib import Path

from haru_backend.api.graphql.schema import schema


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the backend GraphQL schema")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    output = Path(__file__).resolve().parents[1] / "contracts/graphql/schema.graphql"
    content = schema.as_str().rstrip() + "\n"
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != content:
            parser.exit(
                1,
                "GraphQL schema is out of date. Run npm run graphql:schema:export.\n",
            )
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
