from models.model import Summary
from tests.conftest import login, register


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'SmartSummarizer'.encode() in response.data


def test_register_login_logout(client):
    response = register(client)
    assert response.status_code == 302

    response = login(client)
    assert response.status_code == 302

    response = client.get('/archive')
    assert response.status_code == 200

    response = client.post('/logout')
    assert response.status_code == 302
    assert client.get('/archive').status_code == 302


def test_summary_is_saved_and_shown_in_archive(client, app, monkeypatch):
    register(client)
    login(client)

    monkeypatch.setattr(
        'blueprints.frontend.summarize_text',
        lambda text, model_name: 'Testo riassunto'
    )

    response = client.post('/summarize', data={
        'title': 'Test di esempio',
        'original_text': 'Prima frase. Seconda frase. Terza frase.'
    })

    assert response.status_code == 302

    with app.app_context():
        summary = Summary.query.one()
        summary_id = summary.id

        assert summary.original_text == 'Prima frase. Seconda frase. Terza frase.'
        assert summary.summary_text == 'Testo riassunto'

    response = client.get('/archive')
    assert response.status_code == 200
    assert 'Test di esempio'.encode() in response.data

    response = client.get(f'/archive/{summary_id}')
    assert response.status_code == 200
    assert 'Testo riassunto'.encode() in response.data


def test_user_cannot_open_another_users_summary(client, app, monkeypatch):
    register(client, email='first@example.com')
    login(client, email='first@example.com')

    monkeypatch.setattr(
        'blueprints.frontend.summarize_text',
        lambda text, model_name: 'Riassunto'
    )

    client.post('/summarize', data={
        'title': 'Privato',
        'original_text': 'Un testo.'
    })

    with app.app_context():
        summary_id = Summary.query.one().id

    client.post('/logout')

    register(client, email='second@example.com')
    login(client, email='second@example.com')

    response = client.get(f'/archive/{summary_id}')
    assert response.status_code == 404