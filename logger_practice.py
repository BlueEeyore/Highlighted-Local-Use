import logging
import praclib
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')
    praclib.do_something()
    logger.debug('Finished')

if __name__ == '__main__':
    main()
