from . import *

class EIA_Imports(Base):
    __tablename__ = 'eia_imports'
    
    id          = Column(Integer, primary_key=True)
    # time we requested the price
    p_time      = Column(DateTime)
    # time the price was reported
    date        = Column(DateTime, unique=True)
    value       = Column(Integer)


class EIA_Exports(Base):
    __tablename__ = 'eia_exports'
    
    id          = Column(Integer, primary_key=True)
    # time we requested the price
    p_time      = Column(DateTime)
    # time the price was reported
    date        = Column(DateTime, unique=True)
    value       = Column(Integer)



