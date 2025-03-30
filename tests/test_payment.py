import requests

def test_payment_success(mocker):
    # Mock the external API URL
    mocker.patch('app.config.PAYMENT_API_URL', 'http://localhost:5001/api/payment')

    # Simulate a payment request
    response = requests.post('http://localhost:5001/api/payment', json={
        'cardNumber': '4111111111111111',
        'amount': 100.0
    })

    # Assert the response
    assert response.status_code == 200
    assert response.json()['status'] == 'success'

def test_payment_failure(mocker):
    # Mock the external API URL
    mocker.patch('app.config.PAYMENT_API_URL', 'http://localhost:5001/api/payment')

    # Simulate a payment request with an invalid card number
    response = requests.post('http://localhost:5001/api/payment', json={
        'cardNumber': '1234567890123456',
        'amount': 100.0
    })

    # Assert the response
    assert response.status_code == 400
    assert response.json()['status'] == 'failure'
