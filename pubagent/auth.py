import requests
import time
import os
import json
from .config import get_config
from .logger import logger

class AuthService:
    """
    用于管理微信公众号访问令牌（Access Token）的服务。
    包含缓存和自动刷新机制。
    """
    def __init__(self):
        self.config = get_config().wechat
        self.cache_file = "token_cache.json"

    def _load_cache(self) -> dict:
        """从文件中加载缓存的令牌。"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self, token: str, expires_at: float):
        """将令牌和过期时间保存到文件中。"""
        with open(self.cache_file, 'w') as f:
            json.dump({"access_token": token, "expires_at": expires_at}, f)

    def get_access_token(self) -> str:
        """
        获取有效的访问令牌。
        首先检查缓存；如果已过期或缺失，则获取新的令牌。
        """
        cache = self._load_cache()
        current_time = time.time()

        if cache and cache.get("expires_at", 0) > current_time + 60:
            logger.info("Using cached WeChat access token.")
            return cache["access_token"]

        logger.info("Fetching new WeChat access token...")
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.config.app_id,
            "secret": self.config.app_secret
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "access_token" in data:
                token = data["access_token"]
                expires_in = data["expires_in"]
                expires_at = current_time + expires_in
                self._save_cache(token, expires_at)
                logger.info("Successfully fetched and cached new token.")
                return token
            else:
                error_msg = f"Failed to fetch WeChat access token: {data.get('errmsg', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except requests.RequestException as e:
            logger.error(f"HTTP error during token retrieval: {e}")
            raise

auth_service = AuthService()
