from math import sin, cos, pi

class Matrix:
    def __init__(self):
        self.matrix = [[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0],]

    def __repr__(self):
        return "[%f %f %f]\n[%f %f %f]\n[%f %f %f]"%(self.matrix[0][0], 
                                                     self.matrix[0][1],
                                                     self.matrix[0][2],

                                                     self.matrix[1][0],
                                                     self.matrix[1][1],
                                                     self.matrix[1][2],

                                                     self.matrix[2][0],
                                                     self.matrix[2][1],
                                                     self.matrix[2][2],)
    def __mul__(self, matrix2):
        m1 = self.matrix
        m2 = matrix2.matrix
        res = Matrix()
        res.matrix = [[m1[0][0] * m2[0][0] +
                       m1[1][0] * m2[0][1] +
                       m1[2][0] * m2[0][2],
                       
                       m1[0][1] * m2[0][0] +
                       m1[1][1] * m2[0][1] +
                       m1[2][1] * m2[0][2],
                       
                       m1[0][2] * m2[0][0] +
                       m1[1][2] * m2[0][1] +
                       m1[2][2] * m2[0][2],],
                      
                       [m1[0][0] * m2[1][0] +
                        m1[0][1] * m2[1][1] +
                        m1[0][2] * m2[1][2],
                        
                        m1[0][1] * m2[1][0] +
                        m1[1][1] * m2[1][1] +
                        m1[2][1] * m2[1][2],
                        
                        m1[0][2] * m2[1][0] +
                        m1[1][2] * m2[1][1] +
                        m1[2][2] * m2[1][2] ,],
                       
                       [m1[0][0] * m2[2][0] +
                        m1[1][0] * m2[2][1] +
                        m1[2][0] * m2[2][2],

                        m1[0][1] * m2[2][0] +
                        m1[1][1] * m2[2][1] +
                        m1[2][1] * m2[2][2],
                        
                        m1[0][2] * m2[2][0] +
                        m1[1][2] * m2[2][1] +
                        m1[2][2] * m2[2][2],]]
        return res


    def __add__(self, m2):
        pass


class Identity(Matrix):
    # Yeah I know it's the same, call it a vanity class :)
    pass

class Rotation(Matrix):
    def __init__(self, rot):
        Matrix.__init__(self)
        self.matrix[0][0] = cos(rot);
        self.matrix[0][1] = sin(rot);

        self.matrix[1][0] = -sin(rot);
        self.matrix[1][1] = cos(rot);

class Translation(Matrix):
    def __init__(self, trans):
        Matrix.__init__(self)
        self.matrix[0][2] = trans.matrix[0];
        self.matrix[1][2] = trans.matrix[1];

class Scale(Matrix):
    def __init__(self, scale):
        Matrix.__init__(self)
        self.matrix[0][0] = scale.matrix[0];
        self.matrix[1][1] = scale.matrix[1];

class Vector:
    def __init__(self, x, y):
        self.matrix = [x, y, 1]
    
    def __repr__(self):
        return "[%f %f %f]"%(self.matrix[0],
                             self.matrix[1],
                             self.matrix[2])

    def __add__(self, v2):
        return Vector(self.matrix[0] + v2.matrix[0], 
                      self.matrix[1] + v2.matrix[1])

    def __mul__(self, matrix):
        v = self.matrix
        m = matrix.matrix
        
        res = Vector(0, 0)
        res.matrix = [m[0][0] * v[0] + 
                      m[0][1] * v[1] +
                      m[0][2] * v[2],
                     
                      m[1][0] * v[0] + 
                      m[1][1] * v[1] +
                      m[1][2] * v[2],
        
                      m[2][0] * v[0] + 
                      m[2][1] * v[1] +
                      m[2][2] * v[2]]
        return res
        
def test():
    print "Test"
    ident = Identity()
    tra = Translation(Vector(2, 3))
    rot = Rotation(pi / 2)
    scl = Scale(Vector(4.0, 5.0))

    print tra
    print '='
    print ident * tra
    print '---'

    print rot
    print '='
    print ident * rot
    print '---'

    print scl
    print '='
    print ident * scl
    print '---'

    v1 = Vector(1, 1)
    print v1 * tra
    print '---'
    print v1 * rot
    print '---'
    print v1 * scl

                                           
    

