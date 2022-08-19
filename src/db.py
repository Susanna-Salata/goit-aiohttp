from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table


engine = create_engine(
    "sqlite:///exchange.db", connect_args={"check_same_thread": False}, echo=True
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()


async def db_context(app):
    url_db = f"sqlite:///exchange.db"
    DBSession = sessionmaker(bind=create_engine(url_db))
    session = DBSession()
    app['db_session'] = session
    yield
    app['db_session'].close()


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False)

    # source = relationship("Source", back_populates="source")


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, autoincrement=False)
    code = Column(String(3), nullable=False)
    sign = Column(String(1), nullable=False)

    # rate = relationship("Rate", back_populates="currency")


class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rate = Column(Float, nullable=True)
    created = Column(DateTime, default=datetime.now())
    currency_id = Column(Integer, ForeignKey(Currency.id, ondelete="CASCADE"))
    source_id = Column(Integer, ForeignKey(Source.id, ondelete="CASCADE"))

    # currency = relationship("Currency", back_populates="rate")
    # source = relationship("Source", back_populates="rate")
