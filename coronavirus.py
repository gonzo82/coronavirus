import datetime

from coronavirus_database import Database
from coronavirus_json import Json
from coronavirus_gsheet import Gsheet


if __name__ == '__main__':
    today = datetime.datetime.now()
    to_dt = today - datetime.timedelta(days=1)
    from_dt = to_dt - datetime.timedelta(days=2)
    to_date = datetime.date.strftime(to_dt, "%Y-%m-%d")
    from_date = datetime.date.strftime(from_dt, "%Y-%m-%d")
    print(f'{to_dt}, {from_dt}')

    # from_date = '2020-05-21'
    # to_date = '2020-05-22'
    database = Database()
    json = Json()
    gsheet = Gsheet()

    database.delete_last_days(from_date)

    print('Database deleted')

    json.load_countries()
    json.load_regions()
    json.load_country(from_date=from_date, to_date=to_date, country='')

    print('Database loaded')

    database.update_rank()

    print('Database updated')

    gsheet.create_data_sheet()
    gsheet.create_countries_sheet()

    print('Gsheet loaded')


