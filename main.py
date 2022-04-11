# rubi4j

# to stack cube positions for traversation
import queue
import rubi4j_minicube
import rubi4j_neo4j

print('# Welcome to rubi4j!')

print("# initialize queue, minicube, counters and database connection")
cube_perm_queue = queue.Queue()
cube = rubi4j_minicube.minicube()
perm_father = cube.perm_display_short()
cube_perm_queue.put(perm_father)
cube_count = 0
step_count = 0
db_feed = rubi4j_neo4j.minicube_neo4j("bolt://localhost:7687", "neo4j", "rubi4j")
db_feed.permutation_constraint()
db_feed.add_permutation( perm_father )

# three sides to move
rotation_list = [ "UP", "FRONT", "RIGHT"]

cube_count += 1
step_count += 1
while not cube_perm_queue.empty():
    # fetch next permutation
    perm_father = cube_perm_queue.get()
    # count steps
    step_count += 1

    # decide if there is something to do
    children = db_feed.get_number_of_children( perm_father )
    if children == 3:
        # processed node, skip to next permutation
        continue
    if children == -1:
        # cube is not in database
        db_feed.add_permutation( perm_father )
        cube_count += 1
    if children == 0:
        # new cube, three sides to move
        for rotation in rotation_list:
            # load permutation into minicube
            cube.init_via_str(perm_father)
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
            # increase children in father
            db_feed.increase_permutation_children( perm_father )
            # check if cube exists and queue if not
            children = db_feed.get_number_of_children( perm_son )
            if children == -1:
                # insert son into database
                db_feed.add_permutation( perm_son )
                cube_perm_queue.put( perm_son )
                cube_count += 1
            # add relation
            db_feed.add_father_son_relation( perm_father, perm_son, cube_side )

    if step_count == 100:
        print(f'# cube_count = {cube_count}')
        print(f'# perm_father = {perm_father}')
        step_count = 0
        break


print('# close database connection')
db_feed.close()
print("# finished")