# https://api.covid19tracking.narrativa.com/api/countries

from urllib.request import urlopen
from coronavirus_database import Database
import datetime
import json


class Json:

    mydb = Database()

    def read_row(self, data, date, country_id, region_id, subregion_id):
        """
        Esta función, genera una lista desde un diccionario con los elementos
        que tiene que tener y en el orden que tienen que tener
        """
        if region_id == '':
            region_id = country_id
        if subregion_id == '':
            subregion_id = region_id
        row = []
        row.append(country_id)
        row.append(region_id)
        row.append(subregion_id)
        row.append(date)
        try:
            row.append(data['today_confirmed'])
        except:
            row.append('0')
        try:
            row.append(data['today_deaths'])
        except:
            row.append('0')
        try:
            row.append(data['today_recovered'])
        except:
            row.append('0')
        try:
            row.append(data['today_open_case'])
        except:
            row.append('0')

        try:
            row.append(data['today_new_confirmed'])
        except:
            row.append('0')
        try:
            row.append(data['today_new_deaths'])
        except:
            row.append('0')
        try:
            row.append(data['today_new_recovered'])
        except:
            row.append('0')
        try:
            row.append(data['today_new_open_case'])
        except:
            row.append('0')

        try:
            row.append(data['yesterday_confirmed'])
        except:
            row.append('0')
        try:
            row.append(data['yesterday_deaths'])
        except:
            row.append('0')
        try:
            row.append(data['yesterday_recovered'])
        except:
            row.append('0')
        try:
            row.append(data['yesterday_open_case'])
        except:
            row.append('0')
        return row

    def get_data(self, country_id, country, region_id, subregion_id, from_date, to_date):
        url_subregion = 'https://api.covid19tracking.narrativa.com/api' \
                        '/country/{country_id}'.format(country_id=country_id)
        if region_id != '':
            url_subregion = url_subregion + '/region/{region_id}'.format(region_id=region_id)
        if subregion_id != '':
            url_subregion = url_subregion + '/sub_region/{subregion_id}'.format(subregion_id=subregion_id)
        url_subregion = url_subregion + \
                        '?date_from={from_date}&date_to={to_date}'.format(from_date=from_date, to_date=to_date)
        rows = []
        try:
            json_url = urlopen(url_subregion)
            json_data = json.loads(json_url.read())['dates']
            for j in json_data:
                date = '' + j
                if subregion_id != '':
                    data = json_data[date]['countries'][country]['regions'][0]['sub_regions'][0]
                elif region_id != '':
                    data = json_data[date]['countries'][country]['regions'][0]
                else:
                    data = json_data[date]['countries'][country]
                row = self.read_row(data, date, country_id, region_id, subregion_id)
                rows.append(row)
        except:
            print('Error al obtener: {url}'.format(url=url_subregion))
        return rows

    def load_subregion_by_region(self, url, country_id, country, region_id, from_date, to_date):
        url = 'https://api.covid19tracking.narrativa.com{url}'.format(url=url)
        json_url = urlopen(url)
        sub_regions = json.loads(json_url.read())['countries']
        rows = []
        for sr in sub_regions[0][country_id][region_id]:
            # print('        Sub Region: {}'.format(sr['name']))
            row_aux = self.get_data(
                        country_id=country_id,
                        country=country,
                        region_id=region_id,
                        subregion_id=sr['id'],
                        from_date=from_date,
                        to_date=to_date
                    )
            rows = rows + row_aux
        return rows

    def load_region_by_country(self, url, country_id, country, from_date, to_date):
        url = 'https://api.covid19tracking.narrativa.com{url}'.format(url=url)
        json_url = urlopen(url)
        regions = json.loads(json_url.read())['countries']
        rows = []
        for r in regions[0][country_id]:
            print('    Region: {}'.format(r['name']))
            rows_aux = self.get_data(
                country_id=country_id,
                country=country,
                region_id=r['id'],
                subregion_id='',
                from_date=from_date,
                to_date=to_date
            )
            rows = rows + rows_aux
        return rows

    def load_country(self, from_date, to_date, country):
        """Esta función obtiene un json de una api web y lo devuelve"""

        url = 'https://api.covid19tracking.narrativa.com/api/countries'
        json_url = urlopen(url)
        countries = json.loads(json_url.read())['countries']
        rows = []
        for c in countries:
            if c['name'] == country or country == '':
                rows_aux = []
                if c['name'] == 'Spain':
                    rows_aux = self.load_region_by_country(
                        url=c['links'][0]['href'],
                        country_id=c['id'],
                        country=c['name'],
                        from_date=from_date,
                        to_date=to_date
                    )

                if not rows_aux:
                    rows_aux = self.get_data(
                        country_id=c['id'],
                        country=c['name'],
                        region_id='',
                        subregion_id='',
                        from_date=from_date,
                        to_date=to_date
                    )
                rows = rows + rows_aux
                if rows_aux:
                    self.mydb.insert_coronavirus(rows_aux)
        return

    def load_countries(self):
        """Esta función obtiene un json de una api web y lo devuelve"""

        url = 'https://api.covid19tracking.narrativa.com/api/countries'
        json_url = urlopen(url)
        countries = json.loads(json_url.read())['countries']
        self.mydb.insert_country(countries=countries)
        print('Countries have been loaded')
        return

    def load_regions(self):
        url = 'https://api.covid19tracking.narrativa.com/api/countries/spain/regions'
        json_url = urlopen(url)
        regions_aux = json.loads(json_url.read())['countries'][0]
        country_id = list(regions_aux.keys())[0]
        regions = regions_aux['spain']
        for c in regions:
            self.mydb.insert_region(country_id, regions)
            # self.load_subregions(
            #     country_id=country_id,
            #     region_id=c['id'],
            #     url=c['links'][0]['href']
            # )

        self.mydb.create_null_geography()
        print('Regions and subregions have been loaded')

        return

    def load_subregions(self, country_id, region_id, url):
        url = 'https://api.covid19tracking.narrativa.com{url}'.format(url=url)
        json_url = urlopen(url)
        sub_regions = json.loads(json_url.read())['countries']
        self.mydb.insert_subregion(country_id, region_id, sub_regions[0][country_id][region_id])

        return

# Este main es para hacer las cargas iniciales
if __name__ == '__main__':
    json_var = Json()
    database = Database()

    days_per_block = 7
    from_dt = datetime.datetime.strptime('2020-02-01', '%Y-%m-%d')
    to_dt = from_dt + datetime.timedelta(days=days_per_block)
    until_dt = datetime.datetime.strptime('2020-05-05', '%Y-%m-%d')

    while from_dt < until_dt:
        print("Principio de vuelta {}".format(datetime.datetime.now()))
        from_date = datetime.date.strftime(from_dt, "%Y-%m-%d")
        to_date = datetime.date.strftime(to_dt, "%Y-%m-%d")
        json_var.load_country(from_date=from_date, to_date=to_date, country='Spain')
        from_dt = to_dt + datetime.timedelta(days=1)
        to_dt = from_dt + datetime.timedelta(days=days_per_block)
        print("Fin de vuelta {}".format(datetime.datetime.now()))
