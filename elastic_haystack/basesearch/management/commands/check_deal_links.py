# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging, redis, time, requests
import os
import sys
import warnings
from datetime import timedelta
from optparse import make_option

try:
    from django.db import close_old_connections
except ImportError:
    # This can be removed when we drop support for Django 1.7 and earlier:
    from django.db import close_connection as close_old_connections

from django.core.management.base import LabelCommand
from django.db import reset_queries

from haystack import connections as haystack_connections
from haystack.query import SearchQuerySet
from haystack.utils.app_loading import haystack_get_models, haystack_load_apps

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

try:
    from django.utils.encoding import smart_bytes
except ImportError:
    from django.utils.encoding import smart_str as smart_bytes

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    now = datetime.now

DEFAULT_BATCH_SIZE = None
DEFAULT_AGE = None
APP = 'app'
MODEL = 'model'

# modify
pool = redis.ConnectionPool(host='127.0.0.1')
r = redis.Redis(connection_pool=pool)
l_404_links = "404_links_list"
l_timeout_links = "timeout_links_list"


def worker(bits):
    # We need to reset the connections, otherwise the different processes
    # will try to share the connection, which causes things to blow up.
    from django.db import connections

    for alias, info in connections.databases.items():
        # We need to also tread lightly with SQLite, because blindly wiping
        # out connections (via ``... = {}``) destroys in-memory DBs.
        if 'sqlite3' not in info['ENGINE']:
            try:
                close_old_connections()
                if isinstance(connections._connections, dict):
                    del (connections._connections[alias])
                else:
                    delattr(connections._connections, alias)
            except KeyError:
                pass

    if bits[0] == 'do_update':
        func, model, start, end, total, using, start_date, end_date, verbosity, commit = bits
    elif bits[0] == 'do_remove':
        func, model, pks_seen, start, upper_bound, using, verbosity, commit = bits
    else:
        return

    unified_index = haystack_connections[using].get_unified_index()
    index = unified_index.get_index(model)
    backend = haystack_connections[using].get_backend()

    if func == 'do_update':
        qs = index.build_queryset(start_date=start_date, end_date=end_date)
        do_update(backend, index, qs, start, end, total, verbosity=verbosity, commit=commit)
    else:
        raise NotImplementedError('Unknown function %s' % func)


def do_update(backend, index, qs, start, end, total, verbosity=1, commit=True):
    # Get a clone of the QuerySet so that the cache doesn't bloat up
    # in memory. Useful when reindexing large amounts of data.
    small_cache_qs = qs.all()
    current_qs = small_cache_qs.filter(id__gte=start, id__lt=end)
    print("indexed id %s ~ id %s ..." % (start, end))
    sqs = SearchQuerySet()

    if verbosity >= 2:
        if hasattr(os, 'getppid') and os.getpid() == os.getppid():
            print("  indexed %s - %d of %d." % (start + 1, end, total))
        else:
            print("  indexed %s - %d of %d (by %s)." % (start + 1, end, total, os.getpid()))

    # FIXME: Get the right backend.
    for q in current_qs:
        try:
            http_code = requests.get(q.link).status_code
            if http_code >= 400 and http_code < 500:
                # current_qs.remove(id=q.link)
                sr = sqs.filter(autolink=q.autolink)
                print(sr[0].id),
                backend.remove(sr[0].id, commit=commit)
                q.delete()
                print("remove !")
                r.lpush(l_404_links, "%s--%s" % (q.id, q.link))
        except requests.exceptions.ConnectionError:
            print("timeout..")
            r.lpush(l_timeout_links, "%s--%s" % (q.id, q.link))
            continue
        except IndexError:
            print("已经删除"),
            backend.update(index, q, commit=commit)
            print("已重建索引")
            continue

    # backend.update(index, current_qs, commit=commit)


    import time
    backend.remove('basesearch.DATA.316014', commit=commit)
    time.sleep(3)
    # Clear out the DB connections queries because it bloats up RAM.
    reset_queries()


class Command(LabelCommand):
    help = "Freshens the index for the given app(s)."
    base_options = (
        make_option('-a', '--age', action='store', dest='age',
                    default=DEFAULT_AGE, type='int',
                    help='Number of hours back to consider objects new.'
                    ),
        make_option('-s', '--start', action='store', dest='start_date',
                    default=None, type='string',
                    help='The start date for indexing within. Can be any dateutil-parsable string, recommended to be YYYY-MM-DDTHH:MM:SS.'
                    ),
        make_option('-e', '--end', action='store', dest='end_date',
                    default=None, type='string',
                    help='The end date for indexing within. Can be any dateutil-parsable string, recommended to be YYYY-MM-DDTHH:MM:SS.'
                    ),
        make_option('-b', '--batch-size', action='store', dest='batchsize',
                    default=None, type='int',
                    help='Number of items to index at once.'
                    ),
        make_option('-r', '--remove', action='store_true', dest='remove',
                    default=False, help='Remove objects from the index that are no longer present in the database.'
                    ),
        make_option("-u", "--using", action="append", dest="using",
                    default=[],
                    help='Update only the named backend (can be used multiple times). '
                         'By default all backends will be updated.'
                    ),
        make_option('-k', '--workers', action='store', dest='workers',
                    default=0, type='int',
                    help='Allows for the use multiple workers to parallelize indexing. Requires multiprocessing.'
                    ),

        make_option('-i', '--startid', action='store', dest='startid',
                    default=0, type='int',
                    help='Set updateindex start pk num in database'
                    ),

        make_option('--nocommit', action='store_false', dest='commit',
                    default=True, help='Will pass commit=False to the backend.'
                    ),
    )
    option_list = LabelCommand.option_list + base_options

    def handle(self, *items, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.batchsize = options.get('batchsize', DEFAULT_BATCH_SIZE)
        self.start_date = None
        self.end_date = None
        self.remove = options.get('remove', False)
        self.workers = int(options.get('workers', 0))
        self.commit = options.get('commit', True)
        self.startid = options.get('startid', 0)

        if sys.version_info < (2, 7):
            warnings.warn('multiprocessing is disabled on Python 2.6 and earlier. '
                          'See https://github.com/toastdriven/django-haystack/issues/1001')
            self.workers = 0

        self.backends = options.get('using')
        if not self.backends:
            self.backends = haystack_connections.connections_info.keys()

        age = options.get('age', DEFAULT_AGE)
        start_date = options.get('start_date')
        end_date = options.get('end_date')

        if age is not None:
            self.start_date = now() - timedelta(hours=int(age))

        if start_date is not None:
            from dateutil.parser import parse as dateutil_parse

            try:
                self.start_date = dateutil_parse(start_date)
            except ValueError:
                pass

        if end_date is not None:
            from dateutil.parser import parse as dateutil_parse

            try:
                self.end_date = dateutil_parse(end_date)
            except ValueError:
                pass

        if not items:
            items = haystack_load_apps()

        return super(Command, self).handle(*items, **options)

    def handle_label(self, label, **options):
        for using in self.backends:
            try:
                self.update_backend(label, using)
            except:
                logging.exception("Error updating %s using %s ", label, using)
                raise

    def update_backend(self, label, using):
        from haystack.exceptions import NotHandled

        backend = haystack_connections[using].get_backend()
        unified_index = haystack_connections[using].get_unified_index()

        if self.workers > 0:
            import multiprocessing

        for model in haystack_get_models(label):
            try:
                index = unified_index.get_index(model)
            except NotHandled:
                if self.verbosity >= 2:
                    print("Skipping '%s' - no index." % model)
                continue

            if self.workers > 0:
                # workers resetting connections leads to references to models / connections getting
                # stale and having their connection disconnected from under them. Resetting before
                # the loop continues and it accesses the ORM makes it better.
                close_old_connections()

            qs = index.build_queryset(using=using, start_date=self.start_date,
                                      end_date=self.end_date)

            # total 为 id 最大那个
            # modify
            max_id = qs.reverse()[0].id
            total = qs.count()
            print("id 最大为 %s" % (max_id))

            if self.verbosity >= 1:
                print(u"Indexing %d %s" % (total, force_text(model._meta.verbose_name_plural)))

            batch_size = self.batchsize or backend.batch_size

            if self.workers > 0:
                ghetto_queue = []

            # modify
            # for start in range(0, total, batch_size):
            #     end = min(start + batch_size, total)

            ### custom start id


            print(self.startid)

            for start in range(self.startid, max_id, batch_size):
                end = min(start + batch_size, max_id)

                if self.workers == 0:
                    do_update(backend, index, qs, start, end, total, verbosity=self.verbosity, commit=self.commit)
                else:
                    ghetto_queue.append(('do_update', model, start, end, total, using, self.start_date, self.end_date,
                                         self.verbosity, self.commit))

            if self.workers > 0:
                pool = multiprocessing.Pool(self.workers)
                pool.map(worker, ghetto_queue)
                pool.close()
                pool.join()

                # if self.remove:
                #     if self.start_date or self.end_date or total <= 0:
                #         # They're using a reduced set, which may not incorporate
                #         # all pks. Rebuild the list with everything.
                #         qs = index.index_queryset().values_list('pk', flat=True)
                #         database_pks = set(smart_bytes(pk) for pk in qs)
                #
                #         total = len(database_pks)
                #     else:
                #         database_pks = set(smart_bytes(pk) for pk in qs.values_list('pk', flat=True))
                #
                #     # Since records may still be in the search index but not the local database
                #     # we'll use that to create batches for processing.
                #     # See https://github.com/django-haystack/django-haystack/issues/1186
                #     index_total = SearchQuerySet(using=backend.connection_alias).models(model).count()
                #
                #     # Retrieve PKs from the index. Note that this cannot be a numeric range query because although
                #     # pks are normally numeric they can be non-numeric UUIDs or other custom values. To reduce
                #     # load on the search engine, we only retrieve the pk field, which will be checked against the
                #     # full list obtained from the database, and the id field, which will be used to delete the
                #     # record should it be found to be stale.
                #     index_pks = SearchQuerySet(using=backend.connection_alias).models(model)
                #
                #
                #
                #     index_pks = index_pks.values_list('pk', 'id')
                #
                #
                #     # We'll collect all of the record IDs which are no longer present in the database and delete
                #     # them after walking the entire index. This uses more memory than the incremental approach but
                #     # avoids needing the pagination logic below to account for both commit modes:
                #     stale_records = set()
                #
                #     for start in range(0, index_total, batch_size):
                #         upper_bound = start + batch_size
                #
                #         # If the database pk is no longer present, queue the index key for removal:
                #         for pk, rec_id in index_pks[start:upper_bound]:
                #             if smart_bytes(pk) not in database_pks:
                #
                #                 stale_records.add(rec_id)
                #
                #
                #     if stale_records:
                #         if self.verbosity >= 1:
                #             print("  removing %d stale records." % len(stale_records))
                #
                #         for rec_id in stale_records:
                #             # Since the PK was not in the database list, we'll delete the record from the search index:
                #             if self.verbosity >= 2:
                #                 print("  removing %s." % rec_id)
                #
                #             backend.remove(rec_id, commit=self.commit)
