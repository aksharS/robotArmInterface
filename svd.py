import numpy as np

# Estimate a rigid transform between 2 set of points of equal length
# through singular value decomposition(svd)
# return a rotation and a transformation matrix
def rigid_transform_3D(A, B):

    assert len(A) == len(B)
    A=  np.asmatrix(A)
    B=  np.asmatrix(B)
    N = A.shape[0]; 

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))
    H = AA.T * BB
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T * U.T

    # reflection case
    if np.linalg.det(R) < 0:
        Vt[2,:] *= -1
        R = Vt.T * U.T

    t = -R*centroid_A.T + centroid_B.T
    # rotation matrix
    R = np.array(R)
    # translation
    t = (np.array(t).T)[0]

    # B = np.dot(R, A.T).T+t
    # 4 by 4 homogeneous transformation matrix from rotation and translation
    transform = [[R[0][0],R[0][1],R[0][2],t[0]],
                 [R[1][0],R[1][1],R[1][2],t[1]],
                 [R[2][0],R[2][1],R[2][2],t[2]],
                 [0,0,0,1]]

    return (R,t)


# robot 
B = np.array([[-0.11431887416707531, 0.3814339111789867, 0.16166744365529034],
              [-0.014350266648788135, 0.38140851280398025, 0.16165468985917117],
              [-0.014314523546807956, 0.48137927721197304, 0.16165959281295927],
              [-0.014309627681186016, 0.4814272657949279, 0.2616369173640203],
              [-0.01431560412352087, 0.38143950685785866, 0.2616466171397615],
              [-0.11428422054600462, 0.38145571370346787, 0.261651204333932],
              [-0.11432693862951854, 0.4813831222707211, 0.1616735601212191],
              [-0.020596037526103284, 0.4621121306435147, 0.18773964635296073],
              [0.10987190944737607, 0.35636813948572776, 0.16413704214620695],
              [0.2057044530936424, 0.33441515718965453, 0.15205054482733726]])

# camera
A = np.array([[0.025832027196884155, -0.009813138283789158, 0.3440000116825104],
              [0.07331281155347824, -0.011647971346974373, 0.43300002813339233],
              [-0.014669965952634811, -0.00824673380702734, 0.48100003600120544],
              [-0.018499625846743584, -0.1079021617770195, 0.4790000319480896],
              [0.06963459402322769, -0.11206522583961487, 0.4320000112056732],
              [0.021920250728726387, -0.10993209481239319, 0.3440000116825104],
              [-0.061940453946590424, -0.006114500109106302, 0.39400002360343933],
              [-0.0005862417747266591, -0.03450866416096687, 0.4660000205039978],
              [0.15634188055992126, -0.016969691962003708, 0.534000039100647],
              [0.22380852699279785, -0.008460894227027893, 0.609000027179718]])

R, t = rigid_transform_3D(A, B)

print('Rotation: ', R)
print('Translation: ', t)

diff = 0

for i in range(len(A)):
    new_A = A[i]
    new_B = np.dot(R, new_A.T).T+t
    print("#########", i+1, "##############")
    print("observed: ", B[i])
    print("predicted: ", new_B)
    dist = np.sqrt(np.sum((B[i]-new_B)**2)) * 100
    print("Difference: ", dist)
    diff += dist

print("Average difference: ", diff/len(A))


inversed_R, inversed_t = rigid_transform_3D(B, A)

print('Inversed Rotation: ', inversed_R)
print('Inversed Translation: ', inversed_t)








