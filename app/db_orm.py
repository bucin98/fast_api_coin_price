from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()


class Pairs(Base):
    __tablename__ = 'pairs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    binance_name = Column(String)
    coingeko_name = Column(String)


class Database:
    def __init__(self):
        db_log, db_pass, db_name = os.environ['POSTGRES_USER'], os.environ['POSTGRES_PASSWORD'], os.environ[
            'POSTGRES_DB']
        self.DB_URL = f'postgresql://{db_log}:{db_pass}@db:5432/{db_name}'
        self.engine = create_engine(self.DB_URL)
        self.Session = sessionmaker(bind=self.engine)

    def destroy_tables(self):
        Base.metadata.drop_all(self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def get_pairs(self):
        with self.get_session() as session:
            pairs = session.query(Pairs).all()
            return [{'name': pair.name, "binance_name": pair.binance_name, "coingeko_name": pair.coingeko_name} for pair
                    in pairs]


if __name__ == '__main__':
    a = Database()
    a.destroy_tables()
    a.create_tables()
