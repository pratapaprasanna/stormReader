from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.sql.sqltypes import Float

Base = declarative_base()


class Forecast(Base):
    __tablename__ = 'forecast'
    forecast_epoch = Column(BigInteger, primary_key=True, nullable=False)
    storm_id = Column(String, primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    intensity = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Forecast(forecast_epoch='{self.forecast_epoch}, \
            storm_id='{self.storm_id}, latitude='{self.latitude}', \
            longitude={self.longitude}, intensity={self.intensity})>"


class Historical(Base):
    __tablename__ = 'historical'
    id = Column(Integer, primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    intensity = Column(Float, nullable=False)
    storm_id = Column(String, nullable=False)
    entry_date = Column(Date)

    def __repr__(self):
        return f"<Historical(region_id='{self.region_id}, latitude='{self.latitude}', \
            longitude={self.longitude}, intensity={self.intensity}, entry={self.entry_date})>"