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

    def round_off(self, ndigits):
        self.matrix = [[round(x, ndigits) for x in self.matrix[0]],
                       [round(x, ndigits) for x in self.matrix[1]],
                       [round(x, ndigits) for x in self.matrix[2]],]
        return self

    def __eq__(self, matrix2):
        if type(matrix2).__name__ == 'list':
            return matrix2 == self.matrix
        else:
            return matrix2.matrix == self.matrix

    def __ne__(self, matrix2):
        if type(matrix2).__name__ == 'list':
            return matrix2 != self.matrix
        else:
            return matrix2.matrix != self.matrix

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
                        m1[1][0] * m2[1][1] +
                        m1[2][0] * m2[1][2],
                        
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
        self.matrix[0][1] = -sin(rot);

        self.matrix[1][0] = sin(rot);
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

def t2():
    m1 = Matrix()
    m1.matrix = [[0.5, -0.5, 0.0],
                 [0.5, 0.5, 0.0],
                 [0.0, 0.0, 1.0]]
    m2 = Matrix()
    m2.matrix = [[2.0, 0.0, 0.0],
                 [0.0, 4.0, 0.0],
                 [0.0, 0.0, 1.0]]

    print m1 * m2
    print
    print m2 * m1

def test_case(name, want, got):
    print "%s: %s"%(name, ("Pass" if want == got else "Fail"))
    if want != got:
        print "Wanted:"
        print want
        print "Got:"
        print got
        
def test():
    print "Test"
    ident = Identity()
    tra = Translation(Vector(2, 3))
    rot = Rotation(pi / 4)
    scl = Scale(Vector(4, 5))

    test_case("id * id", [[1.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0]],
              ident * ident)
            
    test_case("id * scl", [[4.0, 0.0, 0.0],
                           [0.0, 5.0, 0.0],
                           [0.0, 0.0, 1.0],],
              ident * scl)

    test_case("scl * id", [[4.0, 0.0, 0.0],
                           [0.0, 5.0, 0.0],
                           [0.0, 0.0, 1.0],],
              scl * ident)

    test_case("id * tra", [[1.0, 0.0, 2.0],
                           [0.0, 1.0, 3.0],
                           [0.0, 0.0, 1.0],],
              ident * tra)

    test_case("tra * id", [[1.0, 0.0, 2.0],
                           [0.0, 1.0, 3.0],
                           [0.0, 0.0, 1.0],],
              tra * ident)


    test_case("id * rot", [[0.707107, -0.707107, 0.000000],
                           [0.707107, 0.707107, 0.000000],
                           [0.000000, 0.000000, 1.000000],],
              (ident * rot).round_off(6))

    test_case("rot * id", [[0.707107, -0.707107, 0.000000],
                           [0.707107, 0.707107, 0.000000],
                           [0.000000, 0.000000, 1.000000],],
              (rot * ident).round_off(6))

    # SCALE
    test_case("scl * tra", [[4.0, 0.0, 2.0],
                            [0.0, 5.0, 3.0],
                            [0.0, 0.0, 1.0],],
              scl * tra)

    test_case("tra * scl", [[4.0, 0.0, 8.0],
                            [0.0, 5.0, 15.0],
                            [0.0, 0.0, 1.0],],
              tra * scl)

    test_case("scl * scl", [[16.0, 0.0, 0.0],
                            [0.0, 25.0, 0.0],
                            [0.0, 0.0, 1.0],],
              scl * scl)
    
    test_case("scl * rot", [[2.828427, -3.535534,  0.000000],
                            [2.828427,  3.535534,  0.000000],
                            [0.000000,  0.000000,  1.000000],],
              (scl * rot).round_off(6))

    test_case("rot * scl", [[2.828427, -2.828427, 0.000000],
                            [3.535534,  3.535534, 0.000000],
                            [0.000000,  0.000000, 1.000000],],
              (rot * scl).round_off(6))

    # TRANSLATION
    test_case("tra * tra", [[1.0, 0.0, 4.0],
                            [0.0, 1.0, 6.0],
                            [0.0, 0.0, 1.0],],
              tra * tra)

    test_case("tra * rot", [[0.707107, -0.707107, -0.707107],
                            [0.707107, 0.707107, 3.535534],
                            [0.000000, 0.000000, 1.000000],],
              (tra * rot).round_off(6))

    test_case("rot * tra", [[0.707107, -0.707107, 2.000000],
                            [0.707107, 0.707107, 3.000000],
                            [0.000000, 0.000000, 1.000000],],
              (rot * tra).round_off(6))

    # ROTATION
    test_case("rot * rot", [[0.0, -1.0, 0.0],
                            [1.0, 0.0 ,0.0],
                            [0.0, 0.0, 1.0],],
              (rot * rot).round_off(6))

