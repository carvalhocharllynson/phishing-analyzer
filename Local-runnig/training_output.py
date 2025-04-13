import training
import preprocessing
import imports

# Função para pré-processar a mensagem
def preprocessar_mensagem(mensagem):
    # Aplica a mesma limpeza usada no treinamento do modelo
    mensagem_limpa = preprocessing.limpeza_dataset(mensagem)
    return mensagem_limpa

def avaliar_mensagem(mensagem, modelo, vectorizer):
    # Pré-processa a mensagem
    mensagem_preprocessada = preprocessar_mensagem(mensagem)

    # Vetoriza a mensagem usando o mesmo vetorizador do treinamento
    mensagem_vetorizada = vectorizer.transform([mensagem_preprocessada])

    # Faz a previsão
    previsao = modelo.predict(mensagem_vetorizada)

    return "Phishing" if previsao[0] == 1 else "Segura"

resultado = []

with open('/content/emails_phishing.csv', 'r') as dataset:
    reader = imports.csv.reader(dataset)
    for linha in reader:
      resultado.append(avaliar_mensagem(linha[0], training.modelo, training.vectorizer))
      # print(f"Classificação da mensagem: {resultado}")

for i in range(len(resultado)):
  print(f"Classificacao da mensagem {i}: {resultado[i]}")