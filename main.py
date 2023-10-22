from nbtschematic import SchematicFile
import numpy as np
import math
import os

n = 8
dim = 100
pos = []
max_iter = 20
edge = 2 * dim + 1
blocks = [ 238, 244, 246, 248, 240, 239, 236, 247, 249, 241, 237, 245, 250, 242, 243, 235 ] # blocks and block ids are given at the end

def find_r(z):
    return math.sqrt(z[0]**2 + z[1]**2 + z[2]**2)

'''
You can play around with the block pallete and change the colours. You can swap the blocks with different block ids.
You can even change the logic that the function uses to colour the mandelbulb. I have used a very staight forward one here.
'''

def find_block(vec):
    length = len(blocks)
    x, y, z = vec[0] - dim, vec[1] - dim, vec[2] - dim
    r = int(math.sqrt(x**2 + y**2 + z**2))
    idx = r % length
    return idx

# make the array of positions
for i in range(-dim,dim + 1):
    for j in range(-dim, dim + 1):
        for k in range(-dim, dim + 1):
            pos.append([i,j,k])

pos = np.array(pos, dtype=float)
c = pos*1.5/dim
zeta = np.zeros_like(pos)
iters = np.zeros((c.shape[0], 1), dtype=int)

for i in range(max_iter):
    os.system("cls")
    print(f"Progress: { i*100/max_iter}%")

    # transform function
    '''
        refer below for the formula used :-
        https://www.skytopia.com/project/fractal/2mandelbulb.html#formula
    '''
    zeta2 = zeta.copy()
    r = np.sqrt(zeta2[:, 0]**2 + zeta2[:, 1]**2 + zeta2[:, 2]**2) # I had put zeta2[:, 1] instead of zeta2[:, 2] and went on to debug for next 2 days :)
    theta = np.arctan2( np.sqrt(zeta2[:, 0]**2 + zeta2[:, 1]**2) , zeta2[:,2])
    phi = np.arctan2(zeta2[:,1],zeta2[:,0])
    
    rn = r**n
    thetan = theta * n
    phin = phi * n

    zeta2[:,0] = rn * np.sin(thetan) * np.cos(phin)
    zeta2[:,1] = rn * np.sin(thetan) * np.sin(phin)
    zeta2[:,2] = rn * np.cos(thetan)

    zeta2 = zeta2 + c
    # if values not diverted save them for other iteration
    mask = (r <= 2)
    mask = np.where(mask)
    zeta[mask] = zeta2[mask]
    iters[mask] += 1

os.system("cls")
print("Progress: 100%")

# print(iter_pos[:25])
mandelbulb = np.zeros((edge, edge, edge), dtype=int)

for i in range(iters.shape[0]):
    if 3 < iters[i] and find_r(zeta[i]) >= 2:
        mandelbulb[int(pos[i][2] + dim), int(pos[i][0] + dim), int(pos[i][1] + dim)] = 1

# save in schematic file

# IndexError: index 200 is out of bounds for axis 1 with size 200
# so I made the size 201
sf = SchematicFile(shape=(edge, edge, edge))
assert sf.blocks.shape == (edge, edge, edge)
for i in range(edge):
    for j in range(edge):
        for k in range(edge):
            if mandelbulb[i][j][k] == 1:
                bk = find_block([ i, j, k])
                sf.blocks[i,j,k] = blocks[bk]
sf.save('final.schematic')
print("Saved the schematic file.")

'''
minecraft block ids :-

    Light_blue_glazed_terracotta: 238
    cyan_glazed_terracotta: 244
    blue_glazed_terracotta: 246
    green_glazed_terracotta: 248
    lime_glazed_terracotta: 240
    yellow_glazed_terracotta: 239
    orange_glazed_terracotta: 236
    brown_glazed_terracotta: 247
    red_glazed_terracotta: 249
    pink_glazed_terracotta: 241
    magenta_glazed_terracotta: 237
    purple_glazed_terracotta: 245
    black_glazed_terracotta: 250
    gray_glazed_terracotta: 242
    light_gray_glazed_terracotta: 243
    white_glazed_terracotta: 235
'''
