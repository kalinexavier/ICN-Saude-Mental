import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

# 1. Configuração da Página
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# Estilização CSS
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #EB5E28; border-radius: 0 25px 25px 0; margin: 10px 0; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; }
    .card-lei { background-color: #FFF5EE; padding: 15px; border-radius: 12px; border-left: 6px solid #FFB347; margin-bottom: 12px; }
    .card-portaria { background-color: #FFFFF0; padding: 15px; border-radius: 12px; border-left: 6px solid #FFD700; margin-bottom: 12px; }
    .badge-norma { color: #555; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; display: inline-block; }
    h1 { color: #252422; font-weight: 800; text-align: center; }
    .res-box-clean { background-color: #FFFFFF; padding: 25px; border-radius: 20px; border: 2px solid #FFFFFF; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 10px !important; padding: 15px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Barra Lateral
with st.sidebar:
    st.markdown("### ℹ️ Sobre o PTT")
    st.write("Produto resultante da dissertação de Mestrado Profissional em Gestão Pública da UFPE.")
    st.write("Mensure a aderência institucional à Lei Nº 14.831/2024 e à Portaria SRH/MP Nº 1.261/2010.")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.write("1. Marque os itens atendidos.")
    st.write("2. Descreva evidências ou planos de ação.")

st.title("Índice de Conformidade às Normativas Federais de Saúde Mental")

# 3. Dados dos Indicadores
lei_txt = ["implementação de programas de promoção da saúde mental no ambiente de trabalho", "oferta de acesso a recursos de apoio psicológico e psiquiátrico para seus trabalhadores", "promoção da conscientização sobre a importância da saúde mental (campanhas/treinamentos)", "promoção da conscientização direcionada à saúde mental da mulher", "capacitação de lideranças", "realização de treinamentos específicos em temas de saúde mental de maior interesse dos trabalhadores", "combate à discriminação e ao assédio em todas as suas formas", "avaliação e acompanhamento regular das ações implementadas e seus ajustes", "promoção de ambiente de trabalho seguro e saudável", "incentivo ao equilíbrio entre a vida pessoal e a profissional", "incentivo à prática de atividades físicas e de lazer", "incentivo à alimentação saudável", "incentivo à interação saudável no ambiente de trabalho", "incentivo à comunicação integrativa", "divulgação regular das ações e das políticas de promoção da saúde mental", "manutenção de canal para recebimento de sugestões e de avaliações", "promoção do desenvolvimento de metas e análises periódicas dos resultados"]
port_txt = ["promover ações que mantenham e fortaleçam vínculos e redes de apoio", "realizar programas e ações fundamentados em informações epidemiológicas", "realizar as ações de promoção inclusivas e combate ao estigma", "promover a concepção ampliada de saúde mental", "planejar ações de promoção ao desenvolvimento humano e educação para vida saudável", "ampliar a divulgação e integração dos serviços de saúde mental da rede pública", "detectar precocemente, acolher e monitorar o tratamento", "realizar ações para combater o estigma e apoiar associações", "estabelecer e registrar nexo causal entre trabalho e transtornos mentais", "identificar fatores de adoecimento e propor intervenção na organização", "intervir em conflitos buscando soluções mediadas", "oferecer suporte ao desenvolvimento das competências e habilidades do servidor", "disponibilizar espaços terapêuticos integrados à Política de Atenção", "garantir a realização das atividades de promoção à saúde no horário de trabalho", "incentivar na Administração Pública Federal a implantação de Programas de Preparação à Aposentadoria (PPA)", "identificar situações de trabalho penosas e propor intervenções", "privilegiar programas de promoção da qualidade de vida como fator de proteção", "capacitar os gestores para identificar sofrimento psíquico no trabalho"]

respostas_excel = []

def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**: {texto}", key=f"cb_{tag}")
        det = st.text_input("Plano de Ação/Evidências:", key=f"t_{tag}")
        status = "Sim" if check else "Não"
        respostas_excel.append({"ID": tag, "Indicador": texto, "Conformidade": status, "Plano de Ação/Evidências": det})
        return 1 if check else 0

col_lei, col_port = st.columns(2)
with col_lei:
    st.subheader("🏛️ Lei 14.831/2024")
    count_lei = sum([render_item(f"L{i+1}", txt, "Lei 14.831", "card-lei") for i, txt in enumerate(lei_txt)])
with col_port:
    st.subheader("📋 Portaria 1.261/2010")
    count_port = sum([render_item(f"P{i+18}", txt, "Portaria 1.261", "card-portaria") for i, txt in enumerate(port_txt)])

# 4. Resultados
st.write("---")
icl, icp = count_lei/17, count_port/18
icn = (icl + icp) / 2

c_graf, c_res = st.columns([1.5, 1])
with c_graf:
    fig = go.Figure(go.Bar(
        x=['Lei (ICL)', 'Portaria (ICP)', 'Geral (ICN)'],
        y=[icl, icp, icn],
        marker_color=['#FFB347', '#FFF9A6', '#EB5E28'],
        text=[f"{icl:.2f}", f"{icp:.2f}", f"{icn:.2f}"], textposition='auto'
    ))
    fig.update_layout(yaxis=dict(range=[0, 1.1]), height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with c_res:
    st.markdown(f"""
        <div class='res-box-clean'>
            <p style='color: #444; font-weight: bold; font-size: 1.2rem;'>Índice de Conformidade Geral</p>
            <h1 style='font-size: 75px !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1>
            <p style='font-size: 0.95rem; color: #666;'>Quanto mais próximo de <b>1.00</b>, maior o atendimento às normativas federais de saúde mental.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # GERAÇÃO DO EXCEL REFINADO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Estilos do Excel
        header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#EB5E28', 'border': 1, 'align': 'center'})
        base_fmt = workbook.add_format({'align': 'left', 'valign': 'vcenter'})
        value_fmt = workbook.add_format({'align': 'center', 'bold': True})
        icn_highlight = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#EB5E28', 'align': 'center'})
        orange_light_fmt = workbook.add_format({'bg_color': '#FFD580', 'font_color': '#000000'}) # Laranja claro para o "Não"
        white_fmt = workbook.add_format({'bg_color': '#FFFFFF'}) # Branco para o "Sim"

        # ABA 1: RESUMO DE ÍNDICES
        worksheet_res = workbook.add_worksheet('Resumo de Índices')
        worksheet_res.write(0, 0, 'Métrica', header_fmt)
        worksheet_res.write(0, 1, 'Resultado', header_fmt)
        
        worksheet_res.write(1, 0, 'Índice de Conformidade à Lei (ICL)', base_fmt)
        worksheet_res.write(1, 1, f"{icl:.2f}", value_fmt)
        worksheet_res.write(2, 0, 'Índice de Conformidade à Portaria (ICP)', base_fmt)
        worksheet_res.write(2, 1, f"{icp:.2f}", value_fmt)
        
        # Pular linha para o ICN
        worksheet_res.write(4, 0, 'Índice de Conformidade Geral (ICN)', workbook.add_format({'bold': True, 'bg_color': '#F0F0F0'}))
        worksheet_res.write(4, 1, f"{icn:.2f}", icn_highlight)
        
        worksheet_res.set_column('A:A', 45)
        worksheet_res.set_column('B:B', 15)

        # ABA 2: DIAGNÓSTICO DETALHADO
        df_detalhes = pd.DataFrame(respostas_excel)
        df_detalhes.to_excel(writer, sheet_name='Diagnóstico Detalhado', index=False)
        worksheet_det = writer.sheets['Diagnóstico Detalhado']
        
        for col_num, value in enumerate(df_detalhes.columns.values):
            worksheet_det.write(0, col_num, value, header_fmt)
            
        worksheet_det.set_column('A:A', 5)  # ID
        worksheet_det.set_column('B:B', 70) # Indicador
        worksheet_det.set_column('C:C', 15) # Conformidade
        worksheet_det.set_column('D:D', 70) # Plano/Evidência
        
        # Formatação Condicional na coluna C (Conformidade)
        worksheet_det.conditional_format('C2:C36', {'type': 'cell', 'criteria': '==', 'value': '"Sim"', 'format': white_fmt})
        worksheet_det.conditional_format('C2:C36', {'type': 'cell', 'criteria': '==', 'value': '"Não"', 'format': orange_light_fmt})

    st.write("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Baixar Relatório Profissional (Excel)",
        data=output.getvalue(),
        file_name="ICN_Saude_Mental_UFPE.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True, type="primary"
    )

st.write("---")
st.markdown(f"<p style='text-align:center; color: #888;'>Autora: Kaline Xavier | Contato: kaline.xavier@ufpe.br<br>Mestrado Profissional em Gestão Pública | UFPE</p>", unsafe_allow_html=True)