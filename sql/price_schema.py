from . import *

class Price(Base):
    __tablename__ = 'prices'
    
    id          = Column(Integer, primary_key=True)

    # time we requested the price
    request_time      = Column(DateTime)
    # time the price was reported
    publish_time      = Column(DateTime)
    
    price       = Column(Float)
    ticker      = Column(String(100))
    name        = Column(String(200))
    open_price  = Column(Float)
    previous_close = Column(Float)




