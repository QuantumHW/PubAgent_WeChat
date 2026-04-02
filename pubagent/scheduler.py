from apscheduler.schedulers.blocking import BlockingScheduler
from .config import get_config
from .logger import logger
from typing import Callable

class Scheduler:
    """
    管理 PubAgent 发布流水线的周期性执行。
    使用 APScheduler 进行基于间隔的调度。
    """
    def __init__(self, job_func: Callable):
        self.config = get_config().scheduler
        self.scheduler = BlockingScheduler()
        self.job_func = job_func

    def start(self):
        """
        根据 config.yaml 中指定的间隔启动调度器。
        """
        if not self.config.enabled:
            logger.info("调度器在配置中已被禁用。")
            return

        interval_hours = self.config.interval_hours
        logger.info(f"正在启动调度器，执行间隔: {interval_hours} 小时。")
        
        # 调度任务
        self.scheduler.add_job(self.job_func, 'interval', hours=interval_hours)
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("调度器已停止。")
