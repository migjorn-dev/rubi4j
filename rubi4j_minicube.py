# rubi4j minicube
# Version 1.2 (20.4.2022)
# Author: migjorn-dev
#
# define python class minicube to handle 2x2x2 rubiks cube
# to speed things up there is a explicite routine for rotating sides front, up, right
#
# minicube is stored in the following way and with following side labels
# F(Front) U(Up) R(Right) B(Back) L(Left) D(Down)
#
#        DD                 00 01
#        DD                 02 03
#        BB                 04 05
#        BB                 06 07
#     LL UU RR       08 09  12 13 16 17
#     LL UU RR       10 11  14 15 18 19
#        FF                 20 21
#        FF                 22 23
# colors 0 1 2 3 4 5
# the corner 0,1,2 is used for orientation and will remain on its place during all
# permutations. 


class minicube:
    corner_color_minimum = 3    # orientation corner is the one with the three lowest corner colors
    perm = [ 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
             3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5 ]
#    perm = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
#           12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    def checksum(self):
        sum = 0
        for i in range(len(self.perm)):
            sum += self.perm[i]
        return sum


    def perm_display(self):
        print(f'  .  .{self.perm[0]:2}.{self.perm[1]:2}.  .  ')
        print(f'  .  .{self.perm[2]:2}.{self.perm[3]:2}.  .  ')
        print(f'  .  .{self.perm[4]:2}.{self.perm[5]:2}.  .  ')
        print(f'  .  .{self.perm[6]:2}.{self.perm[7]:2}.  .  ')
        print(f'{self.perm[8]:2}.{self.perm[9]:2}.{self.perm[12]:2}.{self.perm[13]:2}.{self.perm[16]:2}.{self.perm[17]:2}')
        print(f'{self.perm[10]:2}.{self.perm[11]:2}.{self.perm[14]:2}.{self.perm[15]:2}.{self.perm[18]:2}.{self.perm[19]:2}')
        print(f'  .  .{self.perm[20]:2}.{self.perm[21]:2}.  .  ')
        print(f'  .  .{self.perm[22]:2}.{self.perm[23]:2}.  .  ')


    def perm_display_short(self):
        # display the permutation as one string of 24 bytes 
        #
        short = ""
        for i in range(len(self.perm)):
            short = short+str(self.perm[i])
        return short


    def rotate_up_clockwise_90(self):
        #   rotate up 90 clockwise
        #        DD                 00 01               00 01
        #        DD                 02 03               02 03
        #        BB                 04 05               04 05
        #        BB                 06 07               11 09
        #     LL UU RR       08 09  12 13 16 17   08 20 14 12 06 17
        #     LL UU RR       10 11  14 15 18 19   10 21 15 13 07 19
        #        FF                 20 21               18 16
        #        FF                 22 23               22 23
        #
        # copy a list to another list - a real copy!
        tmp = self.perm[:]
        self.perm[6]  = tmp[11]
        self.perm[7]  = tmp[9]
        self.perm[9]  = tmp[20]
        self.perm[12] = tmp[14]
        self.perm[13] = tmp[12]
        self.perm[16] = tmp[6]
        self.perm[11] = tmp[21]
        self.perm[14] = tmp[15]
        self.perm[15] = tmp[13]
        self.perm[18] = tmp[7]
        self.perm[20] = tmp[18]
        self.perm[21] = tmp[16]


    def rotate_right_clockwise_90(self):
        #   rotate right 90 clockwise
        #        DD                 00 01               00 05
        #        DD                 02 03               02 07
        #        BB                 04 05               04 13
        #        BB                 06 07               06 15
        #     LL UU RR       08 09  12 13 16 17   08 09 12 21 18 16
        #     LL UU RR       10 11  14 15 18 19   10 11 14 23 19 17
        #        FF                 20 21               20 01
        #        FF                 22 23               22 03
        #
        # copy a list to another list - a real copy!
        tmp = self.perm[:]
        self.perm[1]  = tmp[5]
        self.perm[3]  = tmp[7]
        self.perm[5]  = tmp[13]
        self.perm[7]  = tmp[15]
        self.perm[13] = tmp[21]
        self.perm[15] = tmp[23]
        self.perm[21] = tmp[1]
        self.perm[23] = tmp[3]
        self.perm[16] = tmp[18]
        self.perm[18] = tmp[19]
        self.perm[17] = tmp[16]
        self.perm[19] = tmp[17]


    def rotate_front_clockwise_90(self):
        #   rotate front 90 clockwise
        #        DD                 00 01               19 18
        #        DD                 02 03               02 03
        #        BB                 04 05               04 05
        #        BB                 06 07               06 07
        #     LL UU RR       08 09  12 13 16 17   08 09 12 13 16 17
        #     LL UU RR       10 11  14 15 18 19   01 00 10 11 14 15
        #        FF                 20 21               22 20
        #        FF                 22 23               23 21
        #
        # copy a list to another list - a real copy!
        tmp = self.perm[:]
        self.perm[10] = tmp[1]
        self.perm[11] = tmp[0]
        self.perm[14] = tmp[10]
        self.perm[15] = tmp[11]
        self.perm[18] = tmp[14]
        self.perm[19] = tmp[15]
        self.perm[20] = tmp[22]
        self.perm[21] = tmp[20]
        self.perm[22] = tmp[23]
        self.perm[23] = tmp[21]
        self.perm[0]  = tmp[19]
        self.perm[1]  = tmp[18]


    def flip_forward(self):
        # flip complete cube on its front side
        #
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
        # flip complete cube on its left side
        #
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
        # rotate complete cube clockwise looking at UP surface
        #
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
            if (sum != self.corner_color_minimum):
                self.rotate_cube_clockwise_90()
            else:
                break
            i += 1
            if (i == 5): # 0-1-2 corner is not in top layer
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


    def rotate_down_clockwise_90(self):
        self.flip_forward()
        self.flip_forward()
        self.rotate_up_clockwise_90()
        self.flip_forward()
        self.flip_forward()


    def init_via_str(self,perm_str):
        for i in range(len(perm_str)):
            self.perm[i] = int(perm_str[i])
