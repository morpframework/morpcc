from RestrictedPython import compile_restricted, safe_builtins, safe_globals
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import (
    full_write_guard,
    guarded_iter_unpack_sequence,
    safer_getattr,
)


def default_inplacevar(op, x, y):
    if op == "+=":
        return x + y
    raise Exception("{} operator is not allowed".format(op))


def get_restricted_function(bytecode, name, local_vars=None):
    local_vars = local_vars or {}
    glob = safe_globals.copy()
    glob["dir"] = dir
    glob["_getiter_"] = default_guarded_getiter
    glob["_getitem_"] = default_guarded_getitem
    glob["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
    glob["_write_"] = full_write_guard
    glob["_inplacevar_"] = default_inplacevar
    glob["getattr"] = safer_getattr
    glob["enumerate"] = enumerate
    exec(bytecode, glob, local_vars)
    return local_vars[name]
