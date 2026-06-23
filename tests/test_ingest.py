import pytest
from ingest import IngestEngine, IngestStatus

def test_ingest_csv(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'test.csv'
    with open(file_path, 'w') as file:
        file.write('1,2\n3,4')
    job_id = engine.ingest(str(file_path))
    engine.process_job(job_id)
    assert engine.get_job_status(job_id)['status'] == IngestStatus.COMPLETED.name

def test_ingest_json(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'test.json'
    with open(file_path, 'w') as file:
        file.write('[{"timestamp": 1, "value": 2}, {"timestamp": 3, "value": 4}]')
    job_id = engine.ingest(str(file_path))
    engine.process_job(job_id)
    assert engine.get_job_status(job_id)['status'] == IngestStatus.COMPLETED.name

def test_ingest_invalid_csv(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'invalid.csv'
    with open(file_path, 'w') as file:
        file.write('1,2,3\n4,5')
    job_id = engine.ingest(str(file_path))
    engine.process_job(job_id)
    assert engine.get_job_status(job_id)['status'] == IngestStatus.FAILED.name
    assert len(engine.get_job_status(job_id)['errors']) > 0

def test_ingest_invalid_json(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'invalid.json'
    with open(file_path, 'w') as file:
        file.write('[{"timestamp": 1, "value": 2}, {"timestamp": 3}]')
    job_id = engine.ingest(str(file_path))
    engine.process_job(job_id)
    assert engine.get_job_status(job_id)['status'] == IngestStatus.FAILED.name
    assert len(engine.get_job_status(job_id)['errors']) > 0

def test_get_job_status_not_found():
    engine = IngestEngine()
    assert engine.get_job_status('not_found')['status'] == 'NOT_FOUND'

def test_ingest_performance(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'large.csv'
    with open(file_path, 'w') as file:
        for i in range(10000):
            file.write(f'{i},{i+1}\n')
    job_id = engine.ingest(str(file_path))
    import time
    start_time = time.time()
    engine.process_job(job_id)
    end_time = time.time()
    assert end_time - start_time < 30

def test_ingest_api_performance(tmp_path):
    engine = IngestEngine()
    file_path = tmp_path / 'test.csv'
    with open(file_path, 'w') as file:
        file.write('1,2\n3,4')
    import time
    start_time = time.time()
    job_id = engine.ingest(str(file_path))
    end_time = time.time()
    assert end_time - start_time < 0.2
