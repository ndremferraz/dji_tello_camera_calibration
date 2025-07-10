import numpy as np 
import cv2 

# Definition of CheckerBoard Dimensions
CHECKERBOARD = (6,9)
objpoints = []
imgpoints = []

criteria = (cv2.TERM_CRITERIA_EPS +cv2.TERM_CRITERIA_MAX_ITER, 309, 0.001)

# numpy array to store 3D coordinates
objp = np.zeros((1,CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1,2) * 0.0225


for i in range(1,8):

    image = cv2.imread(f"calibration_img{i}.jpg")
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret == True:

        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)

        imgpoints.append(corners2)

        image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)

    cv2.imshow('img', image)
    cv2.waitKey(0)

cv2.destroyAllWindows()

__, mtx, dist, __, __ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

fs =  cv2.FileStorage("camera_calibration.yaml", cv2.FILE_STORAGE_WRITE)
fs.write("camera_matrix", mtx)
fs.write("distortion_coeffs", dist)
fs.release()
    