from sqlalchemy.orm import Session
from models import Task, LLM, LLMResponse

class DataAccess:
    def __init__(self, session: Session):
        self.session = session

    def get_all_tasks(self):
        return self.session.query(Task).all()

    def get_task_by_id(self, task_id: str):
        return self.session.query(Task).filter(Task.taskid == task_id).first()

    def get_tasks_by_level(self, level: int):
        return self.session.query(Task).filter(Task.level == level).all()

    def get_all_llms(self):
        return self.session.query(LLM).all()

    def get_llm_by_id(self, llm_id: int):
        return self.session.query(LLM).filter(LLM.llmid == llm_id).first()

    def get_responses_for_task(self, task_id: str):
        return self.session.query(LLMResponse).filter(LLMResponse.taskid == task_id).all()

    def get_responses_for_llm(self, llm_id: int):
        return self.session.query(LLMResponse).filter(LLMResponse.llmid == llm_id).all()