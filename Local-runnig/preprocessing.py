# Abrir dataset
import imports
import csv, sys

nome_dataset = '/Datasets/Phishing_Email.csv'
csv.field_size_limit(sys.maxsize)  

def contadorFreq(lista):
  contador = imports.Counter()

  for item in lista:
    if len(item) < 15:
      contador[item] +=1

  freq = imports.pd.DataFrame(contador.most_common(100), columns=["words", "count"])
  return freq

def clean_bigrams(bigrams, max_word_length=15):

    cleaned_bigrams = []

    for bigram in bigrams:
        # Separa o bigrama em duas palavras
        word1, word2 = bigram

        # Verifica se as palavras tem um tamanho razoável
        if (len(str(word1)) <= max_word_length and
            len(str(word2)) <= max_word_length and
            # Confere se são caracteres alfanuméricos
            word1.isalnum() and
            word2.isalnum()):

            cleaned_bigrams.append(bigram)

    return cleaned_bigrams

def palavra_mais_frequente(lista):
  maisFrequente = imports.Counter(lista).most_common(1)
  return maisFrequente[0][0]

def plotaGraph(word_freq, titulo):
    imports.plt.style.use("_mpl-gallery")

    x = [str(word) for word in word_freq["words"]]
    y = word_freq["count"]

    fig, ax = imports.plt.subplots(figsize=(12, 6))  # Increased figure size

    ax.bar(x, y, width=0.8, edgecolor="white", linewidth=0.7)

    # Ajustar limites dinamicamente
    ax.set_xlim(-0.5, len(x) - 0.5)  # Ajusta para o número exato de palavras
    ax.set_ylim(0, max(y) + 50)  # Ajusta altura baseada no maior valor

    imports.plt.xticks(rotation=90)  # Mantém legível
    imports.plt.title(titulo)

    imports.plt.show()
    
def contar_e_plotar(lista):

  contaFreq = contadorFreq(lista)
  plotaGraph(contaFreq, "Unigrama")

  bigrama = list(imports.nltk.bigrams(lista))
  bigrama2 = clean_bigrams(bigrama)
  contaFreq = contadorFreq(bigrama2)
  plotaGraph(contaFreq, "Bigrama")
  
  
  
def conversor_utf8(text, tipo = None):

  clean_text = imports.re.sub(r'[^\x20-\x7E]', '', text)  # Mantém ASCII
  string_nova = imports.re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', clean_text) # Remover apóstrofos

  # if tipo == "url":
  #   string_nova = remove_repeating_chars(string_nova)

  return string_nova

def processar_dataset(nome_dataset, tipo_email):
  # Pega as letras
  letters = set(imports.string.ascii_letters)

  # Pega caracteres
  all_chars = set(imports.string.printable)

  # Acha caracteres indesejados
  unwanted_chars = sorted((all_chars | {'â', 'ä' ,'ã', 'á', 'à'} - letters) - {'$', '%'})

  # Regex para url
  url_regex = r"(?P<url>https?://[^\s]+)"
  stop_words = set(imports.stopwords.words('english'))
  tokenized_linha = []
  sub_dataset = []

  with open(nome_dataset, 'r') as dataset:
    reader = csv.reader(dataset)
    for linha in reader:

      # Encontrar email com ou sem phishing
      if (linha[2] == tipo_email):

        # Encontra url
        match_url = imports.re.findall(url_regex, linha[1])

        # Encontra linhas contendo urls
        if match_url:
          # salva urls em um csv
          f = open(tipo_email + '_urls.csv', 'a').write(match_url[0] + "\n")

          dt_limpo = conversor_utf8(linha[1], "url")

          # Tokenização e remoção de stopwords
          tokenized_linha = [word.lower() for word in imports.tk.word_tokenize(dt_limpo) if word not in unwanted_chars]
          tokenized_linha = [word for word in tokenized_linha if word not in stop_words and len(word) > 2]
          for word in tokenized_linha:
            sub_dataset.append(word)

    contar_e_plotar(sub_dataset)

    return sub_dataset

# Função para salvar e-mails de phishing
def processar_phishing(nome_dataset, nome_saida):
    emails_phishing = []

    with open(nome_dataset, 'r') as dataset:
        reader = csv.reader(dataset)
        for linha in reader:
            if linha[2] == "Phishing Email":  # Verifica se o email é de phishing
                texto_limpo = conversor_utf8(linha[1])  # Usa conversor_utf8 para limpar o texto
                emails_phishing.append([texto_limpo])

    # Salva os e-mails de phishing em um novo CSV
    with open(nome_saida, 'w', newline='', encoding='utf-8') as arquivo_saida:
        writer = csv.writer(arquivo_saida)
        writer.writerow(["Texto"])  # Cabeçalho do CSV
        writer.writerows(emails_phishing)  # Escreve os dados

# Execução do código
nome_dataset = '/Datasets/Phishing_Email.csv'
nome_saida = '/Datasets/emails_phishing.csv'
processar_phishing(nome_dataset, nome_saida)

# Função para limpar o texto e remover stopwords
def limpeza_dataset(texto):

    # Pega as letras
    letters = set(imports.string.ascii_letters)

    # Pega caracteres
    all_chars = set(imports.string.printable)

    # Acha caracteres indesejados
    unwanted_chars = sorted((all_chars | {'â', 'ä' ,'ã', 'á', 'à'} - letters) - {'$', '%'})

    # Converte para minúsculas
    text = texto.lower()

    # Remove pontuações
    text = text.translate(str.maketrans('', '', imports.string.punctuation))

    # Apenas utf-8
    text = conversor_utf8(text)

    # Remove stopwords
    stop_words = set(imports.stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    filtered_words = [word for word in filtered_words if word not in unwanted_chars]

    # Junta as palavras filtradas de volta em uma string
    cleaned_text = ' '.join(filtered_words)

    return cleaned_text

# Função para salvar e-mails de phishing
def processar_e_salvar_phishing(nome_dataset, nome_saida):
    emails_phishing = []

    with open(nome_dataset, 'r') as dataset:
        reader = csv.reader(dataset)
        for linha in reader:
            if linha[2] == "Phishing Email":  # Verifica se o email é de phishing
                texto_limpo = limpeza_dataset(linha[1])
                emails_phishing.append([texto_limpo])

    # Salva os e-mails de phishing em um novo CSV
    with open(nome_saida, 'w', newline='', encoding='utf-8') as arquivo_saida:
        writer = csv.writer(arquivo_saida)
        writer.writerow(["Texto"])  # Cabeçalho do CSV
        writer.writerows(emails_phishing)  # Escreve os dados

nome_dataset = '/Datasets/Phishing_Email.csv'
nome_saida = '/Datasets/emails_phishing.csv'
processar_e_salvar_phishing(nome_dataset, nome_saida)
