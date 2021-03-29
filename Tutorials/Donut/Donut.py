import bpy, bmesh, random
from bpy import data as D, context as C

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
for vert in vertices:
    # Turn every vertix off
    for i in range(0, len(mesh.verts)):
        vert.select_set(False)

    #mw = ob.matrix_world
#cloc = mw.inverted() @ C.scene.cursor.location
#new_order = sorted(list(range(len(mesh.verts))))
#bm.verts.ensure_lookup_table()
#verts = sorted(mesh.verts, key=lambda v: (v.co - cloc).length)
#
#for i, v in enumerate(verts):
#    v.index = i
#mesh.verts.sort()
#bmesh.update_edit_mesh(ob.data)


#new_order = list(range(len(mesh.verts)))
#random.shuffle(new_order)
##print(new_order)
##new_order = sorted(new_order)
#print(new_order)
#zip1 = [*zip(new_order, mesh.verts)]
#print("Zip I:")
#print(zip1)
#for i, vert in zip(new_order, mesh.verts):
#    vert.index = i
#
#mesh.verts.index_update()
#zip1 = [*zip(new_order, mesh.verts)]
#print("Zip II:")
#print(zip1)
#for i, v in zip(new_order, mesh.verts):
#    v.index = i
#zip1 = [*zip(new_order, mesh.verts)]
#print("Zip III:")
#print(zip1)
#mesh.verts.sort()
#
#zip1 = [*zip(new_order, mesh.verts)]
#print("Zip IV:")
#print(zip1)
#
#bmesh.update_edit_mesh(ob.data)
#zip1 = [*zip(new_order, mesh.verts)]
#print("Zip V:")
#print(zip1)



