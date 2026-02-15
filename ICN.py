import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# CONEXÃO COM GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# ESTILIZAÇÃO CSS
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 0.82rem !important;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .main .stMarkdown p, .main h1, .main h2, .main h3, .main .stWidgetLabel {
        color: #000000 !important;
    }
    .stApp { background-color: #FFFFFF; }
    
    /* REMOVE ESPAÇO NO TOPO DA BARRA LATERAL */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebar"] { 
        background-color: #EB5E28; 
        border-radius: 0 20px 20px 0; 
    }
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stWidgetLabel { 
        color: #FFFFFF !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; margin: 10px 0; }
    
    /* CARDS MAIS FINOS */
    .card-lei, .card-portaria { 
        padding: 5px 10px; border-radius: 6px; margin-bottom: 4px; font-size: 0.82rem; color: #000000 !important;
    }
    .card-lei { background-color: #FFF5EE; border-left: 3px solid #FFB347; }
    .card-portaria { background-color: #FFFFF0; border-left: 3px solid #FFD700; }
    
    .res-box-clean { 
        background-color: #FFFFFF; padding: 10px; border-radius: 15px; border: 2px solid #EB5E28; 
        text-align: center; max-width: 280px; margin: 15px auto; 
    }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (Iniciando no topo)
with st.sidebar:
    st.markdown("### 🏛️ Sobre o PTT")
    st.markdown("""
        <div style="color: white; text-align: justify; font-size: 0.82rem; margin-bottom: 10px;">
            Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada 
            <b>"A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho"</b>, 
            do Mestrado Profissional em Gestão Pública para o Desenvolvimento Do Nordeste - CCSA da UFPE.
            <br><br>
            Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: 
            <b>Lei Nº 14.831/2024</b> e à <b>Portaria SRH/MP Nº 1.261/2010</b>.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.markdown("""
        <div style="color: white; font-size: 0.82rem;">
            1. Marque os itens atendidos.<br><br>
            2. Descreva a <b>Evidência</b> ou o <b>Plano de Ação</b>.<br><br>
            3. Clique em gerar Relatório para salvar e baixar.
        </div>
    """, unsafe_allow_html=True)

# 3. PÁGINA PRINCIPAL
st.markdown("<h1>Índice de Conformidade às Normativas Federais de Saúde Mental</h1>", unsafe_allow_html=True)
c_id1, c_id2 = st.columns(2)
with c_id1:
    nome_inst = st.text_input("🏢 Nome da Instituição/Unidade:", placeholder="Ex: UFPE - Progepe")
with c_id2:
    contato_resp = st.text_input("📧 Contato do Responsável:", placeholder="Ex: gestor@ufpe.br")

st.write("---")

# 4. DICIONÁRIOS COMPLETOS (MANTIDOS)
lei_grupos = {
    "Grupo I - Promoção da saúde mental": [
        "implementação de programas de promoção da saúde mental no ambiente de trabalho",
        "oferta de acesso a recursos de apoio psicológico e psiquiátrico para seus trabalhadores",
        "promover a conscientização sobre a importância da saúde mental (campanhas e treinamentos)",
        "promoção da conscientização direcionada à saúde mental da mulher",
        "capacitação de lideranças",
        "treinamentos específicos que abordem temas de saúde mental de interesse dos trabalhadores",
        "combate à discriminação e ao assédio em todas as suas formas",
        "avaliação e acompanhamento regular das ações implementadas e seus ajustes"
    ],
    "Grupo II - Bem-estar dos trabalhadores": [
        "promoção de ambiente de trabalho seguro e saudável",
        "incentivo ao equilíbrio entre a vida pessoal e a profissional",
        "incentivo à prática de atividades físicas e de lazer",
        "incentivo à alimentação saudável",
        "incentivo à interação saudável no ambiente de trabalho",
        "incentivo à comunicação integrativa"
    ],
    "Grupo III - Transparência e prestação de contas": [
        "divulgação regular das ações e das políticas relacionadas à saúde mental nos meios de comunicação",
        "manutenção de canal para recebimento de sugestões e de avaliações",
        "desenvolvimento de metas e análises periódicas dos resultados das ações de saúde mental"
    ]
}

port_txt = [
    "Fortalecer vínculos entre servidores em sofrimento psíquico, familiares e trabalho",
    "Programas fundamentados em informações epidemiológicas",
    "Ações inclusivas (gênero, raça, orientação sexual, idade) contra o estigma",
    "Concepção ampliada de saúde mental (física e bem-estar socioeconômico)",
    "Educação para vida saudável e acesso a bens culturais",
    "Divulgação e integração dos serviços de saúde mental da rede pública/APF",
    "Detecção precoce, acolhimento e monitoramento do tratamento",
    "Orientação aos trabalhadores para combater o estigma dos transtornos mentais",
    "Registrar nexo causal entre processos de trabalho e transtornos mentais",
    "Mapear fatores de adoecimento e propor intervenção na organização do trabalho",
    "Intervir em conflitos no trabalho buscando soluções dialogadas e éticas",
    "Suporte ao desenvolvimento de competências e projetos de vida do servidor",
    "Disponibilizar espaços terapêuticos integrados à Política de Atenção à Saúde",
    "Garantir atividades de promoção à saúde no horário de trabalho",
    "Implantação de Programas de Preparação à Aposentadoria - PPA",
    "Identificar e intervir em situações de trabalho penosas mentalmente",
    "Programas de qualidade de vida para reduzir recorrência de crises",
    "Capacitar gestores para identificar sofrimento psíquico no trabalho"
]

respostas_excel = []

def render_item(tag, texto, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**: {texto}", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}", placeholder="Detalhe aqui...", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        respostas_excel.append({"ID": tag, "Indicador": texto, "Conformidade": "Sim" if check else "Não", "Detalhes": det})
        return 1 if check else 0

# 5. COLUNAS E DIVISÕES
col_l, col_p = st.columns(2)

with col_l:
    st.markdown("## 🏛️ Lei 14.831/2024")
    idx_l, scores_l = 1, []
    # Usando enumerate para identificar o último grupo e não colocar divisor no fim
    for i, (g, itens) in enumerate(lei_grupos.items()):
        st.markdown(f"#### {g}")
        s = sum([render_item(f"L{idx_l+j}", txt, "card-lei") for j, txt in enumerate(itens)])
        scores_l.append(s / len(itens))
        idx_l += len(itens)
        if i < len(lei_grupos) - 1: # Só coloca divisor se não for o último grupo
            st.divider()
    icl = sum(scores_l) / 3

with col_p:
    st.markdown("## 📋 Portaria 1.261/2010")
    icp = sum([render_item(f"P{i+18}", txt, "card-portaria") for i, txt in enumerate(port_txt)]) / 18

# 6. RESULTADOS E GRÁFICOS (MANTIDOS)
st.write("---")
icn = (icl + icp) / 2
g1, g2, g3 = st.columns(3)
layout_c = {'x':0.5, 'xanchor': 'center', 'font': {'color': 'black'}}

with g1:
    f1 = go.Figure(go.Bar(x=['G-I', 'G-II', 'G-III', 'ICL'], y=scores_l + [icl], marker_color='#FFB347', text=[f"{v:.2f}" for v in scores_l + [icl]], textposition='auto'))
    f1.update_layout(title={'text': "Conformidade à Lei 14.831", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f1, use_container_width=True)

with g2:
    f2 = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFD700', text=[f"{icp:.2f}"], textposition='auto'))
    f2.update_layout(title={'text': "Conformidade à Portaria 1.261", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f2, use_container_width=True)

with g3:
    f3 = go.Figure(go.Bar(x=['Geral (ICN)'], y=[icn], marker_color='#EB5E28', text=[f"{icn:.2f}"], textposition='auto'))
    f3.update_layout(title={'text': "Conformidade Geral (ICN)", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f3, use_container_width=True)

st.markdown(f"<div class='res-box-clean'><p style='color: #000; font-weight: bold; margin-bottom: 2px; font-size: 0.85rem;'>Índice Geral de Conformidade</p><h1 style='font-size: 2.5rem !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1></div>", unsafe_allow_html=True)

# 7. EXPORTAÇÃO E SALVAMENTO (LOGICA DE SUCESSO MANTIDA)
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    pd.DataFrame(respostas_excel).to_excel(writer, index=False)

if st.download_button("📥 Gerar Relatório Profissional (Excel)", 
                      data=output.getvalue(), 
                      file_name=f"ICN_{nome_inst}.xlsx", 
                      type="primary", 
                      use_container_width=True):
    try:
        url_planilha = st.secrets["connections"]["gsheets"]["spreadsheet"]
        nova_linha = pd.DataFrame([{
            "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            "Instituicao": str(nome_inst),
            "Contato": str(contato_resp),
            "ICL": round(icl, 2),
            "ICP": round(icp, 2),
            "ICN": round(icn, 2)
        }])
        # ttl=0 garante que ele não pule linhas na planilha
        existentes = conn.read(spreadsheet=url_planilha, worksheet="Página1", ttl=0)
        df_final = pd.concat([existentes, nova_linha], ignore_index=True) if existentes is not None else nova_linha
        conn.update(spreadsheet=url_planilha, worksheet="Página1", data=df_final)
        st.success("✅ Diagnóstico registrado com sucesso no banco de dados da UFPE!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# RODAPÉ
st.write("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align: center; color: #444; font-size: 0.82rem; line-height: 1.6;'>
        <p><b>Sistema idealizado por Kaline Mirele Silva Xavier sob Orientação do docente Denilson Bezerra Marques.</b><br>
        Mestrado Profissional em Gestão Pública | UFPE</p>
    </div>
""", unsafe_allow_html=True)
