from juniorguru.fetch.jobs import main as fetch_jobs
from juniorguru.fetch.logos import main as fetch_logos
from juniorguru.fetch.metrics import main as fetch_metrics
from juniorguru.fetch.stories import main as fetch_stories
from juniorguru.fetch.supporters import main as fetch_supporters
from juniorguru.fetch.last_modified import main as fetch_last_modified
from juniorguru.fetch.press_releases import main as fetch_press_releases
from juniorguru.fetch.newsletter_mentions import main as fetch_newsletter_mentions
from juniorguru.fetch.transactions import main as fetch_transactions


def main():
    # order-insensitive
    fetch_stories()
    fetch_supporters()
    fetch_last_modified()
    fetch_press_releases()
    fetch_logos()
    fetch_jobs()
    fetch_transactions()

    # order-sensitive
    fetch_metrics()  # depends on jobs & logos
    fetch_newsletter_mentions()  # depends on jobs


if __name__ == '__main__':
    # main() DEBUG
    fetch_jobs()
