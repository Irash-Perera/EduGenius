from datasets import Dataset 
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ragas.metrics import *
from ragas import evaluate
from ragas.llms.base import LangchainLLMWrapper
import os
from dotenv import load_dotenv


load_dotenv()

os.environ['GOOGLE_API_KEY'] =  os.getenv("GOOGLE_GEN_AI_API_KEY")

LLM = LangchainLLMWrapper(GoogleGenerativeAI(model = "gemini-pro", temperature=0.7))
EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

class RAG_Report():
    def __init__(self,question_list,answer_list, context_list, ground_truth_list):  
        if (len(question_list) != len(answer_list)) or (len(question_list) != len(context_list)) or (len(context_list) != len(answer_list)):
                raise ValueError("All lists must be the same length")
            
        self.question_list = question_list
        self.answer_list = answer_list
        self.context_list = context_list
        self.ground_truth_list = ground_truth_list

        self.report = {}

    def generate_report(self):
        self.tester = RAG_Tester(self.question_list, self.answer_list, self.context_list, self.ground_truth_list)
        self.report["faithfulness"] = self.tester.faithfulness()
        self.report["answer_relevancy"] = self.tester.answerRelavance()
        self.report["context_precision"] = self.tester.contextPrecision()
        self.report["context_utilization"] = self.tester.contextUtilization()
        self.report["context_recall"] = self.tester.contextRecall()
        self.report["context_entity_recall"] = self.tester.contextEntitiesRecall()
        self.report["noise_sensitivity"] = self.tester.noiseSensitivity()
        self.report["answer_similarity"] = self.tester.answerSementicSimilarity()
        self.report["answer_correctness"] = self.tester.answerCorrectness()
        return self.report

class RAG_Tester():
    def __init__(self,question_list,answer_list, context_list, ground_truth_list):
        if (len(question_list) != len(answer_list)) or (len(question_list) != len(context_list)) or (len(context_list) != len(answer_list)):
            raise ValueError("All lists must be the same length")
        
        self.question_list = question_list
        self.answer_list = answer_list
        self.context_list = context_list
        self.ground_truth_list = ground_truth_list

        self.data_samples_without_ground_truths = {
            'question': self.question_list,
            'answer' : self.answer_list,
            'contexts': self.context_list
        }

        self.data_samples_with_ground_truths = {
            'question': self.question_list,
            'answer' : self.answer_list,
            'contexts': self.context_list,
            'ground_truth': self.ground_truth_list
        }


    def set_llm_and_embeddings(self,metric):
        m = [metric]
        m[0].__setattr__("llm", LLM)
        m[0].__setattr__("embeddings", EMBEDDINGS)
        return m        

    
    def faithfulness(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list
            }
        )
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(faithfulness))
        return score
    
    
    def answerRelavance(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list
            }
        )
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(answer_relevancy))
        return score
    

    def contextPrecision(self):
        dataset = Dataset.from_dict({
            'question': self.question_list,
            'answer' : self.answer_list,
            'contexts': self.context_list,
            'ground_truth': self.ground_truth_list
        })
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(context_precision))
        return score
    
    def contextUtilization(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list
            }
        )    
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(context_utilization))
        return score.to_pandas()
    
    def contextRecall(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list,
                'ground_truth': self.ground_truth_list
            }
        )  
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(context_recall))
        return score
    

    def contextEntitiesRecall(self):
        dataset = Dataset.from_dict({
            'contexts': self.context_list,
            'ground_truth': self.ground_truth_list
        })
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(context_entity_recall))
        return score
    

    def noiseSensitivity(self):
        dataset = Dataset.from_dict({
            "question": self.question_list,
            "ground_truth": self.ground_truth_list,
            "answer": self.answer_list,
            "contexts": self.context_list
        })
        # metrics = [noise_sensitivity_relevant, noise_sensitivity_irrelevant]

        score = evaluate(dataset,metrics=self.set_llm_and_embeddings(noise_sensitivity_relevant))
        return score

    def answerSementicSimilarity(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list
            }
        )  
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(answer_similarity))
        return score
    

    def answerCorrectness(self):
        dataset = Dataset.from_dict(
             {
                'question': self.question_list,
                'answer' : self.answer_list,
                'contexts': self.context_list
            }
        )  
        score = evaluate(dataset, metrics=self.set_llm_and_embeddings(answer_correctness))
        return score
    

    def aspectCritique(self, name, definition):
        dataset = Dataset.from_dict({
            'question': self.question_list,
            'answer': self.answer_list,
            'contexts': self.context_list
        })        
        critic = AspectCritic(name=name, definition=definition)
        
        metrics = self.set_llm_and_embeddings(critic)
        
        score = evaluate(dataset, metrics=metrics)
        return score




            





        

