import os
from .llm import llm_manager
from .config import get_config
from .logger import logger
from .utils import cache

class ContentPipeline:
    """
    编排多阶段内容生成流程。
    阶段包括：选题生成、正文创作以及摘要生成。
    现在支持从外部文件加载提示词。
    """
    def __init__(self):
        self.config = get_config().llm

    def _get_prompt(self, task_name: str) -> str:
        """
        根据任务名称获取提示词。
        优先从 config.yaml 的 tasks 中读取 prompt，
        如果为空，则从 {prompt_dir}/{active_style}/{task_name}.txt 读取。
        """
        task_cfg = self.config.tasks.get(task_name)
        if task_cfg and task_cfg.prompt:
            return task_cfg.prompt

        # 从文件加载
        file_path = os.path.join(self.config.prompt_dir, self.config.active_style, f"{task_name}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"未找到任务 '{task_name}' 的提示词文件: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
            logger.info(f"成功从文件加载 '{task_name}' 的提示词 (风格: {self.config.active_style})")
            return prompt

    def generate_topic(self) -> str:
        """
        生成一系列候选选题并选择最佳的一个。
        
        返回:
            str: 选定的选题。
        """
        prompt = self._get_prompt("topic")
        cached = cache.get(f"topic_{prompt}")
        if cached:
            return cached

        raw_topics = llm_manager.generate("topic", prompt)
        chosen_topic = raw_topics.strip().split("\n")[0].strip()
        
        cache.set(f"topic_{prompt}", chosen_topic)
        logger.info(f"选定选题: {chosen_topic}")
        return chosen_topic

    def generate_content(self, topic: str) -> str:
        """
        根据选定的选题生成完整的文章内容。
        
        参数:
            topic (str): 文章的主题。
            
        返回:
            str: Markdown 格式的文章内容。
        """
        prompt_template = self._get_prompt("content")
        prompt = prompt_template.format(topic=topic)
        
        cached = cache.get(f"content_{prompt}")
        if cached:
            return cached

        content_md = llm_manager.generate("content", prompt)
        cache.set(f"content_{prompt}", content_md)
        logger.info("成功生成 Markdown 格式的文章内容。")
        return content_md

    def generate_digest(self, content_md: str) -> str:
        """
        为文章内容生成简洁的摘要。
        
        参数:
            content_md (str): 文章内容。
            
        返回:
            str: 简短的摘要。
        """
        prompt_template = self._get_prompt("digest")
        prompt = prompt_template.format(content=content_md)
        
        cached = cache.get(f"digest_{prompt}")
        if cached:
            return cached

        digest = llm_manager.generate("digest", prompt)
        cache.set(f"digest_{prompt}", digest.strip())
        logger.info("成功生成文章摘要。")
        return digest.strip()

content_pipeline = ContentPipeline()
