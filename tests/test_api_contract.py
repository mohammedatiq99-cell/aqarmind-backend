from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mortgage_endpoint_without_cloud_credentials():
    response = client.post(
        '/mortgage',
        json={
            'property_price_aed': 1_500_000,
            'down_payment_percent': 20,
            'annual_interest_rate': 4.5,
            'tenure_years': 25,
        },
    )
    assert response.status_code == 200
    assert response.json()['loan_amount_aed'] == 1_200_000
    assert response.json()['estimated_monthly_payment_aed'] > 0


def test_mortgage_rejects_invalid_input():
    response = client.post('/mortgage', json={'property_price_aed': -1000})
    assert response.status_code == 422


def test_lead_requires_consent_without_touching_database():
    response = client.post(
        '/leads',
        json={
            'name': 'Sample Person',
            'email': 'test@example.com',
            'phone': '+10000000000',
            'consent': False,
        },
    )
    assert response.status_code == 422


def test_chat_rejects_blank_message_without_cloud_call():
    response = client.post('/chat', json={'session_id': 'test-session', 'message': '   '})
    assert response.status_code == 422
