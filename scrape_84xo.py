from pathlib import Path
import datetime
import pytz
from itertools import chain
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    html_content = requests.get("https://84xo.ch").text
    soup = BeautifulSoup(html_content)
    main_headline = soup.select(".MainHighlightedNews_main_highlighted_news_title__uFcsH")[0].text
    main_headline = "\n- " + datetime.datetime.now().strftime("%H:%M %d.%m.%y") + " " + main_headline
    readme = Path("README.md").read_text(encoding="utf8")
    readme_title = "# Latest 84xo Headlines"
    new_readme = readme[:readme.find(readme_title)] + f"{main_headline}\n\n"
    with open("README.md", "w+") as f:
        f.write(new_readme)
