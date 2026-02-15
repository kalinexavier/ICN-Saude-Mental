import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# ESTILIZAÇÃO CSS AVANÇADA
st.markdown("""
    <style>
    /* Configuração Geral de Fontes */
    html, body, [class*="st-"] {
        font-size: 0.82rem !important;
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* FORÇAR TEXTO PRETO NA PÁGINA PRINCIPAL */
    .main .stMarkdown p, .main h1, .main h2, .main h3, .main .stWidgetLabel {
        color: #000000 !important;
    }

    .stApp { background-color: #FFFFFF; }
    
    /* CONFIGURAÇÃO DA BARRA LATERAL (ABA) */
    [data-testid="stSidebar"] { 
        background-color: #EB5E28; 
        border-radius: 0 20px 20px 0; 
    }
    
    /* Remover espaçamentos excessivos no topo da sidebar */
    [data-testid="stSidebar"] .stCustomBlock { padding-top: 1rem; }

    /* Garantir que TUDO na lateral seja branco e sem margens exageradas */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stWidgetLabel { 
        color: #FFFFFF !important;
        font-size: 0.82rem !important;
        margin-bottom: 5px !important;
    }
    
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; margin: 10px 0; }

    /* Estilo dos Cards de Indicadores (Texto Preto) */
    .card-lei, .card-portaria { 
        padding: 8px; 
        border-radius: 10px; 
        margin-bottom: 8px; 
        font-size: 0.82rem;
        color: #000000 !important;
    }
    .card-lei { background-color: #FFF5EE; border-left: 5px solid #FFB347; }
    .card-portaria { background-color: #FFFFF0; border-left: 5px solid #FFD700; }
    
    /* Estilização da Caixa de ICN */
    .res-box-clean { 
        background-color: #FFFFFF; 
        padding: 10px; 
        border-radius: 15px; 
        border: 2px solid #EB5E28; 
        text-align: center; 
        max-width: 280px; 
        margin: 10px auto; 
    }

    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (ABA) - TODO O TEXTO BRANCO
with st.sidebar:
    # Título do PTT no topo
    st.markdown("### 🏛️ Sobre o PTT")
    
    # Texto de apresentação em HTML puro para garantir a cor branca
    st.markdown("""
        <div style="color: white; text-align: justify; font-size: 0.82rem; margin-bottom: 10px;">
            Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada 
            <b>"A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho"</b>, 
            do Mestrado Profissional em Gestão Pública da UFPE.
            <br><br>
            Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: 
            <b>Lei Nº 14.831/2024</b> e <b>Portaria SRH/MP Nº 1.261/2010</b> (SIPEC).
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.markdown("""
        <ul style="color: white; font-size: 0.82rem; padding-left: 15px;">
            <li>Marque os itens atendidos.</li>
            <li>Descreva a Evidência ou o Plano de Ação.</li>
            <li>Clique em Gerar Relatório ao final.</li>
        </ul>
    """, unsafe_allow_html=True)

    # ALERTA ÉTICO (FUNDO BRANCO / LETRA LARANJA)
    st.markdown("""
        <div style="background-color: white; padding: 10px; border-radius: 8px; text-align: left; margin-top: 5px;">
            <span style="color: #EB5E28 !important; font-weight: bold; font-size: 0.72rem; line-height: 1.2;">
                ⚠️ O instrumento serve como termômetro, mas a saúde mental é um tema sério e deve ser tratado com responsabilidade.
            </span>
        </div>
    """, unsafe_allow_html=True)

# 3. PÁGINA PRINCIPAL (TEXTOS PRETOS)
st.markdown("<h1>Índice de Conformidade às Normativas Federais</h1>", unsafe_allow_html=True)

c_id1, c_id2 = st.columns(2)
with c_id1:
    nome_inst = st.text_input("🏢 Nome da Instituição/Unidade:", placeholder="Ex: UFPE - Progepe")
with c_id2:
    contato_resp = st.text_input("📧 Contato do Responsável:", placeholder="Ex: gestor@ufpe.br")

st.write("---")

# 4. INDICADORES (Lembre-se de manter suas frases originais aqui)
lei_grupos = {
    "Grupo I - Promoção da saúde mental": ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"],
    "Grupo II - Bem-estar dos trabalhadores": ["L9", "L10", "L11", "L12", "L13", "L14"],
    "Grupo III - Transparência e prestação de contas": ["L15", "L16", "L17"]
}

respostas_excel = []
def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        # Checkbox e Input com labels que agora serão pretos via CSS
        check = st.checkbox(f"**{tag}**", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}", placeholder="Digite aqui...")
        respostas_excel.append({"ID": tag, "Conformidade": "Sim" if check else "Não", "Detalhes": det})
        return 1 if check else 0

col_l, col_p = st.columns(2)
with col_l:
    st.markdown("## 🏛️ Lei 14.831/2024")
    idx = 1
    scores_l = []
    for g, itens in lei_grupos.items():
        st.markdown(f"### {g}")
        s = sum([render_item(f"L{idx+i}", f"Indicador {idx+i}", "Lei 14.831", "card-lei") for i, _ in enumerate(itens)])
        scores_l.append(s / len(itens))
        idx += len(itens)
    icl = sum(scores_l) / 3

with col_p:
    st.markdown("## 📋 Portaria 1.261/2010")
    icp = sum([render_item(f"P{i+18}", f"Indicador P{i+18}", "Portaria 1.261", "card-portaria") for i in range(18)]) / 18

# 5. RESULTADOS E GRÁFICOS
st.write("---")
icn = (icl + icp) / 2
g1, g2, g3 = st.columns(3)

# Configuração comum de títulos centralizados para os gráficos
layout_charts = {'x':0.5, 'xanchor': 'center', 'font': {'color': 'black'}}

with g1:
    fig1 = go.Figure(go.Bar(x=['G-I', 'G-II', 'G-III', 'ICL'], y=scores_l + [icl], marker_color='#FFB347', text=[f"{v:.2f}" for v in scores_l + [icl]], textposition='auto'))
    fig1.update_layout(title={'text': "Conformidade à Lei 14.831", **layout_charts}, yaxis=dict(range=[0, 1.1]), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    fig2 = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFD700', text=[f"{icp:.2f}"], textposition='auto'))
    fig2.update_layout(title={'text': "Conformidade à Portaria 1.261", **layout_charts}, yaxis=dict(range=[0, 1.1]), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

with g3:
    fig3 = go.Figure(go.Bar(x=['Geral (ICN)'], y=[icn], marker_color='#EB5E28', text=[f"{icn:.2f}"], textposition='auto'))
    fig3.update_layout(title={'text': "Conformidade Geral (ICN)", **layout_charts}, yaxis=dict(range=[0, 1.1]), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)

# CAIXA ICN E BOTÃO
st.markdown(f"""
    <div class='res-box-clean'>
        <p style='color: #000; font-weight: bold; margin-bottom: 2px; font-size: 0.85rem;'>Índice Geral de Conformidade</p>
        <h1 style='font-size: 2.5rem !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1>
    </div>
""", unsafe_allow_html=True)

output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    pd.DataFrame(respostas_excel).to_excel(writer, index=False)

st.download_button("📥 Gerar Relatório Profissional (Excel)", data=output.getvalue(), file_name=f"ICN_{nome_inst}.xlsx", type="primary", use_container_width=True)

# 7. RODAPÉ
st.markdown(f"<p style='text-align: center; color: black; font-size: 0.75rem; margin-top:20px;'>Sistema idealizado por Kaline Xavier | Orientador: Denilson Marques<br>Mestrado Profissional em Gestão Pública - UFPE</p>", unsafe_allow_html=True)
