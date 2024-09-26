from typing import Type

from sqlalchemy.orm import Session, sessionmaker
from src.data_layer.models import Task, LLM, LLMResponse
from sqlalchemy import func, create_engine
import toml
import streamlit as st
class DataAccess:
    def __init__(self):
        DATABASE_URL = st.secrets["database"]["database_url"]

        engine = create_engine(DATABASE_URL)
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        print("Connected to database")
        self.session = session

    def get_all_tasks(self):
        return self.session.query(Task).all()
    def get_random_task_that_is_not_tested(self) -> Type[Task]| None:
        # Perform a left join between Task and LLMResponse, then filter where LLMResponse is NULL
        return (
            self.session.query(Task)
            .outerjoin(LLMResponse, Task.taskid == LLMResponse.taskid)
            .filter(LLMResponse.taskid == None)
            .order_by(func.random())  # Random order
            .first()  # Get one random task
        )

    def get_random_task(self):
        return (
            self.session.query(Task)
            .filter(Task.filename != None)
            .order_by(func.random())
            .first()
        )

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

    def query_by_file_type(self, file_extension: str):
        return (self.session.query(Task).filter(
            func.right(Task.filename, len(file_extension) + 1).like(f'.{file_extension}')
        ).order_by(func.random())
                .first())


data_access_instance = DataAccess()

if __name__ == "__main__":
    data_access_instance = DataAccess()

