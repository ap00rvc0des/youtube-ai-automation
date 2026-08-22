#!/usr/bin/env python3
"""
Scheduled task management
"""

import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Manages scheduled video generation and uploads"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Task scheduler initialized")
    
    def schedule_video_generation(
        self,
        task_id: str,
        topic: str,
        niche: str,
        scheduled_time: datetime = None,
        interval_days: int = None
    ) -> bool:
        """
        Schedule video generation
        
        Args:
            task_id: Unique task identifier
            topic: Video topic
            niche: Video niche
            scheduled_time: When to start (None = immediately)
            interval_days: Repeat every N days (None = one-time)
        
        Returns:
            True if scheduled successfully
        """
        try:
            if interval_days:
                self.scheduler.add_job(
                    self._generate_video_job,
                    'interval',
                    days=interval_days,
                    args=[task_id, topic, niche],
                    id=task_id
                )
                logger.info(f"Recurring task scheduled: {task_id}")
            else:
                run_time = scheduled_time or datetime.now()
                self.scheduler.add_job(
                    self._generate_video_job,
                    'date',
                    run_date=run_time,
                    args=[task_id, topic, niche],
                    id=task_id
                )
                logger.info(f"Task scheduled for {run_time}: {task_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
            return False
    
    def _generate_video_job(self, task_id: str, topic: str, niche: str):
        """Job function for video generation"""
        logger.info(f"Starting scheduled video generation: {task_id}")
        # Implementation will call the video generation pipeline
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task"""
        try:
            self.scheduler.remove_job(task_id)
            logger.info(f"Task cancelled: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling task: {e}")
            return False
    
    def get_scheduled_tasks(self) -> list:
        """Get all scheduled tasks"""
        return self.scheduler.get_jobs()
