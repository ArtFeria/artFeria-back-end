def test_post_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Geraldo',
            'email': 'geraldo@legal.com',
            'password': 'senha123',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'Geraldo',
        'email': 'geraldo@legal.com',
        'id': 1,
    }


def test_post_user_already_created(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'username already registered'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'buddie',
            'email': 'buddie@exemplo.com',
            'password': 'nova senha 321',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'buddie',
        'email': 'buddie@exemplo.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'user deleted'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}
