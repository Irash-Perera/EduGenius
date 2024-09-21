# RAG Evaluvation for EduGenius

This section evaluates various metrics for a Retrieval-Augmented Generation (RAG) system using Google's Generative AI and embeddings. It implements different metrics to measure the performance of the generated answers in terms of relevance, correctness, faithfulness, and more. The aim is to ensure the generated content is accurate, reliable, and contextually relevant.

## Overview

The `RAG_Tester` class allows you to evaluate a wide range of metrics for generated answers based on questions, answers, contexts, and ground truth data. The system integrates with Google Generative AI to analyze these metrics using advanced large language models and embeddings.

## Metrics

### 1. **Faithfulness**

Measures the consistency of the generated answer with respect to the given context. Faithfulness ensures that the generated response does not hallucinate or provide irrelevant information.

**Example Usage**:

```
`faithfulness_score = rag_tester.faithfulness()` 
```
### 2. **Answer Relevance**

Evaluates how relevant the generated answer is to the question. This metric checks if the answer is directly addressing the query and whether it aligns with the context provided.

**Example Usage**:
```
relevance_score = rag_tester.answerRelavance()` 
```
### 3. **Context Precision**

Determines how precisely the context is used when generating an answer. It checks if the generated answer draws the correct information from the context to provide a relevant response.

**Example Usage**:

```
precision_score = rag_tester.contextPrecision()` 
```
### 4. **Context Utilization**

Checks the extent to which the context is utilized when generating an answer. This metric ensures that the context provided is meaningfully referenced to craft a coherent response.

**Example Usage**:

```
utilization_score = rag_tester.contextUtilization()` 
```
### 5. **Context Recall**

Measures how much of the relevant information from the context is recalled in the generated answer. It looks at whether the essential parts of the context are being used to generate the response.

**Example Usage**:

```recall_score = rag_tester.contextRecall()``` 

### 6. **Context Entity Recall**

Evaluates the recall of entities (such as names, locations, or key terms) from the context in the generated answer. This is useful when verifying if the system correctly identifies and includes key entities from the context.

**Example Usage**:

```entity_recall_score = rag_tester.contextEntitiesRecall()` 

### 7. **Noise Sensitivity**

Analyzes the sensitivity of the generated answer to noise in the input. This checks whether introducing irrelevant information impacts the model's performance or output, ensuring that the system is robust to noisy data.

**Example Usage**:

```noise_sensitivity_score = rag_tester.noiseSensitivity()``` 

### 8. **Answer Semantic Similarity**

Measures how semantically similar the generated answer is to the ground truth. This metric evaluates the overall meaning of the answer compared to the expected correct answer, beyond surface-level word matching.

**Example Usage**:

```similarity_score = rag_tester.answerSementicSimilarity()``` 

### 9. **Answer Correctness**

Checks the factual correctness of the generated answer. This metric ensures that the answer provides accurate and correct information based on the question and context.

**Example Usage**:

```correctness_score = rag_tester.answerCorrectness()``` 

### 10. **Aspect Critique**

Allows you to define custom aspects to critique the generated answers. This metric gives flexibility in setting specific evaluation criteria based on a given aspect's name and definition.

**Example Usage**:

```custom_aspect_score = rag_tester.aspectCritique(name="AspectName", definition="AspectDefinition")``` 

## Usage Example

To use the `RAG_Tester`, initialize it with the lists of questions, answers, contexts, and ground truth. Then, call the desired metric methods to evaluate the performance of your RAG system.

```
questions = ["What is AI?", "Define machine learning."]
answers = ["AI is...", "Machine learning is..."]
contexts = ["Context about AI", "Context about machine learning"]
ground_truths = [["True AI definition"], ["True ML definition"]]

rag_tester = RAG_Tester(questions, answers, contexts, ground_truths)

relevance_score = rag_tester.answerRelavance()
print(f"Answer Relevance Score: {relevance_score}")` 
```
## Conclusion
We have to create a dataset from our data and run tests and justify our choices.