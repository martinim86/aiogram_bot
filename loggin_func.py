import logging
def loggin_to_file():
    logging.basicConfig(filename="Loggin_main",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info("Running Urban Planning")

    logger = logging.getLogger('urbanGUI')


