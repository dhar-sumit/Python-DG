# Here er have changed the import to mock_aws from moto as we have installed the latest version of moto.
# Also we have completed all the methods by defining their functionalities.

import boto3
import pytest
from moto import mock_aws
from src.boto3_example import DynamodBExample
from botocore.exceptions import ClientError


@mock_aws
def test_create_dynamo_table():
    '''
        Implement the test logic here for testing create_dynamo_table method
    '''

    db = DynamodBExample()
    db.create_movies_table()

    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    tables = dynamodb.list_tables()['TableNames']

    assert 'Movies' in tables


@mock_aws
def test_add_dynamo_record_table():
    '''
        Implement the test logic here for testing add_dynamo_record_table method
    '''

    db = DynamodBExample()
    db.create_movies_table()

    item = {
        'year': 2025,
        'title': 'My Test Movie',
        'info': 'UnitTest Insert'
    }

    db.add_dynamo_record('Movies', item)


    # Fetching the records and cross checking
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    fetch_item = {k: item[k] for k in list(item)[:2]}
    table = dynamodb.Table('Movies')

    response = table.get_item(Key=fetch_item)

    assert 'Item' in response
    assert response['Item']['title'] == item['title']
    assert response['Item']['info'] == item['info']

@mock_aws
def test_add_dynamo_record_table_failure():
    '''
        Implement the test logic here test_add_dynamo_record_table method for failures
    '''
    db = DynamodBExample()
    db.create_movies_table()

    bad_item = {
        'year': 2025,
        # 'title': 'My Test Movie',
        'info': 'UnitTest Insert'
    }

    with pytest.raises(ClientError):  # Moto simulates boto3 behavior
        db.add_dynamo_record('Movies', bad_item)
