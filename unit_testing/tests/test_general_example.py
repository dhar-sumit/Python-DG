# Here we have completed the whole unit-testing methods.
# Also used patch to mock the result of load_employee_rec_from_database instead of waiting 10s.

from src.general_example import GeneralExample
from unittest.mock import patch

general_example_instance = GeneralExample()

def test_flatten_dictionary():
    content = {
        'key1': [3, 2, 1,7], 
        'key2': [42, 87, 55, 10], 
        'key3': [0, 22, 21, 89]
    }
    expected = [0, 1, 2, 3, 7, 10, 21, 22, 42, 55, 87, 89]

    actual = general_example_instance.flatten_dictionary(content)
    
    assert expected == actual

def test_load_employee_rec_from_database():
    expected = ['emp001', 'Sam', '100000']
    actual = general_example_instance.load_employee_rec_from_database()

    assert expected == actual

@patch.object(GeneralExample, 'load_employee_rec_from_database')
def test_fetch_emp_details(mocked_load):
    
    db_record =  ['emp001', 'Sam', '100000']

    mocked_load.return_value = db_record

    expected = {
        'empId': db_record[0],
        'empName': db_record[1],
        'empSalary': db_record[2]
    }

    actual = general_example_instance.fetch_emp_details()
    assert expected == actual
