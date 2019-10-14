import requests
from bs4 import BeautifulSoup

from src.exceptions import FetchingPageException


class UFOScraper:

    # TODO PROGRESS BAR AND EXCEPTIONS and COMENTAR CÓDIGO PARA QUE SE ENTIENDA
    # https://pypi.org/project/progress/
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#encodings
    def __init__(self, year_limit, output_file):
        self.base_url = "http://www.nuforc.org/webreports/"
        self.principal_url = self.base_url + "ndxevent.html"
        self.reports = None  # dataframe containing the data
        # by default get all the reports between 2019 and 1800
        self.year_limit = year_limit
        self.output_file = output_file

        self.bar = None  # progress bar

    def get_page_html(self, url, retries=4):
        """
        Get a page's source code
        :param retries: number of times to try to get the page
        :param url: the url of the page to fetch
        :return: the page
        """
        try:
            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/77.0.3865.90 Safari/537.36",
            }

            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                raise Exception()
        except (requests.exceptions.RequestException, Exception) as e:
            if retries == 0:
                # TODO PRobar el mensaje que se imprime por pantalla si esto
                #  sucede
                raise FetchingPageException()
            else:
                # try again
                return self.get_page_html(url, retries - 1)

    def metodo_sucio(self, content, nombre):
        with open("temp/{}.html".format(nombre), "w") as file:  # TODO borrar
            file.write(str(content))

    def get_reports_links_by_month(self):
        """
        Get the reports' pages links
        :return:
        """
        html = self.get_page_html(self.principal_url)
        table_links = html.find("table").findAll('a')
        report_links = []

        for link in table_links:
            month_year = link.text
            year = month_year.split("/")[1]
            if self.year_limit > int(year):
                break

            link_suffix = link.get('href')
            report_links.append(link_suffix)

        self.metodo_sucio(str(report_links), "sf")
        return report_links

    def get_a_month_reports_info(self, link_suffix):
        """
        Collect a month's ufo info
        :param link_suffix: The link suffix of the page
        :return:
        """
        html = self.get_page_html(self.base_url + link_suffix)
        self.metodo_sucio(html, "ucollect")

        table = html.find('table')
        table_header = table.find("thead")
        table_body = table.find("tbody")
        table_rows = table.find_all("tr")
        self.metodo_sucio(table_rows, "trcollect")

        #cuidado celdas vacías -- http://www.nuforc.org/webreports/ndxe199502.html
        # get_report_info()
        # a = html_document.encode("iso-8859-1") solo para los strings con
        # string(var, encode=....
        exit(1)

    def scrape(self):
        """
        Scrape the UFO page
        :return:
        """
        reports_links_by_month = self.get_reports_links_by_month()
        for month_report_link in reports_links_by_month:
            self.get_a_month_reports_info(month_report_link)

    def save_to_file(self):
        """
        Save the collected data to file
        :return:
        """
        self.reports.to_csv(self.output_file)
