import json
from pathlib import Path

app_replacements = {
    '# Exibir gráfico de candlestick': '# Display candlestick chart',
    '# Exibir gráfico de linha do preço de fechamento': '# Display closing price line chart',
    '# Opcionalmente exibir tabela de dados brutos': '# Optionally display raw data table',
    'st.subheader("Dados")': 'st.subheader("Data")',
    'st.error(f"Erro ao carregar dados da ação: {e}")': 'st.error(f"Error loading stock data: {e}")',
}

notebook_replacements = {
    'from streamlit_autorefresh import st_autorefresh  # type: ignore': '# from streamlit_autorefresh import st_autorefresh  # removed dependency',
    'from streamlit_autorefresh import st_autorefresh # type: ignore': '# from streamlit_autorefresh import st_autorefresh  # removed dependency',
    'from streamlit_autorefresh import st_autorefresh': '# from streamlit_autorefresh import st_autorefresh  # removed dependency',
    '# # from streamlit_autorefresh import st_autorefresh  # removed dependency  # removed dependency': '# from streamlit_autorefresh import st_autorefresh  # removed dependency',
    'country_select = st.sidebar.selectbox("Selecione o país:", countries)': 'country_select = st.sidebar.selectbox("Select Country:", countries)',
    'stocks = ["AAPL", "MSFT", "GOOGL"]  # Lista de ações - customize com os tickers desejados': 'stocks = ["AAPL", "MSFT", "GOOGL"]  # List of stocks - customize with desired tickers',
    'from_date = st.sidebar.date_input("Data Inicial:", start_date)': 'from_date = st.sidebar.date_input("Start Date:", start_date)',
    'to_date = st.sidebar.date_input("Data Final:", end_date)': 'to_date = st.sidebar.date_input("End Date:", end_date)',
    'from_date = st.sidebar.date_input("Data Inicial:", start_date.date())': 'from_date = st.sidebar.date_input("Start Date:", start_date.date())',
    'to_date = st.sidebar.date_input("Data Final:", end_date.date())': 'to_date = st.sidebar.date_input("End Date:", end_date.date())',
    'interval_select = st.sidebar.selectbox("Selecione o intervalo:", intervals)': 'interval_select = st.sidebar.selectbox("Select Interval:", intervals)',
    'interval_select = st.sidebar.selectbox("Escolha o intervalo de tempo desejado (d - dia | wk - semana | mo - mês):", intervals)': 'interval_select = st.sidebar.selectbox("Select the desired time interval (d - day | wk - week | mo - month):", intervals)',
    'load_data = st.sidebar.checkbox("Carregar Dados")': 'load_data = st.sidebar.checkbox("Load Data")',
    '    st.write(f"Contagem: {count}")': '    st.write(f"Count: {count}")',
    '# Validar intervalo de datas e buscar/exibir dados de ações': '# Validate date range and fetch/display stock data',
    '# Opcionalmente exibir tabela de dados brutos': '# Optionally display raw data table',
    '# Exibindo o título com tamanho de fonte personalizado': '# Displaying title with custom font size',
    'st.sidebar.error("A data inicial deve ser menor que a data final")': 'st.sidebar.error("Start Date must be earlier than End Date")',
    'st.write(f"Data Inicial: {formatted_start_date}")': 'st.write(f"Start Date: {formatted_start_date}")',
    'st.write(f"Data Final: {formatted_end_date}")': 'st.write(f"End Date: {formatted_end_date}")',
    'raise ValueError("Requisições muito frequentes! Aguarde um momento.")': 'raise ValueError("Requests are too frequent! Please wait a moment.")',
    'st.error(f"Erro ao acessar os dados: {ke}")': 'st.error(f"Error accessing data: {ke}")',
    'logging.error(f"Erro ao consultar dados: {e}")': 'logging.error(f"Error querying data: {e}")',
    'st.error(f"Ocorreu um erro ao consultar os dados: {e}")': 'st.error(f"An error occurred while querying data: {e}")',
    '# Criando o restante da barra lateral': '# Creating the rest of the sidebar',
    '# Aplicando melhorias na barra lateral': '# Applying improvements to the sidebar',
    '# Função para limitar requisições por tempo': '# Function to limit requests over time',
    '    """Verifica se o intervalo mínimo entre requisições foi atendido."""': '    """Checks that the minimum interval between requests has been met."""',
    '# Verificação de datas e exibição de gráficos': '# Date validation and chart display',
    '# Verificando se a data inicial é menor que a data final': '# Checking that the start date is earlier than the end date',
    '# Formata as datas no formato brasileiro (DD/MM/YYYY) apenas para exibição': '# Formats dates in Brazilian format (DD/MM/YYYY) for display only',
    '# Usando a ação da Apple (AAPL) entre os dias 1 de janeiro de 2023 e 31 de dezembro de 2023, com intervalo diário (1d)': '# Using Apple (AAPL) between January 1, 2023 and December 31, 2023, with daily interval (1d)',
    '# Capturar dados históricos para ver se são exibidos corretamente, para utilizarem os': '# Capture historical data to see if it is displayed correctly for use',
    '1. Teste de Integridade dos Dados': '1. Data Integrity Test',
    'Checagem da integridade dos dados concluída.': 'Data integrity check completed.',
    '# como exemplo para verificar a integridade dos dados obtidos.': '# as an example to verify the integrity of the obtained data.',
    '    """Testa a integridade dos dados verificando colunas, valores nulos e valores negativos."""': '    """Tests the data integrity by checking columns, null values, and negative values."""',
    'print(f"A coluna {col} possui valores negativos!")': 'print(f"The column {col} contains negative values!")',
    'Os dados são consistentes através de múltiplas requisições.': 'The data is consistent across multiple requests.',
    'Teste 1 - Dados recuperados com sucesso com um intervalo pequeno.': 'Test 1 - Successfully retrieved data with a small interval.',
    '#### LIMPEZA E TRATAMENTO DE DADOS': '#### DATA CLEANING AND PROCESSING',
    'Eventualmente, os dados podem ter lacunas, especialmente se houver interrupções no mercado ou em dias de feriado, portanto começaremos por verificar se os dados possuem valores ausentes (NaN) no DataFrame testado e decidamos como lidar com eles.': 'Data may eventually have gaps, especially if there are market interruptions or holidays, so we will begin by checking whether the data contains missing values (NaN) in the tested DataFrame and decide how to handle them.',
    'O IQR é uma medida estatística que representa a diferença entre o terceiro quartil (Q3) e o primeiro quartil (Q1) de um conjunto de dados.': 'IQR is a statistical measure that represents the difference between the third quartile (Q3) and the first quartile (Q1) of a dataset.',
    'Primeiro Quartil (Q1): É o valor abaixo do qual se encontra 25% dos dados.': 'First Quartile (Q1): It is the value below which 25% of the data is found.',
    'Terceiro Quartil (Q3): É o valor abaixo do qual se encontra 75% dos dados.': 'Third Quartile (Q3): It is the value below which 75% of the data is found.',
    'O IQR é usado principalmente para identificar a dispersão central dos dados e para detectar outliers (valores atípicos). Dados que caem abaixo de 𝑄1 − 1.5 × 𝐼𝑄𝑅 ou acima de 𝑄3 + 1.5 × 𝐼𝑄𝑅 são frequentemente considerados outliers.': 'IQR is mainly used to identify the central dispersion of the data and to detect outliers. Data that falls below 𝑄1 − 1.5 × 𝐼𝑄𝑅 or above 𝑄3 + 1.5 × 𝐼𝑄𝑅 is often considered outliers.',
    'Embora improvável, duplicatas podem ocorrer devido a erros na API ou em requisições repetidas e para evitar isso removeremos quaisquer ocorrência existente para evitar distorções na análise.': 'Although unlikely, duplicates may occur due to API errors or repeated requests, and to avoid this we will remove any existing occurrences to prevent distortion in the analysis.',
    'Podem haver lacunas nas datas, por exemplo, faltando dados em alguns dias úteis e poderemos interpolar ou ajustar os dados, para isto reindexaremos o dataframe para garantir que todas as datas dentro do intervalo estejam presentes e, em seguida, interpolar os dados ausentes, se necessário.': 'There may be gaps in the dates, for example missing data on some business days, and we may interpolate or adjust the data. To do this, we will reindex the DataFrame to ensure that all dates within the range are present and then interpolate missing data if necessary.',
    'Para garantir que, após todas as limpezas e tratamentos, os dados estão consistentes e prontos para análise, faremos uma validação final visualizando um resumo estatístico dos dados e criaremos um gráfico simples para inspecionar a integridade dos dados.': 'To ensure that after all cleaning and processing the data is consistent and ready for analysis, we will perform a final validation by viewing a statistical summary of the data and creating a simple chart to inspect data integrity.',
    'Embora os dados do Yahoo Finance sejam geralmente confiáveis, essas etapas de limpeza e tratamento garantem que estejamos trabalhando com um conjunto de dados robusto, minimizando possíveis erros ou distorções na análise final.': 'Although Yahoo Finance data is generally reliable, these cleaning and processing steps ensure that we are working with a robust dataset, minimizing potential errors or distortions in the final analysis.',
}

notebook_manual_replacements = {
    'count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")': 'if st.sidebar.button("Refresh Data"):\n    st.experimental_rerun()\ncount = 0',
    '    st.write("Contagem é zero")': '    st.write("Count is zero")',
    '    st.write(f"Contagem: {count}")': '    st.write(f"Count: {count}")',
}

notebook_files = [Path('sprint1.ipynb'), Path('sprint2.ipynb'), Path('sprint3.ipynb')]
for path in notebook_files:
    data = json.loads(path.read_text(encoding='utf-8'))
    updated = False
    for cell in data.get('cells', []):
        if cell.get('cell_type') not in ('markdown', 'code'):
            continue
        source = cell.get('source', [])
        new_source = []
        for line in source:
            new_line = line
            for old, new in notebook_replacements.items():
                if old in new_line:
                    new_line = new_line.replace(old, new)
            for old, new in notebook_manual_replacements.items():
                if old in new_line:
                    new_line = new_line.replace(old, new)
            if new_line != line:
                updated = True
            new_source.append(new_line)
        cell['source'] = new_source
    if updated:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'Updated {path}')
    else:
        print(f'No updates for {path}')

app_path = Path('app.py')
app_text = app_path.read_text(encoding='utf-8')
for old, new in app_replacements.items():
    app_text = app_text.replace(old, new)
app_path.write_text(app_text, encoding='utf-8')
print('Updated app.py')

# Verify residual markers
markers = [
    'streamlit_autorefresh', 'st_autorefresh', 'Selecione o país', 'Data Inicial', 'Data Final',
    'Carregar Dados', 'Contagem:', 'A data inicial', 'Erro ao carregar dados', 'Ação',
    'Requisições muito frequentes', 'Erro ao acessar os dados', 'Erro ao consultar os dados',
    'Teste de Integridade', 'Checagem da integridade', 'Dados', 'Exibindo', 'Aplicando melhorias',
]
for path in [app_path] + notebook_files:
    text = path.read_text(encoding='utf-8')
    residuals = [m for m in markers if m in text]
    if residuals:
        print(f'Residual markers in {path}:', residuals)
