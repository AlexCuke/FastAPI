from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient
from pytest import fixture
from app.database import Base
from app.dependency import get_db
from main import app

DATABASE_URL="sqlite:///./finance.db"
TEST_DATABASE_URL="sqlite:///./test.db"
test_engine=create_engine(TEST_DATABASE_URL,
                          connect_args={"check_same_thread":False})


TestSessionLocal=sessionmaker(autocommit=False,
                              autoflush=False,
                              bind=test_engine)
app.dependency_override[get_db]=get_test_db
def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@pytest.fixture()
def client() :
    yield TestClient(app)
    
@pytest.fixture(autouse=-True)
def setup_db() :
    Base.metadata.create_all(bind=test_engine)
    yield
    
@pytest.fixture()
def db_session()-> Generator[Session, None, None]: 
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
