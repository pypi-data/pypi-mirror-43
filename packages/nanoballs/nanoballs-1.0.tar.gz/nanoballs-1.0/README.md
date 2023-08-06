![alt](https://i.imgur.com/5IlGL9R.jpg)  
## Package for SEM Image and Particle Analysis
This package is a tool to help analyze and learn the characteristics of particles captured in an SEM image. It takes an SEM image (supported file types listed [here](https://docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html#imread)), and cleans it up using a variety of noise-reduction and edge-enhancement processes. It then analyzes the image, detects the edges of each particle, and then returns particle characteristics such as the average size, size range, count, and a distribution plot of the particles, as well as a circle-fit image for further use and processing. 

---

### How to Install
1. `pip install nanoballs`
2. Import necessary packages

### Software Dependencies
* __Python3.6__
* __Packages__: argparse, Matplotlib, NumPy, OpenCV, pandas, scikit-learn, SciPy
    * Optional: nose (testing)
* __Tesseract OCR__: Image-to-text converter, available [here](https://pypi.org/project/pytesseract/)
    * Not necessary for use of the code, but helps expedite analysis of large sets of images
    
---

### Packages Included (This will be moved to the "nanoballs/ README")
* __circle.py__: Finds circles using the Hough transform and draws the circle's center and edge
* __contrast_adj.py__: Adjusts brightness and contrast of image to improve edge-detection 
* __convert.py__: Determines most efficient way (OCR, file name, user input) to get the magnification level, returns pixel length to nanometer conversion factor
* __imageseg.py__: Takes pre-processed image, returns segmented image and particle-center coordinates
* __segmentparser.py__: Iterates through the segmented image, calculates image coordinates and area
* __shape_fitting.py__: Fits ellipses to particles, determines the major and minor axis, predicts whether each particle is a circle or an ellipse, and then returns a distribution plot of the shape types


### Project Organization
(Folders and `.py` files)
```
documentation/ (Presentation slides, use cases, etc.)
    Poster/
examples/ (Notebook files, already run with output)
nanoballs/ (Main package folder, contains all necessary .py files)
    tests/ (Tests folder, contains files for unit testing)
        test_nanoballs.py
        __init__.py
        README.md
    circle.py
    contrast_adj.py
    convert.py
    imageseg.py
    segmentparser.py
    shape_fitting.py
    __init__.py
    README.md
notebooks/ (All .ipynb files, contain helpful markdown comments)
sem_images/ (Extra SEM images, can be used for testing or optimization)
LICENSE.txt
README.md
setup.py
```

---

### Example Usage
| (1) Image Input and Pre-Processing | (2) Segmentation | (3) Shape Fitting | (4) Data Output |
:---:|:---:|:---:|:---:
![](https://imgur.com/iYQr9SA.jpg) ![](https://imgur.com/q0LIoAy.jpg) | ![](https://i.imgur.com/xNhUkoP.jpg) ![](https://imgur.com/qXAATw7.jpg) | ![](https://imgur.com/ha1j9Ut.jpg) ![](https://imgur.com/genut41.jpg) |![](https://imgur.com/RTWHMLR.jpg) __This is where the table will go with mean, std.dev, etc.__

---

### Improvements 
This package is a work in progress, and much improvement could be made upon each step of the proccess. Better automization of the image contrast and brightness adjustments could go a long way, as could more complicated transforms. Currently a scaling factor is used to optimize the adjustments, but a script that normalizes the spread of the image histogram could afford more uniformity in proccessing and make this software more robust.

Edge detection could be improved on by stacking edge detection methods, with the hope being that a more contiguous edge would be produced. From there, experimentation with the p algorithm could produce finer edge detection than the built in Watershed algorithms currently available. Integration of the mamba-image package would be neccissary to introduct this functionality.

While the Hough Circle Fitting has proven robust in its implementation, the addition of a degree of freedom to try and fit elipses to the segments has proven difficult. Problems in this implementation could be rooted in how these algorithms work, as well as our understanding of their inputs (logical errors). More work is required to produce a useful end product.

From a stretch goal perspective, this software could also be improved upon by adding more in-depth analysis of the particles, including roughness. Other ideas for improvement include breaking the image down and adjusting the contrast and brightness differently for different tiles within the image to best detect edges, and training a neural network to set these parameters for us.

At the end of the day, though, a major cricicism of our work is our lack of scientific benchmarking. While we can visually see whether or not the code seems to be operating as expected and is throwing out a logical visual output, we do not have a good numeric benchmark of how closely these segmentations, circle fits, etc. are representing our data. Development of a means of better benchmarking our results would help drive development of robust code in the future.



---

### Acknowledgements
Team nanoBALLS wishes to thank David Beck, Chad Curtis, and the rest of the teaching staff for guiding us through this proccess and teaching us enough to get us started.

We also wish to thank Dr. Erika Buckle for collecting these images, the UW MAF for providing equipment and facility management, and Prof. Jim Pfaendtner for the project conception.

Lastly, we wish to extend our gratitutudes to Professors Drobny, Eric Stuve, Samson Jenekhe, and Arka Majumdar for allowing us to participate in this class.
