from freenect import sync_get_depth as get_depth
import numpy as np
import cv, cv2
import serial
import scipy.interpolate

constList = lambda length, val: [val for _ in range(length)] #Gives a list of size length filled with the variable val. length is a list and val is dynamic

class BlobAnalysis:
    def __init__(self,BW): #Constructor. BW is a binary image in the form of a numpy array
        self.BW = BW
        cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Finds the contours
        counter = 0
        """
        These are dynamic lists used to store variables
        """
        centroid = list()
        cHull = list()
        contours = list()
        cHullArea = list()
        contourArea = list()
        while cs: #Iterate through the CvSeq, cs.
            if abs(cv.ContourArea(cs)) > 2000: #Filters out contours smaller than 2000 pixels in area
                contourArea.append(cv.ContourArea(cs)) #Appends contourArea with newest contour area
                m = cv.Moments(cs) #Finds all of the moments of the filtered contour
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0)) #Spatial moment m10
                    m00 = int(cv.GetSpatialMoment(m,0,0)) #Spatial moment m00
                    m01 = int(cv.GetSpatialMoment(m,0,1)) #Spatial moment m01
                    centroid.append((int(m10/m00), int(m01/m00))) #Appends centroid list with newest coordinates of centroid of contour
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Finds the convex hull of cs in type CvSeq
                    cHullArea.append(cv.ContourArea(convexHull)) #Adds the area of the convex hull to cHullArea list
                    cHull.append(list(convexHull)) #Adds the list form of the convex hull to cHull list
                    contours.append(list(cs)) #Adds the list form of the contour to contours list
                    counter += 1 #Adds to the counter to see how many blobs are there
                except:
                    pass
            cs = cs.h_next() #Goes to next contour in cs CvSeq
        """
        Below the variables are made into fields for referencing later
        """
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

# Boundary for centroid
boundary = np.asarray([0, 640, 0, 480])

def get_pos_for_serial(centroid):
    # Just working with the vertical direction
    vert_pos = centroid[1]
    inter_func = scipy.interpolate.interp1d([boundary[3], boundary[2]], [0, 80] )
    out_pos = int(inter_func(vert_pos))
    return out_pos

def hand_tracker(serial_object):
    (depth,_) = get_depth()
    cHullAreaCache = constList(5,12000) #Blank cache list for convex hull area
    areaRatioCache = constList(5,1) #Blank cache list for the area ratio of contour area to convex hull area
    centroidList = list() #Initiate centroid list
    #RGB Color tuples
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    done = False
    previous_object_no_error = True
    min_delta_pos = 1 # as a percentage of total possibilities
    prev_vert_pos = -20
    while not done:
        (depth,_) = get_depth()
        depth = depth.astype(np.float32)
        _,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV) #Threshold the depth for a binary image. Thresholded at 600 arbitary units
        blobData = BlobAnalysis(depthThresh) #Creates blobData object using BlobAnalysis class

        if blobData.counter == 1:
            centroid = blobData.centroid[0]
            previous_object_no_error = True
            vert_pos = get_pos_for_serial(centroid)
            # Check for significant changes
            if np.abs(prev_vert_pos - vert_pos) > min_delta_pos:
                prev_vert_pos = vert_pos
                print str(vert_pos)
                serial_object.write(str(vert_pos)+'\n')
        elif blobData.counter == 0 and previous_object_no_error:
            print 'No tracking objects found'
            previous_object_no_error = False
        elif blobData.counter > 1 and previous_object_no_error:
            print 'Too many tracking objects: {} objects'.format(blobData.counter)
            previous_object_no_error = False

if __name__=='__main__':
    # start serial object
    # ser_obj = serial.Serial('/dev/pts/26')
    ser_obj = serial.Serial('/dev/ttyUSB0')
    try:
        print "Starting hand-tracker"
        hand_tracker(ser_obj)
    except:
        print 'Couldnt start hand-tracker'
        ser_obj.close()
        pass
