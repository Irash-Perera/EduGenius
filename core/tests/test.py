from metrics import RAG_Tester

test_questions = ["What is the Life Insurance Corporation of India (LIC) known for?"]
test_ground_truth =  ["The Life Insurance Corporation of India (LIC) is the largest insurance company in India, established in 1956 through the nationalization of the insurance industry. It is known for managing a large portfolio of investments."]
test_answer = ["The Life Insurance Corporation of India (LIC) is the largest insurance company in India, known for its vast portfolio of investments. LIC contributs to the financial stability of the country."]
test_contexts = [[
        "The Life Insurance Corporation of India (LIC) was established in 1956 following the nationalization of the insurance industry in India.",
        "LIC is the largest insurance company in India, with a vast network of policyholders and a huge investments.",
        "As the largest institutional investor in India, LIC manages a substantial funds, contributing to the financial stability of the country.",
        "The Indian economy is one of the fastest-growing major economies in the world, thanks to the secors like finance, technology, manufacturing etc"
    ]]


rag_tester = RAG_Tester(test_questions, test_answer, test_contexts, test_ground_truth)

# print(rag_tester.faithfulness())
# print(rag_tester.answerRelavance())
# print(rag_tester.contextPrecision())
# print(rag_tester.contextRecall())
# print(rag_tester.contextEntitiesRecall())
# print(rag_tester.contextUtilization())
# print(rag_tester.noiseSensitivity())
print(rag_tester.aspectCritique("correctness", "Is the submission factually correct?"))
