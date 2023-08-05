import os
import DracoPy

with open(os.path.join('./draco/javascript/example/models/bunny.drc'), 'rb') as draco_file:
  file_content = draco_file.read()
  mesh_object = DracoPy.decode_buffer_to_mesh(file_content)
  print('number of points: {0}'.format(len(mesh_object.points)))
  print('number of faces: {0}'.format(len(mesh_object.faces)))
