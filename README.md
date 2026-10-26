# ReelMatch Movie Recommendation System

ReelMatch is a small Streamlit project for the movie recommendation assignment. It includes account registration and sign-in, a poster-based movie catalogue, search and genre filtering, ratings, personalized recommendations, watch history, dashboard charts, and an admin console.

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `streamlit run app.py` from this folder.
4. Create an account in the **Create account** tab, then use **Explore movies** to rate titles.

The app creates `movies.json` and `users.json` the first time it runs. Passwords are stored as salted PBKDF2 hashes rather than plain text. This lightweight file-based account system is for a student demonstration, not a production service.

## Admin access

The demo admin key is `movieadmin123`. Set an environment variable named `ADMIN_KEY` to a private value before deployment. On Streamlit Community Cloud, add `ADMIN_KEY = "your-private-key"` in the app's **Settings → Secrets**. The admin console supports adding, editing, and removing movies and reviewing engagement charts.

## Deploy to Streamlit Community Cloud

Push this folder to a GitHub repository, create a Streamlit Community Cloud app with `app.py` as the main file, and set `ADMIN_KEY` in the app's Secrets settings. Streamlit installs packages from `requirements.txt`. Use the generated public app URL in the assignment documentation. Movie and user data are stored in local JSON files for this simple demo; hosted file writes may not survive restarts, and a shared persistent database would be needed for durable multi-user use.

## Recommendation approach

The app ranks unrated films using the viewer's average rating for a genre (65%), the film's community average rating (25%), and a small capped popularity signal (10%). Saving a rating immediately updates genre preference, community rating, viewing history, and the play count, which changes the next recommendation refresh. This is an explainable recommendation heuristic rather than a trained machine-learning model.
