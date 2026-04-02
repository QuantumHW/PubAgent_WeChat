import logging
import sqlite3
import datetime
import os
from .config import get_config

class SQLiteHandler(logging.Handler):
    """
    自定义日志处理器，将日志消息持久化到 SQLite 数据库中。
    """
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """初始化 SQLite 数据库和日志表。"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    level TEXT,
                    logger_name TEXT,
                    message TEXT
                )
            ''')
            conn.commit()

    def emit(self, record):
        """将单条日志记录写入数据库。"""
        log_entry = self.format(record)
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (timestamp, level, logger_name, message)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, record.levelname, record.name, record.getMessage()))
            conn.commit()

def setup_logger():
    """
    配置并返回系统日志记录器。
    """
    config = get_config()
    log_config = config.logging
    
    logger = logging.getLogger("PubAgent-WeChat")
    logger.setLevel(getattr(logging, log_config.level.upper(), logging.INFO))
    
    # 格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # SQLite 处理器（如果启用）
    if log_config.persist_to_db:
        sqlite_handler = SQLiteHandler(log_config.db_path)
        sqlite_handler.setFormatter(formatter)
        logger.addHandler(sqlite_handler)
    
    return logger

# 初始化日志记录器实例
logger = setup_logger()
