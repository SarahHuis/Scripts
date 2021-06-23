import bpy, bmesh, random, math
from bpy import data as D, context as C

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

    for e, b in enumerate(neighbour_verts):
        ind_coo = coordinates[e]
        tmp = []
        for v in range(len(neighbour_verts[e])):
            vertex = neighbour_verts[e][v]
            coo = coordinates[neighbour_verts[e][v]]

            # Compare to a point far outside of the mesh and get the angle. The smaller the angle the closer the point is in X-direction
            # To get the angle get the distance between ind_coo and the comparison point, and ind_coo and the neighbour vertex.
            # Cosine rule: c2 = a2 + b2 - 2ab cos C (where C is an angle)
            # Rewritten: C = arccos (a2 + b2 - c2) / 2ab

            if ind_coo[0] >= 0 and ind_coo[1] >= 0:  # Moving in Quadrant I (+, +) towards + Y
                if ind_coo[1] == Y_max:  # Transition to Quadrant II
                    # Distance between ind_coo and coo (a)
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between ind_coo and compare_coo
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X-10)), 2) + math.pow((ind_coo[1] - (min_Y-10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    # Distance between compare_coo and coo
                    dis_c = math.sqrt(math.pow(((min_X-10) - coo[0]), 2) + math.pow(((min_Y-10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            elif coo[0] <= 0 and coo[1] >= 0:  # Moving in Q II (-, +) towards - X
                if ind_coo[0] == X_min:  # Transition to Quadrant III
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            elif coo[0] <= 0 and coo[1] <= 0:  # Moving in Q III (-, -) towards - Y
                if ind_coo[1] == Y_min:  # Transition to Q IV
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (min_Y - 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((min_Y - 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
            # elif coo[0] >= 0 and coo[1] <= 0: # Moving in Quadrant IV (+, -) towards + X
            else:
                if ind_coo[0] == X_max:  # Transition to Q I
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (min_X - 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((min_X - 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                else:
                    dis_a = math.sqrt(math.pow((ind_coo[0] - coo[0]), 2) + math.pow((ind_coo[1] - coo[1]), 2) + math.pow((ind_coo[2] - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_b = math.sqrt(math.pow((ind_coo[0] - (max_X + 10)), 2) + math.pow((ind_coo[1] - (max_Y + 10)), 2) + math.pow((ind_coo[2] - 0), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)
                    dis_c = math.sqrt(math.pow(((max_X + 10) - coo[0]), 2) + math.pow(((max_Y + 10) - coo[1]), 2) + math.pow((0 - coo[2]), 2))  # (X1 - X2) + (Y1 - Y2) + (Z1 - Z2)

            angle = math.acos((dis_a ** 2 + dis_b ** 2 - dis_c ** 2) / (2 * dis_a * dis_b))
            result = []
            result.append(vertex)
            result.append(angle)
            tuple(result)
            tmp.append(result)

        # If the angle of the next vertex in the list is smaller, move it to the front of the list
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
        tree.append(tmp_tree)
    return tree

def find_next_vertex(tree, nearest_ind, selected_coordinates, loop_iteration, bm):
    bm.verts.ensure_lookup_table()
    c = 1
    next = nearest_ind[selected_coordinates[loop_iteration]][c]
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
            # Order point
            bpy.ops.mesh.sort_elements(type='SELECTED', elements={'VERT'})
            return next

        # If vertex is already been used before get the next possible vertex
        elif next in selected_coordinates:
            c += 1
            next = nearest_ind[selected_coordinates[loop_iteration]][c]


current_mode = C.object.mode

if current_mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
# Part I of tutorial
# Modelling the donut

bpy.ops.mesh.primitive_torus_add(align='WORLD', 
                                    location=(0, 0, 0), 
                                    rotation=(0, 0, 0), 
                                    major_radius=0.05, 
                                    minor_radius=0.026, 
                                    abso_major_rad=1.25, 
                                    abso_minor_rad=0.75, 
                                    major_segments=28, 
                                    minor_segments=12)

for obj in C.selected_objects:
    obj.name = 'Donut'
    
ob = D.objects['Donut']
bpy.ops.object.mode_set(mode='EDIT')
mesh = bmesh.from_edit_mesh(ob.data)

# Proportional Editing of shape
# Grab every vert and randomnly determine how much to deform the donut to create a lumpy donut
C.scene.tool_settings.use_proportional_edit = True
vertices = [e for e in mesh.verts]
for vert in vertices:
    for i in range(0, 12):
        if vert.index in range(i, (325 + i), 12):
            vert.select_set(True)
            if random.uniform(0, 1) > 0.3:
                bpy.ops.transform.translate(value=(random.uniform(-.4e-3, .4e-3), random.uniform(-.4e-3, .4e-3), random.uniform(-.4e-3, .4e-3)), 
                                                orient_type='GLOBAL', 
                                                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                                                orient_matrix_type='GLOBAL', 
                                                mirror=True, 
                                                use_proportional_edit=True, 
                                                proportional_edit_falloff='SMOOTH', 
                                                proportional_size=random.uniform(0, 1e-1), 
                                                use_proportional_connected=False, 
                                                use_proportional_projected=False)
            # Deselect vert otherwise multiple vertices are selecting for the transformation
            vert.select_set(False)  
                                                
        else:
            vert.select_set(False)
            
# Return to Object mode            
bpy.ops.object.mode_set(mode='OBJECT')
# Smooth currently selected object
bpy.ops.object.shade_smooth()
# Add Subsurf modifier
bpy.ops.object.modifier_add(type='SUBSURF')

        
# trigger viewport update
#C.view_layer.objects.active = ob
#ob.select_set(True)


# Part II of the tutorial
# Modifiers: Icing on top of donut

# Need bmesh information again after exiting EDIT mode
ob = D.objects['Donut']
bpy.ops.object.mode_set(mode='EDIT')
mesh = bmesh.from_edit_mesh(ob.data)
#vertices = [e for e in mesh.verts]
# Select top part of donut
bpy.ops.mesh.select_all(action = 'DESELECT') #Deselecting all
#for vert in vertices:
#    vert.select_set(False)
#    for i in range(1, 6):
#        if vert.index in range(i, (325 + i), 12):
#            vert.select_set(True)

faces = [e for e in mesh.faces]
mesh.faces.ensure_lookup_table()
for face in faces:
    for i in range(1, 5):
        if face.index in range(i, (325 + i), 12):
            face.select_set(True)

bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1})
bpy.ops.mesh.separate(type='SELECTED')

# Rename Icing
for obj in C.selected_objects:
    if obj.name == 'Donut.001':
        obj.name = 'Icing'

# Select Icing and deselect Donut        
bpy.ops.object.mode_set(mode='OBJECT')        
bpy.ops.object.select_all(action='DESELECT')
D.objects['Icing'].select_set(True)
C.view_layer.objects.active = bpy.data.objects['Icing']

# Add the Solidify modifier and move it before the Subsurf modifier
bpy.ops.object.modifier_add(type='SOLIDIFY')
C.object.modifiers['Solidify'].offset = 1
C.object.modifiers['Solidify'].thickness = 2.5e-3
bpy.ops.object.modifier_move_to_index(modifier="Solidify", index=0)


# Part III of tutorial
# Modelling of the Icing

bpy.context.object.modifiers["Solidify"].show_in_editmode = False

# Select all vertices in EDIT mode
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'SELECT') # Selecting all
# Subdivide
bpy.ops.mesh.subdivide(smoothness=1)

# Due to the subdivision the order of the indices are not incremental anymore,
# so reorder the indices, create a copy, and delete the old object.
# https://blender.stackexchange.com/questions/36577/how-are-vertex-indices-determined
ob = D.objects['Icing']
bpy.ops.object.mode_set(mode='EDIT')
mesh = bmesh.from_edit_mesh(ob.data)

vertices = [e for e in mesh.verts]
verts = [vert.co for vert in vertices]
for vert in vertices:
    # Turn every vertix off
    for i in range(0, len(mesh.verts)):
        vert.select_set(False)

connected_v = []
for v in vertices:
    v_other = []
    for e in v.link_edges:
        v_other.append(e.other_vert(v).index)
        tuple(v_other)
        connected_v.append(v_other)

# Now there are several duplicates within, so remove those
neighbour_vert = []
for i in connected_v:
    if i not in neighbour_vert:
        neighbour_vert.append(i)
plain_verts = [vert.to_tuple() for vert in verts]

tree = closest_neighbours(coordinates=plain_verts, neighbour_verts=neighbour_vert)

# Find farthest X coordinate
X_coo = [x[0] for x in plain_verts]
# Most extreme +X point as begin point
max_X = max(X_coo)
max_X_index = X_coo.index(max_X)

# Turn on vertex
mesh.verts.ensure_lookup_table()
vertices[max_X_index].select_set(True)
# Order point
bpy.ops.mesh.sort_elements(type='SELECTED', elements={'VERT'})
# Add found coordinate to list
selected_coordinates = []
selected_coordinates.append(max_X_index)
print(selected_coordinates)

for x in range(0, (len(plain_verts)-1)): # Since first determines the start instead of next closest neighbour
    next = find_next_vertex(tree=plain_verts, nearest_ind=tree, selected_coordinates=selected_coordinates, loop_iteration=x, bm=mesh)

    # Add to list
    selected_coordinates.append(next)


# Make the icing lumpy
mesh = bmesh.from_edit_mesh(ob.data)
vertices = [e for e in mesh.verts]

faces = [e for e in mesh.faces]
mesh.faces.ensure_lookup_table()


for vert in vertices:
    # Turn every vertix off
    for i in range(0, len(mesh.verts)):
        vert.select_set(False)
        # Turn the outermost ring on, so vertices 0 - 55
        if vert.index not in range(0, 56):
            vert.select_set(True)

# Hide the rest of the icing, so only the bottom is selected for the dripples
bpy.ops.mesh.hide(unselected=False)
# Turn every vertices off, including the hidden ones
for vert in vertices:
    for i in range(0, len(mesh.verts)):
        vert.select_set(False)
C.scene.tool_settings.use_snap = True
C.scene.tool_settings.snap_elements = {'FACE'}
C.scene.tool_settings.use_snap_project = True

for vert in vertices:
    for i in range(0, 56):
        vert.select_set(True)

        if i is 24:
            for edge in vert.link_edges:
                print("Vert:", vert)
                print("Edge:", edge.other_vert(vert))
                print("Edge[0]:", edge)
        if random.uniform(0, 1) > 0.3:
            # Make the icing wobbly
            bpy.ops.transform.translate(value=(0, 0, random.uniform(-.6e-3, .6e-3)),
                                        orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL',
                                        mirror=True,
                                        use_proportional_edit=True,
                                        proportional_edit_falloff='RANDOM',
                                        proportional_size=random.uniform(0, 1e-1),
                                        use_proportional_connected=False,
                                        use_proportional_projected=False)
        # Deselect vert otherwise multiple vertices are selecting for the transformation
        vert.select_set(False)

# Fuck dripples
# Make the dripple
'''mark = 0
iter = 0
iter_max = 0
for vert in vertices:

    for i in range(0, 56):
        if mark == 1: # At least one vertex is turned on
            if iter == 1 and iter_max == 2 or iter == 2 and iter_max == 3:
                vert.select_set(True) # All required vertices are turned on, and ready to be extruded
                bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip": False,
                                                                         "use_dissolve_ortho_edges": False,
                                                                         "mirror": False},
                                                 TRANSFORM_OT_translate={"value": (random.uniform(-1e-2, 1e-2), random.uniform(-1e-2, 1e-2), random.uniform(-1e-2, 1e-2)),
                                                                         "orient_type": 'GLOBAL',
                                                                         "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                                                         "orient_matrix_type": 'GLOBAL',
                                                                         "constraint_axis": (False, False, False),
                                                                         "mirror": False,
                                                                         "use_proportional_edit": False,
                                                                         "proportional_edit_falloff": 'SHARP',
                                                                         "proportional_size": random.uniform(0, 1e-1),
                                                                         "use_proportional_connected": False,
                                                                         "use_proportional_projected": False,
                                                                         "snap": False, "snap_target": 'CLOSEST',
                                                                         "snap_point": (0, 0, 0),
                                                                         "snap_align": False,
                                                                         "snap_normal": (0, 0, 0),
                                                                         "gpencil_strokes": False,
                                                                         "cursor_transform": False,
                                                                         "texture_space": False,
                                                                         "remove_on_cancel": False,
                                                                         "release_confirm": False,
                                                                         "use_accurate": False,
                                                                         "use_automerge_and_split": False})

                # Go through all vertices in mesh and turn everyone off
                for i in range(0,56):
                    vert.select_set(False)

                # Reset everything
                mark = 0
                iter = 0
                iter_max = 0

            elif iter == 1 and iter_max == 3:
                vert.select_set(True)
                iter = 2

        else:
            if random.uniform(0, 1) > .2:
                vert.select_set(True)
                mark = 1 # Has been marked to turn the next verts on.
                iter = 1 # First vertex is turned on
                iter_max = random.choice([2, 3]) # Random whether the dribble will be made using a total of 2 vertices or 3.

            #vertices[neighbour_vert[i][0]].select_set(True)
            #vertices[neighbour_vert[i][1]].select_set(True)




            #vertices[neighbour_vert[i][0]].select_set(False)
            #vertices[neighbour_vert[i][1]].select_set(False)
           # vert.select_set(False)
'''


