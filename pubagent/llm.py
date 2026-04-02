import requests
from typing import List, Dict, Optional
from .config import get_config
from .logger import logger

class LLMManager:
    """
    大语言模型任务调度与执行管理器。
    支持针对特定任务的模型配置，并处理统一的 API 通信。
    """
    def __init__(self):
        self.config = get_config().llm

    def _get_model_for_task(self, task_name: str) -> tuple[str, str, str]:
        """
        确定给定任务的适当模型设置。
        
        返回:
            tuple: (api_key, base_url, model_name)
        """
        task_cfg = self.config.tasks.get(task_name)
        if task_cfg:
            # 为简单起见，我们假设 task_cfg 仅覆盖 model_name。
            # API 密钥和基础 URL 从默认配置中提取。
            return (self.config.default.api_key, 
                    self.config.default.base_url, 
                    task_cfg.model_name)
        
        # 回退到默认配置
        return (self.config.default.api_key, 
                self.config.default.base_url, 
                self.config.default.model_name)

    def generate(self, task_name: str, prompt: str) -> str:
        """
        向指定模型发送单个提示词以生成文本。
        
        参数:
            task_name (str): 要执行的任务名称。
            prompt (str): 模型的文本提示词。
            
        返回:
            str: 生成的内容。
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(task_name, messages)

    def chat(self, task_name: str, messages: List[Dict[str, str]]) -> str:
        """
        向指定模型发送对话线程。
        
        参数:
            task_name (str): 要执行的任务名称。
            messages (List[Dict]): 消息字典列表。
            
        返回:
            str: 模型的响应内容。
        """
        api_key, base_url, model_name = self._get_model_for_task(task_name)
        
        url = f"{base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.7
        }
        
        logger.info(f"正在使用模型 '{model_name}' 执行任务 '{task_name}'。")
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            content = data['choices'][0]['message']['content']
            logger.info(f"成功完成任务 '{task_name}'。")
            return content
        except requests.RequestException as e:
            logger.error(f"任务 '{task_name}' 的 LLM 请求出错: {e}")
            raise
        except (KeyError, IndexError) as e:
            logger.error(f"无法解析任务 '{task_name}' 的 LLM 响应: {e}")
            raise Exception("LLM 响应解析失败。")

llm_manager = LLMManager()
