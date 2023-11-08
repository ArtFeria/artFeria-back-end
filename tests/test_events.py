def test_create_event(client, user, token):
    response = client.post(
        '/events/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'pop show',
            'age': 14,
            'description': 'best pop show ever',
            'location': {
                'cep': 0,
                'number': 0,
                'street': 'string',
                'complement': 'string',
            },
            'organizer': user.id,
        },
    )
    assert response.status_code == 201