
import streamlit as st
import pandas as pd
from data import get_monitor_data
from storage import load_metadata, save_metadata, load_settings, save_settings

st.set_page_config(page_title="US Stock Monitor", layout="wide", initial_sidebar_state="collapsed")

# Load settings for column order
if 'settings' not in st.session_state:
    st.session_state['settings'] = load_settings()

DEFAULT_COL_ORDER = [
    "Ticker", "Name", "Overall Rank", "YTD Performance (%)", "5-Day Performance (%)",
    "Turnover Ratio", "Avg Daily Turnover (20d)", "Themes",
    "GICS Sub-Industry", "GICS Industry", "GICS Sector",
    "Rank YTD%", "Rank 5D%", "Rank Turnover Ratio", "Rank 20d Vol",
    "Current Price", "Latest Turnover"
]

if 'col_order' not in st.session_state:
    st.session_state['col_order'] = st.session_state['settings'].get('column_order', DEFAULT_COL_ORDER)

st.title("📱 US Stock Monitor - Cloud")
st.caption("Lightweight version for mobile access and quick scans")

st.markdown("""
**Quick Scan**: Run a fresh scan to analyze all S&P 500 stocks. Themes and settings are saved for your session.
""")

col1, col2 = st.columns([1, 4])
with col1:
    run_btn = st.button("🚀 Run Scan", type="primary")

if 'stock_data' not in st.session_state:
    st.session_state['stock_data'] = pd.DataFrame()

if 'edited_data' not in st.session_state:
    st.session_state['edited_data'] = pd.DataFrame()

if run_btn:
    with st.spinner("🔄 Fetching market data... This may take 1-2 minutes."):
        try:
            df = get_monitor_data(force_refresh_metadata=False)
            
            # Apply current column order if available
            _cols = [c for c in st.session_state['col_order'] if c in df.columns]
            _other = [c for c in df.columns if c not in _cols]
            df = df[_cols + _other]
            
            st.session_state['stock_data'] = df
            st.session_state['edited_data'] = df.copy()
            st.success(f"✅ Scan complete! Found {len(df)} stocks.")
        except Exception as e:
            st.error(f"❌ Error fetching data: {str(e)}")
            st.info("💡 This might be the first run. The app will fetch fresh data from Yahoo Finance (this takes 2-3 minutes).")
            # Try with force refresh
            try:
                df = get_monitor_data(force_refresh_metadata=True)
                _cols = [c for c in st.session_state['col_order'] if c in df.columns]
                _other = [c for c in df.columns if c not in _cols]
                df = df[_cols + _other]
                st.session_state['stock_data'] = df
                st.session_state['edited_data'] = df.copy()
                st.success(f"✅ Scan complete! Found {len(df)} stocks.")
            except Exception as e2:
                st.error(f"❌ Failed to fetch data: {str(e2)}")
                st.stop()


if not st.session_state['stock_data'].empty:
    # Use the session_state for display and editing
    display_df = st.session_state['stock_data'].copy()
    # Exclude pinned columns from draggable order
    pinned = ["Ticker", "Name"]
    available_cols = [c for c in st.session_state['col_order'] if c in display_df.columns and c not in pinned]
    other_cols = [c for c in display_df.columns if c not in available_cols and c not in pinned]
    
    # --- Leaderboard Section ---
    st.header("Strategic Leaderboards")
    tab_theme, tab_sector, tab_industry, tab_sub = st.tabs(["Your Themes", "Sector", "Industry", "Sub-Industry"])

    def calculate_group_performance(data, group_col, is_list=False):
        rows = []
        for _, row in data.iterrows():
            val = row.get(group_col)
            if pd.isna(val) or val == "":
                continue
            
            groups = val.split(', ') if is_list else [val]
            for g in groups:
                rows.append({
                    'Name': g,
                    'YTD Performance (%)': row['YTD Performance (%)'],
                    '5-Day Performance (%)': row.get('5-Day Performance (%)', 0.0),
                    'Turnover Ratio': row.get('Turnover Ratio', 0.0),
                    'Latest Turnover': row.get('Latest Turnover', 0.0)
                })
        
        pdf = pd.DataFrame(rows)
        if pdf.empty:
            return pd.DataFrame()
            
        leaderboard = pdf.groupby('Name').agg({
            'YTD Performance (%)': 'mean',
            '5-Day Performance (%)': 'mean',
            'Turnover Ratio': 'mean',
            'Latest Turnover': 'mean',
            'Name': 'count'
        }).rename(columns={'Name': 'Count'})
        
        leaderboard['Latest Turnover'] = leaderboard['Latest Turnover'] / 1_000_000
        
        # Calculate Ranks for the groups
        leaderboard['Rank YTD%'] = leaderboard['YTD Performance (%)'].rank(ascending=False, method='min')
        leaderboard['Rank 5D%'] = leaderboard['5-Day Performance (%)'].rank(ascending=False, method='min')
        leaderboard['Rank Turnover Ratio'] = leaderboard['Turnover Ratio'].rank(ascending=False, method='min')
        leaderboard['Rank 20d Vol'] = leaderboard['Latest Turnover'].rank(ascending=False, method='min')
        
        # Overall Rank for Categories
        leaderboard['Overall Score'] = (leaderboard['Rank YTD%'] + leaderboard['Rank 5D%'] + 
                                       leaderboard['Rank Turnover Ratio'] + leaderboard['Rank 20d Vol']) / 4
        leaderboard['Overall Rank'] = leaderboard['Overall Score'].rank(ascending=True, method='min')
        
        # Sort by Overall Rank by default
        leaderboard = leaderboard.drop(columns=['Overall Score']).sort_values(by='Overall Rank')
        
        # Reorder columns: Name, Overall Rank, then the rest
        cols = leaderboard.columns.tolist()
        if 'Overall Rank' in cols:
            cols.remove('Overall Rank')
            # Insert Overall Rank right after the index (Name is the index)
            cols.insert(0, 'Overall Rank')
            leaderboard = leaderboard[cols]
        
        return leaderboard

    # Initialize filter states if not present
    if 'sel_themes' not in st.session_state: st.session_state['sel_themes'] = []
    if 'sel_sectors' not in st.session_state: st.session_state['sel_sectors'] = []
    if 'sel_industries' not in st.session_state: st.session_state['sel_industries'] = []
    if 'sel_subs' not in st.session_state: st.session_state['sel_subs'] = []

    def display_styled_leaderboard(leaderboard, title, filter_key):
        if leaderboard.empty:
            st.info(f"No {title} data available.")
            return

        styled = leaderboard.style.background_gradient(
            subset=['YTD Performance (%)', '5-Day Performance (%)'], 
            cmap='RdYlGn'
        ).background_gradient(
            subset=['Turnover Ratio'],
            cmap='Oranges',
            vmin=0.5, vmax=2.5
        ).background_gradient(
            subset=['Latest Turnover'],
            cmap='Blues',
            vmin=0, vmax=500
        ).background_gradient(
            subset=['Overall Rank'],
            cmap='RdYlGn_r',
            vmin=1, vmax=10
        ).format(precision=2)

        event = st.dataframe(
            styled,
            column_config={
                "Overall Rank": st.column_config.NumberColumn("👑 Rank", format="%d"),
                "Rank YTD%": st.column_config.NumberColumn("Rank YTD", format="%d"),
                "Rank 5D%": st.column_config.NumberColumn("Rank 5D", format="%d"),
                "Rank Turnover Ratio": st.column_config.NumberColumn("Rank Surge", format="%d"),
                "Rank 20d Vol": st.column_config.NumberColumn("Rank Total Vol", format="%d"),
                "YTD Performance (%)": st.column_config.NumberColumn("Avg YTD", format="%.2f%%"),
                "5-Day Performance (%)": st.column_config.NumberColumn("Avg 5-Day", format="%.2f%%"),
                "Turnover Ratio": st.column_config.NumberColumn("Avg Turnover Ratio", format="%.2f x"),
                "Latest Turnover": st.column_config.NumberColumn("Avg Turnover ($M)", format="%.0f"),
                "Count": st.column_config.NumberColumn("Count", format="%d")
            },
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key=f"lb_{filter_key}"
        )

        # Drill-down logic: sync with multiselect
        last_key = f"last_sel_{filter_key}"
        if last_key not in st.session_state: st.session_state[last_key] = None

        if event.selection.rows:
            selected_idx = event.selection.rows[0]
            selected_name = leaderboard.index[selected_idx]
            
            if selected_name != st.session_state[last_key]:
                # Handle change/new selection
                current_filters = list(st.session_state.get(filter_key, []))
                if st.session_state[last_key] in current_filters:
                    current_filters.remove(st.session_state[last_key])
                
                if selected_name not in current_filters:
                    current_filters.append(selected_name)
                
                st.session_state[filter_key] = current_filters
                st.session_state[last_key] = selected_name
                st.toast(f"Applied filter: {selected_name}")
                st.rerun()
        else:
            # Handle deselection
            if st.session_state[last_key] is not None:
                current_filters = list(st.session_state.get(filter_key, []))
                if st.session_state[last_key] in current_filters:
                    current_filters.remove(st.session_state[last_key])
                st.session_state[filter_key] = current_filters
                st.session_state[last_key] = None
                st.rerun()

    with tab_theme:
        display_styled_leaderboard(calculate_group_performance(display_df, 'Themes', is_list=True), "User Theme", "sel_themes")
    with tab_sector:
        display_styled_leaderboard(calculate_group_performance(display_df, 'GICS Sector'), "Sector", "sel_sectors")
    with tab_industry:
        display_styled_leaderboard(calculate_group_performance(display_df, 'GICS Industry'), "Industry", "sel_industries")
    with tab_sub:
        display_styled_leaderboard(calculate_group_performance(display_df, 'GICS Sub-Industry'), "Sub-Industry", "sel_subs")
        
    # Load additional UI settings
    if 'col_widths' not in st.session_state:
        st.session_state['col_widths'] = st.session_state['settings'].get('column_widths', {})
    if 'table_height' not in st.session_state:
        st.session_state['table_height'] = st.session_state['settings'].get('table_height', 600)

    # --- Filter & Manual Edit Section ---
    st.header("Manual Theme Assignment & View Settings")
    
    with st.expander("⚙️ Configure View (Column Order, Widths, Height)"):
        # Column Order - Replaced multiselect with a more friendly Rank Editor
        st.markdown("##### 1. Arrange Column Order")
        st.caption("Lower number = further left. Ticker and Name are always pinned to the left.")
        col_list_data = []
        for i, col in enumerate(available_cols + other_cols):
            col_list_data.append({"Column Name": col, "Position": i + 1})
        
        order_df = pd.DataFrame(col_list_data)
        edited_order_df = st.data_editor(
            order_df,
            column_config={
                "Column Name": st.column_config.Column(disabled=True),
                "Position": st.column_config.NumberColumn("Position", min_value=1, max_value=len(order_df), step=1)
            },
            hide_index=True,
            use_container_width=True,
            key="column_order_editor"
        )
        
        new_order = edited_order_df.sort_values("Position")["Column Name"].tolist()
        
        # Column Widths
        st.markdown("##### Column Widths")
        new_widths = st.session_state['col_widths'].copy()
        w_cols = st.columns(3)
        for i, col_name in enumerate(available_cols):
            with w_cols[i % 3]:
                current_w = new_widths.get(col_name, "medium")
                new_widths[col_name] = st.selectbox(
                    f"Width: {col_name}",
                    ["small", "medium", "large", "auto"],
                    index=["small", "medium", "large", "auto"].index(current_w)
                )
        
        # Table Height
        new_height = st.slider("Table Height (pixels)", 300, 1500, st.session_state['table_height'], step=50)
        
        if st.button("Apply View Changes"):
            st.session_state['col_order'] = new_order
            st.session_state['col_widths'] = new_widths
            st.session_state['table_height'] = new_height
            # Reorder current data in session state
            df = st.session_state['stock_data']
            cols = [c for c in new_order if c in df.columns]
            rem = [c for c in df.columns if c not in cols]
            st.session_state['stock_data'] = df[cols + rem]
            st.rerun()

    # Save Logic
    if st.button("💾 SAVE ALL CHANGES (Themes & UI Config)"):
        # Save Themes
        meta_df = load_metadata()
        for _, row in st.session_state['stock_data'].iterrows():
            ticker = row['Ticker']
            theme_val = row['Themes']
            meta_df.loc[meta_df['Symbol'] == ticker, 'Smart Tags'] = theme_val
        save_metadata(meta_df)
        
        # Save UI Settings
        st.session_state['settings']['column_order'] = st.session_state['col_order']
        st.session_state['settings']['column_widths'] = st.session_state['col_widths']
        st.session_state['settings']['table_height'] = st.session_state['table_height']
        save_settings(st.session_state['settings'])
        
        st.success("Configuration persisted successfully!")
        st.rerun()

    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        all_themes = sorted(list(set([t for themes in display_df['Themes'].dropna() for t in themes.split(', ') if t])))
        sel_themes = st.multiselect("Filter Theme", all_themes, key="sel_themes")
    with f_col2:
        all_sectors = sorted(display_df['GICS Sector'].dropna().unique())
        sel_sectors = st.multiselect("Filter Sector", all_sectors, key="sel_sectors")
    with f_col3:
        all_industries = sorted(display_df['GICS Industry'].dropna().unique())
        sel_industries = st.multiselect("Filter Industry", all_industries, key="sel_industries")
    with f_col4:
        all_subs = sorted(display_df['GICS Sub-Industry'].dropna().unique())
        sel_subs = st.multiselect("Filter Sub-Industry", all_subs, key="sel_subs")

    # Apply Filters
    filtered_df = display_df.copy()
    if sel_themes:
        mask = filtered_df['Themes'].apply(lambda x: any(t in x for t in sel_themes) if pd.notna(x) else False)
        filtered_df = filtered_df[mask]
    if sel_sectors:
        filtered_df = filtered_df[filtered_df['GICS Sector'].isin(sel_sectors)]
    if sel_industries:
        filtered_df = filtered_df[filtered_df['GICS Industry'].isin(sel_industries)]
    if sel_subs:
        filtered_df = filtered_df[filtered_df['GICS Sub-Industry'].isin(sel_subs)]

    # Performance Multipliers for display
    # We do the unit conversion here ONLY if it wasn't done before
    # To prevent double division on rerun, we check the magnitude
    if filtered_df['Latest Turnover'].max() > 10_000: # Heuristic for raw values
        filtered_df['Latest Turnover'] = filtered_df['Latest Turnover'] / 1_000_000
        filtered_df['Avg Daily Turnover (20d)'] = filtered_df['Avg Daily Turnover (20d)'] / 1_000_000

    # Sort
    filtered_df = filtered_df.sort_values(by="Overall Rank", ascending=True)
    
    # st.write(f"Showing {len(filtered_df)} stocks. Edit the 'Themes' column below:")
    
    # DATA EDITOR with Styling
    styled_filtered_df = filtered_df.style.background_gradient(
        subset=['YTD Performance (%)', '5-Day Performance (%)'],
        cmap='RdYlGn'
    ).background_gradient(
        subset=['Turnover Ratio'],
        cmap='Oranges',
        vmin=0.5, vmax=3.0
    ).background_gradient(
        subset=['Avg Daily Turnover (20d)'],
        cmap='Blues',
        vmin=0, vmax=500  # Adjust based on typical values in millions
    ).background_gradient(
        subset=['Overall Rank'],
        cmap='RdYlGn_r', # Reverse because 1 is better
        vmin=1, vmax=100
    ).format(precision=2)

    # Prepare Column Config with widths
    WIDTH_MAP = {"small": "small", "medium": "medium", "large": "large", "auto": None}
    cw = st.session_state['col_widths']
    
    base_config = {
        "Ticker": st.column_config.Column(label="Ticker", pinned=True, disabled=True, width=WIDTH_MAP.get(cw.get("Ticker", "auto"))),
        "Name": st.column_config.Column(label="Name", pinned=True, disabled=True, width=WIDTH_MAP.get(cw.get("Name", "auto"))),
        "Overall Rank": st.column_config.NumberColumn("👑 Overall Rank", format="%d", disabled=True, width=WIDTH_MAP.get(cw.get("Overall Rank", "auto"))),
        "Rank YTD%": st.column_config.NumberColumn("Rank YTD", format="%d", disabled=True, width=WIDTH_MAP.get(cw.get("Rank YTD%", "auto"))),
        "Rank 5D%": st.column_config.NumberColumn("Rank 5D", format="%d", disabled=True, width=WIDTH_MAP.get(cw.get("Rank 5D%", "auto"))),
        "Rank Turnover Ratio": st.column_config.NumberColumn("Rank Surge", format="%d", disabled=True, width=WIDTH_MAP.get(cw.get("Rank Turnover Ratio", "auto"))),
        "Rank 20d Vol": st.column_config.NumberColumn("Rank Total Vol", format="%d", disabled=True, width=WIDTH_MAP.get(cw.get("Rank 20d Vol", "auto"))),
        "Themes": st.column_config.TextColumn(
            "Themes (User Input)", 
            width=WIDTH_MAP.get(cw.get("Themes", "large")), 
            required=False
        ),
        "GICS Sector": st.column_config.Column(disabled=True, width=WIDTH_MAP.get(cw.get("GICS Sector", "auto"))),
        "GICS Industry": st.column_config.Column(disabled=True, width=WIDTH_MAP.get(cw.get("GICS Industry", "auto"))),
        "GICS Sub-Industry": st.column_config.Column(disabled=True, width=WIDTH_MAP.get(cw.get("GICS Sub-Industry", "auto"))),
        "Current Price": st.column_config.NumberColumn("Price", format="$%.2f", disabled=True, width=WIDTH_MAP.get(cw.get("Current Price", "auto"))),
        "Latest Turnover": st.column_config.NumberColumn("Latest Turnover ($M)", format="%.0f", disabled=True, width=WIDTH_MAP.get(cw.get("Latest Turnover", "auto"))),
        "Avg Daily Turnover (20d)": st.column_config.NumberColumn("Avg 20D Turnover ($M)", format="%.0f", disabled=True, width=WIDTH_MAP.get(cw.get("Avg Daily Turnover (20d)", "auto"))),
        "Turnover Ratio": st.column_config.NumberColumn("Turnover Ratio", format="%.2f x", disabled=True, width=WIDTH_MAP.get(cw.get("Turnover Ratio", "auto"))),
        "YTD Performance (%)": st.column_config.NumberColumn("YTD %", format="%.2f%%", disabled=True, width=WIDTH_MAP.get(cw.get("YTD Performance (%)", "auto"))),
        "5-Day Performance (%)": st.column_config.NumberColumn("5D %", format="%.2f%%", disabled=True, width=WIDTH_MAP.get(cw.get("5-Day Performance (%)", "auto")))
    }

    edited_df = st.data_editor(
        styled_filtered_df,
        column_config=base_config,
        use_container_width=True,
        hide_index=True, 
        height=st.session_state['table_height'],
        key="theme_editor"
    )
    
    # Save edits back to session state if changed
    if not edited_df['Themes'].equals(filtered_df['Themes']):
        # Merge theme changes back into the main session state
        main_df = st.session_state['stock_data']
        for _, row in edited_df.iterrows():
            ticker = row['Ticker']
            theme_val = row['Themes']
            main_df.loc[main_df['Ticker'] == ticker, 'Themes'] = theme_val
        st.session_state['stock_data'] = main_df
        st.rerun() # Rerun to update leaderboards immediately


else:
    if run_btn:
         st.error("No data found or error in fetching.")
    else:
         st.info("Click 'Run Scan' to load data.")
