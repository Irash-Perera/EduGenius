class Session:
    def __init__(self,session_state,question):
        if session_state["authentication_status"]:
            self.user_name = session_state["name"]
            self.user_email = session_state["email"]
            self.question = question
            self.answer = ""
            self.correctness = ""
            self.marks = ""
            self.explanation = ""
            self.improvements = ""
            self.similar_problems = ""
            self.hint = ""
            self.QAs = []
        else:
            raise Exception("User not authenticated")

    def set_json_response(self,json_object):
        try:
            self.correctness = json_object["Correctness"]["content"]
        except: 
            pass
        try:
            self.marks = json_object["Marks"]["content"]
        except: 
            pass
        try:
            self.explanation = json_object["Explanation"]["content"]
        except:
            pass
        try:
            self.improvements = json_object["Improvements"]["content"]
        except:
            pass
        try:
            self.similar_problems = json_object["Similar Problems"]["content"]
        except:
            pass

    def add_chat(self,user_question, system_answer):
        self.QAs.append({
            "user" : user_question,
            "assistant" :  system_answer
        })

    def get_QAs(self):
        QA_text = ""
        for QA in self.QAs:
            QA_text += f"User : {QA['user']}\nAssistant : {QA['assistant']}\n"
        return QA_text


    def get_current_context(self):
        text = f"""
        question : {self.question}
        answer : {self.answer}
        correctness : {self.correctness}
        marks : {self.marks}
        explanation : {self.explanation}
        improvements : {self.improvements}
        similar_problems : {self.similar_problems}
        hint : {self.hint}
        QAs : {self.get_QAs()}
        """
        return text

        

