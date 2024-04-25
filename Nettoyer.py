import pandas as pd
import glob


# Concatener les fichiers quipoquiz entre eux
path = '/Users/alessandroarensberg/Documents/Visual Studio Code/Hackaton'
all_files = glob.glob(path + "/quipoquiz_*.csv")

all_data = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    all_data.append(df)

frame = pd.concat(all_data, axis=0, ignore_index=True)
frame.to_csv('quipoquiz.csv', index=False)


# Nettoyer le fichier quipoquiz
df = pd.read_csv('quipoquiz.csv')

df.rename(columns={'Lien': 'Thème de la question', 'Explication': 'Réponse à la question'}, inplace=True)

def clean_and_format(link):
    part = link.split('/quiz/')[1].split('/index')[0]
    part = part.replace('-', ' ').capitalize()
    return part

df['Thème de la question'] = df['Thème de la question'].apply(clean_and_format)

df.to_csv('FAQ_Quipoquiz.csv', index=False)


# Nettoyer le fichier quora
df_quora = pd.read_csv('quorascrap.csv')

df_quora.rename(columns={'Sujet': 'Thème de la question', 'Réponse': 'Réponse à la question'}, inplace=True)

df_quora.to_csv('FAQ_Quora.csv', index=False)


# Concatener les fichiers quipoquiz, quora et service-public entre eux
df_quipoquiz = pd.read_csv('/Users/alessandroarensberg/Documents/Visual Studio Code/Hackaton/FAQ_Quipoquiz.csv')
df_quora = pd.read_csv('/Users/alessandroarensberg/Documents/Visual Studio Code/Hackaton/FAQ_Quora.csv')
df_servicepublic = pd.read_csv('/Users/alessandroarensberg/Documents/Visual Studio Code/Hackaton/FAQ_ServicePublic.csv')

df_quipoquiz['Source'] = 'FAQ_Quipoquiz'
df_quora['Source'] = 'FAQ_Quora'
df_servicepublic['Source'] = 'FAQ_ServicePublic'

# S'assurer que tous les DataFrames ont le même ensemble de colonnes avant la concaténation
columns = ['Source', 'Thème de la question', 'Question', 'Réponse à la question', 'Date de vérification de la réponse', 'Auteur de la vérification']
df_quipoquiz = df_quipoquiz.reindex(columns=columns, fill_value=pd.NA)
df_quora = df_quora.reindex(columns=columns, fill_value=pd.NA)
df_servicepublic = df_servicepublic.reindex(columns=columns, fill_value=pd.NA)

df_combined = pd.concat([df_quipoquiz, df_quora, df_servicepublic], ignore_index=True)
df_combined.to_csv('FAQ.csv', index=False)