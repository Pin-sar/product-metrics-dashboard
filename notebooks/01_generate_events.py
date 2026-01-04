import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ----------------------------
# Config
# ----------------------------
N_USERS = 3000
DAYS = 60
N_EVENTS = 90000  # adjust up/down
START_DATE = (datetime.now() - timedelta(days=DAYS)).replace(hour=0, minute=0, second=0, microsecond=0)

platforms = ["web", "desktop"]
countries = ["US", "IN", "BR", "DE", "GB", "CA", "AU", "SG", "JP"]

event_types = [
    "signup", "login", "open_file", "create_file",
    "edit_layer", "add_comment", "invite_collaborator",
    "share_file", "export_design", "create_component",
    "use_plugin", "version_history", "logout"
]

# Event -> feature mapping (for feature-level analysis)
feature_map = {
    "open_file": "file_open",
    "create_file": "file_create",
    "edit_layer": "editor",
    "add_comment": "comments",
    "invite_collaborator": "collaboration",
    "share_file": "sharing",
    "export_design": "export",
    "create_component": "components",
    "use_plugin": "plugins",
    "version_history": "versioning",
    "login": "auth",
    "signup": "auth",
    "logout": "auth"
}

# ----------------------------
# Users table (dimension)
# ----------------------------
users = pd.DataFrame({
    "user_id": np.arange(1, N_USERS + 1),
})

# Signup day distribution: more users sign up earlier than later
signup_offsets = np.random.choice(
    np.arange(DAYS),
    size=N_USERS,
    p=(np.linspace(2.5, 1.0, DAYS) / np.linspace(2.5, 1.0, DAYS).sum())
)

users["signup_time"] = [START_DATE + timedelta(days=int(d), hours=int(np.random.randint(0, 24))) for d in signup_offsets]
country_probs = np.array([0.28, 0.22, 0.08, 0.07, 0.07, 0.06, 0.05, 0.09, 0.05], dtype=float)
country_probs = country_probs / country_probs.sum()  # <-- makes it sum to 1 exactly

users["country"] = np.random.choice(countries, size=N_USERS, p=country_probs)

users["platform_pref"] = np.random.choice(platforms, size=N_USERS, p=[0.55, 0.45])

# ----------------------------
# Generate sessions per user (behavior)
# ----------------------------
# Heavy-tail: most users few sessions, few users lots
sessions_per_user = np.random.negative_binomial(n=2, p=0.55, size=N_USERS) + 1
sessions_per_user = np.clip(sessions_per_user, 1, 25)

session_rows = []
session_id_counter = 1

for _, row in users.iterrows():
    uid = int(row["user_id"])
    s_time = row["signup_time"]

    # session start dates must be after signup
    for _ in range(int(sessions_per_user[uid - 1])):
        day_offset = np.random.randint(0, DAYS)
        session_start = START_DATE + timedelta(days=int(day_offset), hours=int(np.random.randint(0, 24)), minutes=int(np.random.randint(0, 60)))
        if session_start < s_time:
            session_start = s_time + timedelta(hours=int(np.random.randint(0, 48)))

        duration_min = int(np.random.lognormal(mean=2.2, sigma=0.55))  # typical sessions 5–30 min
        duration_min = int(np.clip(duration_min, 2, 120))
        session_end = session_start + timedelta(minutes=duration_min)

        session_rows.append({
            "session_id": f"s_{session_id_counter}",
            "user_id": uid,
            "session_start": session_start,
            "session_end": session_end,
            "platform": row["platform_pref"],
            "country": row["country"]
        })
        session_id_counter += 1

sessions = pd.DataFrame(session_rows)

# Keep only a reasonable number of sessions to match event volume
sessions = sessions.sample(min(len(sessions), 22000), random_state=42).reset_index(drop=True)

# ----------------------------
# Generate events within sessions
# ----------------------------
events = []
event_id_counter = 1

# probabilities of events within a session
event_probs = {
    "login": 0.10,
    "open_file": 0.18,
    "create_file": 0.08,
    "edit_layer": 0.28,
    "add_comment": 0.10,
    "invite_collaborator": 0.04,
    "share_file": 0.05,
    "export_design": 0.05,
    "create_component": 0.06,
    "use_plugin": 0.04,
    "version_history": 0.02,
    "logout": 0.00
}

# For a portion of users, force a signup event once
signup_users = users.sample(frac=0.85, random_state=42)["user_id"].tolist()
signup_set = set(signup_users)

for _, s in sessions.iterrows():
    uid = int(s["user_id"])
    start = pd.to_datetime(s["session_start"])
    end = pd.to_datetime(s["session_end"])

    # number of events in this session (heavy-tail)
    k = int(np.random.lognormal(mean=2.1, sigma=0.6))
    k = int(np.clip(k, 3, 60))

    # ensure at least one "login" and one "open_file" sometimes
    base_events = ["login", "open_file"]
    chosen = base_events + list(np.random.choice(list(event_probs.keys()), size=k - len(base_events), p=np.array(list(event_probs.values())) / sum(event_probs.values())))

    # optional signup near the start of timeline
    if uid in signup_set and np.random.rand() < 0.02:
        chosen.insert(0, "signup")

    # distribute event times within session
    times = np.sort(np.random.uniform(0, (end - start).total_seconds(), size=len(chosen)))
    for etype, t in zip(chosen, times):
        ts = start + timedelta(seconds=float(t))
        events.append({
            "event_id": f"e_{event_id_counter}",
            "user_id": uid,
            "session_id": s["session_id"],
            "event_time": ts,
            "event_type": etype,
            "feature": feature_map.get(etype, "other"),
            "platform": s["platform"],
            "country": s["country"]
        })
        event_id_counter += 1

events = pd.DataFrame(events)

# downsample / upsample to desired N_EVENTS
if len(events) > N_EVENTS:
    events = events.sample(N_EVENTS, random_state=42).sort_values("event_time").reset_index(drop=True)
else:
    events = events.sort_values("event_time").reset_index(drop=True)

# add is_new_user flag: event occurs within 7 days of signup
signup_time_lookup = users.set_index("user_id")["signup_time"].to_dict()
events["signup_time"] = events["user_id"].map(signup_time_lookup)
events["is_new_user"] = (events["event_time"] <= (events["signup_time"] + pd.Timedelta(days=7))).astype(int)
events.drop(columns=["signup_time"], inplace=True)

# ----------------------------
# Save raw data
# ----------------------------
events.to_csv("data/raw_events.csv", index=False)
users.to_csv("data/users.csv", index=False)
sessions.to_csv("data/sessions.csv", index=False)

print("Saved:")
print(" - data/raw_events.csv", events.shape)
print(" - data/users.csv", users.shape)
print(" - data/sessions.csv", sessions.shape)
