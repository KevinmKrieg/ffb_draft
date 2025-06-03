import pandas as pd
import streamlit as st

from draft_app_streamlit import remove_player


def test_remove_player():
    # Prepare projections DataFrame with two players
    st.session_state.projections_data = pd.DataFrame({
        'player': ['Player A', 'Player B'],
        'position': ['QB', 'RB'],
        'team': ['Team1', 'Team2'],
        'points_vor': [100, 90],
        'ceiling_vor': [110, 95],
    })
    # Initialize position counters
    st.session_state.position_counters = {'QB': 0, 'WR': 0, 'RB': 0, 'TE': 0, 'DST': 0}

    # Remove one player
    remove_player('Player A')

    # Player should no longer be in projections_data
    assert 'Player A' not in st.session_state.projections_data['player'].values

    # QB counter should have incremented
    assert st.session_state.position_counters['QB'] == 1
