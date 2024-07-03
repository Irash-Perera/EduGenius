from streamlit_drawable_canvas import st_canvas
import streamlit as st
import cv2

def free_draw():
    canvas = st_canvas(
        fill_color = "#eee",
        stroke_width = 5,
        stroke_color = "black",
        background_color = "white",
        update_streamlit = False, 
        height = 200,
        width= 800,
        drawing_mode="freedraw"
    )
    return canvas

def save_drawing(canvas):
    if canvas.json_data is not None:
        cv2.imwrite('uploads/drawing.png', canvas.image_data)
        return 'uploads/drawing.png'
    else:
        return None