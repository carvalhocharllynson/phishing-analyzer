import imports
import preprocessing
import joblib

palavras_phishing = ["future", "investment", "product", "milion", "online", "price", "receive", "name", "make", "free", "phone", "urgent", "software", "money", "buy", "information", "password", "click", "account", "verify", "login", "bank", "security", "update", "payment", "statements"]
palavras_seguras = ["meeting", "report", "team", "project", "deadline", "client", "agenda", "schedule", "feedback", "progress"]

dados_phishing = imports.pd.DataFrame({"texto": palavras_phishing, "label": 1})
dados_seguros = imports.pd.DataFrame({"texto": palavras_seguras, "label": 0})
dados = imports.pd.concat([dados_phishing, dados_seguros], ignore_index=True)

# Vetorização do texto
vectorizer = imports.CountVectorizer()
X = vectorizer.fit_transform(dados["texto"])
y = dados["label"]

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = imports.train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
modelo = imports.MultinomialNB() # (Prof. Brenda) testar outras variações como o grid search
modelo.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo.predict(X_test)

# Avaliar o modelo e formatar a saída
report = imports.classification_report(y_test, y_pred)
filtered_report = "\n".join(line for line in report.split("\n") if not any(x in line for x in ["accuracy", "macro avg", "weighted avg"]))
print("\nRelatório de classificação:\n", filtered_report)

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

nova_mensagem = "Urgent: Your Account Has Been Compromised Dear Valued Customer, We have detected unusual activity on your account. To secure your account, please verify your identity by clicking the link below: Verify My Account Now If you do not take action within 24 hours, your account will be temporarily suspended. Thank you for your prompt attention to this matter. Sincerely, The Security Team"
resultado = avaliar_mensagem(nova_mensagem, modelo, vectorizer)
print(f"Classificação da mensagem: {resultado}")


joblib.dump(modelo, 'modelo_mensagens.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')