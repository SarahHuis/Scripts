import bpy, bmesh
from sklearn.neighbors import KDTree

def find_next_vertex(tree, nearest_ind, selected_coordinates, loop_iteration, bm):
    bm.verts.ensure_lookup_table()
    print("Selected Coordinates Loop:", selected_coordinates)
    c = 1
    next = nearest_ind[selected_coordinates[loop_iteration], c]
    print("Next:", next)
    # Check if index is used before
    while c < (len(tree)):
        if next not in selected_coordinates:
            # Turn on vertex
            # Bm changes. So, get the coordinates equal to tree[next].
            # Then compare these coordinates to the coordinates in bm.
            # Get this index. This is the index that needs to be turned on
            next_coordinates = tree[next]
            verts = [vert.co for vert in bm.verts]
            plain_verts = [vert.to_tuple() for vert in verts]
            tree_to_bm = plain_verts.index(next_coordinates)

            bm.verts[tree_to_bm].select_set(True)
            selected_verts = [v.index for v in bm.verts if v.select]
            print("Test bm.verts:", selected_verts)
            # Order point
            bpy.ops.mesh.sort_elements(type='SELECTED', elements={'VERT'})
            print("Return")
            return next

        elif next in selected_coordinates:
            c += 1
            next = nearest_ind[selected_coordinates[loop_iteration], c]
            print("Next Else", next)

obj = bpy.context.active_object

if obj.mode == 'EDIT':
    # this works only in edit mode,
    bm = bmesh.from_edit_mesh(obj.data)
    verts = [vert.co for vert in bm.verts]
    index = [ind.index for ind in bm.verts]

else:
    # this works only in object mode,
    verts = [vert.co for vert in obj.data.vertices]
    index = [ind.index for ind in obj.data.vertices]

bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)
# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]
print("Plain Verts:\n", plain_verts)
# Find farthest X coordinate
X_coo = [x[0] for x in plain_verts]
print("List of X coordinates:", X_coo)
# If multiple coordinates have the most extreme positive X value pick the first one
# The max() function does this automatically
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)
print("Largest X Coordinate:", max_X)
print("And its index:", max_X_index)

# Set up tree to search in
tree = KDTree(plain_verts)
nearest_dist, nearest_ind = tree.query(plain_verts, k=len(plain_verts))
print("IND:", "\n".join(str(x) for x in nearest_ind))
# Turn on vertex
bm.verts.ensure_lookup_table()
bm.verts[max_X_index].select_set(True)
# Order point
bpy.ops.mesh.sort_elements(type='SELECTED', elements={'VERT'})
# Add found coordinate to list
selected_coordinates = []
selected_coordinates.append(max_X_index)
print(selected_coordinates)

for x in range(0, (len(plain_verts)-1)): # Since first determines the start instead of next closest neighbour
    next = find_next_vertex(tree=plain_verts, nearest_ind=nearest_ind, selected_coordinates=selected_coordinates, loop_iteration=x, bm=bm)

    # Add to list
    selected_coordinates.append(next)

print("Final:", selected_coordinates)
print(len(selected_coordinates))

# Test to see if bm.verts has changed over time
verts = [vert.co for vert in bm.verts]
index = [ind.index for ind in bm.verts]
plain_verts = [vert.to_tuple() for vert in verts]
tree = KDTree(plain_verts)
new_nearest_dist, new_nearest_ind = tree.query(plain_verts, k=len(plain_verts))
print("Test of ind is equal:")
if (new_nearest_ind == nearest_ind).all():
    print("True")
else:
    print("False")

# Idea
# Search in the coordinates the most extreme X or Y point
# Select this point
# Add this point to a list of previously found coordinates
# Order this point, so this becomes point 0
# Search for the next nearest point on the same Z-height
# Also select this point, and reorder them so that they become 0 - 1
# Add this point to the previously found coordinates list
# Search for the next nearest point etc. until all points on Z-height have been found
# Increase Z height

# Donut 0 is at farthest positive X coordinate
