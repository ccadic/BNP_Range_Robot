import yfinance as yf
import time
import requests

# Paramètres
SYMBOL = "BNP.PA"  # Symbole pour l'action BNP
LOWER_THRESHOLD = 35
UPPER_THRESHOLD = 70
CHECK_INTERVAL = 3600  # Intervalle de vérification en secondes

# Configuration Telegram
TELEGRAM_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # Remplacez par votre token
TELEGRAM_CHAT_ID = "-987654321"  # Remplacez par l'ID de votre groupe ou utilisateur

def send_telegram_message(message):
    """Envoie un message dans le groupe Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message envoyé avec succès sur Telegram.")
        else:
            print(f"Erreur lors de l'envoi sur Telegram : {response.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi Telegram : {e}")

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
                alert_message = f"ALERTE : Le prix de {SYMBOL} est passé sous {LOWER_THRESHOLD} EUR ({current_price:.2f} EUR). Action à acheter !"
                print(alert_message)
                send_telegram_message(alert_message)
                
            elif current_price > UPPER_THRESHOLD:
                alert_message = f"ALERTE : Le prix de {SYMBOL} a dépassé {UPPER_THRESHOLD} EUR ({current_price:.2f} EUR). Action à vendre !"
                print(alert_message)
                send_telegram_message(alert_message)
                
            else:
                print(f"L'action {SYMBOL} est toujours en range ({LOWER_THRESHOLD} - {UPPER_THRESHOLD}).")
            
            # Pause avant la prochaine vérification
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Erreur: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
