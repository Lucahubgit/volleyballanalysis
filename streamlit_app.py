import streamlit as st
import pandas as pd
import glob

# Titolo dell'app
st.title("Stats")

# Trova tutti i file Excel (.xlsx) nella directory corrente
excel_files = glob.glob("*.xlsx")

if excel_files:
    st.sidebar.header("File Excel trovati")
    st.sidebar.write(excel_files)

    total_our_score = 0
    total_opp_score = 0
    fault_count = 0
    team_point_count = 0
    team_error_count = 0
    opponent_error_count = 0
    opponent_point_count = 0
    card_count = 0

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
                total_our_score += df['our_score'].iloc[-1]
                total_opp_score += df['opp_score'].iloc[-1]

            # Conta i parametri della colonna point_type
            if 'point_type' in df.columns:
                fault_count += df['point_type'].str.count("Fault").sum()
                team_point_count += df['point_type'].str.count("Team point").sum()
                team_error_count += df['point_type'].str.count("Team error").sum()
                opponent_error_count += df['point_type'].str.count("Opponent error").sum()
                opponent_point_count += df['point_type'].str.count("Opponent point").sum()
                card_count += df['point_type'].str.count("Card").sum()

            # Analizza i dati per ogni giocatore
            if 'player' in df.columns and 'score' in df.columns:
                for _, row in df.iterrows():
                    player = row['player']
                    score = row['score']

                    # Ignora i valori NaN nella colonna player
                    if pd.isna(player):
                        continue

                    if player not in player_stats:
                        player_stats[player] = {'Point scored': 0, 'Point lost': 0}

                    if score == "Point scored":
                        player_stats[player]['Point scored'] += 1
                    elif score == "Point lost":
                        player_stats[player]['Point lost'] += 1

    # Mostra i risultati generali
    st.write(f"Total scored points: {int(total_our_score)}")
    st.write(f"Total lost points: {int(total_opp_score)}")
    st.write(f"Fault number: {int(fault_count)}")
    st.write(f"Total team points: {int(team_point_count)}")
    st.write(f"Total team errors: {int(team_error_count)}")
    st.write(f"Total opponent errors: {int(opponent_error_count)}")
    st.write(f"Total opponent points: {int(opponent_point_count)}")
    st.write(f"Card number: {int(card_count)}")

    # Mostra i risultati per giocatore
    st.subheader("Stats per player")
    for player, stats in player_stats.items():
        st.write(f"Points {player}: +{int(stats['Point scored'])}; -{int(stats['Point lost'])}")
else:
    st.error("No Excel file (.xlsx) find in the current directory")