import pytest
from unittest.mock import patch, MagicMock
import cv2

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.canvas import free_draw, save_drawing 

"""
As st_canvas needs browser to displat results, we need to test these functions in isloation. 
So, that 
"""

# As st_canvas is closely coupled with complex functionlities of streamlit, 
# we use mocked version of it to test free draw in isloation.

# mock of st_canvas method
@patch('pages.canvas.st_canvas')  
def test_free_draw(mock_st_canvas):
    """
    Functionality: Testing the free_draw function by mocking the st_canvas method from the streamlit_drawable_canvas module.
                : verifies that st_canvas function is called once.
                :verifes the canvas object returned by free_draw function retains expected attributes(json_data, image_data).
    """
    # Set up the mock return value
    mock_st_canvas.return_value = MagicMock(json_data={'objects': []}, image_data=[[255, 255, 255]])

    canvas = free_draw()

    # verify whether st_canvas was called with correct parameters only once
    mock_st_canvas.assert_called_once_with(
        fill_color="#eee",
        stroke_width=5,
        stroke_color="black",
        background_color="white",
        update_streamlit=True,
        height=200,
        width=800,
        drawing_mode="freedraw"
    )

    # verifying the expected outputs from free_draw after st_canvas is mocked return values.
    assert canvas.json_data == {'objects': []}
    assert canvas.image_data == [[255, 255, 255]]
    


# we mock cv2's image write function to test the correct behaviour of save_drawing 
# as imwrite has dependencies with cv2 library. So that we need mocking to test save_drawing in isolation.  

# Mock OpenCV's imwrite function
@patch('cv2.imwrite')  
def test_save_drawing(mock_imwrite):
    """
    Functionality: verifies the functionality of save_drawing by adding mock canvas object when save is successful.
                : verifies whether save_drawing is called only once with correct parameters.
    """

    # setting up mock canvas object using magic mock 
    mock_canvas = MagicMock()

    # setting up json and image data to the mock object
    mock_canvas.json_data = {'objects': []} 
    mock_canvas.image_data = [[255, 255, 255]] 

    file_path = save_drawing(mock_canvas)

    # verify that cv2.imwrite was called only once with the correct arguments
    mock_imwrite.assert_called_once_with('assets/uploads/drawing.png', [[255, 255, 255]])

    # verify whether function returns the correct path.
    # this is a case of successful image write.
    assert file_path == 'assets/uploads/drawing.png'


def test_save_drawing_no_data():
    """
    Functionality: verifies the functionality of save_drawing by adding mock canvas object when save is not successful.
    """

    # mock canvas object case when there's no drawing (json_data is None)
    mock_canvas = MagicMock()
    mock_canvas.json_data = None

    file_path = save_drawing(mock_canvas)

    # verify save_drawing returns None when there's no drawing
    assert file_path is None