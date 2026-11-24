from models.model import Summary
from models.conn import db
from tests.conftest import login, register


def test_api_requires_login(client):
    response = client.get('/api/summaries')
    assert response.status_code == 401


def test_api_create_and_list_summaries(client, app, monkeypatch):
    register(client)
    login(client)
    monkeypatch.setattr('blueprints.api.summarize_text', lambda text, model_name: 'Riassunto via API')

    response = client.post('/api/summaries', json={
        'title': 'Titolo API',
        'text': 'Testo da riassumere.'
    })
    assert response.status_code == 201
    assert response.json['summary_text'] == 'Riassunto via API'

    response = client.get('/api/summaries')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'Titolo API'

    with app.app_context():
        assert Summary.query.count() == 1


def test_api_validates_input(client):
    register(client)
    login(client)
    response = client.post('/api/summaries', json={'title': '', 'text': ''})
    assert response.status_code == 400
