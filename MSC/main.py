import fire

from feelings import ThinkingTheFeelings
from world_news import world_news
from fast_nyt import NYT_articles
from marmelade import ss
from wb import stonks
from darbs import darbs


if __name__ == '__main__':

    fire.Fire(ThinkingTheFeelings)
    fire.Fire(world_news)
    fire.Fire(stonks)
    fire.Fire(NYT_articles)

    fire.Fire(darbs)
    fire.Fire(ss)