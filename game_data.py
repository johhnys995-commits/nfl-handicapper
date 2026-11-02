1
"""
NFL HANDICAPPER PROJECT
Shared Game Data Foundation
All specialist AIs receive the same underlying data.
Missing information must remain None, never be invented.
"""

from datetime import datetime, timezone
from typing import Any
import json

from copy import deepcopy
VERSION = "1.0"

SPECIALISTS = [
    "ChatGPT - Special Teams",
    "Claude - Defense and Coaching",
    "Gemini - Quarterback and Passing",
    "DeepSeek - Offensive and Defensive Lines",
    "Copilot - Weather, Travel and Scheduling",
]


# --------------------------------------------------
# CORE TEAM STATISTICS
# --------------------------------------------------

TEAM_TEMPLATE = {
    "team_name": None,
    "record": None,
    "offense": {
        "epa_per_play": None,
        "epa_per_drive": None,
        "success_rate": None,
        "early_down_success_rate": None,
        "third_down_conversion": None,
        "fourth_down_conversion": None,
        "points_per_drive": None,
        "yards_per_play": None,
        "explosive_play_rate": None,
        "negative_play_rate": None,
        "red_zone_efficiency": None,
        "goal_to_go_efficiency": None,
        "turnover_rate": None,
        "proe": None,
        "pass_effectiveness": None,
    },
    "defense": {
        "epa_allowed_per_play": None,
        "epa_allowed_per_drive": None,
        "success_rate_allowed": None,
        "points_allowed_per_drive": None,
        "third_down_stop_rate": None,
        "fourth_down_stop_rate": None,
        "pressure_rate": None,
        "sack_rate": None,
        "havoc_rate": None,
        "takeaway_rate": None,
        "red_zone_defense": None,
        "explosive_plays_allowed": None,
    },
    "quarterback": {
        "name": None,
        "completion_percentage": None,
        "cpoe": None,
        "passer_rating": None,
        "pressure_performance": None,
        "time_to_pressure": None,
        "pressure_to_sack_rate": None,
        "turnover_worthy_plays": None,
        "clutch_performance": None,
    },
    "offensive_line": {
        "pressure_rate_allowed": None,
        "sack_rate_allowed": None,
        "run_blocking_grade": None,
        "pass_blocking_grade": None,
    },
    "special_teams": {
        "field_goal_percentage": None,
        "punt_average": None,
        "net_punt_average": None,
        "kick_return_average": None,
        "punt_return_average": None,
        "blocked_kicks": None,
        "special_teams_epa": None,
    },
    "roster": {
        "injuries": [],
        "questionable_players": [],
        "returning_players": [],
        "replacement_quality": None,
        "lineup_continuity": None,
        "depth_concerns": [],
    },
    "situational": {
        "home_record": None,
        "away_record": None,
        "rest_days": None,
        "travel_distance": None,
        "time_zone_changes": None,
        "penalties_per_game": None,
        "turnover_differential": None,
        "strength_of_schedule": None,
        "opponent_adjusted_rating": None,
    },
}


# --------------------------------------------------
# COMPLETE GAME DATA TEMPLATE
# --------------------------------------------------

GAME_DATA = {
    "version": VERSION,
    "last_updated": None,
    "game": {
        "date": None,
        "week": None,
        "season": None,
        "home_team": None,
        "away_team": None,
        "stadium": None,
        "surface": None,
    },
    "teams": {
        "home": deepcopy(TEAM_TEMPLATE),
"away": deepcopy(TEAM_TEMPLATE),
    },
    "weather": {
        "temperature": None,
        "wind_speed": None,
        "wind_direction": None,
        "precipitation": None,
        "humidity": None,
        "weather_conditions": None,
        "indoor_or_outdoor": None,
    },
    "historical_matchup": {
        "last_five_years": [],
        "head_to_head_record": None,
        "recent_matchups": [],
        "relevant_trends": [],
    },
    "coaching": {
        "home_coach": None,
        "away_coach": None,
        "decision_risk_home": None,
        "decision_risk_away": None,
        "fourth_down_decisions": None,
        "clock_management": None,
        "tactical_matchups": [],
    },
    "market": {
        "spread": None,
        "moneyline_home": None,
        "moneyline_away": None,
        "over_under": None,
        "opening_spread": None,
        "current_spread": None,
        "line_movement": None,
    },
    "x_factor": {
        "mandatory": True,
        "factors": [],
        "uncertainty_penalty": 0.0,
        "home_index": None,
        "away_index": None,
        "meaningful_factor_found": False,
    },
    "data_quality": {
        "sources": [],
        "missing_fields": [],
        "conflicting_data": [],
        "verification_notes": [],
        "confidence": None,
    },
}


# --------------------------------------------------
# X-FACTOR ANALYSIS
# --------------------------------------------------

X_FACTOR_CATEGORIES = [
    "matchup_specific_advantage",
    "unexpected_player_changes",
    "returning_players",
    "pressure_and_clutch_performance",
    "resilience_after_adversity",
    "special_teams_field_position",
    "coaching_tactical_surprise",
    "weather_and_environment",
    "unusual_matchup_conditions",
    "data_uncertainty",
]


def calculate_x_factor(team, factors, uncertainty_penalty=0.0):
    """
    X = SUM(weight * evidence * confidence) - D

    Only documented evidence counts.
    Unknown events cannot be predicted.
    """

    total = 0.0

    for factor in factors:
        if factor.get("advantage_team") != team:
            continue

        weight = factor.get("weight")
        evidence = factor.get("evidence_strength")
        confidence = factor.get("confidence")
        impact = factor.get("impact")

        if None in (weight, evidence, confidence, impact):
            continue

        values = [weight, evidence, confidence, impact]

        if not all(0.0 <= value <= 1.0 for value in values):
            continue

        if not factor.get("source"):
            continue

        total += weight * evidence * confidence * impact

    penalty = max(0.0, min(1.0, uncertainty_penalty))

    return round(total - penalty, 4)


def update_x_factors(data):
    factors = data["x_factor"]["factors"]
    penalty = data["x_factor"]["uncertainty_penalty"]

    home = data["game"]["home_team"]
    away = data["game"]["away_team"]

    if not home or not away:
        raise ValueError("Both team names are required.")

    data["x_factor"]["home_index"] = calculate_x_factor(
        home, factors, penalty
    )

    data["x_factor"]["away_index"] = calculate_x_factor(
        away, factors, penalty
    )

    data["x_factor"]["meaningful_factor_found"] = any(
        factor.get("source")
        and factor.get("advantage_team") in (home, away)
        for factor in factors
    )

    return data


# --------------------------------------------------
# DATA VALIDATION
# --------------------------------------------------

def validate_game_data(data):

    errors = []

    if not data["game"]["home_team"]:
        errors.append("Missing home team.")

    if not data["game"]["away_team"]:
        errors.append("Missing away team.")

    if not data["game"]["date"]:
        errors.append("Missing game date.")

    if data["game"]["home_team"] == data["game"]["away_team"]:
        errors.append("Home and away teams cannot be identical.")

    for factor in data["x_factor"]["factors"]:
        if factor.get("advantage_team") not in (
            data["game"]["home_team"],
            data["game"]["away_team"],
        ):
            errors.append("X-factor has an invalid team assignment.")

        if not factor.get("source"):
            errors.append("X-factor evidence requires a source.")

    return errors


# --------------------------------------------------
# SHARED DATA PACKAGE
# --------------------------------------------------

def build_shared_game_data(data):

    data["last_updated"] = datetime.now(
        timezone.utc
    ).isoformat()

    update_x_factors(data)

    errors = validate_game_data(data)

    if errors:
        raise ValueError(
            "Game data validation failed: " + "; ".join(errors)
        )

    # Every specialist receives the same snapshot.
    shared_package = {
        "version": VERSION,
        "game_data": data,
        "specialists": SPECIALISTS,
        "identical_data_required": True,
        "independent_analysis_required": True,
    }

    return shared_package


# --------------------------------------------------
# EXPORT DATA
# --------------------------------------------------

def export_game_data(data, filename="game_data.json"):

    package = build_shared_game_data(data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(package, file, indent=4, ensure_ascii=False)

    return filename


if __name__ == "__main__":
    print("NFL Shared Game Data Foundation")
    print("Version:", VERSION)
    print("Specialist AIs:", len(SPECIALISTS))
    print("X-Factor Analysis: MANDATORY")
    print("Data validation: ENABLED")
    print("Ready for game data.")
