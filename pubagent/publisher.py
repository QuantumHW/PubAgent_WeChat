import requests
from .auth import auth_service
from .logger import logger

class WeChatPublisher:
    """
    处理微信公众号草稿箱的文章发布。
    """
    def __init__(self):
        pass

    def publish_draft(self, title: str, content: str, thumb_media_id: str, digest: str = "", author: str = "") -> str:
        """
        在微信平台上创建一篇新的草稿文章。
        
        参数:
            title (str): 文章标题。
            content (str): 文章内容 (HTML 格式)。
            thumb_media_id (str): 封面图片的 media_id。
            digest (str): 文章摘要 (可选)。
            author (str): 作者名称 (可选)。
            
        返回:
            str: 创建成功的草稿 media_id。
        """
        token = auth_service.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        payload = {
            "articles": [
                {
                    "title": title,
                    "author": author,
                    "digest": digest,
                    "content": content,
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 0,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        logger.info(f"正在向微信提交草稿: {title}")
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "media_id" in data:
                logger.info(f"成功创建草稿。草稿 Media ID: {data['media_id']}")
                return data["media_id"]
            else:
                error_msg = f"创建草稿失败: {data.get('errmsg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except requests.RequestException as e:
            logger.error(f"创建草稿时发生 HTTP 错误: {e}")
            raise

publisher = WeChatPublisher()
