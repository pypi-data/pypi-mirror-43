import click
import logging
import time
from tabulate import tabulate

from memorious import settings
from memorious.core import manager, init_memorious
from memorious.model import Queue
from memorious.task_runner import TaskRunner

log = logging.getLogger(__name__)


@click.group()
@click.option('--debug/--no-debug', default=False,
              envvar='MEMORIOUS_DEBUG')
@click.option('--cache/--no-cache', default=True,
              envvar='MEMORIOUS_HTTP_CACHE')
@click.option('--incremental/--non-incremental', default=True,
              envvar='MEMORIOUS_INCREMENTAL')
def cli(debug, cache, incremental):
    """Crawler framework for documents and structured scrapers."""
    settings.HTTP_CACHE = cache
    settings.INCREMENTAL = incremental
    settings.DEBUG = debug
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    init_memorious()


def get_crawler(name):
    crawler = manager.get(name)
    if crawler is None:
        msg = 'Crawler [%s] not found.' % name
        raise click.BadParameter(msg, param=crawler)
    return crawler


@cli.command()
@click.argument('crawler')
def run(crawler):
    """Run a specified crawler."""
    crawler = get_crawler(crawler)
    crawler.run()
    if settings.DEBUG:
        TaskRunner.run_sync()


@cli.command()
@click.argument('crawler')
def cancel(crawler):
    """Abort execution of a specified crawler."""
    crawler = get_crawler(crawler)
    crawler.cancel()


@cli.command()
@click.argument('crawler')
def flush(crawler):
    """Delete all data generated by a crawler."""
    crawler = get_crawler(crawler)
    crawler.flush()


@cli.command()
def process():
    """Start the queue and process tasks as they come. Blocks while waiting"""
    TaskRunner.run()


@cli.command('list')
def index():
    """List the available crawlers."""
    crawler_list = []
    for crawler in manager:
        is_due = 'yes' if crawler.check_due() else 'no'
        if crawler.disabled:
            is_due = 'off'
        crawler_list.append([crawler.name,
                             crawler.description,
                             crawler.schedule,
                             is_due,
                             Queue.size(crawler)])
    headers = ['Name', 'Description', 'Schedule', 'Due', 'Pending']
    print(tabulate(crawler_list, headers=headers))


@cli.command()
@click.option('--wait/--no-wait', default=False)
def scheduled(wait=False):
    """Run crawlers that are due."""
    manager.run_scheduled()
    while wait:
        # Loop and try to run scheduled crawlers at short intervals
        manager.run_scheduled()
        time.sleep(settings.SCHEDULER_INTERVAL)


@cli.command()
def killthekitten():
    """Completely kill redis contents."""
    from memorious.core import connect_redis
    conn = connect_redis()
    conn.flushall()


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
