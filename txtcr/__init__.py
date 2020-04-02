# Decoding
from txtcr.core.decode import decode as _decode
from txtcr.core.encode import encode as _encode

# Types and file manager
from txtcr.core.types import *
from txtcr.core.file_manager import FileManager

# Classes built for inheritance
from txtcr.util.inheritance_classes import Param

# Requests
from .requests import requete


# Decoder
def decode(data, **ops):
    return _decode(data, **ops)


# Encoder
def encode(data, **ops):
    return _encode(data, **ops)


# File
file = FileManager
