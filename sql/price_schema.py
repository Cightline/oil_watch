from . import *

class Price(Base):
    __tablename__ = 'prices'
    
    id          = Column(Integer, primary_key=True)

    # time we requested the price
    p_time      = Column(DateTime)
    # time the price was reported
    r_time      = Column(DateTime)
    
    price       = Column(Float)
    ticker      = Column(String(100))




