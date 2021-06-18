import os
import re
import cv2
import glob
import numpy as np
from argparse import ArgumentParser, Action

class ParseKwargs(Action):
    def __call__(self, arg_parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

def parseParams():

    # set parameters
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-p', '--path', type=str, required=True)
    arg_parser.add_argument('-f', '--filter', type=str, default='gaussian')
    arg_parser.add_argument('-k', '--kernel', type=str, default=None)
    arg_parser.add_argument('-d', '--detector', type=str, default='canny')
    arg_parser.add_argument('-o', '--outputtype', type=str, default='jpg')
    arg_parser.add_argument('-w', '--kwargs', nargs='*', action=ParseKwargs)
    params = arg_parser.parse_args()
    return params

def remove_noise(image, filter_type=None, kernel=None, size=5, sigma=75):
    """remove_noise.
    
    Parameters
    ----------
    image : numpy.array
        Source image.
    filter_type : string
        filter fcuntion in opencv (average, gaussian, median, bilateral)
    kernel : numpy.array
        kernel function in self-defined
    """
    
    # set filter: average, gaussian, median, bilateral
    average = lambda img : cv2.blur(img, (size,size))
    gaussian = lambda img : cv2.GaussianBlur(img, (size, size), 0)
    median = lambda img : cv2.medianBlur(img, size)
    bilateral = lambda img : cv2.bilateralFilter(img, size, sigma, sigma)

    # remove noise with chosen filter
    if filter_type not in ["average", "gaussian", "median", "bilateral"]:
        print(f'your filter function is: {filter_type}, not the correct function name\nplease choose filter function from (average, gaussian, median, bilateral)')
    elif kernel is not None:
        print(f"self-defined kernel is using, filter doesn't work")
        image_filtered = cv2.filter2D(image, -1, kernel)
    else:
        image_filtered = eval(filter_type)(image)

    return image_filtered

def edge_detector(image, detect='canny', depth = cv2.CV_64F):
    """edge_detector.
    
    Parameters
    ----------
    image : numpy.array
        Source image.
    detect : string
        Edge detection fcuntion in opencv (sobel, laplacian, canny)
    depth : int
        Desired depth of the destination image.
    """

    if detect not in  ["sobel", "laplacian", "canny"]:
        print(f'your detect function is: {detect}, not the correct function name\nplease choose detect function from (sobel, laplacian, canny)')
    # Set edge detector
    def sobel(img, depth = depth):
        sobel_x = cv2.Sobel(img, depth, 1, 0)
        sobel_y = cv2.Sobel(img, depth, 0, 1)
        sobel_x = np.uint8(np.absolute(sobel_x))
        sobel_y = np.uint8(np.absolute(sobel_y))
        image_detect = cv2.bitwise_or(sobel_x, sobel_y)
        return image_detect
    laplacian = lambda img, depth: np.uint8(np.abs(cv2.Laplacian(img, depth)))
    canny = lambda img, depth: cv2.Canny(img, 100, 200)

    # detect edge from image
    image_detect = eval(detect)(image, depth)

    return image_detect

if __name__ == '__main__':

    params = parseParams()
    # replace parameter if kwargs exist.
    kwargs = {'threshold': 170, 'size': 5, 'sigma': 75, 'depth': cv2.CV_64F}
    if params.kwargs:
        for key in params.kwargs.keys():
            kwargs[key] = int(params.kwargs[key])

    # load image
    for name in glob.glob('%s'%params.path):
        img_original = cv2.imread(name)
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

        # set kernel if it is not None
        kernel = None
        if params.kernel:
            kernel = eval(params.kernel)
            kernel = np.array(kernel, dtype="float32")

        filtered_image = remove_noise(img_gray, filter_type=params.filter, kernel=kernel, size=kwargs['size'], sigma=kwargs['sigma'] )

        # use threshold to convert image to binary (black, white)
        img_binary = cv2.threshold(filtered_image, kwargs['threshold'], 255, cv2.THRESH_BINARY)[1]

        img_edge = edge_detector(img_binary, detect=params.detector, depth=kwargs['depth'])

        # overlap edge to original figure
        edge = (img_edge > 70).astype(int)
        img_original[:,:,0][edge == 1] = 0
        img_original[:,:,1][edge == 1] = 255
        img_original[:,:,2][edge == 1] = 0


        # output with output pathwith in same name and type
        regExp  = "[ \w-]+?(?=\.)"
        output = re.findall(regExp, name)
        output_path = f'../output/{output[0]}_edge.{params.outputtype}'
        print(output_path)
        if not os.path.exists('../output/'):
            os.makedirs('../output/')
        cv2.imwrite(output_path, img_original)