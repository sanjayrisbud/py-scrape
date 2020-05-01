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
from nba.team import Team


class TestRobot(RawRequests):
    path = None
    htmlpath = None
    teamrsrcpath = None
    playerrsrcpath = None
    csv_team = None
    csv_player = None
    p = None
    t = None
    online = False

    def __init__(self, args):
        super().__init__(args)
        self.p = Player(self._robotname, self._executionid)
        self.t = Team(self._robotname, self._executionid)
        if self.GenericInput.longText1 == "":
            self.t.FetchDate = self.date()
        else:
            self.t.FetchDate = datetime.strptime(self.GenericInput.longText1.split(",")[1], "%m/%d/%Y")

        self.teamrsrcpath = os.path.join(os.path.dirname(__file__), f"rsrc{os.path.sep}team{os.path.sep}")
        self.playerrsrcpath = os.path.join(os.path.dirname(__file__), f"rsrc{os.path.sep}player{os.path.sep}")
        self.path = os.path.join(os.path.dirname(__file__), f"{self.t.FetchDate.strftime('%Y_%m_%d')}")
        self.htmlpath = os.path.join(self.path, f"html{os.path.sep}")
        csvpath = os.path.join(self.path, f"csv{os.path.sep}")
        os.makedirs(self.teamrsrcpath, exist_ok=True)
        os.makedirs(self.playerrsrcpath, exist_ok=True)
        os.makedirs(self.htmlpath, exist_ok=True)
        os.makedirs(csvpath, exist_ok=True)
        self.csv_team = CsvInterface("team.csv", path=csvpath)
        self.csv_team.writerow(self.t.row(header=True))
        self.csv_player = CsvInterface("player.csv", path=csvpath)
        self.csv_player.writerow(self.p.row(header=True))

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
            self.online = True
            response = self.get("https://www.nba.com/teams")
            self.wait()
            html = response.text

            # not essential; only included to fix css and images
            html = html.replace('href="/', 'href="https://www.nba.com/')
            html = html.replace('class="lazyload" data-src="', 'src="https:')

            soup = BeautifulSoup(html, "lxml")
            menu = soup.find("div", class_="team__list_wrapper")
            with open(f"{self.htmlpath}teams.html", "w") as f:
                f.write(str(menu))

            for team in menu.find_all("div", class_="team__list"):
                img = team.find("img")
                url = img["src"]
                self.t.Logo = f'{url.split("/")[-1]}'
                if self.online:
                    response = self.get(url)
                    with open(f"{self.teamrsrcpath}{self.t.Logo}", "wb") as f:
                        f.write(response.content)
                    self.wait()

                anchor = team.find("a")
                self.t.URL = anchor["href"]
                self.logger.info(f"Now loading {self.t.URL}...")
                response = self.get(self.t.URL)
                self.wait()
                html = response.text

                # not essential; only included to fix css and images
                html = html.replace('href="/', 'href="https://www.nba.com/')
                html = html.replace('class="lazyload" data-src="', 'src="https:')

                filename = f'{self.t.URL.split("/")[-1]}.html'
                with open(f"{self.htmlpath}{filename}", "w") as f:
                    f.write(html)
                self.scrape(html)

    def scrape(self, page):
        self.logger.info("Processing page...")
        soup = BeautifulSoup(page, "lxml")
        self.t.Id = soup.find("meta", attrs={"name": "teamId"})["content"]
        self.t.City = soup.find("p", class_="nba-team-header__city-name").get_text().strip()
        self.t.Name = soup.find("p", class_="nba-team-header__team-name").get_text().strip()
        self.csv_team.writerow(self.t.row())
        self._database.store(self.t)

        self.p.FetchDate = self.t.FetchDate
        self.p.Team = self.t.Id
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

            img = player.find("img")
            url = img["src"]
            self.p.Headshot = f'{url.split("/")[-1]}'
            if self.online:
                response = self.get(url)
                with open(f"{self.playerrsrcpath}{self.p.Headshot}", "wb") as f:
                    f.write(response.content)
                self.wait()

            self.csv_player.writerow(self.p.row())
            self._database.store(self.p)
        self.logger.info("Done!")


if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.use_proxies = False
    tr.use_random_agents = False
    tr.execute()
