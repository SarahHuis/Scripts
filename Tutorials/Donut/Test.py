import bpy, bmesh
from sklearn.neighbors import KDTree
import math

# Create a function that builds a tree like KDTree, just with only the nearest vertices
def closest_neighbours(coordinates, neighbour_verts):
    tree = []
    for e, b in enumerate(neighbour_verts):

        #print("Suc:", len(neighbour_verts[0]))
        #print("NN:")
        #print(e)
        tmp = []
        for v in range(len(neighbour_verts[e])):
        #for v in enumerate(range(3)):
            vertex = neighbour_verts[e][v]
            coo = coordinates[neighbour_verts[e][v]]
            ind_coo = coordinates[e]
            #print("V:", v)
            #print("Vertex:", vertex)
            #print("Coo:", coo)
            #print("Ind_coo:", ind_coo)
            #print("Ind_coo[1]:", ind_coo[1])
            #print("Coo[1]:", coo[1])
            #dist_YZ = math.sqrt(math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2)) # (Y1 - Y2) + (Z1 - Z2)
            dist_X = ind_coo[0] - coo[0]
            result = []
            result.append(vertex)
            result.append(dist_X)
            tuple(result)
            #print("Result:", result)
            tmp.append(result)
        #print("TMP:", tmp)

#        for i in range(len(tmp)):
#            if tmp[i][1] < tmp[i-1][1]:
#                tmp.insert((i-1), tmp.pop(i))
#                print("Pop:", tmp)
        c = 1
        while c != 0:
            c = 1
            for i in range(len(tmp)):
                if tmp[i][1] < tmp[i-1][1] and i != 0:
                    tmp.insert((i-1), tmp.pop(i))
                    print("Pop:", tmp)
                    c += 1
            if c == 1:
                c = 0

        tmp_tree = []
        tmp_tree.append(e)
        for i in range(len(tmp)):
            tmp_tree.append(tmp[i][0])
        #print("TMP Tree:", tmp_tree)
        tree.append(tmp_tree)

    print("Tree:", tree)
    return tree

def find_next_vertex(tree, nearest_ind, selected_coordinates, loop_iteration, bm):
    bm.verts.ensure_lookup_table()
    print("Selected Coordinates Loop:", selected_coordinates)
    c = 1
    next = nearest_ind[selected_coordinates[loop_iteration]][c]
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
            next = nearest_ind[selected_coordinates[loop_iteration]][c]
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
tree = closest_neighbours(coordinates=plain_verts, neighbour_verts=neighbour_vert)

#tree = KDTree(plain_verts)
#nearest_dist, nearest_ind = tree.query(plain_verts, k=len(plain_verts))
#print("Tree:", tree)
#print("Nearest Ind:", nearest_ind)

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
    next = find_next_vertex(tree=plain_verts, nearest_ind=tree, selected_coordinates=selected_coordinates, loop_iteration=x, bm=bm)
#    next = find_next_vertex(tree=plain_verts, nearest_ind=calc_average_index, selected_coordinates=selected_coordinates, loop_iteration=x, bm=bm)

    # Add to list
    selected_coordinates.append(next)

print("Final:", selected_coordinates)
print(len(selected_coordinates))


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