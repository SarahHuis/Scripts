import numpy as np
from sklearn.neighbors import KDTree
import csv
import numpy as np
import math, itertools

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
            dist_YZ = math.sqrt(math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2)) # (Y1 - Y2) + (Z1 - Z2)
            result = []
            result.append(vertex)
            result.append(dist_YZ)
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
                    #print("Pop:", tmp)
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



def find_next_vertex(tree, nearest_ind, selected_coordinates, loop_iteration):
    print("Selected Coordinates Loop:", selected_coordinates)
    c = 1
    #next = nearest_ind[selected_coordinates[loop_iteration], c]
    next = nearest_ind[selected_coordinates[loop_iteration]][c]
    print("Next:", next)
    # Check if index is used before
    while c < (len(tree)):
        if next not in selected_coordinates:
            print("Return")
            return next

        elif next in selected_coordinates:
            c += 1
            #next = nearest_ind[selected_coordinates[loop_iteration], c]
            next = nearest_ind[selected_coordinates[loop_iteration]][c]
            print("Next Else", next)


np.random.seed(0)
#X = [(-1.0, -1.0, -1.0),
#        (-1.0, -1.0, 1.0),
#        (-1.0, 1.0, -1.0),
#        (-1.0, 1.0, 1.0),
#        (1.0, -1.0, -1.0),
#        (1.0, -1.0, 1.0),
#        (1.0, 1.0, -1.0),
#        (1.0, 1.0, 1.0)]

# Coordinates
X =  [(-1.0, -1.0, -1.0), (-1.0, -1.0, 1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, -1.0), (1.0, 1.0, 1.0)]
#X = [(0.9510578513145447, -0.30901262164115906, 0.0), (0.8944262266159058, 0.0, 0.44721561670303345), (-0.8944262266159058, 0.0, -0.44721561670303345), (0.276388019323349, 0.8506492376327515, 0.4472198486328125), (-0.26286882162094116, -0.8090116381645203, 0.5257376432418823), (-0.6881893873214722, -0.49999693036079407, -0.5257362127304077), (0.0, 0.9999999403953552, 0.0), (0.16245555877685547, -0.49999526143074036, 0.8506543636322021), (0.6881893873214722, -0.49999693036079407, 0.5257362127304077), (0.8506478667259216, 0.0, -0.5257359147071838), (-0.8506478667259216, 0.0, 0.5257359147071838), (-0.42532268166542053, 0.30901139974594116, 0.8506541848182678), (-0.9510578513145447, 0.30901262164115906, 0.0), (-0.42532268166542053, -0.30901139974594116, 0.8506541848182678), (-0.6881893873214722, 0.49999693036079407, -0.5257362127304077), (0.26286882162094116, -0.8090116381645203, -0.5257376432418823), (0.6881893873214722, 0.49999693036079407, 0.5257362127304077), (-0.276388019323349, 0.8506492376327515, -0.4472198486328125), (0.0, 0.0, 1.0), (0.42532268166542053, -0.30901139974594116, -0.8506541848182678), (0.7236073017120361, -0.5257253050804138, -0.44721952080726624), (0.7236073017120361, 0.5257253050804138, -0.44721952080726624), (0.5877856016159058, -0.8090167045593262, 0.0), (0.42532268166542053, 0.30901139974594116, -0.8506541848182678), (-0.7236073017120361, -0.5257253050804138, 0.44721952080726624), (0.26286882162094116, 0.8090116381645203, -0.5257376432418823), (-0.16245555877685547, -0.49999526143074036, -0.8506544232368469), (-0.9510578513145447, -0.30901262164115906, 0.0), (0.276388019323349, -0.8506492376327515, 0.4472198486328125), (0.0, 0.0, -1.0), (0.5877856016159058, 0.8090167045593262, 0.0), (-0.276388019323349, -0.8506492376327515, -0.4472198486328125), (0.16245555877685547, 0.49999526143074036, 0.8506543636322021), (-0.26286882162094116, 0.8090116381645203, 0.5257376432418823), (0.9510578513145447, 0.30901262164115906, 0.0), (-0.7236073017120361, 0.5257253050804138, 0.44721952080726624), (-0.525729775428772, 0.0, -0.8506516814231873), (-0.16245555877685547, 0.49999526143074036, -0.8506544232368469), (0.0, -0.9999999403953552, 0.0), (-0.5877856016159058, -0.8090167045593262, 0.0), (-0.5877856016159058, 0.8090167045593262, 0.0), (0.525729775428772, 0.0, 0.8506516814231873)]
# Indices of connected vertices
NN = [[2, 1, 4], [0, 3, 5], [0, 3, 6], [1, 2, 7], [6, 5, 0], [7, 4, 1], [2, 7, 4], [3, 6, 5]]

tree = closest_neighbours(coordinates=X, neighbour_verts=NN)

#tree = KDTree(X)
#nearest_dist, nearest_ind = tree.query(X, k=2)  # k=2 nearest neighbors where k1 = identity
#print(X)
#print(nearest_dist[:, 1])  # drop id; assumes sorted -> see args!
#print(nearest_ind[:, 1])  # drop id


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
#print("\nIdea")
# Find farthest X coordinate
X_coo = [x[0] for x in X]
#print("List of X coordinates:", X_coo)
# If multiple coordinates have the most extreme positive X value pick the first one
# The max() function does this automatically
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)
#print("Largest X Coordinate:", max_X)
#print("And its index:", max_X_index)

# Turn on vertex
# Order point

# Search for next nearest point. Difference in Z-values gets smaller, so a specific cut off is a bad idea.
# The donut has 56 vertices per ring. So, if 56 points have been selected go to the next nearest Z-point and start anew
# A cube has 4 before the jump needs to be made to the next "ring" of 4
# So, always find the closest in X value

# Add found coordinate to list
selected_coordinates = []
selected_coordinates.append(max_X_index)
#print(selected_coordinates)

# Set up Tree to search in
#tree = KDTree(X)
#nearest_dist, nearest_ind = tree.query(X, k=len(X))

# --------------------------------
# Set up tree to search in
# Individual X, Y, Z trees
#X_coo = [x[0] for x in X]
#tree_X = KDTree(X_coo)
#Y_coo = [y[1] for y in X]
#tree_Y = KDTree(Y_coo)
#Z_coo = [z[2] for z in X]
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
#for i in range(len(XY_coo)):
#    xy_ind = XY_nearest_ind.tolist().index(i)
#    xz_ind = XZ_nearest_ind.index(i)
#    yz_ind = YZ_nearest_ind.index(i)
#    calc_average_index[i] = xy_ind[i] + xz_ind[i] + yz_ind[i]
# -----------------------------------

#with open('Indices.csv', 'w') as out:
#    csv_out = csv.writer(out)
#    for row in nearest_ind:
#        csv_out.writerow(row)
#print("IND:", "\n".join(str(x) for x in nearest_ind))

for x in range(0, (len(X)-1)): # Since first determines the start instead of next closest neighbour
    next = find_next_vertex(tree=X, nearest_ind=tree, selected_coordinates=selected_coordinates, loop_iteration=x)

    # Add to list
    selected_coordinates.append(next)

#print("Final:", selected_coordinates)
