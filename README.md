# Camera Calibration


----------


This is an unofficial implementation of Z. Zhang, IEEE Transactions 2000. "A flexible new technique for camera calibration"


----------
#Data Prepare
All the data I used are in directory: data/left

----------
#Camera Calibration By OpenCV API
You can run prob1_6.py to see the camera calibration results and the undistrot images results

----------
#Camera Calibration
You can run main.py to see the camera calibration implementation without using function cv2.calibrateCamera().

###Other Functions
pic_data.py: Prepare data.
dlt.py: Caculate Homography of each images.
intrinsics.py: Caculate the intrinsics matrix.
extrinsics.py: Caculate the extrinsics matrix.


----------
#Other notes
1. The intrinsics caculate by using OpenCV API :
A =
 (534.07, 0, 0)
 (0, 534.12, 0)
 (341.53, 232.95, 1)

2. The intrinsics caculate by using my implementation:
A =
 (532.806, 0, 0)
 (1.521, 529.066, 0)
 (350.359, 225.710, 1)

3. Note by Chenyu Gao, Northwestern Polytechnical University, Xi'an, Apr, 2018
4. Any questions:   chenyugao.cs@gmail.com