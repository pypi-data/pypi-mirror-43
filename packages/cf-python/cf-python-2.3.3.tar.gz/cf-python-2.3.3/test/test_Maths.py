# -*- coding: utf-8 -*-
import os
import unittest
import inspect

import numpy
from scipy.ndimage import convolve1d
from scipy.signal import get_window

import cf

class MathTest(unittest.TestCase):
    filename1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'file1.nc')

    chunk_sizes = (300, 10000, 100000)[::-1]
    original_chunksize = cf.CHUNKSIZE()
    
    test_only = []
#    test_only = ('NOTHING!!!!!',)
#    test_only = ('test_Field_convolution_filter')
#    test_only = ('test_Field_derivative')
#    test_only = ('test_relative_vorticity_distance')
#    test_only = ('test_relative_vorticity_latlong')

    def test_Field_convolution_filter(self):
#        return
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return
            
        weights = numpy.ones(5)/5.0

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)

            f = cf.read(self.filename1)[0]
            
            # Test user weights in different modes
            for mode in ('reflect', 'constant', 'nearest', 'mirror', 'wrap'):
                g = f.convolution_filter(('user', weights), mode=mode, cval=0.0)
                self.assertTrue((g.array == convolve1d(f.array, weights,
                                                       mode=mode)).all())
            #--- End: for

            # Test named filters with default parameters
            for window in ('boxcar', 'triang', 'blackman', 'hamming', 'hann',
                           'bartlett', 'flattop', 'parzen', 'bohman',
                           'blackmanharris', 'nuttall', 'barthann', 'cosine',
                           ('kaiser', 5), ('gaussian', 2.5),
                           ('general_gaussian',0.5, 2.5),
                           ('slepian', 0.3), ('chebwin', 50), ('tukey', 1)):
                g = f. convolution_filter(window, 5, mode='reflect')
                self.assertTrue((g.array == convolve1d(f.array,
                                    get_window(window, 5, False))).all())
            #--- End: for

            # Exponential window is a special case
            g = f.convolution_filter(('exponential', 2.5), 5, mode='reflect')
            self.assertTrue((g.array == convolve1d(f.array,
                    get_window(('exponential', None, 2.5), 5, False))).all())
        #--- End: for

        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def

    def test_Field_derivative(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        x_min = 0.0
        x_max = 359.0
        dx = 1.0

        x_1d = numpy.arange(x_min, x_max, dx)

        data_1d = x_1d*2.0 + 1.0

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)

            dim_x = cf.DimensionCoordinate(data=cf.Data(x_1d, 's'),
                                           properties={'axis': 'X'})

            f = cf.Field()
            f.insert_dim(dim_x)
            f.insert_data(cf.Data(data_1d, 'm'), axes='X')
            f.cyclic('X', period=360.0)

            g = f.derivative('X')
            self.assertTrue((g.array == 2.0).all())

            g = f.derivative('X', one_sided_at_boundary=True)
            self.assertTrue((g.array == 2.0).all())

            g = f.derivative('X', cyclic=True)
            self.assertTrue((g.array == 2.0).all())
        #--- End: for

        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def
    
    def test_relative_vorticity_distance(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        x_min = 0.0
        x_max = 100.0
        dx = 1.0

        x_1d = numpy.arange(x_min, x_max, dx)
        size = x_1d.size

        data_1d = x_1d*2.0 + 1.0
        data_2d = numpy.broadcast_to(data_1d[numpy.newaxis, :], (size, size))

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)

            dim_x = cf.DimensionCoordinate(data=cf.Data(x_1d, 'm'),
                                           properties={'axis': 'X'})
            dim_y = cf.DimensionCoordinate(data=cf.Data(x_1d, 'm'),
                                           properties={'axis': 'Y'})

            u = cf.Field()
            u.insert_dim(dim_x)
            u.insert_dim(dim_y)
            u.insert_data(cf.Data(data_2d, 'm/s'), axes=('Y', 'X'))

            v = cf.Field()
            v.insert_dim(dim_x)
            v.insert_dim(dim_y)
            v.insert_data(cf.Data(data_2d, 'm/s'), axes=('X', 'Y'))
            
            rv = cf.relative_vorticity(u, v, one_sided_at_boundary=True)
            self.assertTrue((rv.array == 0.0).all())
        #--- End: for

        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def

    def test_relative_vorticity_latlong(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        lat_min = -90.0
        lat_max = 90.0
        dlat = 1.0

        lat_1d = numpy.arange(lat_min, lat_max, dlat)
        lat_size = lat_1d.size

        lon_min = 0.0
        lon_max = 359.0
        dlon = 1.0

        lon_1d = numpy.arange(lon_min, lon_max, dlon)
        lon_size = lon_1d.size

        u_1d = lat_1d*2.0 + 1.0
        u_2d = numpy.broadcast_to(lat_1d[numpy.newaxis, :],
                                  (lon_size, lat_size))

        v_1d = lon_1d*2.0 + 1.0
        v_2d = numpy.broadcast_to(lon_1d[:, numpy.newaxis],
                                  (lon_size, lat_size))
        v_2d = v_2d*numpy.cos(lat_1d*numpy.pi/180.0)[numpy.newaxis, :]

        rv_array = (u_2d/cf.radius_of_earth()
                    *numpy.tan(lat_1d*numpy.pi/180.0)[numpy.newaxis, :])

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)

            dim_x = cf.DimensionCoordinate(data=cf.Data(lon_1d, 'degrees_east'),
                                           properties={'axis': 'X'})
            dim_y = cf.DimensionCoordinate(data=cf.Data(lat_1d,'degrees_north'),
                                           properties={'axis': 'Y'})

            u = cf.Field()
            u.insert_dim(dim_x)
            u.insert_dim(dim_y)
            u.insert_data(cf.Data(u_2d, 'm/s'), axes=('X', 'Y'))
            u.cyclic('X', period=360.0)

            v = cf.Field()
            v.insert_dim(dim_x)
            v.insert_dim(dim_y)
            v.insert_data(cf.Data(v_2d, 'm/s'), axes=('X', 'Y'))
            v.cyclic('X', period=360.0)
            
            rv = cf.relative_vorticity(u, v, cyclic=True)
            self.assertTrue(numpy.allclose(rv.array, rv_array))
        #--- End: for

        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def

if __name__ == "__main__":
    print 'cf-python version:'     , cf.__version__
    print 'cf-python path:'        , os.path.abspath(cf.__file__)
    print ''
    unittest.main(verbosity=2)
