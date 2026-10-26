from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_FILE = Path(__file__).with_name("movies.json")
USERS_FILE = Path(__file__).with_name("users.json")
ADMIN_KEY = os.getenv("ADMIN_KEY", "movieadmin123")
GENRES = ["Action", "Adventure", "Animation", "Comedy", "Documentary", "Drama", "Fantasy", "Horror", "Romance", "Sci-Fi", "Thriller"]


SAMPLE_MOVIES = [
    #  SCI-FI 
    {
        "id": 1, "title": "Interstellar", "genre": "Sci-Fi", "year": 2014,
        "description": "Explorers travel through a wormhole to find a new home for humanity.",
        "watch_count": 142, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "tagline": "Mankind's next step will be our greatest."
    },
    {
        "id": 2, "title": "The Matrix", "genre": "Sci-Fi", "year": 1999,
        "description": "A hacker discovers that reality is a simulation controlled by machines.",
        "watch_count": 128, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "tagline": "Welcome to the real world."
    },
    {
        "id": 3, "title": "Dune", "genre": "Sci-Fi", "year": 2021,
        "description": "A young nobleman faces his destiny on a dangerous desert planet.",
        "watch_count": 116, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
        "tagline": "It begins."
    },

    #  DRAMA 
    {
        "id": 4, "title": "The Shawshank Redemption", "genre": "Drama", "year": 1994,
        "description": "Two prisoners develop an enduring friendship while holding on to hope.",
        "watch_count": 153, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg",
        "tagline": "Fear can hold you prisoner. Hope can set you free."
    },
    {
        "id": 5, "title": "Forrest Gump", "genre": "Drama", "year": 1994,
        "description": "A kind-hearted man experiences extraordinary events throughout American history.",
        "watch_count": 137, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "tagline": "Life is like a box of chocolates."
    },
    {
        "id": 6, "title": "The Pursuit of Happyness", "genre": "Drama", "year": 2006,
        "description": "A struggling father works tirelessly to build a better life for his son.",
        "watch_count": 119, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/lBYOKAMcxIvuk9s9hMuecB9dPBV.jpg",
        "tagline": "Never give up."
    },

    #  ACTION 
    {
        "id": 7, "title": "Mad Max: Fury Road", "genre": "Action", "year": 2015,
        "description": "A drifter joins a rebel warrior in a high-speed escape across a wasteland.",
        "watch_count": 164, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/hA2ple9q4qnwxp3hKVNhroipsir.jpg",
        "tagline": "What a lovely day."
    },
    {
        "id": 8, "title": "John Wick", "genre": "Action", "year": 2014,
        "description": "A retired assassin returns to the criminal underworld seeking vengeance.",
        "watch_count": 149, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg",
        "tagline": "Don't set him off."
    },
    {
        "id": 9, "title": "The Dark Knight", "genre": "Action", "year": 2008,
        "description": "Batman confronts the Joker, a criminal mastermind threatening Gotham City.",
        "watch_count": 171, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "tagline": "Why so serious?"
    },

    #  DOCUMENTARY 
    {
        "id": 10, "title": "Free Solo", "genre": "Documentary", "year": 2018,
        "description": "A climber prepares to scale El Capitan without ropes or safety equipment.",
        "watch_count": 91, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/a0GM57AnJtNi7lMOCamniiyV10W.jpg",
        "tagline": "Fear. Less."
    },
    {
        "id": 11, "title": "My Octopus Teacher", "genre": "Documentary", "year": 2020,
        "description": "A filmmaker forms an extraordinary bond with an octopus in a kelp forest.",
        "watch_count": 84, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/original/u96gR99ZUtdmE3bAzASnjZqzioR.jpg",
        "tagline": "A friendship beneath the waves."
    },
    {
        "id": 12, "title": "March of the Penguins", "genre": "Documentary", "year": 2005,
        "description": "Emperor penguins endure Antarctica's brutal winter to raise their young.",
        "watch_count": 73, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/original/tF35l7PWDvfGl4vhZHUnnFRtfpX.jpg",
        "tagline": "The journey of a lifetime."
    },

    #  ROMANCE 
    {
        "id": 13, "title": "The Notebook", "genre": "Romance", "year": 2004,
        "description": "Two young lovers struggle against social differences and the passage of time.",
        "watch_count": 133, "ratings": {},
        "poster": "https://www.themoviedb.org/t/p/w220_and_h330_face/lfA4GW15zJd7Xn4pWkFMyMUDOyi.jpg",
        "tagline": "Behind every great love is a great story."
    },
    {
        "id": 14, "title": "La La Land", "genre": "Romance", "year": 2016,
        "description": "A jazz musician and an aspiring actress fall in love while pursuing their dreams.",
        "watch_count": 126, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
        "tagline": "Here's to the fools who dream."
    },
    {
        "id": 15, "title": "Pride & Prejudice", "genre": "Romance", "year": 2005,
        "description": "Elizabeth Bennet and Mr. Darcy navigate pride, class, and unexpected love.",
        "watch_count": 108, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/sGjIvtVvTlWnia2zfJfHz81pZ9Q.jpg",
        "tagline": "A romance ahead of its time."
    },

    #  COMEDY 
    {
        "id": 16, "title": "The Grand Budapest Hotel", "genre": "Comedy", "year": 2014,
        "description": "A hotel concierge and his protégé become embroiled in a stolen painting mystery.",
        "watch_count": 97, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
        "tagline": "A perfectly planned adventure."
    },
    {
        "id": 17, "title": "Home Alone", "genre": "Comedy", "year": 1990,
        "description": "A young boy must defend his house from burglars after being left home alone.",
        "watch_count": 145, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/onTSipZ8R3bliBdKfPtsDuHTdlL.jpg",
        "tagline": "A family holiday to remember."
    },
    {
        "id": 18, "title": "The Mask", "genre": "Comedy", "year": 1994,
        "description": "A timid bank clerk gains outrageous powers from a mysterious magical mask.",
        "watch_count": 112, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/original/zzRIncsQoPPvT5BnwQ9z8L4aNKJ.jpg",
        "tagline": "From zero to hero."
    },

    #  THRILLER 
    {
        "id": 19, "title": "Gone Girl", "genre": "Thriller", "year": 2014,
        "description": "A husband's life unravels when his wife disappears and suspicion turns toward him.",
        "watch_count": 139, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/original/rrCizjAFXlLqEmipMDceYwf5rbw.jpg",
        "tagline": "You don't know what you've got till it's gone."
    },
    {
        "id": 20, "title": "Shutter Island", "genre": "Thriller", "year": 2010,
        "description": "Two US marshals investigate a disappearance at a remote psychiatric institution.",
        "watch_count": 131, "ratings": {},
        "poster": "https://image.tmdb.org/t/p/w500/4GDy0PHYX3VRXUtwK5ysFbg3kEx.jpg",
        "tagline": "Someone is missing."
    },
]



CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#24212b; --muted:#777482; --panel:#ffffff; --line:#e8e5ed; --accent:#e84761; }
.stApp { background: radial-gradient(ellipse at 75% -15%, rgba(241,205,221,.34), transparent 36%), #fbfafc; color:var(--ink); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(251,250,252,.86); }
[data-testid="stSidebar"] { background:#f4f1f6; border-right:1px solid var(--line); }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:var(--muted); }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; }
h1 { font-size:2.45rem !important; font-weight:800 !important; }
h2 { font-size:1.65rem !important; font-weight:750 !important; }
h3 { font-size:1.05rem !important; font-weight:700 !important; }
p, label, [data-testid="stCaptionContainer"] { color:var(--muted); }
.brand { font:800 1.25rem 'Manrope',sans-serif; letter-spacing:-.06em; color:#26222e; padding:.4rem 0 1.2rem; }
.brand span { color:var(--accent); }
.eyebrow { color:var(--accent); font-size:.72rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; margin-bottom:.55rem; }
.hero { min-height:325px; padding:2.2rem 2.5rem; border:1px solid var(--line); border-radius:22px; display:flex; flex-direction:column; justify-content:flex-end; background:linear-gradient(90deg,rgba(19,16,25,.92) 0%,rgba(19,16,25,.72) 42%,rgba(19,16,25,.06) 100%),linear-gradient(0deg,rgba(19,16,25,.42),transparent 45%),url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1600&q=90') center 44%/cover; margin:.2rem 0 1.8rem; }
.hero h1 { max-width:580px; margin:0 0 .55rem; }
.hero p { max-width:500px; font-size:1rem; color:#d1ced7; }
.hero-meta { color:#e8e5ed; font-size:.82rem; margin-bottom:.7rem; }
.poster { position:relative; overflow:hidden; border-radius:14px; border:1px solid var(--line); background:#fff; box-shadow:0 5px 20px rgba(35,27,48,.055); transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease; }
.poster:hover { transform:translateY(-4px); border-color:rgba(255,77,103,.65); }
.poster img { width:100%; height:265px; object-fit:cover; display:block; }
.poster-copy { padding:.8rem .9rem 1rem; }
.poster-title { color:#282430; font:700 .95rem 'Manrope',sans-serif; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.poster-meta { margin-top:.27rem; color:#85818d; font-size:.76rem; }
.poster-tag { position:absolute; top:10px; left:10px; background:rgba(12,11,16,.78); border:1px solid rgba(255,255,255,.16); padding:.24rem .5rem; border-radius:99px; color:white; font-size:.67rem; backdrop-filter:blur(8px); }
.section-label { display:flex; align-items:center; gap:.65rem; margin:1.8rem 0 .85rem; color:#292531; font:700 1.15rem 'Manrope',sans-serif; }
.section-label:before { content:''; width:4px; height:20px; border-radius:4px; background:var(--accent); }
.metric-card { background:linear-gradient(145deg,#fff,#f8f6fa); border:1px solid var(--line); border-radius:15px; padding:1rem 1.1rem; box-shadow:0 4px 16px rgba(35,27,48,.04); }
.metric-label { color:var(--muted); font-size:.76rem; }
.metric-value { color:#282430; font:800 1.65rem 'Manrope',sans-serif; margin-top:.2rem; }
.muted-small { color:var(--muted); font-size:.78rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { background:#fff; border-color:var(--line); border-radius:14px; }
div.stButton > button { border-radius:10px; border:1px solid var(--line); font-weight:700; }
div.stButton > button[kind="primaryFormSubmit"],div.stButton > button[kind="primary"] { background:var(--accent); border-color:var(--accent); color:#fff !important; }
div[data-testid="stForm"] button[kind="primaryFormSubmit"],div[data-testid="stForm"] button[kind="primaryFormSubmit"] span { color:#fff !important; }
div[data-testid="stTextInput"] input,div[data-testid="stNumberInput"] input,div[data-testid="stTextArea"] textarea { background:#fff; color:#282430; border-color:var(--line); border-radius:10px; }
div[data-baseweb="select"] > div { background:#fff; border-color:var(--line); border-radius:10px; }
div[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:1rem; border-radius:14px; box-shadow:0 4px 16px rgba(35,27,48,.04); }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color:#282430; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.login-shell { max-width:440px; margin:4vh auto; padding:2rem 2rem 1.5rem; border:1px solid var(--line); border-radius:20px; background:linear-gradient(145deg,#fff,#f8f6fa); box-shadow:0 18px 55px rgba(35,27,48,.08); }
.login-sub { color:var(--muted); margin-top:-.5rem; margin-bottom:1.3rem; }
.stTabs [data-baseweb="tab-list"] { gap:.5rem; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"] { color:var(--muted); }
.stTabs [aria-selected="true"] { color:#282430 !important; }
</style>
"""


def load_json(path: Path, fallback):
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return fallback


def save_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_movies() -> list[dict]:
    """Load the catalogue in app.py and merge persisted activity by movie title.

    The Python catalogue is the source of truth for supplied movie details. The
    JSON file stores ratings, watch history, and admin-added titles. Matching by
    normalized title prevents stale IDs from attaching activity to the wrong film.
    """
    saved = load_json(DATA_FILE, [])
    if isinstance(saved, dict):
        saved = saved.get("movies", [])
    if not isinstance(saved, list):
        saved = []

    def title_key(movie: dict) -> str:
        return " ".join(str(movie.get("title", "")).casefold().split())

    saved_by_title = {title_key(movie): movie for movie in saved if isinstance(movie, dict) and title_key(movie)}
    movies: list[dict] = []
    used_titles: set[str] = set()

    # Always apply the supplied in-code list, even if an older movies.json exists.
    for supplied in SAMPLE_MOVIES:
        movie = dict(supplied)
        key = title_key(movie)
        old = saved_by_title.get(key, {})
        movie["ratings"] = {**old.get("ratings", {}), **movie.get("ratings", {})}
        movie["watch_history"] = list(old.get("watch_history", movie.get("watch_history", [])))
        # Keep the current persisted play count while using the supplied movie text/poster.
        movie["watch_count"] = old.get("watch_count", movie.get("watch_count", 0))
        movie.setdefault("tagline", "A story worth discovering")
        movie.setdefault("poster", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=700&q=85")
        movie.setdefault("watch_history", [])
        movie.setdefault("ratings", {})
        movies.append(movie)
        used_titles.add(key)

    # Keep extra entries created in the JSON file (for example through the admin console).
    next_id = max((int(movie.get("id", 0)) for movie in movies), default=0) + 1
    for old in saved:
        if not isinstance(old, dict) or not title_key(old) or title_key(old) in used_titles:
            continue
        movie = dict(old)
        movie["id"] = next_id
        next_id += 1
        movie.setdefault("genre", "Other")
        movie.setdefault("year", datetime.now().year)
        movie.setdefault("description", "")
        movie.setdefault("tagline", "A story worth discovering")
        movie.setdefault("poster", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=700&q=85")
        movie.setdefault("watch_count", 0)
        movie.setdefault("ratings", {})
        movie.setdefault("watch_history", [])
        movies.append(movie)
        used_titles.add(title_key(movie))
    return movies


def save_movies(movies: list[dict]) -> None:
    save_json(DATA_FILE, movies)


def load_users() -> dict:
    users = load_json(USERS_FILE, {})
    return users if isinstance(users, dict) else {}


def password_hash(password: str, salt: str | None = None) -> dict:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 180_000).hex()
    return {"salt": salt, "hash": digest}


def password_matches(password: str, record: dict) -> bool:
    candidate = password_hash(password, record.get("salt", ""))["hash"]
    return hmac.compare_digest(candidate, record.get("hash", ""))


def average_rating(movie: dict) -> float | None:
    ratings = list(movie.get("ratings", {}).values())
    return sum(ratings) / len(ratings) if ratings else None


def recommend_movies(movies: list[dict], username: str, limit: int = 8) -> list[dict]:
    rated_ids = {movie["id"] for movie in movies if username in movie.get("ratings", {})}
    genre_scores: dict[str, list[int]] = {}
    for movie in movies:
        rating = movie.get("ratings", {}).get(username)
        if rating:
            genre_scores.setdefault(movie["genre"], []).append(rating)
    genre_average = {genre: sum(scores) / len(scores) for genre, scores in genre_scores.items()}
    candidates = [movie for movie in movies if movie["id"] not in rated_ids]

    def score(movie: dict):
        personal = genre_average.get(movie["genre"], 3.0)
        community = average_rating(movie) or 3.0
        popularity = min(movie.get("watch_count", 0), 100) / 100
        return personal * 0.65 + community * 0.25 + popularity * 0.1

    return sorted(candidates, key=score, reverse=True)[:limit]


def section(title: str, detail: str | None = None) -> None:
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)
    if detail:
        st.markdown(f'<div class="muted-small" style="margin-top:-.65rem;margin-bottom:.9rem">{detail}</div>', unsafe_allow_html=True)


def poster_card(movie: dict, index: int, show_match: bool = False) -> None:
    avg = average_rating(movie)
    badge = f"★ {avg:.1f}" if avg else movie["genre"]
    st.markdown(
        f'''<div class="poster">
        <div class="poster-tag">{badge}</div>
        <img src="{movie.get('poster', '')}" alt="Poster for {movie['title']}">
        <div class="poster-copy"><div class="poster-title">{movie['title']}</div>
        <div class="poster-meta">{movie['year']} &nbsp;·&nbsp; {movie['genre']}</div></div></div>''',
        unsafe_allow_html=True,
    )
    if show_match:
        st.caption(f"{movie.get('watch_count', 0)} people watched")
    with st.expander("Details and rate"):
        st.caption(movie.get("tagline", ""))
        st.write(movie.get("description", ""))
        current = movie.get("ratings", {}).get(st.session_state.username, 3)
        rating = st.select_slider("Your rating", [1, 2, 3, 4, 5], value=current, key=f"rate_{index}_{movie['id']}", format_func=lambda value: f"{value} ★")
        if st.button("Save rating", key=f"save_{index}_{movie['id']}", use_container_width=True, type="primary"):
            movie.setdefault("ratings", {})[st.session_state.username] = rating
            movie["watch_count"] = movie.get("watch_count", 0) + 1
            movie.setdefault("watch_history", []).append({"user": st.session_state.username, "time": datetime.now().isoformat(timespec="minutes"), "rating": rating})
            save_movies(st.session_state.movies)
            st.toast("Rating saved — your recommendations have been updated.", icon="⭐")
            st.rerun()


def poster_row(movies: list[dict], key_prefix: str, show_match: bool = False) -> None:
    if not movies:
        st.info("No titles to show yet.")
        return
    columns = st.columns(min(4, len(movies)), gap="medium")
    for index, movie in enumerate(movies):
        with columns[index % len(columns)]:
            poster_card(movie, index + (abs(hash(key_prefix)) % 1000), show_match)


def sign_in() -> None:
    st.markdown('<div class="brand">REEL<span>MATCH</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    st.markdown("## Your next favourite starts here")
    st.markdown('<div class="login-sub">Sign in or create a free account to get recommendations picked for you.</div>', unsafe_allow_html=True)
    login_tab, signup_tab = st.tabs(["Sign in", "Create account"])
    users = st.session_state.users
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username", placeholder="Your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Your password")
            submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if submit:
            record = users.get(username.strip().lower())
            if record and password_matches(password, record):
                st.session_state.username = record["username"]
                st.rerun()
            st.error("Username or password is incorrect.")
    with signup_tab:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username", key="signup_username", placeholder="At least 3 characters")
            new_password = st.text_input("Create a password", key="signup_password", type="password", placeholder="At least 6 characters")
            confirm = st.text_input("Confirm password", key="signup_confirm", type="password")
            submit_signup = st.form_submit_button("Create account", type="primary", use_container_width=True)
        if submit_signup:
            normalized = new_username.strip().lower()
            if not re.fullmatch(r"[a-zA-Z0-9_.-]{3,24}", new_username.strip()):
                st.error("Use 3–24 letters, numbers, dots, dashes, or underscores for your username.")
            elif normalized in users:
                st.error("That username is already taken.")
            elif len(new_password) < 6:
                st.error("Choose a password with at least 6 characters.")
            elif new_password != confirm:
                st.error("The passwords do not match.")
            else:
                users[normalized] = {"username": new_username.strip(), **password_hash(new_password)}
                save_json(USERS_FILE, users)
                st.session_state.users = users
                st.session_state.username = new_username.strip()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#7e7a87;font-size:.75rem;margin-top:1rem'>A lightweight student project demo · Your data is stored locally</div>", unsafe_allow_html=True)


def user_dashboard(username: str) -> None:
    movies = st.session_state.movies
    rated = [movie for movie in movies if username in movie.get("ratings", {})]
    history = [entry | {"Movie": movie["title"]} for movie in movies for entry in movie.get("watch_history", []) if entry.get("user") == username]
    preferred = max(set(m["genre"] for m in rated), key=lambda genre: sum(m["ratings"][username] for m in rated if m["genre"] == genre), default="your next genre")
    st.markdown(f'<div class="eyebrow">YOUR PERSONAL FILM CLUB</div><h1>Good to see you, {username}.</h1><p>Your watchlist is waiting. Here are a few stories we think you’ll love.</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, label, value in [(c1, "Movies rated", len(rated)), (c2, "Watch sessions", len(history)), (c3, "Top genre", preferred)]:
        col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

    recs = recommend_movies(movies, username)
    if recs:
        feature = recs[0]
        st.markdown(f'''<div class="hero" style="background-image:linear-gradient(90deg,rgba(19,16,25,.92) 0%,rgba(19,16,25,.72) 42%,rgba(19,16,25,.06) 100%),linear-gradient(0deg,rgba(19,16,25,.42),transparent 45%),url('{feature['poster']}')">
        <div class="eyebrow">PICKED FOR YOU · {feature['genre'].upper()}</div><h1>{feature['title']}</h1>
        <div class="hero-meta">{feature['year']} &nbsp; · &nbsp; {feature.get('watch_count',0)} plays &nbsp; · &nbsp; ★ {average_rating(feature) or 'New'}</div><p>{feature['description']}</p></div>''', unsafe_allow_html=True)
        with st.expander("Rate this pick"):
            rating = st.select_slider("How would you rate it?", [1, 2, 3, 4, 5], value=3, key="hero_rating", format_func=lambda value: f"{value} ★")
            if st.button("Save rating", key="hero_save", type="primary"):
                feature.setdefault("ratings", {})[username] = rating
                feature["watch_count"] = feature.get("watch_count", 0) + 1
                feature.setdefault("watch_history", []).append({"user": username, "time": datetime.now().isoformat(timespec="minutes"), "rating": rating})
                save_movies(movies)
                st.rerun()
        section("Because you might like these", "Recommendations learn from your ratings, genre preferences, and the community.")
        poster_row(recs[:4], "recommendations", True)
    else:
        st.success("You have rated every title. Add more movies from the catalogue to get fresh recommendations.")

    left, right = st.columns([1.2, 1])
    with left:
        section("Trending this week")
        for movie in sorted(movies, key=lambda item: item.get("watch_count", 0), reverse=True)[:5]:
            avg = average_rating(movie)
            st.markdown(f"**{movie['title']}**  \n<span class='muted-small'>{movie['genre']} · {movie.get('watch_count',0)} plays · {f'{avg:.1f} ★' if avg else 'New'}</span>", unsafe_allow_html=True)
            st.progress(min(movie.get("watch_count", 0) / max(1, max(m.get("watch_count", 0) for m in movies)), 1.0))
    with right:
        section("Popular genres")
        genre_counts = pd.Series([movie["genre"] for movie in movies]).value_counts().rename_axis("Genre").to_frame("Titles")
        st.bar_chart(genre_counts, color="#ff4d67", height=250)

    section("Your viewing activity")
    activity_tab, ratings_tab = st.tabs(["Watch history", "Rating log"])
    with activity_tab:
        if history:
            st.dataframe(pd.DataFrame([{"Movie": entry["Movie"], "Watched": entry.get("time", ""), "Rating": f"{entry.get('rating', '-')}/5"} for entry in sorted(history, key=lambda x: x.get("time", ""), reverse=True)]), hide_index=True, use_container_width=True)
        else:
            st.info("Rate a movie to start building your watch history.")
    with ratings_tab:
        if rated:
            st.bar_chart(pd.DataFrame({"Your rating": [movie["ratings"][username] for movie in rated]}, index=[movie["title"] for movie in rated]), color="#ff4d67")
        else:
            st.info("Your ratings and rating insights will appear here.")


def browse_movies(username: str) -> None:
    st.markdown('<div class="eyebrow">THE REELMATCH LIBRARY</div>', unsafe_allow_html=True)
    st.title("Find your next favourite")
    st.write("Search the catalogue, explore a genre, and tell us what you think.")
    search_col, genre_col = st.columns([2, 1])
    query = search_col.text_input("Search movies", placeholder="Search titles, genres, or stories…", label_visibility="collapsed")
    genre = genre_col.selectbox("Genre", ["All genres"] + sorted({movie["genre"] for movie in st.session_state.movies}), label_visibility="collapsed")
    results = [movie for movie in st.session_state.movies if (not query or query.lower() in (movie["title"] + " " + movie["genre"] + " " + movie.get("description", "")).lower()) and (genre == "All genres" or movie["genre"] == genre)]
    st.caption(f"{len(results)} title{'s' if len(results) != 1 else ''} to explore")
    if not results:
        st.info("No films match that search. Try another title or genre.")
    for start in range(0, len(results), 4):
        poster_row(results[start:start + 4], f"browse_{start}")


def admin_console() -> None:
    st.markdown('<div class="eyebrow">RESTRICTED AREA</div>', unsafe_allow_html=True)
    st.title("Studio control room")
    if not st.session_state.get("admin_authenticated"):
        st.write("Sign in with the administrator access key to manage the catalogue and view engagement.")
        with st.form("admin_login"):
            key = st.text_input("Administrator key", type="password")
            submitted = st.form_submit_button("Unlock control room", type="primary")
        if submitted:
            if hmac.compare_digest(key, ADMIN_KEY):
                st.session_state.admin_authenticated = True
                st.rerun()
            st.error("That administrator key is not correct.")
        st.caption("Demo key: movieadmin123 · Configure ADMIN_KEY in deployment secrets before publishing.")
        return

    if st.button("Lock admin session"):
        st.session_state.admin_authenticated = False
        st.rerun()
    movies = st.session_state.movies
    a, b, c = st.columns(3)
    a.metric("Catalogue titles", len(movies))
    b.metric("Recorded plays", sum(movie.get("watch_count", 0) for movie in movies))
    c.metric("Community ratings", sum(len(movie.get("ratings", {})) for movie in movies))
    manage_tab, trends_tab = st.tabs(["Manage catalogue", "Engagement insights"])
    with manage_tab:
        add_tab, edit_tab = st.tabs(["Add a movie", "Edit or remove"])
        with add_tab:
            with st.form("add_movie", clear_on_submit=True):
                title = st.text_input("Movie title")
                genre = st.selectbox("Genre", GENRES)
                year = st.number_input("Release year", 1888, 2100, 2025)
                description = st.text_area("Short synopsis")
                poster = st.text_input("Poster image URL", placeholder="https://…")
                if st.form_submit_button("Add to catalogue", type="primary"):
                    if not title.strip():
                        st.error("Please enter a movie title.")
                    elif any(movie["title"].lower() == title.strip().lower() for movie in movies):
                        st.error("A title with that name is already in the catalogue.")
                    else:
                        movies.append({"id": max((movie["id"] for movie in movies), default=0) + 1, "title": title.strip(), "genre": genre, "year": int(year), "description": description.strip(), "tagline": "A story worth discovering", "poster": poster.strip() or SAMPLE_MOVIES[5]["poster"], "watch_count": 0, "ratings": {}, "watch_history": []})
                        save_movies(movies)
                        st.success("Movie added.")
                        st.rerun()
        with edit_tab:
            if movies:
                selected_id = st.selectbox("Select a title", [movie["id"] for movie in movies], format_func=lambda movie_id: next(movie["title"] for movie in movies if movie["id"] == movie_id))
                selected = next(movie for movie in movies if movie["id"] == selected_id)
                with st.form("edit_movie"):
                    edit_title = st.text_input("Title", selected["title"])
                    edit_genre = st.selectbox("Genre", GENRES, index=GENRES.index(selected["genre"]) if selected["genre"] in GENRES else 0)
                    edit_year = st.number_input("Year", 1888, 2100, int(selected["year"]))
                    edit_description = st.text_area("Synopsis", selected.get("description", ""))
                    edit_poster = st.text_input("Poster image URL", selected.get("poster", ""))
                    save_edit = st.form_submit_button("Save changes", type="primary")
                if save_edit:
                    selected.update({"title": edit_title.strip(), "genre": edit_genre, "year": int(edit_year), "description": edit_description.strip(), "poster": edit_poster.strip()})
                    save_movies(movies)
                    st.success("Movie updated.")
                    st.rerun()
                if st.button("Remove this movie", type="secondary"):
                    st.session_state.movies = [movie for movie in movies if movie["id"] != selected_id]
                    save_movies(st.session_state.movies)
                    st.success("Movie removed.")
                    st.rerun()
            else:
                st.info("The catalogue is empty.")
    with trends_tab:
        if movies:
            engagement = pd.DataFrame([{"Movie": movie["title"], "Genre": movie["genre"], "Plays": movie.get("watch_count", 0), "Average rating": round(average_rating(movie) or 0, 1)} for movie in movies]).sort_values("Plays", ascending=False)
            st.subheader("Most watched movies")
            st.bar_chart(engagement.head(8).set_index("Movie")["Plays"], color="#ff4d67")
            st.dataframe(engagement, hide_index=True, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="ReelMatch | Movie discovery", page_icon="🎬", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    # Re-read on each Streamlit rerun so edits to the supplied catalogue or
    # persisted JSON are visible without requiring a new browser session.
    st.session_state.movies = load_movies()
    if "users" not in st.session_state:
        st.session_state.users = load_users()
    if "username" not in st.session_state:
        st.session_state.username = ""
    if not st.session_state.username:
        sign_in()
        return

    with st.sidebar:
        st.markdown('<div class="brand">REEL<span>MATCH</span></div>', unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.username}**  \n<span class='muted-small'>MEMBER</span>", unsafe_allow_html=True)
        if st.button("Sign out", use_container_width=True):
            st.session_state.username = ""
            st.rerun()
        st.divider()
        page = st.radio("YOUR SPACE", ["For you", "Explore movies", "Admin console"], label_visibility="visible")
        st.divider()
        st.markdown("<span class='muted-small'>Your ratings help us discover your taste and improve your picks.</span>", unsafe_allow_html=True)

    if page == "Admin console":
        admin_console()
    elif page == "Explore movies":
        browse_movies(st.session_state.username)
    else:
        user_dashboard(st.session_state.username)


if __name__ == "__main__":
    main()
