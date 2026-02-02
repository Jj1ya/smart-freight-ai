# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 주소 가져오기
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 1. 엔진 생성 (DB와 연결하는 커넥터)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. 세션 공장 생성 (데이터를 주고받을 통로)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 베이스 클래스 생성 (모든 모델의 조상)
Base = declarative_base()