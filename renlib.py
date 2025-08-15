import io

import decompiler
import deobfuscate
from unrpyc import Context, read_ast_from_file


def renlib_get_ast(file_bytes: io.BytesIO, try_harder=False):
    if try_harder:
        ast = deobfuscate.read_ast(file_bytes, Context())
    else:
        ast = read_ast_from_file(file_bytes, Context())
    return ast

def renlib_decompile_rpyc(file_bytes: bytes, try_harder=False):
    bytes_io = io.BytesIO()
    bytes_io.write(file_bytes)
    bytes_io.seek(0)

    ast = renlib_get_ast(bytes_io, try_harder)

    str_output = io.StringIO()

    options = decompiler.Options(log=lambda: print(""), translator=None, init_offset=None, sl_custom_names=None)
    decompiler.pprint(str_output, ast, options)

    return str_output.getvalue()
