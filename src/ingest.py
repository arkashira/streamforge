import json
import csv
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

class IngestStatus(Enum):
    QUEUED = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

@dataclass
class IngestJob:
    id: str
    status: IngestStatus
    file_path: str
    errors: List[Dict[str, str]]

class IngestEngine:
    def __init__(self):
        self.jobs = {}

    def ingest(self, file_path: str) -> str:
        job_id = str(len(self.jobs))
        self.jobs[job_id] = IngestJob(job_id, IngestStatus.QUEUED, file_path, [])
        return job_id

    def process_job(self, job_id: str):
        job = self.jobs.get(job_id)
        if job:
            job.status = IngestStatus.PROCESSING
            try:
                with open(job.file_path, 'r') as file:
                    if job.file_path.endswith('.csv'):
                        reader = csv.reader(file)
                        for i, row in enumerate(reader):
                            if len(row) != 2:
                                job.errors.append({'line': str(i+1), 'error': 'Invalid row'})
                    elif job.file_path.endswith('.json'):
                        data = json.load(file)
                        for i, row in enumerate(data):
                            if not isinstance(row, dict) or 'timestamp' not in row or 'value' not in row:
                                job.errors.append({'line': str(i+1), 'error': 'Invalid row'})
                if not job.errors:
                    job.status = IngestStatus.COMPLETED
                else:
                    job.status = IngestStatus.FAILED
            except Exception as e:
                job.status = IngestStatus.FAILED
                job.errors.append({'line': '0', 'error': str(e)})

    def get_job_status(self, job_id: str) -> Dict[str, str]:
        job = self.jobs.get(job_id)
        if job:
            return {'status': job.status.name, 'errors': job.errors}
        return {'status': 'NOT_FOUND', 'errors': []}
