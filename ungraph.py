import sys
import cv2
import numpy as np
import os
import pickle
from parameter_input import popup as variable_popup

from state import State
from checker import check

if not 1 < len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} image_file [output_file_prefix]")
    exit(-1)

controls = """

Controls:

  Component selection:
     x: edit x axis positions
     y: edit y axis positions
     z: edit curves
     
     w: set values on axis
   
     c: create new curve
     p: delete curve

  Point editing: 
     e: next point
     q: previous point
 
     a: add data point
     d: delete data point
     
  I/O:
     r: reset
     [enter]: write data and quit
     o: show plot
"""

print(controls)

im_filename = sys.argv[1]
filename_parts = im_filename.split(".")

if len(sys.argv) == 3:
    editor_filename = sys.argv[2] + ".gph"
    output_filename_prefix = sys.argv[2]
else:
    editor_filename = ".".join(filename_parts[:-1] + ["gph"])
    output_filename_prefix = ".".join(filename_parts[:-1])



if os.path.exists(editor_filename):
    with open(editor_filename, 'rb') as fid:
        state = pickle.load(fid)
else:
    state = State()

framename = "Ungraph"
base_im = cv2.imread(im_filename)

def mouse_click(x, y):
    state.set_point(x, y)

mouse_pos = [0, 0]

def mouse_callback(event, x, y, flags, param):
    global mouse_pos
    if event == cv2.EVENT_LBUTTONUP:
        mouse_click(int(x), int(y))

    mouse_pos[0] = int(x)
    mouse_pos[1] = int(y)


cv2.imshow(framename, base_im)
cv2.setMouseCallback(framename, mouse_callback)


while True:
    im = base_im.copy()

    for (x, y, b, g, r) in state.drawable_points():
        cv2.drawMarker(im, (x,y), (b,g,r))

    selected = state.selected_point()
    if selected is not None:
        cv2.drawMarker(im, selected, (128,0,128), cv2.MARKER_SQUARE)

    for text, pt, color in state.text():
        cv2.putText(im, text, pt, cv2.FONT_HERSHEY_PLAIN, 2, color)

    for line, color in state.lines():
        cv2.polylines(im, [np.array(line)], False, color, 1, cv2.LINE_AA)

    cv2.imshow(framename, im)
    key = cv2.waitKey(10)

    if key == ord("e"):
        state.next_point()

    elif key == ord("q"):
        state.prev_point()

    elif key == ord("c"):
        state.new_curve()

    elif key == ord("p"):
        state.del_curve()

    elif key == ord("x"):
        state.set_x()

    elif key == ord("y"):
        state.set_y()

    elif key == ord("z"):
        state.set_curves()

    elif key == ord("w"):
        variable_popup(state)

    elif key == ord("a"):
        state.add_point(mouse_pos[0], mouse_pos[1])

    elif key == ord("d"):
        state.del_point()

    elif key == ord("o"):
        check(state)

    elif key == 13:
        break

with open(editor_filename, 'wb') as fid:
    pickle.dump(state, fid)

print(os.curdir)
for i, curve in enumerate(state.transformed_curve_points()):
    filename = "%s_%i.csv"%(output_filename_prefix, i)
    print("Writing to '%s'"%filename)
    with open(filename, 'w') as fid:
        for i in range(len(curve)):
            fid.write("%g, %g\n"%(curve[i,0], curve[i,1]))

