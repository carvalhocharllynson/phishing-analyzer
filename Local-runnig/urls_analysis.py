import pandas as pd
from urllib.parse import urlparse
import re
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Função para extrair características das URLs
def extrair_caracteristicas(url):
    caracteristicas = {}

    # Comprimento da URL
    caracteristicas["comprimento"] = len(url)

    # Número de subdomínios
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        caracteristicas["num_subdominios"] = dominio.count('.') if dominio else 0

        # Presença de IP no domínio
        caracteristicas["tem_ip"] = 1 if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", dominio) else 0

        # Presença de caracteres especiais
        caracteristicas["tem_caracteres_especiais"] = 1 if re.search(r"[@_\-]", url) else 0

        # Extensão do domínio
        extensao = dominio.split('.')[-1] if dominio else ""
        caracteristicas["extensao_suspeita"] = 1 if extensao not in ["com", "org", "net", "gov", "edu"] else 0

        # Comprimento do caminho
        caminho = parsed_url.path
        caracteristicas["comprimento_caminho"] = len(caminho)

        # Presença de palavras-chave suspeitas
        palavras_chave = ["login", "secure", "verify", "account", "bank", "paypal"]
        caracteristicas["palavras_chave_suspeitas"] = sum(1 for palavra in palavras_chave if palavra in url.lower())
    except Exception as e:
        # Se houver erro, define valores padrão
        caracteristicas["num_subdominios"] = 0
        caracteristicas["tem_ip"] = 0
        caracteristicas["tem_caracteres_especiais"] = 0
        caracteristicas["extensao_suspeita"] = 0
        caracteristicas["comprimento_caminho"] = 0
        caracteristicas["palavras_chave_suspeitas"] = 0

    return caracteristicas

# Carregar URLs de phishing
urls_phishing = pd.read_csv('/content/Dataset/Phishing URLs.csv')
urls_phishing["label"] = 1  # 1 para phishing

# Carregar URLs seguras
urls_seguras = pd.read_csv('/content/Dataset/Legitimate URLs.csv')
urls_seguras["label"] = 0  # 0 para URLs seguras

# Combinar os datasets
dados_urls = pd.concat([urls_phishing, urls_seguras], ignore_index=True)

# Extrair características
dados_urls["caracteristicas"] = dados_urls["url"].apply(extrair_caracteristicas)
caracteristicas_df = pd.DataFrame(dados_urls["caracteristicas"].tolist())
dados_finais = pd.concat([caracteristicas_df, dados_urls["label"]], axis=1)

# Dividir os dados em treino e teste
X = dados_finais.drop("label", axis=1)
y = dados_finais["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
modelo_urls = RandomForestClassifier(random_state=42)
modelo_urls.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo_urls.predict(X_test)

# Avaliar o modelo e formatar a saída
report = classification_report(y_test, y_pred)
filtered_report = "\n".join(line for line in report.split("\n") if not any(x in line for x in ["accuracy", "macro avg", "weighted avg"]))
print("\nRelatório de classificação:\n", filtered_report)

# Função para classificar novas URLs
def classificar_url(url, modelo):
    # Extrair características da URL
    caracteristicas = extrair_caracteristicas(url)
    caracteristicas_df = pd.DataFrame([caracteristicas])

    # Fazer a previsão
    previsao = modelo.predict(caracteristicas_df)

    return "URL Falsa (Phishing)" if previsao[0] == 1 else "URL Segura"

# Testar com uma URL de phishing do dataset
url_phishing_teste = urls_phishing.sample(1)["url"].values[0]
resultado = classificar_url(url_phishing_teste, modelo_urls)
print(f"\nClassificação da URL de phishing: {resultado}")
print(f"URL de phishing usada: {url_phishing_teste}")

# Testar com uma URL segura do dataset
url_segura_teste = urls_seguras.sample(1)["url"].values[0]
resultado = classificar_url(url_segura_teste, modelo_urls)
print(f"\nClassificação da URL segura: {resultado}")
print(f"URL segura usada: {url_segura_teste}")

nova_url = "https://anoe.co.jp.iqgnnjo.cn/aeon"
resultado = classificar_url(nova_url, modelo_urls)
print(f"Classificação da URL: {resultado}")

import joblib
joblib.dump(modelo_urls, 'modelo_urls.pkl')