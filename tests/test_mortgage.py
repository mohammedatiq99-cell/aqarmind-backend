from app.services.mortgage import calculate_mortgage


def test_mortgage_returns_positive_payment():
    result = calculate_mortgage(
        property_price_aed=1_500_000,
        down_payment_percent=20,
        annual_interest_rate=4.5,
        tenure_years=25,
    )
    assert result["loan_amount_aed"] == 1_200_000
    assert result["estimated_monthly_payment_aed"] > 0
