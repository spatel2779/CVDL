import cv2
import base64
import io
import streamlit as st
from PIL import Image
import numpy as np
from filters import *

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format='JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

st.title('Artistic Image Filters')

upload_file = st.file_uploader('Choose an image file:', type=['jpg', 'png'])

if upload_file is not None:
    raw_bytes = np.asarray(bytearray(upload_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    
    input_col, output_col = st.columns(2)
    with input_col:
        st.header('Original')
        st.image(img, channels='BGR', use_column_width=True)
        
    st.header('Files Example:')
    option = st.selectbox(
        'Select a filter:',
        ('None', 'Black and White', 'Sepia/Vintage', 'Vignette Effect', 'Pencil Sketch')
    )
     
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption('Black and White')
        st.image('C:/Users/sgaje/OneDrive/Pictures/Test/CVDL/rosebw.png')
    with col2:
        st.caption('Sepia/Vintage')
        st.image('C:/Users/sgaje/OneDrive/Pictures/Test/CVDL/rosesepia.png')
    with col3:
        st.caption('Vignette Effect')
        st.image('C:/Users/sgaje/OneDrive/Pictures/Test/CVDL/rosevignette.png')
    with col4:
        st.caption('Pencil Sketch')
        st.image('C:/Users/sgaje/OneDrive/Pictures/Test/CVDL/rosesketch.png')
    
    output_flag = 1
    color = 'BGR'
    
    if option == 'None':
        output_flag = 0
    elif option == 'Black and White':
        output = bw_filter(img)
        color = 'GRAY'
    elif option == 'Sepia/Vintage':
        output = sepia(img)
    elif option == 'Vignette Effect':
        level = st.slider('Level', 0, 5, 2)
        output = vignette(img, level)
    elif option == 'Pencil Sketch':
        ksize = st.slider('Blur kernel size', 1, 11, 5, step=2)
        output = pencilsketch(img, ksize)
        color = 'GRAY'


    with output_col:
        if output_flag == 1:
            st.header('Output')
            if color == 'BGR':
                if len(output.shape) == 3 and output.shape[2] == 3:
                    st.image(output, channels=color)
                    result = Image.fromarray(output[:, :, ::-1])
                else:
                    st.error("Output image does not have 3 channels.")
            elif color == 'GRAY':
                if len(output.shape) == 2:
                    st.image(output, channels='GRAY')
                    result = Image.fromarray(output)
                else:
                    st.error("Output image is not grayscale.")
            else:
                st.error("Unexpected output format.")
                
            st.markdown(get_image_download_link(result, 'output.png', 'Download Output'), unsafe_allow_html=True)
