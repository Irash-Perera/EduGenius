import os
import ocr
import metrics
import pandas as pd
import time

df = pd.read_excel("./ocr/testing/Ground_truths.xlsx")

file_name = df["file_name"].to_list()
content = df["content"].to_list()
GT = {}

for i in range(len(file_name)):
    GT[file_name[i]] = content[i]
# print(dict)



for file in os.listdir(f"./OCR/testing/test_data"):
    if file.endswith(".png"):
        ground_truth = GT[f"{file}"]
        start = time.time()
        prediction = ocr.ninja_OCR(f"./OCR/testing/test_data/{file}")
        end = time.time()
        print(f"Execution Time : {end-start}")
        metrics.metrics_report(file, prediction, ground_truth)


for file in os.listdir(f"./OCR/testing/test_data"):
    if file.endswith(".png"):
        ground_truth = GT[f"{file}"]
        start = time.time()
        prediction = ocr.Gemini_Flash_OCR(f"./OCR/testing/test_data/{file}")
        end = time.time()
        print(f"Execution Time : {end-start}")
        metrics.metrics_report(file, prediction, ground_truth)


for file in os.listdir(f"./OCR/testing/test_data"):
    if file.endswith(".png"):
        ground_truth = GT[f"{file}"]
        start = time.time()
        prediction = ocr.Gemini_Pro_OCR(f"./OCR/testing/test_data/{file}")
        end = time.time()
        print(f"Execution Time : {end-start}")
        metrics.metrics_report(file, prediction, ground_truth)
        time.sleep(10)
