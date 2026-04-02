import requests
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from .auth import auth_service
from .logger import logger

class MediaManager:
    """
    微信公众号素材资源管理器。
    处理文章内容图片的上传以及封面图（thumb）media_id 的获取。
    """
    def __init__(self):
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def upload_image(self, file_path: str) -> str:
        """
        将本地图片上传到微信服务器，以便在文章内容中使用。
        
        参数:
            file_path (str): 磁盘上的图片文件路径。
            
        返回:
            str: 已上传图片的公共 URL。
        """
        token = auth_service.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"未找到图片文件 {file_path}。")

        logger.info(f"正在上传内容图片: {file_path}")
        with open(file_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            
            if "url" in data:
                logger.info("成功上传内容图片。")
                return data["url"]
            else:
                error_msg = f"上传图片失败: {data.get('errmsg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def upload_thumb(self, file_path: str) -> str:
        """
        将图片上传为“封面图”（thumb）并返回其 media_id。
        
        参数:
            file_path (str): 封面图片文件的路径。
            
        返回:
            str: 已上传图片的 thumb_media_id。
        """
        token = auth_service.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"未找到封面文件 {file_path}。")

        logger.info(f"正在上传封面图片 (thumb): {file_path}")
        with open(file_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            
            if "media_id" in data:
                logger.info(f"成功上传封面。Media ID: {data['media_id']}")
                return data["media_id"]
            else:
                error_msg = f"上传封面失败: {data.get('errmsg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)

media_manager = MediaManager()
