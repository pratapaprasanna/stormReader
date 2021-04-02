from datetime import datetime


def get_epoch_time(date_str, format="%Y-%m-%d:%H:%M"):
    return int(datetime.strptime(date_str, format).\
                              timestamp() * 1000)