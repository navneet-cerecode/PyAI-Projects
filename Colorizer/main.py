import numpy as np
import cv2

# Models : https://github.com/richzhang/colorization/tree/caffe/colorization/models
# Points : https://github.com/richzhang/colorization/blob/caffe/colorization/resources/pts_in_hull.npy
# Inspired By : https://github.com/opencv/opencv/blob/master/samples/dnn/colorization.py

prototxt_path = 'models/colorization_deploy_v2.prototxt'
model_path = 'models/colorization_release_v2.caffemodel'
kernel_path = 'models/pts_in_hull.npy'
image_path = 'lion2.jpg'

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
points = np.load(kernel_path)

points = points.transpose().reshape(2,313,1,1)

net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]

net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1,313], 2.606, dtype="float32")] #Copied from OpenCV Documentation

bw_image = cv2.imread(image_path)
normalized = bw_image.astype("float32") / 255.0 #Values geting normalised from 0 to 255 TO 0 to 1
lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

# Dimensions of pictures model is trained on 224 x 224

resized = cv2.resize(lab, (224, 224))
# resized = cv2.resize(lab, (224, 224), interpolation=cv2.INTER_CUBIC)
L = cv2.split(resized)[0]
L -= 37 #This values can be Changed for finetuning

net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1,2,0))

ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
L = cv2.resize(L, (bw_image.shape[1], bw_image.shape[0]))
# ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]), interpolation=cv2.INTER_CUBIC)
# L = cv2.resize(L, (bw_image.shape[1], bw_image.shape[0]), interpolation=cv2.INTER_CUBIC)

colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2) #Concatenating BW With Colours
colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)

colorized = (255.0 * colorized).astype("uint8")

cv2.imshow("BW Image", bw_image) #Display BW Image
cv2.imshow("Colorized", colorized ) #Display Colorized Image
cv2.waitKey(0)
cv2.destroyAllWindows()
# LAB -> = Lightness a* b*