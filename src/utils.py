import dlib
import cv2

g_thickness = 1
g_color = (0, 255, 0)
g_delay = 25

def check_points(x):
    x = (x[2],x[1],x[0],x[3]) if x[0] > x[2] else x
    x = (x[0],x[3],x[2],x[1]) if x[1] > x[3] else x
    return x

def select_corners(frame):
    select_corners.start, select_corners.end = None, None
    select_corners.mouse_down = False

    frame_copy = frame.copy()
    window_name = "Select objects to be tracked here"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.imshow(window_name,frame_copy)

    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and not select_corners.start:
            select_corners.mouse_down = True
            select_corners.start = (x, y)
       
        elif event == cv2.EVENT_LBUTTONUP and select_corners.mouse_down == True:
            select_corners.mouse_down = False
            select_corners.end = (x,y)
            print("Object selected at [{}, {}]".format(select_corners.start, select_corners.end))
       
        elif event == cv2.EVENT_MOUSEMOVE and select_corners.mouse_down == True:
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, select_corners.start, (x, y), g_color, g_thickness)
            cv2.imshow(window_name, frame_copy)

    cv2.setMouseCallback(window_name, callback)
    
    print("Select the object to be tracked.")
    print("Press key `p` to continue with the selected points.")
    print("Press key `d` to discard the last object selected.")
    print("Press ESC to quit the program.")

    while True:
        #print(select_corners.start)
        
        key = cv2.waitKey(g_delay)
        
        # resume
        if key == ord('p') and select_corners.start and select_corners.end:
            break

        # quit on ESC
        elif key == 27:
            exit()

        # delete
        elif key == ord('d'):
            if select_corners.mouse_down == False:
                select_corners.start = select_corners.end = None
                cv2.imshow(window_name,frame.copy())
            else:
                print("No object to delete.")

    cv2.destroyAllWindows()
    corners = check_points([select_corners.start[0],select_corners.start[1],\
                        select_corners.end[0],select_corners.end[1]])
    return corners