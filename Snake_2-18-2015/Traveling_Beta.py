import Vector_Class
import math
import Snake_Class

A = Snake_Class.A
B = Snake_Class.B
C = Snake_Class.C
D = Snake_Class.D
E = Snake_Class.E
F = Snake_Class.F
G = Snake_Class.G

"""
Creates vectors between adjacent points
""" 
ABvector = Vector_Class.Vector(A,B)
BCvector = Vector_Class.Vector(B,C)
CDvector = Vector_Class.Vector(C,D)
DEvector = Vector_Class.Vector(D,E)
EFvector = Vector_Class.Vector(E,F)
FGvector = Vector_Class.Vector(F,G)


"""
Gets the forward momnet of the snakes head as a vector
"""
head_new_vector = Vector_Class.Vector([point_x_speed,0], [0,point_y_speed])

"""vector addition to get the resulting vectors from adding the bodys portions current 
direction and the perceding vectors direction
"""  
resulting_vector = ABvector.vector_addition(head_new_vector) # connects AB to head movemnet 
resulting_vectorBC = BCvector.vector_addition(ABvector)# relates BC to AB
resulting_vectorCD = CDvector.vector_addition(BCvector)
resulting_vectorDE = DEvector.vector_addition(CDvector)
resulting_vectorEF = EFvector.vector_addition(DEvector)
resulting_vectorFG = FGvector.vector_addition(EFvector)


"""
These if statments say that if the distance between two adjacent points 
are greater than 100, start moving the latter point in the direction of the 
resulting vector (which we calulated abouve)
"""
if distance(A,B) >= 100:
	B = [B[0] + resulting_vector[0], B[1] + resulting_vector[1]]
if distance(B,C) >= 100:
	C = [C[0] + resulting_vectorBC[0], C[1] + resulting_vectorBC[1]]
if distance(C,D) >= 100:
	D = [D[0] + resulting_vectorCD[0], D[1] + resulting_vectorCD[1]]
if distance(D,E) >= 100:
	E = [E[0] + resulting_vectorDE[0], E[1] + resulting_vectorDE[1]]
	#D = [D[0] + point_x_speed, D[1] + point_y_speed]
if distance(E,F) >= 100:
	F = [F[0] + resulting_vectorEF[0], F[1] + resulting_vectorEF[1]]
if distance(F,G) >= 100:
	G = [G[0] + resulting_vectorFG[0], G[1] + resulting_vectorFG[1]]
	#F = [F[0] + resulting_vector[0], F[1] + resulting_vector[1]]