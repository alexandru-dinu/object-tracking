import dlib
import cv2
import argparse as ap

import numpy as np
import utils

g_index = 0
g_path_len = 50
g_path_buffer = []

def draw_path(frame):
    l = len(g_path_buffer)

    if l < 2:
        return

    for i in range(l - 1):
        start = g_path_buffer[i]
        end = g_path_buffer[i+1]

        cv2.line(frame, start, end, utils.g_color, 2)

def draw_rectangle(frame, rectangle):
    # draw bounding box
    point1 = (int(rectangle.left()), int(rectangle.top()))
    point2 = (int(rectangle.right()), int(rectangle.bottom()))

    cv2.rectangle(frame, point1, point2, utils.g_color, utils.g_thickness)

    # draw path
    center_x = (point1[0] + point2[0]) // 2
    center_y = (point1[1] + point2[1]) // 2

    center = (center_x, center_y)

    draw_path(frame)

    # max length reached, only add new center at the end
    if len(g_path_buffer) == g_path_len:
        g_path_buffer[0:g_path_len-1] = g_path_buffer[1:g_path_len]
        g_path_buffer[-1] = center

    # accumulate until g_path_len is reached
    elif len(g_path_buffer) < g_path_len:
        g_path_buffer.append(center)


    cv2.circle(frame, center, 1, utils.g_color, -1)

def display_coordinates(frame, rectangle):
    offset = 30

    point1 = (int(rectangle.left()), int(rectangle.top()))
    point2 = (int(rectangle.right()), int(rectangle.bottom()))

    position = (point1[0], point1[1] - offset)
    text = "{}, {}".format(point1, point2)

    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, .5, \
            utils.g_color, utils.g_thickness)

def tracking(video_source, tracker, show_coordinates):
    while True:
        ret, frame = video_source.read()

        if ret == False:
            exit()

        # update the tracker and get the bounding box
        tracker.update(frame)
        rectangle = tracker.get_position()

        # draw the bounding box
        draw_rectangle(frame, rectangle)

        # display coordinates if needed
        if show_coordinates:
            display_coordinates(frame, rectangle)

        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Video", frame)

        # exit if ESC is pressed
        if cv2.waitKey(utils.g_delay) == 27:
            exit()


def await_selection(video_source):
    while True:
        ret, frame = video_source.read()

        if ret == False:
            exit()

        key = cv2.waitKey(utils.g_delay)

        # if 'p' is pressed, return the current frame
        if key == ord('p'):
            return frame
        
        # if ESC is pressed, exit
        if key == 27:
            exit()
        

        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Video", frame)



def main(source, show_coordinates=False):
    video_source = cv2.VideoCapture(source)

    if not video_source.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    # continous reading from source until pause is pressed
    frame = await_selection(video_source)
        
    cv2.destroyWindow("Video")

    points = utils.select_corners(frame)

    if not points:
        print("No object to be tracked. Exiting...")
        exit()
    
    print("Chosen area is:", points)

    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    cv2.imshow("Video", frame)

    # instantiate a new dlib tracker
    tracker = dlib.correlation_tracker()
    tracker.start_track(frame, dlib.rectangle(*points))

    # continuously run the tracking after a selection has been made
    tracking(video_source, tracker, show_coordinates)

    # clean-up
    video_source.release()
    


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-c', "--showCoord", dest="showCoord", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video (file / camera)
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])

    main(source, args["showCoord"])