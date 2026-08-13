def calculate_mortgage(
    property_price_aed: float,
    down_payment_percent: float,
    annual_interest_rate: float,
    tenure_years: int,
) -> dict:
    down_payment = property_price_aed * (down_payment_percent / 100)
    principal = property_price_aed - down_payment
    months = tenure_years * 12

    if annual_interest_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_rate = annual_interest_rate / 100 / 12
        monthly_payment = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    return {
        "property_price_aed": round(property_price_aed, 2),
        "down_payment_aed": round(down_payment, 2),
        "loan_amount_aed": round(principal, 2),
        "estimated_monthly_payment_aed": round(monthly_payment, 2),
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "disclaimer": "Illustrative estimate only; lender terms and eligibility may differ.",
    }
