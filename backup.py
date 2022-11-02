"""
This script is inspired by the post "Auto-Updating Your Github Profile With Python" by Dylan Roy 
available here https://towardsdatascience.com/auto-updating-your-github-profile-with-python-cde87b638168
"""

from pathlib import Path
import datetime
import pytz
from itertools import chain
import requests
from bs4 import BeautifulSoup

MAIN_WEBSITE = "https://ealizadeh.com"
BLOG_FEED = f"{MAIN_WEBSITE}/blog"
NUM_POST = 7
READ_MORE_BADGE_URL = "https://img.shields.io/badge/-Read%20more%20on%20my%20blog-brightgreen?style=for-the-badge"
READ_MORE_BADGE_HTML = f'<a href="https://ealizadeh.com/blog" target="_blank"><img alt="Personal Blog" src="{READ_MORE_BADGE_URL}" /></a>'


def update_footer():
    timestamp = datetime.datetime.now(pytz.timezone("America/Montreal")).strftime("%c")
    footer = Path("./footer.md").read_text()
    return footer.format(timestamp=timestamp)


def flatten_post_tags(post_tags):
    tags = [list(item.values()) for item in post_tags]  # will generate a nested list
    return set(list(chain(*tags)))


def update_latest_blog_posts_readme(blog_feed, readme_base, join_on):
    post_tags = blog_feed.find_all("a")

    posts = []
    for count, post in enumerate(post_tags):
        post_url = MAIN_WEBSITE + post.get("href")
        post_content = BeautifulSoup(requests.get(post_url).text, "lxml")
        post_title = post_content.find('h1').text
        posts.append(f' - [{post_title}]({post_url})')

        if count == NUM_POST:
            break

    posts_joined = "\n".join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"


if __name__ == "__main__":
    rss_title = "## 📕 Latest Blog Posts"
    readme = Path("../README.md").read_text(encoding="utf8")

    html_content = requests.get(BLOG_FEED).text
    soup = BeautifulSoup(html_content, "lxml")
    main_blog_content = soup.find("main")

    updated_readme = update_latest_blog_posts_readme(main_blog_content, readme, rss_title)
    updated_readme += f"\n<space>\n \t {READ_MORE_BADGE_HTML}\n"

    with open("../README.md", "w+") as f:
        f.write(updated_readme + update_footer())
