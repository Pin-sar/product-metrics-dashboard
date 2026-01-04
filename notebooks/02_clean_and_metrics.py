import pandas as pd

events = pd.read_csv("data/raw_events.csv", parse_dates=["event_time"])
users = pd.read_csv("data/users.csv", parse_dates=["signup_time"])
sessions = pd.read_csv("data/sessions.csv", parse_dates=["session_start", "session_end"])

# 1) remove duplicates
before = len(events)
events = events.drop_duplicates(subset=["event_id"])
after = len(events)

# 2) remove impossible timestamps
events = events.dropna(subset=["event_time"])
events = events[events["event_time"].dt.year >= 2020]  # sanity rule

# 3) enforce known event types (prevents typos)
valid_events = set([
    "signup","login","open_file","create_file","edit_layer","add_comment",
    "invite_collaborator","share_file","export_design","create_component",
    "use_plugin","version_history","logout"
])
events = events[events["event_type"].isin(valid_events)]

# 4) event ordering check per session
events = events.sort_values(["session_id", "event_time"]).reset_index(drop=True)

print(f"Deduped: {before} -> {after}")
print("Final events:", events.shape)

events.to_csv("outputs/clean_events.csv", index=False)
print("Saved outputs/clean_events.csv")
