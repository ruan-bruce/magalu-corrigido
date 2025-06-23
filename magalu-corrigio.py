import streamlit as st
import pandas as pd

estados = {
    "SP": 20, "RJ": 25, "MG": 25, "ES": 25,
    "PR": 30, "SC": 30, "RS": 30,
    "BA": 35, "SE": 35, "AL": 35, "PE": 35,
    "CE": 45, "RN": 45, "PB": 45,
    "MA": 50, "PI": 50,
    "DF": 40, "GO": 40, "MT": 40, "MS": 40,
    "AM": 60, "PA": 60, "RO": 60, "AC": 60, "RR": 60, "AP": 60, "TO": 50
}

comissao_magalu = 0.18
tarifa_fixa = 5.00

def calcular_preco_minimo(custo, frete, margem_desejada):
    # Agora a margem é sobre o custo do produto
    margem_valor = custo * (margem_desejada / 100)
    denominador = 1 - comissao_magalu
    preco_min = (custo + frete + tarifa_fixa + margem_valor) / denominador
    return round(preco_min, 2)

def gerar_tabela(custo, margem):
    dados = []
    for estado, frete in estados.items():
        preco_min = calcular_preco_minimo(custo, frete, margem)
        comissao = preco_min * comissao_magalu
        lucro = preco_min - comissao - tarifa_fixa - frete - custo
        margem_liq = (lucro / custo) * 100  # Margem em relação ao custo
        dados.append({
            "Estado": estado,
            "Frete (R$)": frete,
            "Preço Mínimo (R$)": preco_min,
            "Comissão (R$)": round(comissao, 2),
            "Lucro Líquido (R$)": round(lucro, 2),
            "Margem sobre Custo (%)": round(margem_liq, 2)
        })
    return pd.DataFrame(dados)

def main():
    st.title("Calculadora de Preço Mínimo - Magalu DSLite")

    custo = st.number_input("Custo do Produto (R$):", min_value=0.01, value=53.17)
    margem = st.slider("Margem Desejada sobre o Custo (%):", min_value=1, max_value=100, value=30)
    estado = st.selectbox("Estado de Destino:", list(estados.keys()))

    preco_min = calcular_preco_minimo(custo, estados[estado], margem)

    st.write(f"### Preço Mínimo para {estado}: R$ {preco_min}")

    df = gerar_tabela(custo, margem)
    st.dataframe(df)

if __name__ == "__main__":
    main()
