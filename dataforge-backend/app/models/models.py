from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    role = Column(String(50), default="member")
    workspace_id = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text)
    structured_intent = Column(JSON)
    dag_definition = Column(JSON)
    version = Column(Integer, default=1)
    status = Column(String(50), default="draft")  # draft, approved, running, completed, failed
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_monitor = Column(Boolean, default=False)
    schedule = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaskRun(Base):
    __tablename__ = "task_runs"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    status = Column(String(50), default="queued")  # queued, running, completed, failed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    records_collected = Column(Integer, default=0)
    error_log = Column(Text, nullable=True)
    progress = Column(Float, default=0.0)
    logs = Column(JSON, default=list)

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), index=True)
    type = Column(String(50))  # api, scrape, rss, search
    robots_allowed = Column(Boolean, default=True)
    trust_score = Column(Float, default=0.8)
    last_checked_at = Column(DateTime, default=datetime.utcnow)

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), index=True)
    task_run_id = Column(Integer, ForeignKey("task_runs.id"), nullable=True)
    entity_type = Column(String(100))
    field_values = Column(JSON)
    confidence_score = Column(Float, default=0.9)
    dedup_cluster_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class FieldProvenance(Base):
    __tablename__ = "field_provenance"
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("records.id"), index=True)
    field_name = Column(String(100))
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    source_url = Column(String(1024))
    extracted_at = Column(DateTime, default=datetime.utcnow)
    transformation_notes = Column(Text, nullable=True)
    confidence = Column(Float, default=0.9)
