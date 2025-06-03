import streamlit as st
import pandas as pd

# Initialize a rerun flag if not already in session state
if 'need_rerun' not in st.session_state:
    st.session_state.need_rerun = False

# Load projections data if not already in session state
if 'projections_data' not in st.session_state:
    file_path = "2023_season_projections.csv"
    st.session_state.projections_data = pd.read_csv(file_path)

# Initialize search query if not already in session state
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Initialize counters for positions if not already in session state
if 'position_counters' not in st.session_state:
    st.session_state.position_counters = {'QB': 0, 'WR': 0, 'RB': 0, 'TE': 0, 'DST': 0}

def display_top_players(position_filter=None):
    filtered_data = st.session_state.projections_data if position_filter == 'All' else st.session_state.projections_data[st.session_state.projections_data['position'] == position_filter]
    top_players = filtered_data.nlargest(20, 'ceiling_vor')
    columns_to_display = ['player', 'position', 'team', 'points_vor', 'ceiling_vor']
    return top_players[columns_to_display]

def remove_player(player_name):
    player_row = st.session_state.projections_data[st.session_state.projections_data['player'] == player_name]
    if not player_row.empty:
        position = player_row.iloc[0]['position']
        st.session_state.position_counters[position] += 1
        st.session_state.projections_data = st.session_state.projections_data[st.session_state.projections_data['player'] != player_name]
        return f"Player '{player_name}' has been removed."
    else:
        return f"Player '{player_name}' not found."




# Title and instructions
st.title('Fantasy Football Draft App')
st.write('Select a position or click on a player to remove them. Leave blank to reset.')

# Dropdown for position selection
#position = st.selectbox('Select Position:', ['', 'RB', 'QB', 'WR', 'TE', 'DST'], key='position')

# Create columns for position filter and search bar
cols = st.columns(2)

# Position filter in the first column
position = cols[1].selectbox('Select Position:', ['All', 'RB', 'QB', 'WR', 'TE', 'DST'], key='position')

# Text input for searching players, using session state, in the second column
st.session_state.search_query = cols[0].text_input('Search Player:', value=st.session_state.search_query, key='search_player')


# Filter players based on the search input
if st.session_state.search_query:
    matching_players = st.session_state.projections_data[st.session_state.projections_data['player'].str.contains(st.session_state.search_query, case=False, na=False)]
    # Display buttons for each matching player
    for index, row in matching_players.iterrows():
        player_info = f"{row['player']} - {row['position']} - {row['team']} - Points VOR: {row['points_vor']} - Ceiling VOR: {row['ceiling_vor']}"
        if st.button(player_info):
            message = remove_player(row['player'])
            st.write(message)
            st.session_state.search_query = ""
            st.session_state.need_rerun = True

# Check the rerun flag and rerun the app if needed
if st.session_state.need_rerun:
    st.session_state.need_rerun = False
    st.experimental_rerun()

# Display the top 20 players based on the current filter
top_players = display_top_players(position if position else None)

# Define color mapping using emojis
color_mapping = {
    'QB': '🟥', # Red square
    'WR': '🟩', # Green square
    'RB': '🟦', # Blue square
    'TE': '🟧', # Orange square
    'DST': '🟪', # Purple square
}

st.sidebar.write('Players Taken by Position:')
for position, count in st.session_state.position_counters.items():
    st.sidebar.write(f"{position}: {count}")

# Create buttons for each player, including colored square
for index, row in top_players.iterrows():
    color_emoji = color_mapping.get(row['position'], '⬛') # Default to black square
    player_info = f"{color_emoji} {row['player']} - {row['team']} - Points VOR: {row['points_vor']} - Ceiling VOR: {row['ceiling_vor']}"
    if st.button(player_info):
        message = remove_player(row['player'])
        st.write(message)
        # Refresh the app to display the updated top 10 players
        #st.experimental_rerun()
        st.session_state.search_query = ""
        st.session_state.need_rerun = True

# Check the rerun flag and rerun the app if needed
if st.session_state.need_rerun:
    st.session_state.need_rerun = False
    st.experimental_rerun()

# Button to quit the app
if st.button('Quit'):
    st.write('Good luck with your draft!')