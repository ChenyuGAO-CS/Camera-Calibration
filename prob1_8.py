import numpy as np
import glob
import cv2
import math

def cal_v(i, j, h):
    v=np.zeros([6,1],dtype=np.float32)
    i = i-1
    j = j-1
    v[0,0] = h[0,i]*h[0,j]
    v[1,0] = h[0,i]*h[1,j]+h[1,i]*h[0,j]
    v[2,0] = h[1,i]*h[1,j]
    v[3,0] = h[2,i]*h[0,j]+h[0,i]*h[2,j]
    v[4,0] = h[2,i]*h[1,j]+h[1,i]*h[2,j]
    v[5,0] = h[2,i]*h[2,j]
    return v

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

images = glob.glob('data\left\*.jpg')

hm=np.ndarray([22,6],dtype=float)
tflag = int(0)
for fname in images:
    img = cv2.imread(fname)
    #print(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
    # If found, add object points, image points (after refining them)
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    if ret == True:
        objpoints.extend(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        for item in corners2:
            imgpoints.extend(item)
        # Draw and display the corners
        #img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        h, status = cv2.findHomography(np.array(objpoints), np.array(imgpoints))
        print(h)
        h1 = np.transpose(cal_v(1, 2, h))
        h2 = np.transpose(cal_v(1, 1, h) - cal_v(2, 2, h))
        # print(a1)
        hm[tflag, :] = h1[:]
        tflag = tflag + 1
        hm[tflag, :] = h2[:]
        tflag = tflag + 1
        #cv2.imshow('img',img)
        #cv2.waitKey()
#cv2.destroyAllWindows()

A=np.mat(hm)
A=np.dot(np.array(A).T.copy(),np.array(A))

ss,vv,dd = np.linalg.svd(np.dot(np.transpose(A),A))
idx=list(filter(lambda i:vv[i]==min(vv),range(0,len(vv))))[0]
x=dd[idx]
print(x)

B = np.zeros([4,4],dtype=np.float32)
B[1,1] = x[0]
B[1,2] = x[1]
B[2,2] = x[2]
B[1,3] = x[3]
B[2,3] = x[4]
B[3,3] = x[5]

cy = (B[1,2]*B[1,3]-B[1,1]*B[2,3])/(B[1,1]*B[2,2]-B[1,2]*B[1,2])
lamb = B[3,3]-(B[1,3]*B[1,3]+cy*(B[1,2]*B[1,3]-B[1,1]*B[2,3]))/B[1,1]
#print(lamb/B[1,1])
ax = math.sqrt(float(lamb/B[1,1]))
#print(float(lamb*B[1,1]/(B[1,1]*B[2,2]-B[1,2]*B[1,2])))
ay = math.sqrt(float(lamb*B[1,1]/(B[1,1]*B[2,2]-B[1,2]*B[1,2])))
s = -B[1,2]*ax*ax*ay/lamb
cx = s*cy/ay-B[1,3]*ax*ax/lamb

K = np.zeros([3,3],dtype=np.float32)
K[0,0] = ax
K[0,1] = s
K[0,2] = cx
K[1,1] = ay
K[1,2] = cy
K[2,2] = 1
print("intrinsics\n")
print(K)




