# -*- coding: utf-8 -*-

# Etapa 1: Importação de bibliotecas
import unicodedata
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# SOLUÇÃO DEFINITIVA ATUAL: utilização da função solve_ivp da biblioteca SciPy,
# 
from scipy.integrate import solve_ivp

def run_simulation():
    """
    Função principal para encapsular todo o processo de simulação.
    """
    # --- Configuração de visualização ---
    sns.set_style("whitegrid")
    plt.style.use("seaborn-v0_8-whitegrid")
    print("Bibliotecas importadas com sucesso.")

    # --- Carregar o conjunto de dados ---
    try:
        df = pd.read_csv('indicators_sdi_covid19 (1).csv')
        print("Arquivo 'indicators_sdi_covid19 (1).csv' carregado com sucesso.")
    except FileNotFoundError:
        print("Erro: O arquivo 'indicators_sdi_covid19 (1).csv' não foi encontrado.")
        print("Por favor, certifique-se de que o arquivo está na mesma pasta que o script.")
        return

    # --- Filtrar dados para Recife/PE ---
    df_recife = df[(df['name_mun'] == 'Recife') & (df['name_fu'] == 'Pernambuco')].copy()
    if df_recife.empty:
        print("Atenção: Nenhum dado encontrado para Recife/PE.")
        return
    print(f"Dados de Recife extraídos com sucesso. Dimensões: {df_recife.shape}")

    # --- Limpeza e formatação dos nomes das colunas ---
    def clean_col_names(df_to_clean):
        new_cols = {}
        for col in df_to_clean.columns:
            normalized_col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
            cleaned_col = re.sub(r'[^\w\s-]', '', normalized_col).strip().lower()
            cleaned_col = re.sub(r'[-\s]+', '_', cleaned_col)
            new_cols[col] = cleaned_col
        return df_to_clean.rename(columns=new_cols)

    df_recife_clean = clean_col_names(df_recife)
    df_recife_clean.to_csv('recife_dados_limpos.csv', index=False)
    print("DataFrame limpo salvo como 'recife_dados_limpos.csv'.")

    # Etapa 2: Preparar Dados para o Modelo SIR
    print("\n--- Configurando Parâmetros para o Modelo SIR ---")
    N = int(df_recife_clean['pop_2020'].iloc[0])
    print(f"População total de Recife (N): {N:,}")

    # Cenário 1: COVID-19
    periodo_infeccioso_covid = 10
    gamma_covid = 1 / periodo_infeccioso_covid
    r0_covid = 2.5
    beta_covid = r0_covid * gamma_covid

    # Cenário 2: Arbovirose
    periodo_infeccioso_arbo = 7
    gamma_arbo = 1 / periodo_infeccioso_arbo
    r0_arbo = 1.8
    beta_arbo = r0_arbo * gamma_arbo

    # Condições Iniciais e Duração
    I0 = 1
    S0 = N - I0
    R0 = 0
    y0 = [S0, I0, R0] # Vetor de condições iniciais
    dias_simulacao = 365
    t_span = [0, dias_simulacao] # Intervalo de tempo para a simulação
    t_eval = np.linspace(t_span[0], t_span[1], dias_simulacao) # Pontos onde a solução é calculada

    # Etapa 3: Definir e Executar o Modelo SIR com SciPy
    def sir_model(t, y, N, beta, gamma):
        """
        Define as equações diferenciais do modelo SIR para o solver da SciPy.
        t: tempo (requerido pelo solver, mas não usado nas equações aqui)
        y: vetor com as populações S, I, R
        N: população total
        beta: taxa de transmissão
        gamma: taxa de recuperação
        """
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    print("\n--- Executando Simulações com SciPy ---")
    
    # Simulação COVID-19
    print("Executando modelo para COVID-19...")
    sol_covid = solve_ivp(
        fun=sir_model,
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        args=(N, beta_covid, gamma_covid)
    )
    results_covid = pd.DataFrame({'t': sol_covid.t, 'S': sol_covid.y[0], 'I': sol_covid.y[1], 'R': sol_covid.y[2]})
    print("Simulação para COVID-19 concluída.")

    # Simulação Arbovirose
    print("Executando modelo para Arbovirose...")
    sol_arbo = solve_ivp(
        fun=sir_model,
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        args=(N, beta_arbo, gamma_arbo)
    )
    results_arbo = pd.DataFrame({'t': sol_arbo.t, 'S': sol_arbo.y[0], 'I': sol_arbo.y[1], 'R': sol_arbo.y[2]})
    print("Simulação para Arbovirose concluída.")

    # Etapa 4: Visualizar e Interpretar Resultados
    print("\n--- Gerando Gráficos ---")
    
    # Gráfico COVID-19
    plt.figure(figsize=(12, 7))
    plt.plot(results_covid['t'], results_covid['S'], label='Suscetíveis', color='blue')
    plt.plot(results_covid['t'], results_covid['I'], label='Infetados', color='red')
    plt.plot(results_covid['t'], results_covid['R'], label='Recuperados', color='green')
    plt.xlabel('Tempo (dias)')
    plt.ylabel('Número de Pessoas')
    plt.title(f'Simulação do Modelo SIR para COVID-19 em Recife (N={N:,})')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

    # Gráfico Arbovirose
    plt.figure(figsize=(12, 7))
    plt.plot(results_arbo['t'], results_arbo['S'], label='Suscetíveis', color='blue')
    plt.plot(results_arbo['t'], results_arbo['I'], label='Infetados', color='orange')
    plt.plot(results_arbo['t'], results_arbo['R'], label='Recuperados', color='green')
    plt.xlabel('Tempo (dias)')
    plt.ylabel('Número de Pessoas')
    plt.title(f'Simulação do Modelo SIR para Arbovirose em Recife (N={N:,})')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

    # Gráfico Comparativo
    plt.figure(figsize=(14, 8))
    plt.plot(results_covid['t'], results_covid['I'], label='Infetados (COVID-19)', color='red', linewidth=2.5)
    plt.plot(results_arbo['t'], results_arbo['I'], label='Infetados (Arbovirose)', color='orange', linestyle='--', linewidth=2.5)
    plt.xlabel('Tempo (dias)')
    plt.ylabel('Número de Infetados')
    plt.title('Comparação das Curvas de Infeção: COVID-19 vs. Arbovirose em Recife')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Análise e Interpretação com Fatores Socioeconómicos
    print("\n--- Análise e Interpretação dos Resultados ---")
    densidade_residencial = df_recife_clean['pct_house_density_2'].iloc[0]
    gdp_per_capita = df_recife_clean['gdp_per_capita'].iloc[0]
    taxa_analfabetismo = df_recife_clean['illiteracy_rate'].iloc[0]
    pico_covid_y = results_covid['I'].max()
    pico_arbo_y = results_arbo['I'].max()

    print("A simulação demonstra como os parâmetros fundamentais de uma doença (β e γ) geram curvas epidémicas distintas.")
    print("A integração de dados socioeconómicos do ficheiro `indicators_sdi_covid19 (1).csv` é crucial não para alterar o modelo dinamicamente, mas para justificar a escolha dos parâmetros e contextualizar os resultados.")
    print(f"\n1. **COVID-19 (Doença Respiratória):** A simulação projeta um pico de {int(pico_covid_y):,} infetados. A escolha de um R₀ (e, consequentemente, um beta) mais elevado é justificada por indicadores de Recife como a alta densidade domiciliar (percentagem de casas com mais de 2 pessoas por quarto: {densidade_residencial:.2f}%). Esta condição acelera a transmissão de patógenos respiratórios, levando a uma epidemia mais explosiva.")
    print(f"\n2. **Arbovirose (Doença Vetorial):** O pico projetado é menor, com {int(pico_arbo_y):,} infetados. A dinâmica de transmissão é menos agressiva porque depende de um vetor (mosquito). Fatores socioeconómicos como o PIB per capita (R$ {gdp_per_capita:,.2f}) e a taxa de analfabetismo ({taxa_analfabetismo:.2f}%) são proxies para condições de saneamento e habitação que influenciam a proliferação do vetor, justificando uma dinâmica de propagação mais lenta em comparação com a transmissão direta.")
    print("\n**Conclusão para o Artigo:** Este modelo, embora simples, ilustra como os fatores socioeconómicos de uma população informam a parametrização de modelos epidemiológicos. Cidades com alta densidade populacional são inerentemente mais vulneráveis a surtos de doenças respiratórias, enquanto os desafios de doenças vetoriais estão mais ligados a indicadores de desenvolvimento e infraestrutura.")


    # Etapa 5: Exportar Resultados
    print("\n--- Exportando Resultados ---")
    results_covid['cenario'] = 'COVID-19'
    results_arbo['cenario'] = 'Arbovirose'
    df_resultados_finais = pd.concat([results_covid, results_arbo], ignore_index=True)
    df_resultados_finais.to_csv('resultados_simulacao_sir_recife.csv', index=False)
    print("Resultados completos da simulação salvos em 'resultados_simulacao_sir_recife.csv'.")

    # Resumo Estatístico
    resumo_covid = {"Cenário": "COVID-19", "Pico de Infetados": f"{int(results_covid['I'].max()):,}", "Dia do Pico": int(results_covid['t'][results_covid['I'].idxmax()])}
    resumo_arbo = {"Cenário": "Arbovirose", "Pico de Infetados": f"{int(results_arbo['I'].max()):,}", "Dia do Pico": int(results_arbo['t'][results_arbo['I'].idxmax()])}
    df_resumo = pd.DataFrame([resumo_covid, resumo_arbo])
    print("\n--- Resumo Estatístico das Simulações ---")
    print(df_resumo.to_string(index=False))

if __name__ == '__main__':
    run_simulation()