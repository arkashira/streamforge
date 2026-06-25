import pytest
import sys
from streamforge import load_yaml_config, create_stream, write_credentials_to_secrets_store, StreamConfig

def test_load_yaml_config(tmp_path):
    config_file = tmp_path / 'config.yaml'
    with open(config_file, 'w') as file:
        file.write('''name: test-stream
description: Test stream description
credentials:
  username: test-user
  password: test-password
''')
    config = load_yaml_config(str(config_file))
    assert config.name == 'test-stream'
    assert config.description == 'Test stream description'
    assert config.credentials == {'username': 'test-user', 'password': 'test-password'}

def test_create_stream():
    config = StreamConfig(name='test-stream', description='Test stream description', credentials={'username': 'test-user', 'password': 'test-password'})
    stream_id = create_stream(config)
    assert stream_id == 'stream-test-stream'

def test_write_credentials_to_secrets_store(capsys):
    config = StreamConfig(name='test-stream', description='Test stream description', credentials={'username': 'test-user', 'password': 'test-password'})
    stream_id = 'stream-test-stream'
    write_credentials_to_secrets_store(config, stream_id)
    captured = capsys.readouterr()
    assert captured.out == f"Writing credentials for stream {stream_id} to secrets store\n"

def test_main(capsys, tmp_path):
    config_file = tmp_path / 'config.yaml'
    with open(config_file, 'w') as file:
        file.write('''name: test-stream
description: Test stream description
credentials:
  username: test-user
  password: test-password
''')
    sys.argv = ['streamforge.py', '--config', str(config_file)]
    from streamforge import main
    main()
    captured = capsys.readouterr()
    assert captured.out == f"Writing credentials for stream stream-test-stream to secrets store\nStream created successfully: stream-test-stream\n"
