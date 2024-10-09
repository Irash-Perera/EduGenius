from metrics import RAG_Tester, RAG_Report
import pandas as pd


df = pd.read_excel("./test_data/TestCases.xlsx",index_col=False)
print()

test_questions = df["Question"].to_list()
test_ground_truth =  df["Ground_Truth"].to_list()
test_answer = df["Answer"].to_list()
test_contexts = []

for i in range(len(df["Context"].to_list())):
    test_contexts.append([df["Context"].to_list()[i]])

rag_tester = RAG_Tester(test_questions, test_answer, test_contexts, test_ground_truth)
# rag_report = RAG_Report(test_questions, test_answer, test_contexts, test_ground_truth)

print(rag_tester.faithfulness())
print(rag_tester.answerRelavance())
print(rag_tester.contextPrecision())
print(rag_tester.contextRecall())
print(rag_tester.contextEntitiesRecall())
print(rag_tester.contextUtilization())
print(rag_tester.noiseSensitivity())
print(rag_tester.aspectCritique("correctness", "Is the submission factually correct?"))

# print(rag_report.generate_report())