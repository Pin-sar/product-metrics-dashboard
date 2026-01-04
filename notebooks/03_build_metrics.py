import pandas as pd

events = pd.read_csv("outputs/clean_events.csv", parse_dates=["event_time"])

events["event_date"] = events["event_time"].dt.date

# ---- Daily Active Users (DAU)
dau = events.groupby("event_date")["user_id"].nunique().reset_index(name="DAU")

# ---- Feature Adoption (daily unique users per feature)
feature_users = (
    events.groupby(["event_date", "feature"])["user_id"]
    .nunique()
    .reset_index(name="unique_users")
)

# ---- Sessions per user per day
sessions_per_user_day = (
    events.groupby(["event_date", "user_id"])["session_id"]
    .nunique()
    .reset_index(name="sessions")
)

# ---- Events per session
events_per_session = (
    events.groupby("session_id")["event_id"]
    .count()
    .reset_index(name="events_in_session")
)

# ---- Save tables
dau.to_csv("outputs/daily_dau.csv", index=False)
feature_users.to_csv("outputs/daily_feature_users.csv", index=False)
sessions_per_user_day.to_csv("outputs/sessions_per_user_day.csv", index=False)
events_per_session.to_csv("outputs/events_per_session.csv", index=False)

print("Saved metric tables in outputs/")
