import struct
import numpy as np

def read_record(f, expectedbytes=None, id='data'):
    nbytes = struct.unpack('i', f.read(4))[0]
    buf = f.read(nbytes)
    check = struct.unpack('i', f.read(4))[0]
    if check != nbytes:
        raise ValueError('Error - malformed record in DCD file.')
    if expectedbytes is not None:
        if nbytes != expectedbytes:
            raise IOError('Error reading {} from DCD file.'.format(id))
    return buf

def write_record(f, buf):
    nbytes = len(buf)
    f.write(struct.pack('i', nbytes))
    f.write(struct.pack('{}s'.format(nbytes), buf))
    f.write(struct.pack('i', nbytes))

class DCDHeader(object):
    """
    The header block for a DCD file.
    """
    def __init__(self, istart=1, nsavec=0, deltat=1.0, version=24, extra=0):
        self.istart = istart
        self.nsavec = nsavec
        self.deltat = deltat
        self.version = version
        self.nsets = 0
        self.extra = extra


def read_dcd_header(f):
    f.seek(0)
    buf = read_record(f, 84, 'header')
    magic = struct.unpack('4s', buf[:4])[0]
    if magic.decode('utf-8') != 'CORD':
        raise IOError('Error - this does not seem to be a DCD format file ({}).'.format(magic))
    header = DCDHeader()
    header.version = struct.unpack('i', buf[80:])[0]
    header.extra = struct.unpack('i', buf[44:48])[0]
    header.nsets, header.istart, header.nsavec = struct.unpack('3i', buf[8:20])
    header.deltat = struct.unpack('f', buf[40:44])[0]
    return header

def write_dcd_header(f, header):
    f.seek(0)
    buf = bytearray(84)
    buf[:4] = struct.pack('4s', b'CORD')
    buf[8:20] = struct.pack('3i', header.nsets, header.istart, header.nsavec)
    buf[40:48] = struct.pack('fi', header.deltat, header.extra)
    buf[80:] = struct.pack('i', header.version)
    write_record(f, buf)
    
def update_dcd_header(f, nsavec, deltat=None):
    here = f.tell()
    f.seek(20)
    f.write(struct.pack('i', nsavec))
    if deltat is not None:
        f.seek(44)
        f.write(struct.pack('f', deltat))
    f.seek(here)

def read_dcd_titles(f):
    buf = read_record(f)
    ntitle = struct.unpack('i', buf[:4])[0]
    if (len(buf) - 4) // 80 != ntitle:
        raise IOError('Error - cannot read title info from DCD file.')
    titles = []
    for i in range(ntitle):
        offset = 4 + (80 * i)
        titles.append(struct.unpack('80s', buf[offset:offset+80])[0])
    return titles

def write_dcd_titles(f, titles):
    ntitles = len(titles)
    buf = bytearray(4 + 80 * ntitles)
    buf[:4] = struct.pack('i', ntitles)
    for i in range(ntitles):
        offset = 4 + (80 * i)
        title = titles[i]
        lt = len(title)
        lt = min(lt, 80)
        if isinstance(title, str):
            title = bytes(title[:lt], 'utf-8')
        
        buf[offset:offset+lt] = struct.pack('{}s'.format(lt), title)
    write_record(f, buf)

def read_dcd_natoms(f):
    buf = read_record(f, 4, 'natoms')
    natoms = struct.unpack('i', buf)[0]
    return natoms

def write_dcd_natoms(f, natoms):
    buf = struct.pack('i', natoms)
    write_record(f, buf)
    
def read_dcd_unit_cell(f):
    buf = read_record(f, 48, 'box data')
    unit_cell_info = struct.unpack('6d', buf)
    return unit_cell_info

def write_dcd_unit_cell(f, unit_cell_data):
    if len(unit_cell_data) != 6:
        raise IOError('Error - must be 6 values in unit cell data list.')
    buf = struct.pack('6d', *unit_cell_data)
    write_record(f, buf)

def read_dcd_coordinates(f, natoms):
    buf = read_record(f, natoms * 4, 'x-coordinates')
    x = struct.unpack('{}f'.format(natoms), buf)
    buf = read_record(f, natoms * 4, 'y-coordinates')
    y = struct.unpack('{}f'.format(natoms), buf)
    buf = read_record(f, natoms * 4, 'z-coordinates')
    z = struct.unpack('{}f'.format(natoms), buf)
    return [list(c) for c in zip(x,y,z)]

def write_dcd_coordinates(f, crds):
    x = [c[0] for c in crds]
    natoms = len(x)
    xbuf = struct.pack('{}f'.format(natoms), *x)
    write_record(f, xbuf)
    y = [c[1] for c in crds]
    write_record(f, struct.pack('{}f'.format(natoms), *y))
    z = [c[2] for c in crds]
    write_record(f, struct.pack('{}f'.format(natoms), *z))

class Frame(object):
    """
    A frame of trajectory data.
    
    """
    def __init__(self, crds, box=None, time=0.0, precision=None, timestep=1.0):
        crds = np.array(crds, dtype=np.float32)
        if len(crds.shape) != 2:
            raise TypeError('Error - crds must be a [N,3] array')
        if crds.shape[1] != 3:
            raise TypeError('Error - crds must be a [N,3] array')
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
        self.time = time
        self.timestep = timestep
        self.precision = precision


class DCDFileReader(object):
    def __init__(self, f):
        self.f  = f
        self.header = read_dcd_header(f)
        self.titles = read_dcd_titles(f)
        self.natoms = read_dcd_natoms(f)
        self.hasbox = self.header.extra == 1
        self.framecount = 0
        self.nframes = self.header.nsavec
        
    def __del__(self):
        try:
            self.f.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
    
    def close(self):
        self.f.close()
        
    def read_frame(self):
        if self.framecount >= self.nframes:
            return None
        if self.hasbox:
            box = read_dcd_unit_cell(self.f)
        else:
            box = None
        crds = read_dcd_coordinates(self.f, self.natoms)
        self.framecount += 1
        timestep = self.header.istart + self.framecount - 1
        time = timestep * self.header.deltat
        frame = Frame(crds, box, time=time, timestep=timestep)
        return frame
        
class DCDFileWriter(object):
    def __init__(self, f, titles=['Created by DCDFileWriter']):
        self.f = f
        self.header = None
        self.titles = titles
        self.natoms = None
        self.hasbox = None
        self.framecount = 0
        self.deltat = None
        
    def __del__(self):
        try:
            self.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        
    def close(self):
        if self.header is not None:
            if self.deltat < 0:
                self.deltat = 1.0
            update_dcd_header(self.f, self.framecount, self.deltat)
        self.f.close()
        
        
    def write_frame(self, frame):
        if self.natoms is None:
            self.natoms = frame.natoms
            self.hasbox = frame.box is not None
        elif self.natoms != frame.natoms:
            raise IOError('Error - expected {} atoms in frame, found {}.'.format(self.natoms, frame.natoms))
        
        if self.hasbox and (frame.box is None):
            raise IOError('Error - frame is missing box data.')
        if not self.hasbox and (frame.box is not None):
            raise IOError('Error - frame has unexpected box data.')
            
        if self.header is None:
            self.header = DCDHeader()
            if self.hasbox:
                self.header.extra = 1
            else:
                self.header.extra = 0
            write_dcd_header(self.f, self.header)
            write_dcd_titles(self.f, self.titles)
            write_dcd_natoms(self.f, self.natoms)
        if self.deltat is None:
            self.deltat = -frame.time
        elif self.deltat < 0:
            self.deltat += frame.time
        if self.hasbox:
            box = frame.box
            tbox = [box[0,0]]
            tbox.append(box[1,0])
            tbox.append(box[1,1])
            tbox.append(box[2,0])
            tbox.append(box[2,1])
            tbox.append(box[2,2])
            write_dcd_unit_cell(self.f, tbox)
        write_dcd_coordinates(self.f, frame.crds)
        self.framecount += 1

def dcd_open(filename, mode='r'):
    if not mode in ['r', 'w']:
        raise ValueError('Error - mode must be "r" or "w".')
    if mode == 'r':
        f = open(filename, 'rb')
        filehandler = DCDFileReader(f)
    elif mode == 'w':
        f = open(filename, 'wb')
        filehandler = DCDFileWriter(f)
    return filehandler
