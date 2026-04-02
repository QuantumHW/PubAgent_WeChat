import json
import os
import hashlib
from .logger import logger

class SimpleCache:
    """
    一个简单的基于文件的缓存，用于存储生成的文章数据。
    有助于在开发过程中避免针对相同选题或阶段重复调用 LLM。
    """
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_hash(self, key: str) -> str:
        """返回给定键的 MD5 哈希值。"""
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def get(self, key: str) -> str:
        """根据键从缓存中检索值。"""
        file_path = os.path.join(self.cache_dir, self._get_hash(key))
        if os.path.exists(file_path):
            logger.info(f"缓存命中，键: {key[:50]}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def set(self, key: str, value: str):
        """根据键将值存储到缓存中。"""
        file_path = os.path.join(self.cache_dir, self._get_hash(key))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(value)
        logger.info(f"已缓存值，键: {key[:50]}...")

# SimpleCache 实例
cache = SimpleCache()
