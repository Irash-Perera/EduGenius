# RAG Evaluvation for EduGenius

  

This section evaluates various metrics for a Retrieval-Augmented Generation (RAG) system using Google's Generative AI and embeddings. It implements different metrics to measure the performance of the generated answers in terms of relevance, correctness, faithfulness, and more. The aim is to ensure the generated content is accurate, reliable, and contextually relevant.

  

## Overview

  

The `RAG_Tester` class allows you to evaluate a wide range of metrics for generated answers based on questions, answers, contexts, and ground truth data. The system integrates with Google Generative AI to analyze these metrics using advanced large language models and embeddings.

  

## Metrics

  

### 1. **Faithfulness**

  

Measures the consistency of the generated answer with respect to the given context. Faithfulness ensures that the generated response does not hallucinate or provide irrelevant information.

  

### 2. **Answer Relevance**

  

Evaluates how relevant the generated answer is to the question. This metric checks if the answer is directly addressing the query and whether it aligns with the context provided.

  

### 3. **Context Precision**

  

Determines how precisely the context is used when generating an answer. It checks if the generated answer draws the correct information from the context to provide a relevant response.

  

### 4. **Context Utilization**

  

Checks the extent to which the context is utilized when generating an answer. This metric ensures that the context provided is meaningfully referenced to craft a coherent response.

  

### 5. **Context Recall**

  

Measures how much of the relevant information from the context is recalled in the generated answer. It looks at whether the essential parts of the context are being used to generate the response.

  
  

### 6. **Context Entity Recall**

  

Evaluates the recall of entities (such as names, locations, or key terms) from the context in the generated answer. This is useful when verifying if the system correctly identifies and includes key entities from the context.

  
  

### 7. **Noise Sensitivity**

  

Analyzes the sensitivity of the generated answer to noise in the input. This checks whether introducing irrelevant information impacts the model's performance or output, ensuring that the system is robust to noisy data.

  

### 8. **Answer Semantic Similarity**

  

Measures how semantically similar the generated answer is to the ground truth. This metric evaluates the overall meaning of the answer compared to the expected correct answer, beyond surface-level word matching.

  

### 9. **Answer Correctness**

  

Checks the factual correctness of the generated answer. This metric ensures that the answer provides accurate and correct information based on the question and context.

  

### 10. **Aspect Critique**

  

Allows you to define custom aspects to critique the generated answers. This metric gives flexibility in setting specific evaluation criteria based on a given aspect's name and definition.

  

## Evaluvation Report

### Evalivation Report for Non-Context QA Generation without wolfarm

|Metric			|	Value
|----------------|-----------------|
|Faithfulness| 0.0000|
|Answer Relevancy | 0.7187|
|Context Precision| 0.1000|
|Context Recall| 0.6083|
|Context Entity Recall| 0.0000|
|noise_sensitivity_relevant| 0.1429|
|correctness| 0.8000|
  
#### Context Utilization
|Testcase | context_utilization|
|-------------|-----------------|
|0 |0.0|
|1 | 0.0|
|2 | 0.0|
|3 | 0.0|
|4 | 0.0|
|5 | 0.0|
|6 | 0.0|
|7 | 1.0|
|8 | 0.0|
|9 | 0.0|


### Evalivation Report for Non-Context QA Generation with wolfarm



### Evalivation Report for With-Context QA Generation

## Conclusion
We have to create a dataset from our data and run tests and justify our choices.