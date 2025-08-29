# 🦠 Simulação Epidemiológica com Modelo SIR -  Recife/PE

Este projeto de Iniciação Científica Voluntária realiza uma simulação comparativa da propagação de **Doenças Respiratórias** (COVID-19) e **Arbovirose** - na cidade de **Recife**, utilizando o modelo matemático **SIR (Suscetíveis, Infectados, Recuperados)**. A análise é enriquecida com dados socioeconômicos reais para contextualizar os resultados.

## 📦 Estrutura do Projeto

- `run_simulation()`: Função principal que executa todas as etapas da simulação.
- `indicators_sdi_covid19 (1).csv`: Arquivo com dados socioeconômicos dos municípios brasileiros.
- `recife_dados_limpos.csv`: Dados filtrados e limpos apenas para Recife.
- `resultados_simulacao_sir_recife.csv`: Resultados finais das simulações para COVID-19 (doenças respiratórias) e Arbovirose.

## 🧪 Tecnologias Utilizadas

- **Python 3**
- `pandas`, `numpy`: Manipulação de dados
- `matplotlib`, `seaborn`: Visualização gráfica
- `scipy.integrate.solve_ivp`: Resolução numérica de equações diferenciais

## 📊 Etapas da Simulação

1. **Importação e limpeza dos dados**
2. **Filtragem para Recife/PE**
3. **Definição dos parâmetros epidemiológicos**
4. **Modelagem matemática com equações diferenciais**
5. **Simulação com `solve_ivp`**
6. **Visualização dos resultados**
7. **Interpretação com base em indicadores socioeconômicos**
8. **Exportação dos resultados**

## 🧠 Modelo SIR

O modelo é definido pelas equações:



\[
\frac{dS}{dt} = -\beta \frac{SI}{N}, \quad
\frac{dI}{dt} = \beta \frac{SI}{N} - \gamma I, \quad
\frac{dR}{dt} = \gamma I
\]



Onde:
- `S`: população suscetível
- `I`: população infectada
- `R`: população recuperada
- `β`: taxa de transmissão
- `γ`: taxa de recuperação
- `N`: população total

## 📍 Contexto Local

A simulação considera fatores como:
- Densidade domiciliar
- PIB per capita
- Taxa de analfabetismo

Esses dados ajudam a justificar os parâmetros epidemiológicos e interpretar os resultados de forma mais realista.

## 📈 Resultados

- Gráficos individuais para COVID-19 (doenças respiratórias) e Arbovirose
- Comparação entre os picos de infecção
- Exportação dos dados simulados para análise posterior

## 📝 Conclusão

Este projeto inicial mostra como modelos matemáticos simples podem ser combinados com dados reais para gerar insights sobre a dinâmica de doenças em contextos urbanos específicos. É uma ferramenta útil para estudos acadêmicos, planejamento de saúde pública e ensino de epidemiologia.

---

**PIC 2024-2025 UFRPE**
