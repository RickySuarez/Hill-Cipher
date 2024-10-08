import numpy as np

def cofactor(matrix, i, j):
    if matrix.shape[0] != matrix.shape[1]:
        raise Exception("Matrix is not square.")
    
    if matrix.shape[0] == 1:
        return 1
    
    sub = submatrix(matrix,i,j)
    return ((-1) ** (i+j)) * determinant(sub)
    
def determinant(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        raise Exception("Matrix is not square.")
    size = matrix.shape[0]

    if size == 1:
        return matrix[0][0]
        
    det = 0
    for x in range(size):
        sub = submatrix(matrix, 0, x)
        det = ((det + ((-1) ** x) * matrix[0][x] * determinant(sub)) % 256) % 256
        
    return det
    
def submatrix(matrix, i, j):
    size = matrix.shape[0]
    ls = []
    for x in range(size):
        if x != i:
            tmp = []
            for y in range(size):
                if y != j:
                    tmp.append(matrix[x][y])
            ls.append(tmp)
    return np.array(ls)  
    
def transpose(matrix):
    rows = matrix.shape[0]
    columns = matrix.shape[1]
    ls = []
    for x in range(rows):
        tmp = []
        for y in range(columns):
            tmp.append(matrix[y][x])
        ls.append(tmp)
    return np.array(ls)
    
def adjoint(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        raise Exception("Matrix is not square.")
    
    size = matrix.shape[0]

    ls = []
    for x in range(size):
        tmp = []
        for y in range(size):
            tmp.append(cofactor(matrix,x,y))
        ls.append(tmp)
        
    return transpose(np.array(ls))