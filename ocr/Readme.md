# OCR for EduGenius

  

## Introduction

The main focus of this code section is to provide OCR capability to the EduGenius system while justifying the OCR method. Currently, there are 3 methods to achieve OCR .


1.  **Ninja APIs** 
2.  **Gemini Flash Model** 
3.  **Gemini Pro Model**

## Test Metrics
### 1. Character Error Rate (CER)
This first removes all spaces, newline, and tab characters from both the ground truth and prediction and then checks how many wrong character predictions are in the prediction string by iterating through both processed prediction and ground truth strings. Then the CER is equal to
<p  align="center">
CER = Unmatched Character count/ Max(Predicted Character Count, GroundTruth Character Count)
</p>

### 2. Word Error Rate (WER)
Like the CER, this first removes the newline and tab characters and then splits the sentences from spaces from both predicted text and ground truth text to create word lists. Then like in CER the WER is 
<p  align="center">
WER = Unmatched Word count/ Max(Predicted Word Count, Ground Truth Word Count)
</p>

### 3. Character Diffence (CDiff)
This provides the character difference between the predicted text and the ground truth

<p  align="center">
CDiff = Number of Characters in Predicted Text -  Number of Characters in Ground Truth
</p>

### 4. Levenshtein Distance/Edit Distance (LD)
Levenshtein Distance provides the minimal number of edits(Insertions/Updates/Deletions) that have to be done to make the predicted text convert into the ground truth.

### 5. Average Levenshtein Distance/Average Edit Distance (ALD)
Since the LD depends on the length of the ground truth or the predicted text, It is suitable to consider average value of LD

<p  align="center">
ALD = LD/Length of the Ground Truth
</p>

### 6. Exection Time
You know what execution time is.

 ## What is the best model for EduGenius
### Test Report for the Ninja API
```
Execution Time : 1.2197825908660889
Metric Score Summerization for test01.png
        CER : 1.0
        CDiff : 1
        WER : 1.0
        LD : 27
        ALD : 0.9310344827586207


Execution Time : 1.3170254230499268
Metric Score Summerization for test02.png
        CER : 1.0
        CDiff : -25
        WER : 1.0
        LD : 55
        ALD : 0.8461538461538461


Execution Time : 0.9984798431396484
Metric Score Summerization for test03.png
        CER : 1.0
        CDiff : -17
        WER : 1.0
        LD : 33
        ALD : 0.8918918918918919


Execution Time : 1.1845042705535889
Metric Score Summerization for test04.png
        CER : 0.96
        CDiff : -19
        WER : 1.0
        LD : 33
        ALD : 0.825
```
### Test Results for the Gemini Flash Model
```
Execution Time : 6.84578537940979
Metric Score Summerization for test01.png
        CER : 0.0
        CDiff : 0
        WER : 0.0
        LD : 1
        ALD : 0.034482758620689655


Execution Time : 4.077542066574097
Metric Score Summerization for test02.png
        CER : 0.9555555555555556
        CDiff : 7
        WER : 0.7916666666666666
        LD : 20
        ALD : 0.3076923076923077


Execution Time : 3.9547219276428223
Metric Score Summerization for test03.png
        CER : 0.0
        CDiff : 0
        WER : 0.5384615384615384
        LD : 4
        ALD : 0.10810810810810811


Execution Time : 4.750878572463989
Metric Score Summerization for test04.png
        CER : 0.9629629629629629
        CDiff : 2
        WER : 0.9411764705882353
        LD : 9
        ALD : 0.225

``` 

### Test Results for the Gemini Pro Model
```
Execution Time : 4.5506432056427
Metric Score Summerization for test01.png
        CER : 0.5
        CDiff : 1
        WER : 0.4166666666666667
        LD : 13
        ALD : 0.4482758620689655


Execution Time : 0.0
Metric Score Summerization for test02.png
        CER : 0.9555555555555556
        CDiff : 7
        WER : 0.4583333333333333
        LD : 23
        ALD : 0.35384615384615387


Execution Time : 0.015550374984741211
Metric Score Summerization for test03.png
        CER : 1.0
        CDiff : 5
        WER : 0.6153846153846154
        LD : 7
        ALD : 0.1891891891891892
        

Could not finish the last test case as the given resources were exhausted
```
###  Conclusion
Given the test results, it is obvious that the Gemini Flash and the Gemini Pro Model perform better as they have relatively low average Levenshtein distance. Although the Gemini Pro model has very minimum execution time, it has minimal API calls. Therefore, it is unsuitable for a web application like EduGenius as many users will use the platform concurrently. So the best approach is to use the Gemini Flash Model.


## Usage
In the code import the ocr.py file and call the OCR functions. **Gemini_Flash_OCR** is the function that utilize the Gemini Flash Model

  

