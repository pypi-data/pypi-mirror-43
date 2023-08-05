# -*- coding: utf-8 -*-
# (c) 2019 The PatZilla Developers
import pickle
import logging
from tqdm import tqdm
from bunch import bunchify
from pymongo import MongoClient
from mongodb_gridfs_beaker import MongoDBGridFSNamespaceManager
from patzilla.util.logging import boot_logging

boot_logging()

logger = logging.getLogger(__name__)


# Monkey patch 3rd party class to fix runtime error
MongoDBGridFSNamespaceManager.lock_dir = None

url = 'mongodb://localhost:27017/beaker.cache'
client = MongoClient(url)
database = client['beaker']


def pdf_filter(document, metadata):
    namespace = document['namespace']
    if '_pdf' in namespace or 'pdf_' in namespace:
        cache_file, cache_method = namespace.split('|')
        metadata['cache_file'] = cache_file
        metadata['cache_method'] = cache_method
        if cache_method != 'get_ops_image_pdf':
            return True


def iterate_pdf():
    collection = database['cache.files']
    result = collection.find()
    result_count = result.count()
    logger.info('Iterating %s items', result_count)
    for document in tqdm(result, total=result_count):
        metadata = {}
        if pdf_filter(document, metadata):
            #logger.info('Using document %s', document)
            result = bunchify({
                '_id': document['_id'],
                '_namespace': document['namespace'],
                'method': metadata['cache_method'],
                'filename': document['filename'],
                'length': document['length'],
            })
            yield result


def purge_non_pdf(gridfs_item):
    # EP3405364A1, EP2706864A2
    nsm = MongoDBGridFSNamespaceManager(gridfs_item._namespace, url=url)
    payload = nsm[gridfs_item.filename][2]
    if not payload.startswith('%PDF'):
        logger.info('Purging invalid PDF file %s', gridfs_item.filename)
        del nsm[gridfs_item.filename]
        nsm.do_remove()


def get_file(gridfs_item):

    nsm = MongoDBGridFSNamespaceManager(gridfs_item._namespace, url=url)
    payload = nsm[gridfs_item.filename][2]
    print payload
    return

    chunks = database['cache.chunks']

    item = chunks.find_one({"files_id": id})
    #print 'item:', item
    try:

        data = item['data']
        print 'data-1:', data
        data = pickle.loads(item['data'])
        print 'data-2:', data
    except:
        pass


def sensible_pdfs():
    # Iterate all sensible PDFs
    for gridfs_item in iterate_pdf():
        if gridfs_item.length >= 250000:
            print gridfs_item
            get_file(gridfs_item)
            #sys.exit(2)


def cleanup_pdfs():
    # Cleanup broken PDFs
    map(purge_non_pdf, iterate_pdf())


def run():
    cleanup_pdfs()


if __name__ == '__main__':
    run()
