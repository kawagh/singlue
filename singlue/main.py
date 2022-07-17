import ast
import sys
import argparse
from pathlib import Path
from typing import Optional


def resolve_fn_or_cls(name: str, src_ast: ast.Module) -> Optional[ast.stmt]:
    found_fn_or_cls = next(
        filter(lambda x: getattr(x, "name") == name, src_ast.body), None
    )
    return found_fn_or_cls


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="file to glue")
    parser.add_argument(
        "-s",
        "--show_before",
        default=False,
        action="store_true",
        help="output source (before integrating) to standard error",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    assert Path(args.source).exists()
    with open(Path(args.source)) as f:
        res = ast.parse(source=f.read())

    if args.show_before:
        print("====================================", file=sys.stderr)
        for stmt in res.body:
            print(ast.unparse(stmt), file=sys.stderr)
        print("====================================", file=sys.stderr)

    for stmt in res.body:
        if isinstance(stmt, ast.ImportFrom):
            # TODO replace import part to resolved code
            for func_or_cls in stmt.names:
                if not Path(args.source).parent.joinpath(f"{stmt.module}.py").exists():
                    # skip standard library (Example:`from math import sin`)
                    continue
                with open(Path(args.source).parent / f"{stmt.module}.py") as f:
                    res = ast.parse(source=f.read())
                    found_fn_or_cls = resolve_fn_or_cls(func_or_cls.name, res)
                    if found_fn_or_cls:
                        print(ast.unparse(found_fn_or_cls))
                    else:
                        raise RuntimeError(f"cannot find {func_or_cls.name}")
        else:
            print(ast.unparse(stmt))
    # TODO resolve,duplicate import


if __name__ == "__main__":
    main()
