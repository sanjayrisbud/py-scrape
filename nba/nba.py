'''
sample robot to demonstrate the framework
this robot goes to nba.com and scrapes each team's player names
to perform a full run (save pages and scrape), execute the robot without parameters
to only scrape from previously saved pages, execute the robot specifying fetch date as parameter e.g. scrape,12/1/2019
'''

import os
import sys
from datetime import datetime

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.raw_req import RawRequests
from framework.csv_int import CsvInterface
from nba.player import Player


class TestRobot(RawRequests):
    path = None
    htmlpath = None
    csv = None
    p = None

    def __init__(self, args):
        super().__init__(args)
        self.p = Player(self._robotname, self._executionid)
        if self.GenericInput.longText1 == "":
            self.p.FetchDate = self.date()
        else:
            self.p.FetchDate = datetime.strptime(self.GenericInput.longText1.split(",")[1], "%m/%d/%Y")
        self.path = os.path.join(os.path.dirname(__file__), f"{self.p.FetchDate.strftime('%Y_%m_%d')}")
        self.htmlpath = os.path.join(self.path, f"html{os.path.sep}")
        csvpath = os.path.join(self.path, f"csv{os.path.sep}")
        os.makedirs(self.htmlpath, exist_ok=True)
        os.makedirs(csvpath, exist_ok=True)
        self.csv = CsvInterface("output.csv", path=csvpath)
        self.csv.writerow(self.p.row(header=True))

    def run(self):
        if self.GenericInput.longText1.startswith("scrape"):
            with open(f"{self.htmlpath}teams.html", "r") as f:
                html = f.read()
            soup = BeautifulSoup(html, "lxml")
            menu = soup.find("div", class_="team__list_wrapper")
            for l in menu.find_all("a"):
                url = l.get("href")
                filename = f'{url.split("/")[-1]}.html'
                self.logger.info(f"Reading {filename}...")
                with open(f"{self.htmlpath}{filename}", "r") as f:
                    html = f.read()
                self.scrape(html)
        else:
            response = self.get("https://www.nba.com/teams")
            self.wait()
            html = response.text

            # not essential; only included to fix css and images
            html = html.replace('href="/', 'href="https://www.nba.com/')
            html = html.replace('class="lazyload" data-src="', 'src="https:')

            with open(f"{self.htmlpath}teams.html", "w") as f:
                f.write(html)
            soup = BeautifulSoup(html, "lxml")
            menu = soup.find("div", class_="team__list_wrapper")
            for l in menu.find_all("a"):
                url = l.get("href")
                self.logger.info(f"Now loading {url}...")
                response = self.get(url)
                self.wait()
                html = response.text

                # not essential; only included to fix css and images
                html = html.replace('href="/', 'href="https://www.nba.com/')
                html = html.replace('class="lazyload" data-src="', 'src="https:')

                filename = f'{url.split("/")[-1]}.html'
                with open(f"{self.htmlpath}{filename}", "w") as f:
                    f.write(html)
                self.scrape(html)

    def scrape(self, page):
        self.logger.info("Processing page...")
        soup = BeautifulSoup(page, "lxml")
        team = soup.find("div", class_="nba-team-header__team-location").get_text()
        self.p.Team = " ".join(team.split())
        players_section = soup.find("section", class_="nba-player-index")
        for player in players_section.find_all("section", class_="nba-player-index__trending-item"):
            self.p.Jersey = player.span.text
            self.p.Name = player.a["title"]
            self.p.URL = player.a["href"]
            details = player.find("div", class_="nba-player-index__details")
            self.p.Position = details.span.text
            vitals = details.find_all("span")[1].get_text()
            vitals = " ".join(vitals.split()).replace(" | ", "|")
            self.p.Height, self.p.Weight = vitals.split('|')
            self.csv.writerow(self.p.row())
        self.logger.info("Done!")


if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.use_proxies = False
    tr.use_random_agents = False
    tr.execute()
