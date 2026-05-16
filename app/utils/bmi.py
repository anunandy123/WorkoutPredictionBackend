def calculate_bmi(weight: float, height_cm: float) -> str:
    """
    Calculate BMI given weight (kg) and height (cm).
    Returns BMI as a float rounded to 2 decimals.
    If parameters are missing, returns 'PLEASE PROVIDE ALL PARAMS'.
    """
    if weight == 0.0 or height_cm == 0.0:
        return "PLEASE PROVIDE ALL PARAMS"

    try:
        height_m = height_cm / 100
        bmi = weight / (height_m**2)
        return str(round(bmi, 2))
    except Exception:
        return "PLEASE PROVIDE ALL PARAMS"
