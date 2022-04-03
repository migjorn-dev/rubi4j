# This is a sample Python script.
class minicube:
    ''' Minicube F(Front) U(Up) R(Right) B(Back) L(Left) D(Down)
        DD                 00 01
        DD                 02 03
        BB                 04 05
        BB                 06 07
     LL UU RR       08 09  12 13 16 17
     LL UU RR       10 11  14 15 18 19
        FF                 20 21
        FF                 22 23
         colors 0 1 2 3 4 5
         side order top, left, front, right, rear, bottom
     '''
    perm = [ 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
             3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5 ]
#    perm = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
#           12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    def perm_display(self):
        print(f'  .  .{self.perm[0]:2}.{self.perm[1]:2}.  .  ')
        print(f'  .  .{self.perm[2]:2}.{self.perm[3]:2}.  .  ')
        print(f'  .  .{self.perm[4]:2}.{self.perm[5]:2}.  .  ')
        print(f'  .  .{self.perm[6]:2}.{self.perm[7]:2}.  .  ')
        print(f'{self.perm[8]:2}.{self.perm[9]:2}.{self.perm[12]:2}.{self.perm[13]:2}.{self.perm[16]:2}.{self.perm[17]:2}')
        print(f'{self.perm[10]:2}.{self.perm[11]:2}.{self.perm[14]:2}.{self.perm[15]:2}.{self.perm[18]:2}.{self.perm[19]:2}')
        print(f'  .  .{self.perm[20]:2}.{self.perm[21]:2}.  .  ')
        print(f'  .  .{self.perm[22]:2}.{self.perm[23]:2}.  .  ')

    def rotate_up_clockwise_90(self):
        '''
        DD                 00 01
        DD                 02 03
        BB                 04 05
        BB                 06 07
     LL UU RR       08 09  12 13 16 17
     LL UU RR       10 11  14 15 18 19
        FF                 20 21
        FF
        '''
        # UP
        tmp = self.perm[12]
        self.perm[12] = self.perm[14]
        self.perm[14] = self.perm[15]
        self.perm[15] = self.perm[13]
        self.perm[13] = tmp
        # top layer sides
        tmp = self.perm[6]
        self.perm[6] = self.perm[11]
        self.perm[11] = self.perm[21]
        self.perm[21] = self.perm[16]
        self.perm[16] = tmp
        #
        tmp = self.perm[7]
        self.perm[7] = self.perm[9]
        self.perm[9] = self.perm[20]
        self.perm[20] = self.perm[18]
        self.perm[18] = tmp


    def flip_forward(self):
        '''
        DD                 00 01
        DD                 02 03
        BB                 04 05
        BB                 06 07
     LL UU RR       08 09  12 13 16 17
     LL UU RR       10 11  14 15 18 19
        FF                 20 21
        FF                 22 23
        '''
        # store down
        tmp1 = self.perm[0]
        tmp2 = self.perm[1]
        tmp3 = self.perm[2]
        tmp4 = self.perm[3]
        # FRONT -> DOWN
        self.perm[0] = self.perm[20]
        self.perm[1] = self.perm[21]
        self.perm[2] = self.perm[22]
        self.perm[3] = self.perm[23]
        # UP -> FRONT
        self.perm[20] = self.perm[12]
        self.perm[21] = self.perm[13]
        self.perm[22] = self.perm[14]
        self.perm[23] = self.perm[15]
        # BACK -> UP
        self.perm[12] = self.perm[4]
        self.perm[13] = self.perm[5]
        self.perm[14] = self.perm[6]
        self.perm[15] = self.perm[7]
        # stored DOWN -> BACK
        self.perm[4] = tmp1
        self.perm[5] = tmp2
        self.perm[6] = tmp3
        self.perm[7] = tmp4
        # rotate LEFT
        tmp           = self.perm[8]
        self.perm[8]  = self.perm[10]
        self.perm[10] = self.perm[11]
        self.perm[11] = self.perm[9]
        self.perm[9]  = tmp
        # rotate RIGHT
        tmp           = self.perm[16]
        self.perm[16] = self.perm[17]
        self.perm[17] = self.perm[19]
        self.perm[19] = self.perm[18]
        self.perm[18] = tmp


    def flip_left(self):
        '''
        DD                 00 01
        DD                 02 03
        BB                 04 05
        BB                 06 07
     LL UU RR       08 09  12 13 16 17
     LL UU RR       10 11  14 15 18 19
        FF                 20 21
        FF                 22 23
        '''
        # store UP
        tmp1 = self.perm[12]
        tmp2 = self.perm[13]
        tmp3 = self.perm[14]
        tmp4 = self.perm[15]
        # RIGHT -> UP
        self.perm[12] = self.perm[16]
        self.perm[13] = self.perm[17]
        self.perm[14] = self.perm[18]
        self.perm[15] = self.perm[19]
        # DOWN -> RIGHT
        self.perm[16] = self.perm[3]
        self.perm[17] = self.perm[2]
        self.perm[18] = self.perm[1]
        self.perm[19] = self.perm[0]
        # LEFT -> DOWN
        self.perm[0] = self.perm[11]
        self.perm[1] = self.perm[10]
        self.perm[2] = self.perm[9]
        self.perm[3] = self.perm[8]
        # UP -> LEFT
        self.perm[8]  = tmp1
        self.perm[9]  = tmp2
        self.perm[10] = tmp3
        self.perm[11] = tmp4
        # rotate FRONT
        tmp = self.perm[20]
        self.perm[20] = self.perm[21]
        self.perm[21] = self.perm[23]
        self.perm[23] = self.perm[22]
        self.perm[22] = tmp
        # rotate BACK
        tmp = self.perm[6]
        self.perm[6] = self.perm[7]
        self.perm[7] = self.perm[5]
        self.perm[5] = self.perm[4]
        self.perm[4] = tmp


    def rotate_cube_clockwise_90(self):
        '''
        rotate cube clockwise looking at UP surface
        DD                 00 01
        DD                 02 03
        BB                 04 05
        BB                 06 07
     LL UU RR       08 09  12 13 16 17
     LL UU RR       10 11  14 15 18 19
        FF                 20 21
        FF                 22 23
        '''
        # store BACK
        tmp1 = self.perm[4]
        tmp2 = self.perm[5]
        tmp3 = self.perm[6]
        tmp4 = self.perm[7]
        # LEFT -> BACK
        self.perm[4] = self.perm[10]
        self.perm[5] = self.perm[8]
        self.perm[6] = self.perm[11]
        self.perm[7] = self.perm[9]
        # FRONT -> LEFT
        self.perm[8]  = self.perm[22]
        self.perm[9]  = self.perm[20]
        self.perm[10] = self.perm[23]
        self.perm[11] = self.perm[21]
        # RIGHT -> FRONT
        self.perm[20]  = self.perm[18]
        self.perm[21]  = self.perm[16]
        self.perm[22] = self.perm[19]
        self.perm[23] = self.perm[17]
        # BACK (stored) -> RIGHT
        self.perm[16]  = tmp3
        self.perm[17]  = tmp1
        self.perm[18] =  tmp4
        self.perm[19] =  tmp2
        # rotate UP
        tmp = self.perm[12]
        self.perm[12] = self.perm[14]
        self.perm[14] = self.perm[15]
        self.perm[15] = self.perm[13]
        self.perm[13] = tmp
        # rotate
        tmp = self.perm[2]
        self.perm[2] = self.perm[0]
        self.perm[0] = self.perm[1]
        self.perm[1] = self.perm[3]
        self.perm[3] = tmp


    def corner_sum(self):
        # return color sum of corner 6-9-12
        return self.perm[6] + self.perm[9] + self.perm[12]


    def orientate_cube(self):
        # bring 0-1-2 colored corner on position 6-9-12
        i = 1
        # check all corner pieces
        while(i <= 8):
            sum = self.corner_sum()
            if (sum != 3):
                self.rotate_cube_clockwise_90()
            else:
                print( "Corner found!" )
                break
            i += 1
            if (i == 5): # 0-1-2 corner is not in top layer
                print( "ff " )
                self.flip_forward()
                self.flip_forward()
        # bring color 0 on position 12
        if self.perm[6] == 0:
            self.flip_forward()
            self.rotate_cube_clockwise_90()
        if self.perm[9] == 0:
            self.flip_left()
            self.flip_left()
            self.flip_left()
            self.rotate_cube_clockwise_90()
            self.rotate_cube_clockwise_90()
            self.rotate_cube_clockwise_90()


print('Hello rubi4j!')
cube = minicube()
cube.rotate_up_clockwise_90()
#cube.rotate_up_clockwise_90()
#cube.rotate_up_clockwise_90()

cube.flip_left()
#cube.flip_left()
#cube.flip_left()

cube.flip_forward()
#cube.flip_forward()
#cube.flip_forward()

cube.rotate_cube_clockwise_90()
#cube.rotate_cube_clockwise_90()
#cube.rotate_cube_clockwise_90()


print(cube.orientate_cube())
cube.perm_display()

#cube.perm_display()
#cube.rotate_cube_clockwise_90()

print("finished")
print(cube.corner_sum())
