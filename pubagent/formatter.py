import markdown
from .logger import logger

class Formatter:
    """
    为微信公众号格式化内容。
    将 Markdown 转换为 HTML 并处理图像嵌入。
    """
    def markdown_to_html(self, md_content: str) -> str:
        """
        将 Markdown 文本转换为 HTML。
        使用基础扩展以确保与微信有限的 HTML 支持兼容。
        
        参数:
            md_content (str): 要转换的 Markdown 字符串。
            
        返回:
            str: 转换后的 HTML 字符串。
        """
        try:
            # We use standard markdown conversion. 
            # WeChat's editor is quite restrictive, so we keep it simple.
            html = markdown.markdown(md_content, extensions=['extra', 'nl2br', 'sane_lists'])
            logger.info("Successfully converted Markdown to HTML.")
            return html
        except Exception as e:
            logger.error(f"Error converting Markdown to HTML: {e}")
            raise

    def insert_image(self, html: str, image_url: str) -> str:
        """
        在 HTML 内容的开头插入图像 URL。
        
        参数:
            html (str): 现有的 HTML 内容。
            image_url (str): 要插入的图像 URL。
            
        返回:
            str: 修改后的 HTML 内容。
        """
        img_tag = f'<img src="{image_url}" style="width: 100%; height: auto;" />'
        return f"{img_tag}\n{html}"

formatter = Formatter()
