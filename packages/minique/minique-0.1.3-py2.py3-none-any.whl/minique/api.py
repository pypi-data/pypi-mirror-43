import json
import time

from minique.enums import JobStatus
from minique.excs import DuplicateJob
from minique.models.job import Job
from minique.models.queue import Queue
from minique.utils import get_random_pronounceable_string


def enqueue(redis, queue_name, callable, kwargs=None, job_id=None, job_ttl=0, result_ttl=86400 * 7):
    if not isinstance(callable, str):
        callable = '{module}.{qualname}'.format(
            module=callable.__module__,
            qualname=callable.__qualname__,
        )

    if not job_id:
        job_id = get_random_pronounceable_string()
    job = Job(redis, job_id)
    if job.exists:
        raise DuplicateJob('duplicate job: {id}'.format(id=job_id))
    payload = {
        'queue': queue_name,
        'callable': str(callable),
        'kwargs': json.dumps(kwargs or {}),
        'status': JobStatus.NONE.value,
        'ctime': time.time(),
        'job_ttl': int(job_ttl),
        'result_ttl': int(result_ttl),
    }
    queue = Queue(redis, name=queue_name)
    with redis.pipeline() as p:
        p.hmset(job.redis_key, payload)
        if payload['job_ttl'] > 0:
            p.expire(job.redis_key, payload['job_ttl'])
        p.rpush(queue.redis_key, job.id)
        p.execute()
    job.ensure_exists()
    return job


def get_job(redis, job_id):
    job = Job(redis, job_id)
    job.ensure_exists()
    return job


def cancel_job(redis, job_id):
    """
    Cancel the job with the given job ID.

    If a worker is already busy with the job, it may not immediately quit,
    and as such, the job is not set to cancelled state.

    :type redis: redis.StrictRedis
    :param job_id: Job ID.
    :raises minique.excs.NoSuchJob: if the job does not exist.
    """
    job = get_job(redis, job_id)
    if not (job.has_finished or job.has_started):
        # Cancel the job and remove it from the queue it may be in.
        redis.hset(job.redis_key, 'status', JobStatus.CANCELLED.value)
        redis.lrem(job.get_queue().redis_key, 0, job.id)
        return True
    return False
