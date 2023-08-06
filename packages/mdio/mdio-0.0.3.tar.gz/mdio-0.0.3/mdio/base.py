import numpy as np
class Frame(object):
    """
    A frame of trajectory data.
    
    """
    def __init__(self, crds, box=None, time=0.0, precision=1000, timestep = 1.0):
        crds = np.array(crds, dtype=np.float32)
        if len(crds.shape) != 2:
            raise TypeError('Error - crds must be a [N,3] array.')
        if crds.shape[1] != 3:
            raise TypeError('Error - crds must be a [N,3] array.')
        self.natoms = crds.shape[0]
        self.crds = crds
        if box is not None:
            box = np.array(box, dtype=np.float32)
            if len(box.shape) == 1 and len(box) == 6:
                tbox = np.zeros((3,3), dtype=np.float32)
                tbox[0, 0] = box[0]
                tbox[1, 0] = box[1]
                tbox[1, 1] = box[2]
                tbox[2, 0] = box[3]
                tbox[2, 1] = box[4]
                tbox[2, 2] = box[5]
                box = tbox
            elif box.shape != (3,3):
                raise ValueError('Error - unrecognised box data {}'.format(box))
        self.box = box
        self.time = float(time)
        self.precision = int(precision)
        self.timestep = timestep
