# distutils: language = c++

from cpython.mem cimport PyMem_Malloc, PyMem_Free
cimport DracoPy
import struct

class DracoMesh(object):
    def __init__(self, cython_mesh_struct, encoding_options=None):
        self.cython_mesh_struct = cython_mesh_struct
        self.encoding_options = encoding_options
    
    @property
    def points(self):
        return self.cython_mesh_struct['points']

    @property
    def faces(self):
        return self.cython_mesh_struct['faces']

    @property
    def normals(self):
        return self.cython_mesh_struct['normals']

class EncodingOptions(object):
    def __init__(self, quantization_bits, quantization_range, quantization_origin):
        self.quantization_bits = quantization_bits
        self.quantization_range = quantization_range
        self.quantization_origin = quantization_origin


def encode_mesh_to_buffer(points, faces, quantization_bits=14, compression_level=1, quantization_range=0, quantization_origin=None, encode_custom_options=False):
    cdef float* quant_origin = NULL
    num_dims = 3
    if quantization_origin is not None:
        quant_origin = <float *>PyMem_Malloc(sizeof(float) * num_dims)
        for dim in range(num_dims):
            quant_origin[dim] = quantization_origin[dim]
    encodedMesh = DracoPy.encode_mesh(points, faces, quantization_bits, compression_level, quantization_range, quant_origin)
    if quant_origin != NULL:
        PyMem_Free(quant_origin)
    if encode_custom_options:
        encoded_floats = bytes([0, 0, 0, 0])
        if quantization_origin is not None:
            encoded_floats = struct.pack('%sf' % (num_dims + 1), quantization_range, *quantization_origin)
        return b''.join([bytes([quantization_bits]), encoded_floats, bytes(encodedMesh)])
    else:
        return bytes(encodedMesh)

def decode_buffer_to_mesh(buffer):
    cython_mesh_struct = DracoPy.decode_buffer(buffer, len(buffer))
    return DracoMesh(cython_mesh_struct)

def decode_buffer_with_encoded_options_to_mesh(buffer):
    quantization_bits = buffer[0]
    quantization_range = struct.unpack("=f", buffer[1:5])
    quantization_origin = []
    for dim in range(3):
        quantization_origin.append(struct.unpack("=f", buffer[5+dim*4:9+dim*4]))
    cython_mesh_struct = DracoPy.decode_buffer(buffer[17:], len(buffer[17:]))
    return DracoMesh(cython_mesh_struct, EncodingOptions(quantization_bits, quantization_range, quantization_origin))
    


