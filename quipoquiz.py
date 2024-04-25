import requests as rq
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv


# Récupération des liens et noms des quizz
response = rq.get("https://quipoquiz.com/fr/tous-les-quiz")
soup = BeautifulSoup(response.content, 'html.parser')

imagesQuizz = soup.find_all('img', class_='img_quiz img-fluid')
listeNomsQuizz = [img['alt'] for img in imagesQuizz if 'alt' in img.attrs]
listeLiensQuizz = [img.parent.get('href') for img in imagesQuizz if img.parent.name == 'a']


# Récupération des questions et explications
driver = webdriver.Safari()

listeLiens = []
listeQuestions = []
listeExplications = []

def wait_for_new_explication(old_explication, timeout=30):
    def explication_has_changed(driver):
        try:
            current_explication = driver.find_elements(By.TAG_NAME, "p")[1].text
            return current_explication != old_explication and current_explication != ""
        except IndexError:
            return False
    return WebDriverWait(driver, timeout).until(explication_has_changed)

compteur = 0
nbrEnregistrements = 0

for lien in listeLiensQuizz[:77]:
    driver.get(f"https://quipoquiz.com{lien}")
    compteur += 1
    print(f'Scraping du site numéro {compteur} sur {len(listeLiensQuizz)}')
    
    # Clique sur le bouton pour commencer le quiz
    startButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_quiz.btn.btn-primary"))
    )
    startButton.click()

    old_explication = None
    for _ in range(10):
        # Clique sur le bouton "VRAI"
        trueButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_quiz.tf_btn.btn.btn-primary.mr-2"))
        )
        trueButton.click()

        # Attente que l'explication change
        wait_for_new_explication(old_explication)

        question, explication = driver.find_elements(By.TAG_NAME, "p")[:2]
        old_explication = explication.text  # Mise à jour de l'explication précédente

        listeLiens.append(lien)
        listeQuestions.append(question.text)
        listeExplications.append(explication.text)

        # Clique sur le bouton "CONTINUER"
        continueButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_continue"))
        )
        continueButton.click()

        # Enregistrement intermédiaire des données pour éviter de tout perdre en cas de crash
        if len(listeExplications) % 10 == 0:
            print(f'Enregistrement intermédiaire numéro {nbrEnregistrements}')
            nbrEnregistrements += 1
            with open('quipoquiz_77-.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Lien', 'Question', 'Explication'])
                for i in range(len(listeLiens)):
                    writer.writerow([listeLiens[i], listeQuestions[i], listeExplications[i]])

driver.quit()