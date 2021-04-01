import bpy, bmesh
from sklearn.neighbors import KDTree
import math

# Create a function that builds a tree like KDTree, just with only the nearest vertices
def closest_neighbours(coordinates, neighbour_verts):
    tree = []
    # Find max and min X and Y locations of object to compare to
    X_coo = [x[0] for x in coordinates]
    Y_coo = [y[1] for y in coordinates]
    max_X = max(X_coo)
    max_Y = max(Y_coo)
    max_X_index = X_coo.index(max_X)
    max_Y_index = Y_coo.index(max_Y)

    # Same for the min value
    min_X = min(X_coo)
    min_Y = min(Y_coo)
    min_X_index = X_coo.index(min_X)
    min_Y_index = Y_coo.index(min_Y)

    # Get coordinates
    X_min = coordinates[min_X_index]
    X_max = coordinates[max_X_index]
    Y_min = coordinates[min_Y_index]
    Y_max = coordinates[max_Y_index]

    compare_coo = [((max_X + 10), (max_Y + 10), 0)]
    for e, b in enumerate(neighbour_verts):
        ind_coo = coordinates[e]
        #print("Suc:", len(neighbour_verts[0]))
        #print("NN:")
        #print(e)
        tmp = []
        for v in range(len(neighbour_verts[e])):
        #for v in enumerate(range(3)):
            vertex = neighbour_verts[e][v]
            coo = coordinates[neighbour_verts[e][v]]

            #print("V:", v)
            #print("Vertex:", vertex)
            #print("Coo:", coo)
            #print("Ind_coo:", ind_coo)
            #print("Ind_coo[1]:", ind_coo[1])
            #print("Coo[1]:", coo[1])
            #dist_XZ = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[2] - coo[2]), 2)) # (Y1 - Y2) + (Z1 - Z2)
            #dist_Z = abs(ind_coo[2] - coo[2])

            #dist = abs(ind_coo[2] - coo[2])
            #dist = math.sqrt(math.pow((0 - coo[0]), 2) + math.pow((0 - coo[1]), 2)) # Distance to XY-plane

            #if coo[0] >= 0 and coo[1] >= 0: # Moving in Quadrant I (+, +) towards Y_max
                #dist = coo[1]
            #    dist = math.sqrt(math.pow((Y_max[1] - coo[1]), 2) + math.pow((Y_max[2] - coo[2]), 2)) # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            #elif coo[0] <= 0 and coo[1] >= 0: # Moving in Q II (-, +) towards X_min
                #dist = abs(coo[0])
            #    dist = math.sqrt(math.pow((X_min[0] - coo[0]), 2)+ math.pow((X_min[2] - coo[2]), 2)) # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            #elif coo[0] <= 0 and coo[1] <= 0: # Moving in Q III (-, -) towards Y_min
                #dist = abs(coo[1])
            #    dist = math.sqrt(math.pow((Y_min[1] - coo[1]), 2) + math.pow((Y_min[2] - coo[2]), 2)) # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            # elif coo[0] >= 0 and coo[1] <= 0: # Moving in Quadrant IV (+, -) towards X_max
            #else:
                #dist = coo[0]
            #    dist = math.sqrt(math.pow((X_max[0] - coo[0]), 2) + math.pow((X_max[2] - coo[2]), 2)) # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)

            # Create vectors, normalise these and you have the direction.
            # The one that has the largest (positive) Y-value is the one needed (might need to append with Quadrons
            vector = [ind_coo[0] - coo[0], ind_coo[1] - coo[1], ind_coo[2] - coo[2]]
            norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
            dir = [vector[0] / norm, vector[1] / norm, vector[2] / norm]

            if ind_coo[0] >= 0 and ind_coo[1] >= 0: # Moving in Quadrant I (+, +) towards + Y
                if ind_coo[1] == Y_max: # Transition to Quadrant II
                    dist = dir[0]
                else:
                    dist = dir[1]
            elif coo[0] <= 0 and coo[1] >= 0:  # Moving in Q II (-, +) towards - X
                if ind_coo[0] == X_min: # Transition to Quadrant III
                    dist = dir[1]
                else:
                    dist = dir[0]
            elif coo[0] <= 0 and coo[1] <= 0:  # Moving in Q III (-, -) towards - Y
                if ind_coo[1] == Y_min: # Transition to Q IV
                    dist = dir[0]
                else:
                    dist = dir[1]
            # elif coo[0] >= 0 and coo[1] <= 0: # Moving in Quadrant IV (+, -) towards + X
            else:
                if ind_coo[0] == X_max: # Transition to Q I
                    dist = dir[1]
                else:
                    dist = dir[0]

            # Compare to a point far outside of the mesh and get the angle. The smaller the angle the closer the point is in X-direction
            # To get the angle get the distance between ind_coo and the comparison point, and ind_coo and the neighbour vertex.
            # Cosine rule: c2 = a2 + b2 - 2ab cos C (where C is an angle)
            # Rewritten: C = arccos (a2 + b2 - c2) / 2ab
            # Distance between ind_coo and coo (a)
            dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) +math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2)) # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            # Distance between ind_coo and compare_coo
            dis_b = math.sqrt(math.pow((ind_coo[0] - compare_coo[0][0]), 2) + math.pow((ind_coo[1] - compare_coo[0][1]), 2) + math.pow((ind_coo[2] - compare_coo[0][2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            # Distance between compare_coo and coo
            dis_c = math.sqrt(math.pow((compare_coo[0][0] - coo[0]), 2) + math.pow((compare_coo[0][1] - coo[1]), 2) + math.pow((compare_coo[0][2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)

            if ind_coo[0] >= 0 and ind_coo[1] >= 0:  # Moving in Quadrant I (+, +) towards + Y
                if ind_coo[1] == Y_max:  # Transition to Quadrant II
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X-10)), 2) + math.pow((ind_coo[1] - (min_Y-10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((min_X-10) - coo[0]), 2) + math.pow(((min_Y-10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            elif coo[0] <= 0 and coo[1] >= 0:  # Moving in Q II (-, +) towards - X
                if ind_coo[0] == X_min:  # Transition to Quadrant III
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            elif coo[0] <= 0 and coo[1] <= 0:  # Moving in Q III (-, -) towards - Y
                if ind_coo[1] == Y_min:  # Transition to Q IV
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            # elif coo[0] >= 0 and coo[1] <= 0: # Moving in Quadrant IV (+, -) towards + X
            else:
                if ind_coo[0] == X_max:  # Transition to Q I
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)

            angle = math.acos((dis_a ** 2 + dis_b ** 2 - dis_c ** 2) / (2 * dis_a * dis_b))

            #dist = abs(dir[2])
            result = []
            result.append(vertex)
            # result.append(dist)
            result.append(angle)
            tuple(result)
            #print("Result:", result)
            tmp.append(result)
        #print("TMP:", tmp)



#        for i in range(len(tmp)):
#            if tmp[i][1] < tmp[i-1][1]:
#                tmp.insert((i-1), tmp.pop(i))
#                print("Pop:", tmp)
# ------------------------------------------
# Old method
        c = 1
        while c != 0:
            c = 1
            for i in range(len(tmp)):
                if tmp[i][1] < tmp[i-1][1] and i != 0:
                    tmp.insert((i-1), tmp.pop(i))
                    #print("Pop:", tmp)
                    c += 1
            if c == 1:
                c = 0
# ----------------------------------------

# -------------------------------------
# Quadrants
#        c = 1
#        while c != 0:
#            c = 1
#            for i in range(len(tmp)): # tmp[i] are the vertices indices, tmp[i][1] gets the vector, tmp[i][1][0] is the X-coordinate
#                if ind_coo[0] >= 0 and ind_coo[1] >= 0:  # Moving in Quadrant I (+, +) towards + Y
#                    if ind_coo[1] == Y_max:  # Transition to Quadrant II
#                       if tmp[i][1][0] < tmp[i - 1][1][0] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                    else:
#                        if tmp[i][1][1] > tmp[i - 1][1][1] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                elif coo[0] <= 0 and coo[1] >= 0:  # Moving in Q II (-, +) towards - X
#                    if ind_coo[0] == X_min:  # Transition to Quadrant III
#                        if tmp[i][1][1] < tmp[i - 1][1][1] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                    else:
#                       if tmp[i][1][0] < tmp[i - 1][1][0] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                elif coo[0] <= 0 and coo[1] <= 0:  # Moving in Q III (-, -) towards - Y
#                    if ind_coo[1] == Y_min:  # Transition to Q IV
#                        if tmp[i][1][0] > tmp[i - 1][1][0] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                    else:
#                       if tmp[i][1][1] < tmp[i - 1][1][1] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                # elif coo[0] >= 0 and coo[1] <= 0: # Moving in Quadrant IV (+, -) towards + X
#                else:
#                    if ind_coo[0] == X_max:  # Transition to Q I
#                        if tmp[i][1][1] > tmp[i - 1][1][1] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#                    else:
#                        if tmp[i][1][0] > tmp[i - 1][1][0] and i != 0: #and tmp[i][1][2] < tmp[i - 1][1][2]:
#                            tmp.insert((i - 1), tmp.pop(i))
#                            c += 1
#
#            if c == 1:
#                c = 0
#
# -------------------------------------------
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
    #print("Selected Coordinates Loop:", selected_coordinates)
    c = 1
    next = nearest_ind[selected_coordinates[loop_iteration]][c]
    #print("Next:", next)
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
            #print("Test bm.verts:", selected_verts)
            # Order point
            bpy.ops.mesh.sort_elements(type='SELECTED', elements={'VERT'})
            #print("Return")
            return next

        elif next in selected_coordinates:
            c += 1
            next = nearest_ind[selected_coordinates[loop_iteration]][c]
            #print("Next Else", next)

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
        #print("%d -> %d via edge %d" % (v.index, e.other_vert(v).index, e.index))
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
#print("List of X coordinates:", X_coo)
# If multiple coordinates have the most extreme positive X value pick the first one
# The max() function does this automatically
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)
#print("Largest X Coordinate:", max_X)
#print("And its index:", max_X_index)

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