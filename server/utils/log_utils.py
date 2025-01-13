import logging

class LogUtils:
    @staticmethod
    def get_logger():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - [%(levelname)s] - [%(threadName)s]:  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                logging.FileHandler("app.log"),
                                logging.StreamHandler()
                            ])
        return logging.getLogger(__name__)
