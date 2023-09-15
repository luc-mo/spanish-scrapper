import os
from http import client
from bs4 import BeautifulSoup
from urllib.parse import quote

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for letter in letters:
  print(f'Getting words for letter: {letter}')
  connection = client.HTTPSConnection('www.listapalabras.com', timeout=10)
  connection.request('GET', f'/palabras-con.php?letra={quote(letter)}&total=s')

  response = connection.getresponse()
  data = response.read()
  decoded = data.decode("utf-8")

  soup = BeautifulSoup(decoded, 'html.parser')
  words = soup.find(id='columna_resultados_generales')
  conjugations = soup.find(id='columna_resultados_conjugaciones')

  lower_letter = letter.lower()
  route = f'./words/{letter.lower()}'

  if not os.path.exists(route):
    os.makedirs(route)

  with open(f'{route}/{lower_letter}.txt', 'a', encoding='utf-8') as file:
    for w in words.find_all('a'):
      word = w.text.strip().replace('\n', '').lower()
      file.write(f'{word}\n')

  with open(f'{route}/{lower_letter}.conj.txt', 'a', encoding='utf-8') as file:
    for c in conjugations.find_all('a'):
      conjugation = c.text.strip().replace('\n', '').lower()
      file.write(f'{conjugation}\n')
  