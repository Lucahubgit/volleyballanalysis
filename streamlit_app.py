import streamlit as st
import pandas as pd
import glob

# NON POSSIAMO CALCOLARE: numero di partite giocate, numero di set giocati, efficienza, 

# Titolo dell'app
st.title("Game stats")

# Trova tutti i file Excel (.xlsx) nella directory corrente
excel_files = glob.glob("*.xlsx")

if excel_files:
    st.sidebar.header("File Excel trovati")
    st.sidebar.write(excel_files)

    # Opzione per scegliere tra statistiche cumulative o per singola partita
    mode = st.sidebar.radio("Seleziona la modalità:", ["Cumulative stats", "Single match stats"])

    if mode == "Single match stats":
        # Seleziona un file specifico
        selected_file = st.sidebar.selectbox("Seleziona un file Excel:", excel_files)
        excel_files = [selected_file]  # Considera solo il file selezionato

    total_our_score = 0
    total_opp_score = 0
    fault_count = 0
    team_point_count = 0
    team_error_count = 0
    opp_error_count = 0
    opp_point_count = 0
    card_count = 0
    unknown_count = 0

    # Dizionario per memorizzare i dati per ogni giocatore
    player_stats = {}

    for file_name in excel_files:
        # Legge tutti i fogli del file Excel
        excel_data = pd.ExcelFile(file_name)
        sheet_names = excel_data.sheet_names

        for sheet_name in sheet_names:
            # Legge il foglio corrente
            df = pd.read_excel(file_name, sheet_name=sheet_name)

            # Conta punti persi e guadagnati
            if 'our_score' in df.columns and 'opp_score' in df.columns:
                if not df.empty and not df['our_score'].isna().all() and not df['opp_score'].isna().all():
                    total_our_score += df['our_score'].iloc[-1]
                    total_opp_score += df['opp_score'].iloc[-1]

            # Conta i parametri della colonna point_type
            if 'point_type' in df.columns:
                fault_count += df['point_type'].str.count("foul").sum()
                team_point_count += df['point_type'].str.count("team point").sum()
                team_error_count += df['point_type'].str.count("team error").sum()
                opp_error_count += df['point_type'].str.count("opp error").sum()
                opp_point_count += df['point_type'].str.count("opp point").sum()
                card_count += df['point_type'].str.count("card").sum()
                unknown_count += df['point_type'].str.count("unknown").sum()

            # Analizza i dati per ogni giocatore
            if 'player' in df.columns and 'score' in df.columns:
                for _, row in df.iterrows():
                    player = row['player']
                    score = row['score']
                    serve_zone = row['serve_zone'] if 'serve_zone' in df.columns else None
                    attack_zone = row['attack_zone'] if 'attack_zone' in df.columns else None
                    block_zone = row['block_zone'] if 'block_zone' in df.columns else None

                    # Ignora i valori NaN nella colonna player
                    if pd.isna(player):
                        continue

                    if player not in player_stats:
                        player_stats[player] = {'S': 0, 'L': 0, 'Ace': 0, 'Attack point': 0, 'Block': 0}  # Inizializza anche il contatore dei muri

                    if score == "S":
                        player_stats[player]['S'] += 1
                        # Controlla se è un ace
                        if serve_zone and not pd.isna(serve_zone):
                            player_stats[player]['Ace'] += 1
                        # Controlla se è un punto attacco
                        if attack_zone and not pd.isna(attack_zone):
                            player_stats[player]['Attack point'] += 1
                        # Controlla se è un muro
                        if block_zone and not pd.isna(block_zone):
                            player_stats[player]['Block'] += 1
                    elif score == "L":
                        player_stats[player]['L'] += 1

    # Mostra i risultati generali
    st.write(f"Total scored points: {int(total_our_score)}")
    st.write(f"Total lost points: {int(total_opp_score)}")
    st.write(f"Fault number: {int(fault_count)}")
    st.write(f"Total team points: {int(team_point_count)}")
    st.write(f"Total team errors: {int(team_error_count)}")
    st.write(f"Total opponent errors: {int(opp_error_count)}")
    st.write(f"Total opponent points: {int(opp_point_count)}")
    st.write(f"Total card: {int(card_count)}")
    st.write(f"Total unknown: {int(unknown_count)}")

 # Mostra i risultati per giocatore
    st.subheader("Stats per player")
    for player, stats in player_stats.items():
        st.markdown(f"""
        **Player:** {player}  
        - **Points scored:** +{int(stats['S'])}  
        - **Points lost:** -{int(stats['L'])}  
        - **Aces:** {int(stats['Ace'])}  
        - **Attack points:** {int(stats['Attack point'])}  
        - **Blocks:** {int(stats['Block'])}
        """)
else:
    st.error("No Excel file (.xlsx) found in the current directory")