import os
import argparse
from pubagent.pipeline import content_pipeline
from pubagent.formatter import formatter
from pubagent.media import media_manager
from pubagent.publisher import publisher
from pubagent.logger import logger
from pubagent.scheduler import Scheduler

def run_pipeline():
    """
    执行完整的文章生成和发布流程。
    """
    try:
        logger.info("--- 正在启动 PubAgent-WeChat 流水线 ---")
        
        # 1. 生成选题
        topic = content_pipeline.generate_topic()
        
        # 2. 生成正文
        content_md = content_pipeline.generate_content(topic)
        
        # 3. 生成摘要
        digest = content_pipeline.generate_digest(content_md)
        
        # 4. 格式化内容 (Markdown -> HTML)
        html = formatter.markdown_to_html(content_md)
        
        # 5. 素材管理 (MVP 版本的占位逻辑)
        # 注意：在生产环境中，你可以使用 LLM 生成图片提示词或获取相关图片。
        # 此处我们查找本地文件。
        image_path = "assets/content_image.jpg"
        thumb_path = "assets/cover_image.jpg"
        
        final_html = html
        thumb_id = ""

        if os.path.exists(image_path):
            image_url = media_manager.upload_image(image_path)
            final_html = formatter.insert_image(html, image_url)
        else:
            logger.warning(f"未在 {image_path} 找到正文图片。跳过图片插入。")

        if os.path.exists(thumb_path):
            thumb_id = media_manager.upload_thumb(thumb_path)
        else:
            logger.error(f"未在 {thumb_path} 找到封面图片 (thumb)。微信草稿需要封面图。")
        
        # 6. 发布到微信
        if thumb_id:
            draft_id = publisher.publish_draft(
                title=topic,
                content=final_html,
                thumb_media_id=thumb_id,
                digest=digest
            )
            logger.info(f"流水线执行成功。草稿 ID: {draft_id}")
        else:
            logger.error("流水线失败：缺失 thumb_media_id。")

    except Exception as e:
        logger.exception(f"流水线执行过程中发生错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="PubAgent-WeChat: 微信公众号自动发布系统")
    parser.add_argument("--once", action="store_true", help="运行一次流水线后退出。")
    parser.add_argument("--schedule", action="store_true", help="启动调度器进行周期性运行。")
    
    args = parser.parse_args()

    # 如果 assets 目录不存在则创建
    if not os.path.exists("assets"):
        os.makedirs("assets")
        logger.info("已创建 'assets' 目录。请将 'content_image.jpg' 和 'cover_image.jpg' 放入其中。")

    if args.once:
        run_pipeline()
    elif args.schedule:
        scheduler = Scheduler(run_pipeline)
        # 如果需要，可以在此处进行初始运行
        # run_pipeline()
        scheduler.start()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
