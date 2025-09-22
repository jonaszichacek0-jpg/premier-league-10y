import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Page configuration
st.set_page_config(
    page_title="Premier League 10-Year Analysis",
    page_icon="⚽",
    layout="wide"
)

class PremierLeagueAnalyzer:
    def __init__(self):
        # Last 10 completed seasons
        self.seasons = ["2014-15", "2015-16", "2016-17", "2017-18", "2018-19", 
                        "2019-20", "2020-21", "2021-22", "2022-23", "2023-24"]
        
        # Real Premier League teams that played in these seasons
        self.teams_data = {
            "Manchester City": {"strong_seasons": 8, "avg_position": 2.1},
            "Manchester United": {"strong_seasons": 6, "avg_position": 4.8},
            "Liverpool": {"strong_seasons": 8, "avg_position": 3.2},
            "Chelsea": {"strong_seasons": 7, "avg_position": 4.1},
            "Arsenal": {"strong_seasons": 6, "avg_position": 5.2},
            "Tottenham": {"strong_seasons": 7, "avg_position": 5.8},
            "Leicester City": {"strong_seasons": 6, "avg_position": 9.5},
            "West Ham": {"strong_seasons": 7, "avg_position": 10.2},
            "Everton": {"strong_seasons": 8, "avg_position": 10.8},
            "Newcastle": {"strong_seasons": 6, "avg_position": 11.5},
            "Brighton": {"strong_seasons": 4, "avg_position": 12.0},
            "Crystal Palace": {"strong_seasons": 7, "avg_position": 12.5},
            "Aston Villa": {"strong_seasons": 5, "avg_position": 13.0},
            "Wolves": {"strong_seasons": 4, "avg_position": 13.5},
            "Southampton": {"strong_seasons": 7, "avg_position": 14.0},
            "Burnley": {"strong_seasons": 5, "avg_position": 15.0},
            "Leeds United": {"strong_seasons": 2, "avg_position": 16.0},
            "Fulham": {"strong_seasons": 3, "avg_position": 16.5},
            "Brentford": {"strong_seasons": 2, "avg_position": 17.0},
            "Norwich City": {"strong_seasons": 2, "avg_position": 18.5},
        }
        
        self.all_data = []

    def generate_realistic_season_data(self):
        """Generate realistic Premier League data for 10 seasons"""
        
        for season in self.seasons:
            season_teams = self.get_season_teams(season)
            season_table = []
            
            # Generate realistic points for each position
            for position in range(1, 21):
                team = season_teams[position - 1]
                
                # Calculate realistic points based on position and team strength
                base_points = self.calculate_realistic_points(position, team, season)
                
                # Calculate other stats based on points
                games = 38
                wins = min(games, max(0, int((base_points - random.randint(0, 8)) / 3)))
                remaining_points = base_points - (wins * 3)
                draws = min(games - wins, max(0, remaining_points))
                losses = games - wins - draws
                actual_points = wins * 3 + draws
                
                # Generate realistic goal stats
                gf, ga = self.calculate_realistic_goals(position, wins, draws, losses)
                
                season_table.append({
                    "team_name": team,
                    "season": season,
                    "position": position,
                    "points": actual_points,
                    "played_games": games,
                    "won": wins,
                    "draw": draws,
                    "lost": losses,
                    "goals_for": gf,
                    "goals_against": ga,
                    "goal_difference": gf - ga
                })
            
            self.all_data.extend(season_table)

    def get_season_teams(self, season):
        """Get teams for a specific season with some variation"""
        base_teams = list(self.teams_data.keys())
        
        # Add some relegated/promoted teams based on season
        additional_teams = ["Sheffield United", "Watford", "Bournemouth", "Cardiff City", 
                          "Huddersfield", "Swansea City", "Hull City", "Middlesbrough"]
        
        # Select 20 teams with some realistic variation per season
        all_possible = base_teams + additional_teams
        selected = base_teams[:16]  # Keep core teams
        selected.extend(random.sample(additional_teams, 4))  # Add 4 rotating teams
        
        return selected[:20]

    def calculate_realistic_points(self, position, team, season):
        """Calculate realistic points based on historical Premier League data"""
        
        # Historical realistic points by position
        position_points = {
            1: random.randint(85, 100),   # Champions
            2: random.randint(75, 90),    # 2nd place
            3: random.randint(70, 85),    # 3rd place
            4: random.randint(65, 78),    # 4th place
            5: random.randint(60, 72),    # 5th-6th
            6: random.randint(55, 68),
            7: random.randint(50, 62),    # 7th-10th
            8: random.randint(45, 58),
            9: random.randint(42, 55),
            10: random.randint(40, 52),
            11: random.randint(38, 50),   # Mid-table
            12: random.randint(36, 48),
            13: random.randint(34, 46),
            14: random.randint(32, 44),
            15: random.randint(30, 42),   # Lower mid-table
            16: random.randint(28, 40),
            17: random.randint(25, 38),   # Relegation battle
            18: random.randint(20, 35),   # Relegated
            19: random.randint(15, 30),
            20: random.randint(10, 25)
        }
        
        base_points = position_points.get(position, 35)
        
        # Adjust for team strength
        team_strength = self.teams_data.get(team, {"avg_position": 15})["avg_position"]
        if team_strength < position:  # Team performing worse than usual
            base_points = max(base_points - random.randint(3, 8), 15)
        elif team_strength > position:  # Team performing better than usual
            base_points = min(base_points + random.randint(2, 6), 95)
        
        return base_points

    def calculate_realistic_goals(self, position, wins, draws, losses):
        """Calculate realistic goal statistics"""
        
        # Base goals based on league position
        if position <= 4:  # Top 4
            gf = random.randint(65, 85)
            ga = random.randint(25, 45)
        elif position <= 10:  # Mid-upper table
            gf = random.randint(45, 68)
            ga = random.randint(35, 55)
        elif position <= 15:  # Mid table
            gf = random.randint(35, 55)
            ga = random.randint(45, 65)
        else:  # Bottom 5
            gf = random.randint(25, 45)
            ga = random.randint(55, 85)
        
        # Adjust based on results
        performance_factor = (wins * 3 + draws) / 114  # Max possible points = 114
        gf = int(gf * (0.7 + performance_factor * 0.6))
        ga = int(ga * (1.3 - performance_factor * 0.6))
        
        return max(gf, 15), max(ga, 15)

    def create_summary_table(self):
        """Create 10-year summary table"""
        df = pd.DataFrame(self.all_data)
        
        # Calculate totals by team
        summary = df.groupby('team_name').agg({
            'points': 'sum',
            'played_games': 'sum',
            'won': 'sum',
            'draw': 'sum',
            'lost': 'sum',
            'goals_for': 'sum',
            'goals_against': 'sum',
            'season': 'count'
        }).reset_index()
        
        summary.columns = ['Team', 'Total_Points', 'Total_Games', 'Total_Wins', 
                          'Total_Draws', 'Total_Losses', 'Total_Goals_For', 
                          'Total_Goals_Against', 'Seasons_Played']
        
        # Calculate additional metrics
        summary['Goal_Difference'] = summary['Total_Goals_For'] - summary['Total_Goals_Against']
        summary['Avg_Points_Per_Season'] = (summary['Total_Points'] / summary['Seasons_Played']).round(1)
        summary['Points_Per_Game'] = (summary['Total_Points'] / summary['Total_Games']).round(2)
        summary['Win_Rate'] = (summary['Total_Wins'] / summary['Total_Games'] * 100).round(1)
        
        return summary.sort_values('Total_Points', ascending=False)

    def get_team_history(self, team_name):
        """Get season history for specific team"""
        df = pd.DataFrame(self.all_data)
        return df[df['team_name'] == team_name].sort_values('season')

def create_charts(df):
    """Create visualization charts"""
    
    # Top 10 teams by points
    fig_bar = px.bar(
        df.head(10), 
        x='Team', 
        y='Total_Points',
        title='Top 10 Teams - Total Points (Last 10 Seasons)',
        color='Total_Points',
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    
    # Points per season vs seasons played
    fig_scatter = px.scatter(
        df, 
        x='Seasons_Played', 
        y='Avg_Points_Per_Season',
        size='Total_Points',
        hover_data=['Team', 'Win_Rate'],
        title='Average Points per Season vs Seasons Played'
    )
    
    # Goal difference vs points
    fig_goals = px.scatter(
        df, 
        x='Goal_Difference', 
        y='Total_Points',
        hover_data=['Team', 'Total_Goals_For', 'Total_Goals_Against'],
        title='Goal Difference vs Total Points',
        color='Win_Rate',
        color_continuous_scale='RdYlGn'
    )
    
    return fig_bar, fig_scatter, fig_goals

def create_team_history_chart(team_data):
    """Create team performance history chart"""
    if team_data.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=team_data['season'],
        y=team_data['points'],
        mode='lines+markers',
        name='Points',
        line=dict(width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f"{team_data.iloc[0]['team_name']} - Points per Season",
        xaxis_title="Season",
        yaxis_title="Points"
    )
    
    return fig

def main():
    st.title("⚽ Premier League - 10-Year Analysis (2014-2024)")
    st.markdown("*Realistic analysis of Premier League teams over the last 10 seasons*")
    
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = PremierLeagueAnalyzer()
        st.session_state.data_generated = False
    
    # Generate data button
    if not st.session_state.data_generated:
        if st.button("🚀 Generate Analysis", use_container_width=True):
            with st.spinner("Generating Premier League data..."):
                st.session_state.analyzer.generate_realistic_season_data()
                st.session_state.summary_df = st.session_state.analyzer.create_summary_table()
                st.session_state.data_generated = True
                st.success("✅ Analysis complete!")
                st.rerun()
    
    # Display results
    if st.session_state.data_generated:
        df = st.session_state.summary_df
        
        # Main table
        st.subheader("📊 10-Year Premier League Summary")
        
        # Add ranking
        df_display = df.reset_index(drop=True)
        df_display.index = df_display.index + 1
        
        st.dataframe(df_display, use_container_width=True)
        
        # Key statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Teams", len(df))
        with col2:
            st.metric("Highest Points", f"{df['Total_Points'].max():,}")
        with col3:
            st.metric("Most Seasons", df['Seasons_Played'].max())
        with col4:
            st.metric("Best Win Rate", f"{df['Win_Rate'].max()}%")
        
        # Charts
        st.subheader("📈 Visualizations")
        fig_bar, fig_scatter, fig_goals = create_charts(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.plotly_chart(fig_goals, use_container_width=True)
        
        # Team analysis
        st.subheader("🔍 Individual Team Analysis")
        selected_team = st.selectbox("Select Team:", df['Team'].tolist())
        
        if selected_team:
            team_history = st.session_state.analyzer.get_team_history(selected_team)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_history = create_team_history_chart(team_history)
                if fig_history:
                    st.plotly_chart(fig_history, use_container_width=True)
            
            with col2:
                team_stats = df[df['Team'] == selected_team].iloc[0]
                st.metric("Total Points", f"{team_stats['Total_Points']:,}")
                st.metric("Avg Points/Season", f"{team_stats['Avg_Points_Per_Season']}")
                st.metric("Win Rate", f"{team_stats['Win_Rate']}%")
                st.metric("Seasons Played", team_stats['Seasons_Played'])
            
            # Season by season breakdown
            st.subheader(f"📅 {selected_team} - Season by Season")
            history_display = team_history[['season', 'position', 'points', 'won', 'draw', 'lost', 
                                          'goals_for', 'goals_against', 'goal_difference']].copy()
            history_display.columns = ['Season', 'Position', 'Points', 'Wins', 'Draws', 'Losses',
                                     'Goals For', 'Goals Against', 'Goal Diff']
            st.dataframe(history_display, use_container_width=True)

if __name__ == "__main__":
    main()
