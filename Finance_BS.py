import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from datetime import datetime, date, timedelta
from Fonction_brownien import get_input
from joblib import Memory

# Configuration de l'emplacement du cache
location = './cache_folder'  # Indiquez l'emplacement où vous souhaitez stocker le cache

# Initialisation de l'objet Memory de joblib
memory = Memory(location, verbose=0)

# Définition de la fonction pour récupérer les données et la mettre en cache
@memory.cache
def get_stock_data(symbol, start_date, end_date):
    """
    Juste une fonction pour eviter de telecharger plusieurs fois le taux sans risque
    """
    return yf.download(symbol, start=start_date, end=end_date)



def get_date_yesterday():
    """
    Une fonction pour obtenir la dernière date valide si on demande des informations boursière
    """
    today = date.today()
    return today - timedelta(days = 1)



def geometric_brownian_motion(S, drift, volatility, T, N):
    """
    C'est une fonction pour générer la bourse grace à un mouvement brownien.
    """
    dt = T / N
    t = np.linspace(0., T, N+1)
    W = np.random.standard_normal(size=N+1) 
    W = np.cumsum(W) * np.sqrt(dt) 
    X = (drift - 0.5 * volatility**2) * t + volatility * W 
    S = S * np.exp(X) 
    return S

def black_scholes(S, K, r, sigma, T):
    """
    C'est une fonction pour calculer le prix d'une option d'achat
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

#On fait une bibliothèque d'actions et d'indices

dict_ticket = {"Apple" : ("Apple", "AAPL", 1), "Bois" : ("Bois", "WOOD", 0), "CAC40" : ("CAC40", "^FCHI", 1), "Crédit Agricole": ("Crédit Agricole", "ACA.PA", 1),
                "Amazon": ("Amazon", "AMZN", 1), "Netflix": ("Netflix", "NFLX", 1), "Tesla" : ("Tesla", "TSLA", 1), "Air Liquide": ("Air liquide", "AI.PA", 0), 
                "L'Oreal" : ("L'Oreal", "OR.PA", 1), "LVMH" : ("LVMH", "MC.PA", 1), "Maïs" : ("Mais", "CORN", 0), "Blé" : ("Blé", "WEAT", 0), 
                "Soja" : ("Soja", "SOYB", 0), "Sucre" : ("Sucre", "CANE", 0), "Acier" : ("Acier", "SLX", 0), "Cuivre": ("Cuivre", "COPX", 0), "Or" : ("Or", "GC=F", 0),
                "Volkswagen" : ("Volkswagen", "VLKAF", 1), "Airbus" : ("Airbus", "AIR.PA", 1), "Safran" : ("Safran", "SAF.PA", 1), "Google" : ("Goodle", "GOOGL", 1),
                "Alstom" : ("Alstrom", "ALO.PA", 1), "Axa" : ("Axa", "CS.PA", 1), "Sanofi" : ("Sanofi", "SAN.PA", 1), "Café" : ("Café", "KC=F", 0),
                "Coton" : ("Coton", "CT=F", 0)}


#On choisis un ticket
ticket = dict_ticket["Apple"]

while True:

    liste_ticket = list(dict_ticket)

    #On affiche les tickets

    for i in range(len(liste_ticket)):
        print(f"{i} : {liste_ticket [i]}", end="\t")
        if (i+1) % 4 == 0:
            print("")

    print("")

    #On demande quel action ou matière premiere l'utilisateur veux analyser
    number = get_input("Choissez le numero de votre ticket : ", default_value=0, value_type=int, min_value=0, max_value=len(liste_ticket)-1)
    ticket = dict_ticket[liste_ticket[number]]

    #On choisit la periode de l'echantillon que l'on va analyser
    start_date_donnees = '2022-01-01'
    end_date_donnees = '2022-12-31'

    print(f"Echantillon analysé : {ticket[0]} de {start_date_donnees} à {end_date_donnees} (AAAA-MM-JJ)")


    #On telecharge les informations boursière du ticket
    stock_data = yf.download(ticket[1], start=start_date_donnees, end=end_date_donnees)
    nb_business_day_stock_data = len(stock_data)

    #On definit des paramètres coeherant sur l'echantillon de temps sur leque on va calculer le taux sans risque et la volatilité
    parametre_signma_r_actions = (90, 90)
    parametre_signma_r_matiere_premier = (60, 15)

    #On choisit quel paramètre on prend, soit celui es actions soit celui des matière premières
    if ticket[2] == 0:
        parametre_signma_r = parametre_signma_r_matiere_premier
    elif ticket[2] == 1:
        parametre_signma_r = parametre_signma_r_actions

    #On calcule la volatilté sur l'echantillon de temps choisit
    stock_returns = stock_data['Close'].pct_change(periods=parametre_signma_r[0]).dropna()
    volatility_stock = stock_returns.std()


    #On télécharge un indice pour calculer le taux dans risque 
    #treasury_10y = yf.download('^TNX', start=start_date_donnees, end=end_date_donnees)
    treasury_10y = get_stock_data('^TNX',start_date_donnees,end_date_donnees)

    # Calcul du rendement sur l'echantillon de temps
    treasury_returns = treasury_10y['Close'].pct_change(periods=parametre_signma_r[1]).dropna()
    risk_free_rate = treasury_returns.mean()

    # Paramètres pour la simulation GBM
    S0 = stock_data['Close'].iloc[-1]  # Prix initial de l'action
    T = 1.     # Temps jusqu'à l'expiration de l'option (en années)
    r = risk_free_rate # Taux sans risque
    sigma = volatility_stock  # Volatilité
    drift = r


    #On donne la peridode sur laquelle on veut faire la prévision
    start_date_previsions = '2022-12-30'
    end_date_previsions =  '2023-12-31'
    end_date_previsions_date = datetime.strptime(end_date_previsions, '%Y-%m-%d').date()




    # Calcul du nombre de jours ouvrés entre les deux dates
    nb_business_days = pd.date_range(start=start_date_previsions, end=end_date_previsions, freq='B').shape[0]

    #Si la periode dépasse la date d'hier, on rogne la courbe réelle
    yesterday = get_date_yesterday()
    if end_date_previsions_date > yesterday:
        stock_data_next = yf.download(ticket[1], start=start_date_previsions, end=yesterday)
    else:
        stock_data_next = yf.download(ticket[1], start=start_date_previsions, end=end_date_previsions)


    # Création de la figure et des axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Premier graphique : Prix de clôture AAPL - Année précédente
    ax.plot(stock_data['Close'], label=f'Prix de clôture {ticket[0]} - Année précédente', color='orange')
    ax.set_xlabel('Temps')
    ax.set_ylabel("Prix de l'action - Année précédente", color='orange')
    ax.legend(loc='upper left')
    ax.grid(True)

    # Deuxième graphique : Simulation du prix de l'action
    paths = 500
    alpha_paths = 0.1
    N = nb_business_days
    option_prices = [geometric_brownian_motion(S0, drift, sigma, T, N-1) for _ in range(paths)]
    mean_prices = np.mean(option_prices, axis=0)

    #On affiche le prix d'origine

    print(f"Prix de l'origine  : ",S0)

    #On demande le prix à l'utilisateur
    strike_price = get_input("Choissez le prix d'exerice de l'option ", default_value=1.1*S0, value_type=float, min_value=0)

    #On calcule le prix de l'option d'achat et on l'affiche
    call_option_price = black_scholes(S0, strike_price, r, sigma, T)
    print(f'Prix de l\'option d\'achat (call option) : {call_option_price}')

    # Date de départ
    start_date = stock_data.index[-1]

    # Générer la liste des jours ouvrés
    business_days = pd.date_range(start=start_date, periods=N, freq='B')


    for i in range(paths):
        plt.plot(business_days, option_prices[i], color='deepskyblue', alpha=alpha_paths, lw=1)

    plt.plot(business_days, mean_prices, color='blue', label='Moyenne des simulations', lw=2)
    plt.legend(loc='best')

    ax.plot(stock_data_next['Close'], label=f'Prix de clôture {ticket[0]} - Année suivante', color='red')
    ax.legend(loc='best')

    # Ajustement de l'espacement entre les sous-graphiques
    plt.tight_layout()

    # Affichage des graphiques
    plt.show()

    recommencer = get_input("\nVoulez vous recommencer", default_value=True, value_type=bool)

    if recommencer == False:
        break
    else:
        print("\n\n")
