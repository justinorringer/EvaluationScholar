import pytest

def test_update_period(client):
    resp = client.get('/task_manager/update_period')
    assert resp.status_code == 200
    assert resp.json['value'] != None
    assert int(resp.json['value']) > 0

    resp = client.put('/task_manager/update_period', json={'value': '1'})
    assert resp.status_code == 200

    resp = client.get('/task_manager/update_period')
    assert resp.status_code == 200
    assert int(resp.json['value']) == 1

    resp = client.put('/task_manager/update_period', json={'value': '0'})
    assert resp.status_code == 400

    resp = client.put('/task_manager/update_period', json={'value': 'na8'})
    assert resp.status_code == 400