import requests
from bs4 import BeautifulSoup

from dataframer import DataFramer
from exceptions import FetchingPageException


class UFOScraper:

    def __init__(self, year_limit, output_file):
        self.base_url = "http://www.nuforc.org/webreports/"
        self.principal_url = self.base_url + "ndxevent.html"
        self.reports = None  # dataframe containing the data
        # by default get all the reports between 2019 and 1800
        self.year_limit = year_limit
        self.output_file = output_file

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
            response.encoding = "cp1252"
            if response.status_code == 200:
                return BeautifulSoup(response.text,
                                     'html.parser')
            else:
                raise Exception()
        except (requests.exceptions.RequestException, Exception):
            if retries == 0:
                raise FetchingPageException("Could not get one of the pages")
            else:
                # try again
                return self.get_page_html(url, retries - 1)

    def get_reports_links(self):
        """
        Get the reports' pages links
        :return:
        """
        html = self.get_page_html(self.principal_url)
        table_links = html.find("table").findAll('a')
        report_links = []

        for link in table_links:
            month_year = link.text

            if "UNSPECIFIED" in month_year:
                break

            year = month_year.split("/")[1]
            if self.year_limit > int(year):
                break

            link_suffix = link.get('href')
            report_links.append(link_suffix)

        return report_links

    def get_a_month_reports(self, link_suffix):
        """
        Collect a month's ufo info
        :param link_suffix: The link suffix of the page
        """
        html = self.get_page_html(self.base_url + link_suffix)
        table = html.find('table')

        if self.reports is None:
            # if this is the first scraped month create a dataframe and get
            # column names
            table_header = [x.text for x in table.find("thead").find_all('th')]
            column_names = table_header
            self.reports = DataFramer.initialize_dataframe(column_names)

        table_rows = table.find("tbody").find_all("tr")

        for row in table_rows:
            # add info of a single report to the dataframe with the rest of
            # them
            row_elements = [x.text.replace(";", "") for x in
                            row.find_all("font")]
            self.reports = DataFramer.append_to(self.reports, row_elements)

    def scrape(self):
        """
        Scrape the UFO page
        :return:
        """
        print("Getting report links")
        reports_links_by_month = self.get_reports_links()
        print("Links obtained")
        print("Scraping reports")
        num_reports = len(reports_links_by_month)
        i = 1
        for month_report_link in reports_links_by_month:
            print("{}/{}".format(i, num_reports))
            self.get_a_month_reports(month_report_link)
            i += 1

    def save_to_file(self):
        """
        Save the collected data to file
        :return:
        """
        if self.reports is not None:
            DataFramer.export_to_csv(self.reports, self.output_file)
            print("The UFO dataset has been exported")
        else:
            raise Exception("There is no data to export")
