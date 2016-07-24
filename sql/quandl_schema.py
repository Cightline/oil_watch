from . import *


class Quandl(Base):
    __tablename__ = 'quandl'
    
    id          = Column(Integer, primary_key=True)
    # time we requested the price
    p_time      = Column(DateTime)
    # time the price was reported
    date        = Column(DateTime)
    value       = Column(Float)
    code        = Column(String(200))




