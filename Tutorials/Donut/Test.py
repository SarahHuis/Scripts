import bpy, bmesh
from sklearn.neighbors import KDTree

# Create a function that builds a tree like KDTree, just with only the nearest vertices
#def closest_neighbours(coordinates, neighbour_verts):
#    for e in enumerate(neighbour_verts):
#        print("Suc:", len(neighbour_verts[0]))
#        #for v in range(len(neighbour_verts[0])):
#        for v in enumerate(range(3)):
#            print("Success:", neighbour_verts[e][v])


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
edges = [edge for edge in bm.edges]
connected_v = []
for v in bm.verts:
    v_other = []
    for e in v.link_edges:
        v_other.append(e.other_vert(v).index)
        tuple(v_other)
        # print some info
        print("%d -> %d via edge %d" % (v.index, e.other_vert(v).index, e.index))
        connected_v.append(v_other)

# Now there are several duplicates within, so remove those
neighbour_vert = []
for i in connected_v:
    if i not in neighbour_vert:
        neighbour_vert.append(i)
print("Neighbour_vert:", neighbour_vert)
# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]
print("Plain Verts:\n", plain_verts)
#plain_edges = [connected_v.to_tuple() for edge in edges]
#print("Plain Edges:\n", plain_edges)



# Find farthest X coordinate
X_coo = [x[0] for x in plain_verts]
print("List of X coordinates:", X_coo)
# If multiple coordinates have the most extreme positive X value pick the first one
# The max() function does this automatically
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)
print("Largest X Coordinate:", max_X)
print("And its index:", max_X_index)

# Old implementation
tree = KDTree(plain_verts)
nearest_dist, nearest_ind = tree.query(plain_verts, k=len(plain_verts))
print("Tree:", tree)
print("Nearest Ind:", nearest_ind)

closest_neighbours(coordinates=plain_verts, neighbour_verts=neighbour_vert)


## Does not work in current stuff
# Append Solution:
# Create X,Y X,Z and Y,Z trees, so there are still spatial coordinates
# 1D arrays are not allowed
# --------------------------------
# Set up tree to search in
# Individual X, Y, Z trees
#X_coo = [x[0] for x in plain_verts]
#tree_X = KDTree(X_coo)
#Y_coo = [y[1] for y in plain_verts]
#tree_Y = KDTree(Y_coo)
#Z_coo = [z[2] for z in plain_verts]
#tree_Z = KDTree(Z_coo)

# Create the X,Y X,Z Y,Z trees
#XY_coo = list(zip(X_coo, Y_coo))
#XZ_coo = list(zip(X_coo, Z_coo))
#YZ_coo = list(zip(Y_coo, Z_coo))
#for x in range(len(X_coo)):
#    XY_coo = np.column_stack((X_coo[x], Y_coo[x]))
#    XZ_coo = [X_coo[x], Z_coo[x]]
#    YZ_coo = [Y_coo[x], Z_coo[x]]

#XY_tree = KDTree(XY_coo)
#XZ_tree = KDTree(XZ_coo)
#YZ_tree = KDTree(YZ_coo)

#nearest_dist, nearest_ind = tree.query(plain_verts, k=len(plain_verts))
#print("IND:", "\n".join(str(x) for x in nearest_ind))

# Calculate each distances
#XY_nearest_dist, XY_nearest_ind = XY_tree.query(XY_coo, k=len(XY_coo))
#XZ_nearest_dist, XZ_nearest_ind = XZ_tree.query(XZ_coo, k=len(XZ_coo))
#YZ_nearest_dist, YZ_nearest_ind = YZ_tree.query(YZ_coo, k=len(YZ_coo))
#calc_average_index = []
#for i in range(len(tree_XZ)):
#    xy_ind[i] = XY_nearest_ind.index(i)
#    xz_ind[i] = XZ_nearest_ind.index(i)
#    yz_ind[i] = YZ_nearest_ind.index(i)
#    calc_average_index[i] = xy_ind[i] + xz_ind[i] + yz_ind[i]
# -----------------------------------


# Most extreme +X point as begin point
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)

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
#    next = find_next_vertex(tree=plain_verts, nearest_ind=calc_average_index, selected_coordinates=selected_coordinates, loop_iteration=x, bm=bm)

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

# Idea to get all vertices selected in one plane at a time
# First, find max X (arbitrary)
# Instead of one calculation of nearest distance overall find nearest neighbour based on one specific axis
# Find closest neighbour on X
# Find closest on Y
# Find closest on Z
# These three might overlap, but likely will have slight differences between them
# Thought:
# To find the closest point, average the three indices of each found point.
# So, if point 3 is at index 2 for X, 3 for Y, and 10 for Z, then its average index would be 5.
# Lowest possible index is 1+1+1 (since 0 is the point itself), so an average of 1.
# Perhaps division is not not necessary, so total would be 15 and 3, respectively.
# Then pick this lowest index and that is the new vertex to turn on.