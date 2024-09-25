
from sqlalchemy import create_engine, Column, Integer, String, JSON, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
Base = declarative_base()
class Task(Base):
    __tablename__ = 'tasks'

    taskid = Column(String, primary_key=True, name="taskid")  # lowercase column names
    question = Column(String, nullable=False, name="question")
    expectedanswer = Column(String, name="expectedanswer")
    level = Column(Integer, name="level")
    filename = Column(String, name="filename")
    filepath = Column(String, name="filepath")
    annotations = Column(JSON, name="annotations")

    def __repr__(self):
        return f"<Task(taskid='{self.taskid}', question='{self.question[:30]}...', level={self.level})>"

class LLM(Base):
    __tablename__ = 'llms'

    llmid = Column(Integer, primary_key=True, name="llmid")
    llmname = Column(String, nullable=False, name="llmname")
    version = Column(String, name="version")
    parameters = Column(String, name="parameters")

    def __repr__(self):
        return f"<LLM(llmid={self.llmid}, llmname='{self.llmname}', version='{self.version}')>"

class LLMResponse(Base):
    __tablename__ = 'llmresponses'

    responseid = Column(Integer, primary_key=True, name="responseid")
    taskid = Column(String, name="taskid")
    llmid = Column(Integer, name="llmid")
    responsetext = Column(String, nullable=False, name="responsetext")
    isannotated = Column(Boolean, default=False, name="isannotated")
    resultcategory = Column(String, name="resultcategory")
    timestamp = Column(DateTime, default=datetime.utcnow, name="timestamp")

    def __repr__(self):
        return f"<LLMResponse(responseid={self.responseid}, taskid='{self.taskid}', llmid={self.llmid})>"
#TODO: Update url locally
# Database connection
DATABASE_URL = "***"
engine = create_engine(DATABASE_URL)
SessionMaker = sessionmaker(bind=engine)
