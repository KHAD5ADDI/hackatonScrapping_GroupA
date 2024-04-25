import requests as rq
from bs4 import BeautifulSoup

import csv


# Récupération des données
response = rq.get("https://www.service-public.fr/particuliers/vosdroits/questions-reponses")
soup = BeautifulSoup(response.content, 'html.parser')

div_principal = soup.find('div', class_="fiche-bloc bloc-principal")

listeThemes = []
listeQuestions = []
listeLiens = []

for fiche_item in div_principal.find_all('div', class_='fiche-item'):
    titreTheme = fiche_item.find('h2').text.strip() # Titre du thème
    
    for ul in fiche_item.find_all('ul'):
        for li in ul.find_all('li'):
            textQuestion = li.text # Question
            lienQuestion = li.a['href'] # Lien vers la page de la question

            listeThemes.append(titreTheme)
            listeQuestions.append(textQuestion)
            listeLiens.append(lienQuestion)

listeTitres = []
listeDates = []
listeReponses = []

for lien in listeLiens:
    response = rq.get(lien)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article', class_='article')

    titre_article = article.find('h1').text
    dateVerification = article.find('p', class_='fr-text--xs sp-text--mention').text
    reponse_element = article.find('p', class_='fr-text--lg') or article.find('p', attrs={'data-test': 'contenu-texte'})
    
    if reponse_element:
        reponse = reponse_element.text
    else:
        reponse = "Réponse non trouvée"

    listeDates.append(dateVerification)
    listeReponses.append(reponse)

dateVerification = []
auteurVerification = []

for term in listeDates:
    split_term = term.split(" - ")
    dateVerification.append(split_term[0])
    auteurVerification.append(split_term[1])


# Sauvegarde des données dans un DataFrame
with open('service-public.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Thème de la question", "Question", "URL de la question", "Date de vérification", "Auteur de la vérification de la réponse", "Réponse à la question"])
    for i in range(len(listeThemes)):
        writer.writerow([listeThemes[i], listeQuestions[i], listeLiens[i], dateVerification[i], auteurVerification[i], listeReponses[i]])