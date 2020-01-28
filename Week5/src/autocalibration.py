import numpy as np

import utils as h
import reconstruction as rc
import maths as mth

def estimate_aff_hom(cams, vps):
    # your code here
    C1 = cams[-2]
    C2 = cams[-1]

    vps1 = vps[-2]
    vps2 = vps[-1]

    es = rc.estimate_3d_points(C1, C2, vps1.T, vps2.T)
    es = es/(es[3])
    A = [es.T]
    U, S, V = np.linalg.svd(A)

    Ha = V.T[:, 3];
    Ha = Ha/Ha[3]

    aff_hom = np.identity(4)
    aff_hom[3,:] = Ha.T

    return aff_hom 

def estimate_euc_hom(cams_aff, vps):

    u = vps[0]
    v = vps[1]
    z = vps[2]
    #print("________________ ESTIMATE EUC HOM _______________-")
    #print(u, v, z) #[1681.7798 1449.4006] [-50431.625    2681.8096] [  1116.6058 -16080.212 ]

    row1 = [u[0]*v[0], u[0]*v[1]+u[1]*v[0], u[0]*1+1*v[0], u[1]*v[1], u[1]*1+1*v[1], 1*1]
    row2 = [u[0]*z[0], u[0]*z[1]+u[1]*z[0], u[0]*1+1*z[0], u[1]*z[1], u[1]*1+1*z[1], 1*1]
    row3 = [v[0]*z[0], v[0]*z[1]+v[1]*z[0], v[0]*1+1*z[0], v[1]*z[1], v[1]*1+1*z[1], 1*1]
    row4 = [0,1,0,0,0,0]
    row5 = [1,0,0,-1,0,0]

    A = np.vstack((row1,row2,row3,row4,row5))

    U, S, V = np.linalg.svd(A)

    W = V.T[:,-1]


    row1 = [W[0], W[1], W[2]]
    row2 = [W[1], W[3], W[4]]
    row3 = [W[2], W[4], W[5]]
    M = cams_aff[:, 0:2]
    Wp  =  np.vstack((row1,row2,row3))
    r = M.T @ Wp @ M
    ri = np.linalg.inv(r)
    A = np.linalg.cholesky(ri)

    Ha = np.eye(4, 4)
    Ha[0: 2, 0: 2] = np.linalg.inv(A)
    return Ha