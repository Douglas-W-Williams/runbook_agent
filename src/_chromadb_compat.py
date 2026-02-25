"""Compatibility shim for ChromaDB on Python 3.14+.

Python 3.14 breaks Pydantic v1's type inference for some fields in
ChromaDB's Settings class. This module patches the issue before
ChromaDB is imported. Import this module before importing chromadb.
"""

import sys

if sys.version_info >= (3, 14):
    import pydantic.v1.fields as _fields

    _original = _fields.ModelField._set_default_and_type

    def _patched(self):
        try:
            _original(self)
        except Exception:
            import typing
            self.outer_type_ = typing.Optional[typing.Any]
            self.type_ = typing.Any
            self.required = False

    _fields.ModelField._set_default_and_type = _patched
