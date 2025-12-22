def calculate_volatility(data):
    returns = data['Close'].pct_change()
    volatility = returns.std()
    return volatility

def classify_risk(volatility):
    if volatility < 0.02:
        return "Low Risk"
    
    elif volatility < 0.05:
        return "Medium Risk"
    
    else:
        return "High Risk"
    
