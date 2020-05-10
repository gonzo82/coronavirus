import MySQLdb
import sqlite3
from coronavirus_db_connection import *
from coronavirus_qslSentence_sqlite import (
    SELECT_CORONAVIRUS_STATEMENT,
    SELECT_GEOGRAPHY_STATEMENT,
    INSERT_STATEMENT,
    INSERT_COUNTRY_STATEMENT,
    INSERT_REGION_STATEMENT,
    INSERT_SUBREGION_STATEMENT,
    INSERT_NULL_SUBREGIONS,
    INSERT_NULL_REGIONS,
    DELETE_STATEMENT
)


class Database:
    mydb = sqlite3.connect(DDBB_SQL_LITE)

    cursor = mydb.cursor()

    def insert_coronavirus(self, coronavirus_data):
        for cd in coronavirus_data:
            try:
                self.cursor.execute(INSERT_STATEMENT, cd)
            except:
                print('The next row give error: {}'.format(cd))
        self.mydb.commit()
        return

    def insert_country(self, countries):
        for c in countries:
            row = [c['id'], c['name'], c['name_es'], c['name'], c['name_es']]
            self.cursor.execute(INSERT_COUNTRY_STATEMENT, row)
        self.mydb.commit()
        return

    def insert_region(self, country_id, regions):
        for c in regions:
            row = [country_id, c['id'], c['name'], c['name_es'], c['name'], c['name_es']]
            self.cursor.execute(INSERT_REGION_STATEMENT, row)
        self.mydb.commit()
        return

    def insert_subregion(self, country_id, region_id, sub_regions):
        for sr in sub_regions:
            row = [region_id, sr['id'], sr['name'], sr['name_es'], sr['name'], sr['name_es']]
            self.cursor.execute(INSERT_SUBREGION_STATEMENT, row)
        self.mydb.commit()
        return

    def create_null_geography(self):
        self.cursor.execute(INSERT_NULL_REGIONS)
        self.cursor.execute(INSERT_NULL_SUBREGIONS)
        self.mydb.commit()

    def coronavirus_data(self):
        self.cursor.execute(SELECT_CORONAVIRUS_STATEMENT)
        result = self.cursor.fetchall()
        return result

    def coronavirus_geography(self):
        self.cursor.execute(SELECT_GEOGRAPHY_STATEMENT)
        result = self.cursor.fetchall()
        return result

    def coronavirus_data_list(self):
        self.cursor.execute(SELECT_CORONAVIRUS_STATEMENT)
        result = self.cursor.fetchall()
        # The row name is the first entry for each entity in the description tuple.
        gsheet_list = []
        column_names = list()
        for i in self.cursor.description:
            column_names.append(i[0])

        gsheet_list.append(list(column_names))

        for row in result:
            gsheet_list.append(list(row))

        return gsheet_list

    def coronavirus_geography_list(self):
        self.cursor.execute(SELECT_GEOGRAPHY_STATEMENT)
        result = self.cursor.fetchall()
        # The row name is the first entry for each entity in the description tuple.
        gsheet_list = []
        column_names = list()

        for i in self.cursor.description:
            column_names.append(i[0])
        gsheet_list.append(list(column_names))

        for row in result:
            gsheet_list.append(list(row))

        return gsheet_list

    def update_rank(self):
        try:
            self.cursor.callproc('coronavirus.update_countries_ranks', ())
        except:
            pass
        self.mydb.commit()

    def delete_last_days(self, from_date):
        row = [from_date, ]
        self.cursor.execute(DELETE_STATEMENT, row)
        self.mydb.commit()

    def __init__(self):
        self.mydb = sqlite3.connect(DDBB_SQL_LITE)
        self.cursor = self.mydb.cursor()
        return

    def __del__(self):
        self.cursor.close()
        self.mydb.close()
        return

if __name__ == '__main__':
    ddbb = Database()
    print(ddbb.coronavirus_geography_list())
    pass

