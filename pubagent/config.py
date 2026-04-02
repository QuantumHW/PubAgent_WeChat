import yaml
import os
from pydantic import BaseModel, Field
from typing import Dict, Optional

class WeChatConfig(BaseModel):
    app_id: str
    app_secret: str

class LLMModelConfig(BaseModel):
    api_key: str
    base_url: str
    model_name: str

class LLMTaskConfig(BaseModel):
    model_name: str
    prompt: Optional[str] = None # 使 prompt 变为可选

class LLMConfig(BaseModel):
    prompt_dir: str = "prompts"   # 新增：提示词根目录
    active_style: str = "default" # 新增：当前激活的写作风格
    default: LLMModelConfig
    tasks: Dict[str, LLMTaskConfig]

class SchedulerConfig(BaseModel):
    enabled: bool
    interval_hours: int

class LoggingConfig(BaseModel):
    level: str = "INFO"
    persist_to_db: bool = False
    db_path: str = "logs.db"

class Config(BaseModel):
    wechat: WeChatConfig
    llm: LLMConfig
    scheduler: SchedulerConfig
    logging: LoggingConfig

_config: Optional[Config] = None

def load_config(file_path: str = "config.yaml") -> Config:
    """
    从 YAML 文件加载配置。
    
    参数:
        file_path (str): config.yaml 文件的路径。
        
    返回:
        Config: 经验证的配置对象。
    """
    global _config
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"未找到配置文件 {file_path}。")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        _config = Config(**data)
        return _config

def get_config() -> Config:
    """
    获取已加载的配置对象。
    
    返回:
        Config: 配置对象。
    """
    if _config is None:
        return load_config()
    return _config
