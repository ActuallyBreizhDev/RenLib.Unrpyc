import io
import argparse
from shutil import ignore_patterns

import decompiler
import deobfuscate
from pathlib import Path
from unrpyc import Context, read_ast_from_file


def renlib_get_ast(in_file, try_harder=False):
    if try_harder:
        ast = deobfuscate.read_ast(in_file, Context())
    else:
        ast = read_ast_from_file(in_file, Context())
    return ast

def renlib_decompile_rpyc(input_path, output_path, try_harder=False):
    in_path = Path(input_path).resolve()
    out_path = Path(output_path).resolve()

    if not in_path.is_file():
        raise FileNotFoundError(f"Input file {in_path} does not exist")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("rb") as f_in:
        ast = renlib_get_ast(f_in, try_harder)


    with out_path.open("w", encoding="utf-8") as f_out:
        options = decompiler.Options(log=lambda: print(""), translator=None, init_offset=None, sl_custom_names=None)
        decompiler.pprint(f_out, ast, options)


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_file", type=str, help="Input file")
    ap.add_argument("output_file", type=str, help="Output file")
    ap.add_argument("--try-harder", action="store_true", help="Try harder")
    return ap.parse_args()

if __name__ == '__main__':
    args = _parse_args()

    in_path = Path(args.input_file)
    out_path = Path(args.output_file)

    if not in_path.is_absolute():
        in_path = in_path.resolve()
    if not out_path.is_absolute():
        out_path = out_path.resolve()

    renlib_decompile_rpyc(in_path, out_path, try_harder=args.try_harder)
    print(f"Decompiled: {in_path} -> {out_path}")

