# rubi4j

# to stack cube positions for traversation
import queue
import time
import sys
import rubi4j_minicube

print('# Welcome to rubi4j!')

# initialize
print('# initialize queue for unprocessed permutations')
cube_perm_queue = queue.Queue()
print('# initialize dictionary to store permutation state')
cube_perm_dict = {}
print('# initialize cube')
cube = rubi4j_minicube.minicube()
print(f'# checksum = {cube.checksum()}')
perm_father = cube.perm_display_short()
print('# queue unscrambled permutation')
cube_perm_queue.put(perm_father)
cube_perm_dict[perm_father] = 0
print('# set counter to zero')
cube_count = 0
step_count = 0
print('# open file for bulk load output')
try:
    bulkfile = open('rubi4j.bulk', 'w')
except:
    print('### error open bulkfile')
    sys.exit(1)

print('# note start time')
cube_time_start = time.time()

# three sides to move
rotation_list = [ "UP", "FRONT", "RIGHT"]
#rotation_list = [ "UP" ]


print( "# start permutation")
while not cube_perm_queue.empty():
    # fetch next permutation
    perm_father = cube_perm_queue.get()

    # decide if there is something to do
    try:
        children = cube_perm_dict[perm_father]
    except:
        print(f'### {perm_father} in queue but no children which is an error!')
        break
    if children != 0:
        # processed node, skip to next permutation
        continue

    # three sides to move
    for rotation in rotation_list:
        # load permutation into minicube
        cube.init_via_str(perm_father)
        # checksum test
        #if cube.checksum() != 60:
        #    print(f"### checksum error at cube_count = {cube_count}, perm_father = {perm_father}")
        #    break

        if rotation == "UP":
            cube.rotate_up_clockwise_90()
            cube_side = "U"
        if rotation == "FRONT":
            cube.rotate_front_clockwise_90()
            cube_side = "F"
        if rotation == "RIGHT":
            cube.rotate_right_clockwise_90()
            cube_side = "R"
        # store new permutation as son
        perm_son = str( cube.perm_display_short() )
        try:
            children = cube_perm_dict[perm_son]
        except:
            cube_perm_dict[perm_son] = 0
            cube_perm_queue.put( perm_son )
        # store move
        bulkline = perm_father+","+cube_side+","+perm_son+"\n"
        bulkfile.write(bulkline)
    # all three sides moved, therefore 3 children
    cube_perm_dict[perm_father] = 3
    # count another processed cube
    cube_count += 1
    # count steps
    step_count += 1
    if step_count == 100000:
        cube_time_end = time.time()
        cube_time = cube_time_end - cube_time_start
        print(f'# {step_count} cubes processed in {cube_time:.0f} seconds, ' +
              f'cubes processed = {cube_count}, cubes hashed = {len(cube_perm_dict)}, ' +
              f'queued = {cube_perm_queue.qsize()}')
        #print(f'# {perm_father[2]}-{perm_father[4]}-{perm_father[8]}')
        step_count = 0
        cube_time_start = cube_time_end

print(f'# final cube count = {cube_count}')
print(f'# final dict count = {len(cube_perm_dict)}')
bulkfile.close()
print("# finished")