import logging

from podder_task_base.log.log_setting import LogSetting


class SqlalchemyLoggerSetting():
    def __init__(self):
        setting = LogSetting().load()
        format = setting["sql_log_format"]
        level = setting["sql_log_level"]

        logging.basicConfig()

        sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
        sqlalchemy_logger.setLevel(level)

        if sqlalchemy_logger.hasHandlers() is False:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            handler.setFormatter(
                logging.Formatter(format)
            )
            sqlalchemy_logger.addHandler(handler)
