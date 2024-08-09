import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Define the vertices of a tetrahedron
# vertices = np.array([
#     [1, 1, 1],
#     [-1, -1, 1],
#     [-1, 1, -1],
#     [1, -1, -1]
# ])

# vertices = np.array([
#     [1, 1, 1],
#     [-1, -1, 1],
#     [-1, 1, -1],
#     [1, -1, -1]
# ])

vertices = np.array([[ 1.11022302e-16, 1.41421356e+00, 1.00000000e+00],
 [-1.11022302e-16, -1.41421356e+00, 1.00000000e+00],
 [-1.41421356e+00, 1.11022302e-16, -1.00000000e+00],
 [ 1.41421356e+00, -1.11022302e-16, -1.00000000e+00]])

# Define the faces of the tetrahedron
faces = [
    [vertices[0], vertices[1], vertices[2]],
    [vertices[0], vertices[1], vertices[3]],
    [vertices[0], vertices[2], vertices[3]],
    [vertices[1], vertices[2], vertices[3]]
]

# Define the corners of the plane
plane_vertices = np.array([
    [-1, -1, 1],
    [1, 1, -1],
    [-1, -1, -1],
    [1, 1, 1]
])

# plane_vertices = np.array([
#     [-1, -1, -1],
#     [-1, -1, 1],
#     [1, 1, -1],
#     [1, 1, 1]
# ])

# Define the plane faces (since we need a single face)
plane_face = [plane_vertices[0], plane_vertices[1], plane_vertices[3], plane_vertices[2]]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the faces of the tetrahedron
ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='black', alpha=0.15))

# Plot the vertices of the tetrahedron and label them
for vertex in vertices:
    ax.scatter(*vertex, color='k')
    # ax.text(*vertex, f'({vertex[0]}, {vertex[1]}, {vertex[2]})', color='black')

# Plot the plane
# ax.add_collection3d(Poly3DCollection([plane_face], facecolors='red', linewidths=1, edgecolors='red', alpha=0.25))
# ax.add_collection3d(Poly3DCollection([plane_face], facecolors='red', linewidths=1, alpha=0.25))
# Plot the vertices of the plane and label them
# for vertex in plane_vertices:
#     ax.scatter(*vertex, color='k')
    # ax.text(*vertex, f'({vertex[0]}, {vertex[1]}, {vertex[2]})', color='black')

# # Plot a line
# line_start = [0, 0, -1]
# line_end = [0, 0, 1]
# ax.plot([line_start[0], line_end[0]], [line_start[1], line_end[1]], [line_start[2], line_end[2]], color='blue')

# Set the aspect ratio
ax.set_box_aspect([1, 1, 1])

# Set the axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Hide the axes
# ax.set_xticks([])
# ax.set_yticks([])
# ax.set_zticks([])
# ax.set_axis_off()
plt.savefig('output.png', format='png', dpi=600)
# Show the plot
plt.show()