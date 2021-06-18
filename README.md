# Edge_Detection_of_CheckerBoard
Detech Edge for figure of checkerboard with noise and rotation. 
# Installation
## requirements
* [Python 3.7.9](https://www.python.org/downloads/)
* [OpenCV 4.5.2](https://pypi.org/project/opencv-python/)
* [Numpy 1.19.3](https://pypi.org/project/numpy/)
* os, re, glob, Argparse (As of Python >= 2.7 and >= 3.2, they thus come pre-installed with Python) 
```
pip install opencv-python        <opencv>
pip install numpy                <Numpy>
```

# Experiment
## Data
The [Data] folder include five pictures of chessboard, each of them has different noise and rotation.
![pic1](https://user-images.githubusercontent.com/70020458/122487395-7739db80-cfdb-11eb-9e0e-845e6e1116b7.jpg)

## Algorithms
### Grey scale
If we want to detect edge of checkerboard, first we need to change colour to grey scale, which represent only amount of light, it is only intensity information.
![pic2](https://user-images.githubusercontent.com/70020458/122487398-786b0880-cfdb-11eb-8c89-4f4bb00daf8c.jpg)

### Noise Reduction
Noise is a important factor for edge detection, so here we need to use different smooth filter to reduce noise, thus, to enhance the result.
There are four common kernel for noise removing provided by opencv: 
* [Average](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37): Blurs an image using the normalized box filter. It simply takes the average of all the pixels under kernel area and replaces the central element with this average.
* [Gaussian](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1): Blurs an image using a Gaussian filter. Gaussian filtering is highly effective in removing Gaussian noise from the image.
* [Median](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#ga564869aa33e58769b4469101aac458f9):Blurs an image using the median filter. the median of all the pixels under the kernel window and the central pixel is replaced with this median value.
* [Bilateral](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed): Applies the bilateral filter to an image. it is highly effective at noise removal while preserving edges. But the operation is slower compared to other filters. 

### Threshold
Threshold will change grey scale to binary impression, if pixel value larger than threshold become 255, while 0 if under threshold.
![pic3](https://user-images.githubusercontent.com/70020458/122487400-799c3580-cfdb-11eb-8177-e84ef6c69cf1.jpg)

### Edge Detection
Edge detection is one of the important operation when we do image processing. It helps us reduce the amount of pixels to process and maintains the structure of the image. There are three common edge dection functions provided by opencv:
* [Canny](https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html): Canny uses a multi-stage algorithm to detect a wide range of edges in images, also known to many as the optimal detector
* [Sobel](https://docs.opencv.org/3.4/d2/d2c/tutorial_sobel_derivatives.html): Sobel algorithm is a gradient method based on the first ODE. It calculates the first derivatives of the image separately for the x and y axes.
* [Laplacian](https://docs.opencv.org/3.4/d5/db5/tutorial_laplace_operator.html): Laplacian algorithm calculates second order derivatives in a single pass.

# Usage
Run edge_detector.py with following parameters:
```
python edge_detector.py -p PATH [-f FILTER] [-k KERNEL] [-d DETECTOR] [-o OUTPUTTYPE] [-w [KWARGS [KWARGS ...]]]
```
input path is neccessary, other parameters are optinal.

- *-p*: your input path, this model provides both single (**project_folder/data/Image_01.png**) and multiple (**project_folder/data/*.png**) inputs, but only for single file format.
- *-f*: noise removal filter which provided by opencv, the default function is **gaussian** filter, you can choose filter in **average, gaussian, median, bilateral**.
- *-k*: self-defined kernel, the default is **None**, once kernel is defined, filter will not available anymore. e.g., ([0.5, 0.1, 0.1],[0.1, 0.36, 0.1],[0.1, 0.1, 0.06])
- *-d*: Edge detection function, the default is **canny**, you can choose detector in **sobel, laplacian, canny**.
- *-o*: output file format, the default is **jpg**, you can choose file format from [cv2.imwrite()](https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce).
- *-w*: kwargs, the default is below, you can change the size and sigma parameters in noise reduction, depth in edge function and the threshold from grey scale to binary. You can change the parameter by **-w 'size'=int.type 'sigma'=int.type 'depth'=int.type 'threshold'=int.type**. All parameters need to following the limitation in opencv
```
'threshold': 150 
'size': 5
'sigma': 75
'depth': 6
```
if calling filter or detector with wrong name, it will show what you input and what you could choose to take.

if kernel is not **None**, it will show kernel is using, filter doesn't work.

if model run successfully, then it will show the output path with output file name.


## usage example
```
python .\edge_detector.py -p "../data/*.png"
python .\edge_detector.py -p "../data/Image_1.png" -d "laplacian" -w size=7
python .\edge_detector.py -p "../data/*.jpg" -f "average"
python .\edge_detector.py -p "../data/Image_5.jpg" -k "([0.5, 0.1, 0.1],[0.1, 0.36, 0.1],[0.1, 0.1, 0.06])" -o png
python .\edge_detector.py -p "../data/*.png" -f "median" -d "sobel" -w depth=5
python .\edge_detector.py -p "../data/*.png" -f "bilateral" -o jpg -w threshold=140 sigma=65 -o png
```

## output
result with default parameters.
![pic4](https://user-images.githubusercontent.com/70020458/122487642-03e49980-cfdc-11eb-9ce7-8be708b51de3.jpg)
