import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Define the vertices of the orthorhombic unit cell
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])
orth_faces = [
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom face
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # top face
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # front face
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # back face
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # right face
    [vertices[0], vertices[3], vertices[7], vertices[4]]   # left face
]
# Define the edges of the orthorhombic unit cell
edges = [
    [vertices[0], vertices[1]], [vertices[1], vertices[2]], [vertices[2], vertices[3]], [vertices[3], vertices[0]],
    [vertices[4], vertices[5]], [vertices[5], vertices[6]], [vertices[6], vertices[7]], [vertices[7], vertices[4]],
    [vertices[0], vertices[4]], [vertices[1], vertices[5]], [vertices[2], vertices[6]], [vertices[3], vertices[7]]
]
#-------------------------------------------------------------
# therhe
# tetra_vertices = np.array([
#     [0, 0, 0],   # Vertex on x=0 plane
#     [0, 0.5, 0],   # Vertex on x=0 plane
#     [0.5, 0.25, 0.5], # Vertex symmetrical about x=0 plane
#     [-0.5, 0.25, 0.5] # Vertex symmetrical about x=0 plane
# ])

tetra_vertices1 = np.array([[ 1.11022302e-16, 1.41421356e+00, 1.00000000e+00],
 [-1.11022302e-16, -1.41421356e+00, 1.00000000e+00],
 [-1.41421356e+00, 1.11022302e-16, -1.00000000e+00],
 [ 1.41421356e+00, -1.11022302e-16, -1.00000000e+00]])

tetra_vertices = tetra_vertices1/5.0
tetra_vertices += 0.1

y_shift = 0.3
z_shift = 0.3
tetra_vertices[0][1] += y_shift
tetra_vertices[1][1] += y_shift
tetra_vertices[2][1] += y_shift
tetra_vertices[3][1] += y_shift

tetra_vertices[0][2] += z_shift
tetra_vertices[1][2] += z_shift
tetra_vertices[2][2] += z_shift
tetra_vertices[3][2] += z_shift
#----------------------------------
tetra_vertices2 = tetra_vertices.copy()
tetra_vertices2 += 0.5
tetra_vertices2 += 0.1

# tetra_vertices2[0][0] += 0.5
# tetra_vertices2[1][0] += 0.5
# tetra_vertices2[2][0] += 0.5
# tetra_vertices2[0][2] += 0.5
# tetra_vertices2[1][2] += 0.5
# tetra_vertices2[2][2] += 0.5
# tetra_vertices2[0][1] += 0.5
# tetra_vertices2[1][1] += 0.5
# tetra_vertices2[2][1] += 0.5

# Define the faces of the second tetrahedron
tetra_faces = [
    [tetra_vertices[0], tetra_vertices[1], tetra_vertices[2]],
    [tetra_vertices[0], tetra_vertices[1], tetra_vertices[3]],
    [tetra_vertices[0], tetra_vertices[2], tetra_vertices[3]],
    [tetra_vertices[1], tetra_vertices[2], tetra_vertices[3]]
]
# Define the plane faces (since we need a single face)
plane_face = [tetra_vertices[0], tetra_vertices[1], tetra_vertices[3], tetra_vertices[2]]

tetra_faces2 = [
    [tetra_vertices2[0], tetra_vertices2[1], tetra_vertices2[2]],
    [tetra_vertices2[0], tetra_vertices2[1], tetra_vertices2[3]],
    [tetra_vertices2[0], tetra_vertices2[2], tetra_vertices2[3]],
    [tetra_vertices2[1], tetra_vertices2[2], tetra_vertices2[3]]
]
plane_face2 = [tetra_vertices2[0], tetra_vertices2[1], tetra_vertices2[3], tetra_vertices2[2]]



# Define the plane x=0
plane_x0 = [
    vertices[0], vertices[3], vertices[7], vertices[4]
]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the edges of the orthorhombic unit cell
for edge in edges:
    ax.plot3D(*zip(*edge), color='b')

# Plot the plane x=0
# ax.add_collection3d(Poly3DCollection([plane_x0], facecolors='yellow', linewidths=1, alpha=0.25))

#-------------------
# Plot the faces of the tetrahedron
ax.add_collection3d(Poly3DCollection(tetra_faces, facecolors='cyan', linewidths=1, edgecolors='black', alpha=0.15))
ax.add_collection3d(Poly3DCollection(orth_faces, facecolors='yellow', linewidths=1, edgecolors='black', alpha=0.25))
# Plot the vertices of the tetrahedron and label them
# for vertex in vertices:
#     ax.scatter(*vertex, color='k')
    # ax.text(*vertex, f'({vertex[0]}, {vertex[1]}, {vertex[2]})', color='black')

# Plot the faces of the tetrahedron
ax.add_collection3d(Poly3DCollection(tetra_faces2, facecolors='cyan', linewidths=1, edgecolors='grey', alpha=0.1, linestyles='dashed'))

# Plot the vertices of the tetrahedron and label them
# for vertex in vertices:
#     ax.scatter(*vertex, color='k')
    # ax.text(*vertex, f'({vertex[0]}, {vertex[1]}, {vertex[2]})', color='black')
#-----------------------

# Set the aspect ratio
ax.set_box_aspect([1, 1, 1])

# Set the axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.savefig('output.png', format='png', dpi=600)
# Show the plot
plt.show()