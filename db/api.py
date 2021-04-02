import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import config
from db import models
from db.models import Base

from contextlib import contextmanager

engine = create_engine(config.DATABASE_URI)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    Base.metadata.create_all(engine)


def check_tables(table):
    if table in engine.table_names():
        return True
    else:
        return False


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_values_forecast(forecast_epoch, storm_id, lat, long, intensity):
    forecast = models.Forecast(
        forecast_epoch=forecast_epoch,
        storm_id=storm_id,
        longitude=long,
        latitude=lat,
        intensity=intensity
    )
    with session_scope() as sess:
        forecast_ref = sess.query(models.Forecast).\
            filter_by(forecast_epoch=forecast_epoch, storm_id=storm_id)
        if forecast_ref.first():
            values = dict()
            values['longitude'] =  long
            values['latitude'] = lat
            values['intensity'] = intensity
            forecast_ref.update(values)
        else:
            sess.add(forecast)


def insert_values_historical(lat, long, intensity, storm_id, doc):
    historical = models.Historical(
        id=str(uuid.uuid4()).split('-')[0],
        latitude=lat,
        longitude=long,
        intensity=intensity,
        storm_id=storm_id,
        entry_date=doc
    )
    with session_scope() as sess:
        sess.add(historical)


def fetch_data_forecast(storm_id):
    sess = Session()
    sess.query(models.Forecast)
    data = sess.query(models.Forecast).filter(models.Forecast.storm_id.in_([storm_id])).all()
    return data


def fetch_data_historical(storm_id):
    sess = Session()
    sess.query(models.Historical)
    data = sess.query(models.Historical).filter(models.Historical.storm_id.in_([storm_id])).all()
    return data
