import subprocess
from multiprocessing import Pool
from pathlib import Path

from juniorguru.lib.log import get_log
from juniorguru.lib import timer
from juniorguru.lib.club import discord_task, count_downvotes, count_upvotes, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.scrapers.settings import IMAGES_STORE


log = get_log('jobs')


JOBS_CHANNEL = 834443926655598592
JOBS_VOTING_CHANNEL = 841680291675242546


@timer.notify
def main():
    # If the creation of the directory is left to the spiders, they can end
    # up colliding in making sure it gets created
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    with db:
        db.drop_tables([Job, JobError, JobDropped, SpiderMetric])
        db.create_tables([Job, JobError, JobDropped, SpiderMetric])

    spider_names = [
        'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'wwr',
        'dobrysef',
    ]
    Pool().map(run_spider, spider_names)

    manage_jobs_channel()
    manage_jobs_voting_channel()  # experimenting with Mila and ML


@discord_task
async def manage_jobs_channel(client):
    channel = await client.fetch_channel(JOBS_CHANNEL)

    jobs = list(Job.listing())
    seen_links = set()

    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            if job.link.rstrip('/') in message.content:
                log.info(f'Job {job.link} exists')
                seen_links.add(job.link)
                if message.reactions:
                    job.upvotes = count_upvotes(message.reactions)
                    job.downvotes = count_downvotes(message.reactions)
                    with db:
                        job.save()
                    log.info(f'Saved {job.link} reactions')

    if DISCORD_MUTATIONS_ENABLED:
        new_jobs = [job for job in jobs if job.link not in seen_links]
        log.info(f'Posting {len(new_jobs)} new jobs')
        for job in new_jobs:
            await channel.send(f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}')


@discord_task
async def manage_jobs_voting_channel(client):
    channel = await client.fetch_channel(JOBS_VOTING_CHANNEL)
    seen_links = set()

    log.info('Processing voting for jobs')
    jobs = list(Job.select().where(Job.magic_is_junior == False))  # TODO PoC, move this to models or revamp models altogether?
    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            link = job.link
            if link.rstrip('/') in message.content:
                log.info(f'Job {link} exists')
                seen_links.add(link)
                if message.reactions:
                    job.upvotes += count_upvotes(message.reactions)
                    job.downvotes += count_downvotes(message.reactions)
                    with db:
                        job.save()
                    log.info(f'Saved {link} reactions')

    log.info('Processing voting for dropped jobs')
    jobs_dropped = list(JobDropped.select().where(JobDropped.magic_is_junior == True))  # TODO PoC, move this to models or revamp models altogether?
    async for message in channel.history(limit=None, after=None):
        for job_dropped in jobs_dropped:
            link = job_dropped.item['link']
            if link.rstrip('/') in message.content:
                log.info(f'Job {link} exists')
                seen_links.add(link)
                if message.reactions:
                    job_dropped.upvotes += count_upvotes(message.reactions)
                    job_dropped.downvotes += count_downvotes(message.reactions)
                    with db:
                        job_dropped.save()
                    log.info(f'Saved {link} reactions')

    if DISCORD_MUTATIONS_ENABLED:
        new_jobs = [job for job in jobs if job.link not in seen_links]
        log.info(f'Posting {len(new_jobs)} new jobs')
        for job in new_jobs:
            await channel.send(f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}')

        new_jobs_dropped = [job_dropped for job_dropped in jobs_dropped if job_dropped.item['link'] not in seen_links]
        log.info(f'Posting {len(new_jobs_dropped)} new dropped jobs')
        for job_dropped in new_jobs_dropped:
            await channel.send(f"**{job_dropped.item['title']}**\n{job_dropped.item['company_name']} – {job_dropped.item['locations_raw']}\n{job_dropped.item['link']}")


def run_spider(spider_name):
    proc = subprocess.Popen(['scrapy', 'crawl', spider_name], text=True, bufsize=1,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in proc.stdout:
            print(f'[jobs/{spider_name}] {line}', end='')
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()


if __name__ == '__main__':
    main()
