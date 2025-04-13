import preprocessing
import imports

Phishing_email_processed = preprocessing.processar_dataset(preprocessing.nome_dataset, "Phishing Email")

Safe_email_processed = preprocessing.processar_dataset(preprocessing.nome_dataset, "Safe Email")

# Palavras mais frequêntes nos emails de phishing do dataset utilizado
# Caminho do arquivo CSV
dataset_path = "/content/emails_phishing.csv"

# Carregar os dados
df = imports.pd.read_csv(dataset_path)

# Supondo que cada linha já contenha palavras tokenizadas e processadas em formato de string
palavras_phishing = []

for mensagem in df.iloc[:, 0].dropna():  # Usa apenas a primeira coluna e remove NaN
    palavras_phishing.extend(mensagem.split())  # Assume que as palavras estão separadas por espaço

# Contagem de frequência
contador = imports.Counter(palavras_phishing)
freq_palavras = imports.pd.DataFrame(contador.most_common(200), columns=["Palavra", "Frequência"])

# Salvar e exibir os resultados
freq_palavras.to_csv("palavras_frequentes.csv", index=False)
freq_palavras.head(100)