import yfinance as yf
import time

# Paramètres
SYMBOL = "BNP.PA"  # Symbole pour l'action BNP (vérifiez le suffixe .PA pour Euronext Paris)
LOWER_THRESHOLD = 35
UPPER_THRESHOLD = 70
CHECK_INTERVAL = 60  # Intervalle de vérification en secondes

def get_stock_price(symbol):
    """Récupère le dernier prix de l'action."""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="1m")  # Données intrajournalières
    if not data.empty:
        return data["Close"].iloc[-1]  # Dernier prix
    else:
        raise ValueError("Impossible de récupérer les données de l'action.")

def main():
    print("Lancement du robot de surveillance de l'action BNP...")
    while True:
        try:
            current_price = get_stock_price(SYMBOL)
            print(f"Prix actuel de {SYMBOL}: {current_price:.2f} EUR")
            
            if current_price < LOWER_THRESHOLD:
                print(f"ALERTE : Le prix est passé sous {LOWER_THRESHOLD} EUR. Action à acheter.")
                
            elif current_price > UPPER_THRESHOLD:
                print(f"ALERTE : Le prix a dépassé {UPPER_THRESHOLD} EUR. Action à vendre.")
                
            else:
                print(f"L'action {SYMBOL} est toujours en range ({LOWER_THRESHOLD} - {UPPER_THRESHOLD}).")
            
            # Pause avant la prochaine vérification
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Erreur: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
