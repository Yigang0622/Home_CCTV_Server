# Home_CCTV_Server
# test 
# Created by Yigang Zhou on 2020-01-09.
# Copyright © 2020 Yigang Zhou. All rights reserved.

import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
frame_rate = 24
out = cv2.VideoWriter('outpy.avi',fourcc, frame_rate, (frame_width, frame_height))

a = 0

while a < 10000:
    ret, frame = cap.read()

    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)
        a += 1

    # When everything done, release the video capture and video write objects
# print("release")
# cap.release()
# out.release()
#
# # Closes all the frames
# cv2.destroyAllWindows()