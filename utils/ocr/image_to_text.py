# Run this file seperately to generate the OCR results of the images in the data directory


import os
import requests


# Ninja Api for OCR 
# Good with text. But not good with the mathematical symbols
api_url = 'https://api.api-ninjas.com/v1/imagetotext'


# Load the names of the files in the data directory
year_dir = os.listdir("../data/")


for year in year_dir:
    # Open a txt file with the year directory name to append the OCR results
    text_file = open(f"{year}.txt","a")
    
    # Iterate throgh each file in the year directory
    for file in os.listdir(f"../data/{year}"):
        # Check if the file is a png
        if file.endswith(".png"):
            
            print(file)
            
            # Write the file name to the file
            text_file.write(f"{str(file)}   ")
            
            # Load the image to read as a binary file
            image_file_descriptor = open(f"../data/{year}/{file}", 'rb')

            # Send the image to the OCR API
            files = {'image': image_file_descriptor}
            r = requests.post(api_url, files=files)
            
            # This api recognize words not sentences. Each word has to be appended together to create the text
            string = ""
            for i in r.json():
                string += i['text']
                string += " "
            string += "\n"
            
            # Some results from the OCR API is not in unicode as a result of geometriic expressions and some mathematical expressions.
            # Therefore try except was added to handle not unicode errors while writing to the file
            try:
                text_file.write(string)
            except:
                pass 

    # Safely close the file
    text_file.close()      

