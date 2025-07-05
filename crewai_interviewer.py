
# Import necessary types for type hinting
from typing import List, Dict, Any


# Guardrails class to validate candidate responses
class Guardrails:
    @staticmethod
    def check_response(response: str) -> bool:
        # Block empty or inappropriate responses
        inappropriate_keywords = ['offensive', 'inappropriate', 'nonsense']
        if not response.strip():  # Check for empty response
            return False
        for word in inappropriate_keywords:
            if word in response.lower():  # Check for inappropriate keywords
                return False
        return True


# ContextManager class to keep track of the interview Q&A
class ContextManager:
    def __init__(self):
        # Store history as a list of question/response dicts
        self.history: List[Dict[str, Any]] = []

    def add_entry(self, question: str, response: str):
        # Add a new Q&A entry to the history
        self.history.append({'question': question, 'response': response})

    def get_context(self) -> List[Dict[str, Any]]:
        # Return the full interview context
        return self.history


# SkillModule class to represent a skill and its questions
class SkillModule:
    def __init__(self, skill_name: str, questions: List[str]):
        self.skill_name = skill_name  # Name of the skill (e.g., Python)
        self.questions = questions    # List of questions for the skill

    def get_questions(self) -> List[str]:
        # Return the list of questions for this skill
        return self.questions


# InterviewerAgent class to manage the interview process
class InterviewerAgent:
    def __init__(self, skills: List[SkillModule]):
        self.skills = skills  # List of SkillModule objects
        self.context = ContextManager()  # Context manager instance
        self.guardrails = Guardrails()   # Guardrails instance

    def conduct_interview(self):
        print("Welcome to the CrewAI Interviewer Agent!")
        # Iterate through each skill module
        for skill in self.skills:
            print(f"\n--- {skill.skill_name} Section ---")
            # Ask each question for the current skill
            for question in skill.get_questions():
                print(f"Question: {question}")
                response = input("Your answer: ")  # Get candidate response
                # Check response with guardrails
                if not self.guardrails.check_response(response):
                    print("Response failed guardrails. Please provide an appropriate answer.")
                    continue
                # Add valid response to context
                self.context.add_entry(question, response)
        print("\nInterview complete. Thank you!")
        print("Interview Context:")
        # Print the full interview context
        for entry in self.context.get_context():
            print(f"Q: {entry['question']}\nA: {entry['response']}\n")


# Main function to set up and run the interviewer agent
def main():
    # Define questions for each skill
    python_questions = [
        "Explain the difference between a list and a tuple in Python.",
        "How do you handle exceptions in Python?"
    ]
    pyspark_questions = [
        "What is an RDD in PySpark?",
        "How do you optimize PySpark jobs for large datasets?"
    ]
    sql_questions = [
        "Write a SQL query to find duplicate records in a table.",
        "Explain the difference between INNER JOIN and LEFT JOIN."
    ]
    kubernetes_questions = [
        "What is a Kubernetes pod?",
        "How do you perform rolling updates in Kubernetes?"
    ]

    # Create SkillModule objects for each skill
    skills = [
        SkillModule("Python", python_questions),
        SkillModule("PySpark", pyspark_questions),
        SkillModule("SQL", sql_questions),
        SkillModule("Kubernetes", kubernetes_questions)
    ]

    # Instantiate the interviewer agent and start the interview
    agent = InterviewerAgent(skills)
    agent.conduct_interview()

# Entry point for the script
if __name__ == "__main__":
    main()
