import io
import pathlib

import decompiler
from unrpyc import Context, get_ast


def renlib_decompile_rpyc(filepath: str, try_harder=False):
    file = pathlib.Path(filepath)

    ast = get_ast(file, try_harder, Context())

    strOutput = io.StringIO()

    options = decompiler.Options(log=lambda: print(""), translator=None, init_offset=None, sl_custom_names=None)
    decompiler.pprint(strOutput, ast, options)

    return strOutput.getvalue()
