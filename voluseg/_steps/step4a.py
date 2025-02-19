def define_blocks(lx, ly, lz, n_cells_block, n_voxels_cell, volume_mask):
    '''get coordinates of individual blocks'''

    import os
    # disable numpy multithreading
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
    import numpy as np

    # get initial estimate for the number of blocks
    n_blocks = lx * ly * lz / (n_cells_block * n_voxels_cell)

    # get initial block coordinates
    if lz == 1:
        part_block = np.round(np.sqrt(n_blocks)).astype(int)
        z0_range = np.array([0, 1])
    else:
        part_block = np.round(np.cbrt(n_blocks)).astype(int)
        z0_range = np.unique(np.round(np.linspace(0, lz, part_block+1)).astype(int))

    x0_range = np.unique(np.round(np.linspace(0, lx, part_block+1)).astype(int))
    y0_range = np.unique(np.round(np.linspace(0, ly, part_block+1)).astype(int))

    ijk, xyz = [], []
    for i, x0 in enumerate(x0_range):
        for j, y0 in enumerate(y0_range):
            for k, z0 in enumerate(z0_range):
                ijk.append([i, j, k])
                xyz.append([x0, y0, z0])

    dim = np.max(ijk, 0)
    XYZ = np.zeros(np.r_[dim+1, 3], dtype=int)
    XYZ[tuple(zip(*ijk))] = xyz

    xyz0, xyz1 = [], []
    for i in range(dim[0]):
        for j in range(dim[1]):
            for k in range(dim[2]):
                xyz0.append(XYZ[i  , j  ,   k])
                xyz1.append(XYZ[i+1, j+1, k+1])

    # get final block number and coordinates
    xyz0 = np.array(xyz0)
    xyz1 = np.array(xyz1)

    # get coordinates and number of blocks
    x0, y0, z0 = xyz0[:, 0], xyz0[:, 1], xyz0[:, 2]
    x1, y1, z1 = xyz1[:, 0], xyz1[:, 1], xyz1[:, 2]
    n_blocks = x0.size

    # get indices of masked blocks
    block_valids = np.ones(n_blocks, dtype=bool)
    for i in range(n_blocks):
        block_valids[i] = np.any(volume_mask[x0[i]:x1[i], y0[i]:y1[i], z0[i]:z1[i]])

    return n_blocks, block_valids, xyz0, xyz1
