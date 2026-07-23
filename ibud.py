import os
import re
import uuid
from datetime import date, time

import streamlit as st
from supabase import Client, create_client


st.set_page_config(page_title="iBud", page_icon="🤝", layout="wide")

# Put these values in .streamlit/secrets.toml when you deploy.  Never use a
# service-role key in a Streamlit app.

SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "https://xbdlzzjparnvrsvsjfca.supabase.co"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiZGx6empwYXJudnJzdnNqZmNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MzQ0NDYsImV4cCI6MjA5MzUxMDQ0Nn0.h0AxxjVJZWpTCkywH-Et30TCn4nKQwGXfvmPbVmgZJo"
))

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets before running iBud.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ACTIVITIES = [
    ("☕", "Coffee"), ("🍽️", "Lunch"), ("🚶", "Walk"),
    ("🏃", "Exercise"), ("📚", "Study"), ("🎬", "Movie"),
    ("🛍️", "Shopping"), ("🎾", "Sports"), ("🎮", "Gaming"),
    ("🎵", "Music"), ("🐕", "Dog Walk"), ("➕", "Other"),
]
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$")
MAX_APPLICANTS = 5


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def default_title(category: str, purpose: str) -> str:
    if purpose == "Offering":
        return f"Available for {category}"
    return f"Looking for a {category} buddy"


def upload_image(image, folder: str) -> str | None:
    """Upload one image and return its public URL. The ibud_images bucket must be public."""
    if image is None:
        return None

    extension = image.name.rsplit(".", 1)[-1].lower()
    file_path = f"{folder}/{uuid.uuid4().hex}.{extension}"
    supabase.storage.from_("ibud_images").upload(
        file_path,
        image.getvalue(),
        {"content-type": image.type or "image/jpeg", "upsert": "false"},
    )
    return supabase.storage.from_("ibud_images").get_public_url(file_path)


def create_post(category: str, purpose: str, title: str, description: str, city: str,
                activity_date: date, activity_time: time, email: str, image_url: str | None):
    return supabase.table("ibud_posts").insert({
        "category": category,
        "purpose": purpose,
        "title": title,
        "description": description,
        "city": city,
        "activity_date": activity_date.isoformat(),
        "activity_time": activity_time.isoformat(),
        "email": email,
        "image_url": image_url,
    }).execute()


def post_form(category: str, purpose: str):
    st.subheader(f"{purpose}: {category}")
    st.caption(
        "Offering creates a simple availability ad with one photo. "
        "Wanted accepts up to five buddy applications."
    )
    prefix = f"{category}_{purpose}"
    title = st.text_input("Title", value=default_title(category, purpose), key=f"{prefix}_title")
    description = st.text_area("About the plan", key=f"{prefix}_description")
    city = st.text_input("City", key=f"{prefix}_city")
    left, right = st.columns(2)
    activity_date = left.date_input("Date", key=f"{prefix}_date")
    activity_time = right.time_input("Time", key=f"{prefix}_time")
    email = st.text_input("Your email", key=f"{prefix}_email")
    image = st.file_uploader("Your photo (one image)", type=["jpg", "jpeg", "png"], key=f"{prefix}_image")

    if st.button("Publish ad", key=f"{prefix}_publish", type="primary"):
        if not title.strip() or not description.strip() or not city.strip():
            st.error("Please complete the title, plan, and city.")
        elif not is_valid_email(email):
            st.error("Enter a valid email address.")
        elif image is None:
            st.error("Please add one photo.")
        else:
