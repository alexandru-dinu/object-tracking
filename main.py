import dlib
import cv2
import argparse as ap

def check_points(x):
    x = (x[2],x[1],x[0],x[3]) if x[0] > x[2] else x
    x = (x[0],x[3],x[2],x[1]) if x[1] > x[3] else x
    return x

def select_corners(img):
    select_corners.start, select_corners.end = None, None
    select_corners.mouse_down = False

    img_copy = img.copy()
    window_name = "Select objects to be tracked here"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.imshow(window_name,img_copy)

    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and not select_corners.start:
            select_corners.mouse_down = True
            select_corners.start = (x, y)
       
        elif event == cv2.EVENT_LBUTTONUP and select_corners.mouse_down == True:
            select_corners.mouse_down = False
            select_corners.end = (x,y)
            print "Object selected at [{}, {}]".format(select_corners.start, select_corners.end)
       
        elif event == cv2.EVENT_MOUSEMOVE and select_corners.mouse_down == True:
            img_copy = img.copy()
            cv2.rectangle(img_copy, select_corners.start, (x, y), (255,255,255), 3)
            cv2.imshow(window_name, img_copy)

    cv2.setMouseCallback(window_name, callback)
    
    print "Press and release mouse around the object to be tracked."
    print "Press key `p` to continue with the selected points."
    print "Press key `d` to discard the last object selected."
    print "Press key `q` to quit the program."

    while True:
        print(select_corners.start)
        key = cv2.waitKey(30)
        if key == ord('p') and select_corners.start and select_corners.end:
            break
        elif key == ord('q'):
            exit()
        elif key == ord('d'):
            if select_corners.mouse_down == False:
                select_corners.start = select_corners.end = None
                cv2.imshow(window_name,img.copy())
            else:
                print("No object to delete.")

    cv2.destroyAllWindows()
    corners = check_points([select_corners.start[0],select_corners.start[1],\
                        select_corners.end[0],select_corners.end[1]])
    return corners


def run(source=0, dispLoc=False):
    cam = cv2.VideoCapture(source)

    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()

    while True:
        retval, img = cam.read()

        if not retval:
            print "Cannot capture frame device"
            exit()

        if cv2.waitKey(20) == ord('p'):
            break
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    points = select_corners(img)
    print("Chosen area was:")
    


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])