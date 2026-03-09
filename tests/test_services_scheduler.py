from datetime import timedelta

from app.core.config import settings
from app.services.scheduler import create_scheduler


def test_create_scheduler_registers_single_interval_job():
    async def job():
        return None

    scheduler = create_scheduler(job)
    jobs = scheduler.get_jobs()

    assert len(jobs) == 1
    assert jobs[0].func is job
    assert jobs[0].trigger.interval == timedelta(minutes=settings.parse_schedule_minutes)
    assert jobs[0].coalesce is True
    assert jobs[0].max_instances == 1

