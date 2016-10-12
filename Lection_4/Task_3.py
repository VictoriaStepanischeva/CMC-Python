class Argument_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value
class Type_Error(TypeError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value
class Index_Error(IndexError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value
class Solve:
    def __ludecomposition(A):
        for j in range(len(A)):
            for i in range(j+1):
                current = A[i][j]
                for k in range(i):
                    current -= A[i][k]*A[k][j]
                A[i][j] = current
            for i in range(j + 1, len(A)):
                current = A[i][j]
                for k in range(j):
                    current -= A[i][k] * A[k][j]
                A[i][j] = current / A[j][j]

    def __lubksb(A, B):
        for i in range(len(A)):
            current = B[i]
            for j in range(i):
                current -= A[i][j] * B[j]
            B[i] = current
        for i in range(len(A) - 1, -1, -1):
            current = B[i]
            for j in range(i + 1, len(A)):
                current -= A[i][j] * B[j]
            B[i] = current / A[i][i]

    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.lu = A[:]
        self.x = B[:]
        __class__.__ludecomposition(self.lu)
        __class__.__lubksb(self.lu, self.x)
        if len(A)!=len(B):
            raise Argument_Error("Dimensions are not compatible")

    def __getitem__(self, i):
        if i<0 or i>=len(self.x):
            raise Index_Error("Solution index out of range")
        return self.x[i]

    def __setitem__(self, i, value):
        raise Type_Error("Object is immutable")


