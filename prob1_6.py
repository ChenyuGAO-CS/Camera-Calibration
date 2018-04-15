import cv2
import numpy as np
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('data\left\*.jpg')
#print(images)

for fname in images:
    img = cv2.imread(fname)
    #print(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #print(gray)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey()

#cv2.destroyAllWindows()
print(imgpoints)
print(objpoints)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print(mtx)
print(dist)
print(rvecs)
print(tvecs)

img = cv2.imread('.\left\left14.jpg')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
#cv2.imwrite('calibresult.png',dst)
cv2.imshow('dst',dst)
cv2.imshow('img',img)
cv2.waitKey()
cv2.destroyAllWindows()
