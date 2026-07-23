import streamlit as st
from supabase import create_client, Client
import re

from PIL import Image
import io
import base64


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="iBud",
    page_icon="🤝",
    layout="wide"
)


# ==========================================================
# SUPABASE CONNECTION
# ==========================================================

SUPABASE_URL = "https://xbdlzzjparnvrsvsjfca.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiZGx6empwYXJudnJzdnNqZmNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MzQ0NDYsImV4cCI6MjA5MzUxMDQ0Nn0.h0AxxjVJZWpTCkywH-Et30TCn4nKQwGXfvmPbVmgZJo"


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email)



# ==========================================================
# TITLE
# ==========================================================

st.title("🤝 iBud")

st.caption(
    "Find someone to do something with today."
)


# ==========================================================
# SAVE POST
# ==========================================================

def save_post(
    category,
    purpose,
    title,
    description,
    city,
    activity_date,
    activity_time,
    email,
    photo
):

    photo_data = None

    if photo:

        photo_data = base64.b64encode(
            photo.read()
        ).decode()


    data = {

        "category": category,

        "purpose": purpose,

        "title": title,

        "description": description,

        "city": city,

        "activity_date": str(activity_date),

        "activity_time": str(activity_time),

        "email": email,

        "photo_url": photo_data

    }


    supabase.table(
        "ibud_posts"
    ).insert(
        data
    ).execute()



# ==========================================================
# DELETE POST
# ==========================================================

def delete_post(post_id):

    supabase.table(
        "ibud_posts"
    ).delete().eq(
        "id",
        post_id
    ).execute()



# ==========================================================
# SHOW LISTINGS
# ==========================================================

def show_posts(category):


    st.subheader(
        f"📋 {category} Listings"
    )


    response = (

        supabase

        .table(
            "ibud_posts"
        )

        .select("*")

        .eq(
            "category",
            category
        )

        .execute()

    )


    posts = response.data


    if posts:


        for post in posts:


            with st.container():


                st.write(
                    "### " + post["title"]
                )


                st.write(
                    "Type:",
                    post["purpose"]
                )


                st.write(
                    post["description"]
                )


                st.write(
                    "📍",
                    post["city"]
                )


                st.write(
                    "📅",
                    post["activity_date"]
                )


                st.write(
                    "🕒",
                    post["activity_time"]
                )


                st.write(
                    "📧",
                    post["email"]
                )


                if st.button(
                    "🗑 Delete",
                    key=f"delete_{post['id']}"
                ):

                    delete_post(
                        post["id"]
                    )

                    st.success(
                        "Listing deleted"
                    )

                    st.rerun()


                st.divider()


    else:

        st.info(
            "No listings found."
        )



# ==========================================================
# POST FORM
# ==========================================================

def post_form(category, purpose):

    st.subheader(
        f"{purpose}: {category}"
    )

    title = st.text_input(
        "Title",
        key=f"{category}_{purpose}_title"
    )

    description = st.text_area(
        "Description",
        key=f"{category}_{purpose}_description"
    )

    city = st.text_input(
        "City",
        key=f"{category}_{purpose}_city"
    )

    activity_date = st.date_input(
        "Date",
        key=f"{category}_{purpose}_date"
    )

    activity_time = st.time_input(
        "Time",
        key=f"{category}_{purpose}_time"
    )

    email = st.text_input(
        "Email",
        key=f"{category}_{purpose}_email"
    )

    photo = st.file_uploader(
        "Your Photo (1 picture only)",
        type=["jpg", "jpeg", "png"],
        key=f"{category}_{purpose}_photo"
    )
    if photo:
        image = Image.open(photo)
        st.image(
            image,
            caption="Your profile photo",
            width=200
        )

    if st.button(
        "Post",
        key=f"{category}_{purpose}_post"
    ):

        if not valid_email(email):

            st.error(
                "Please enter a valid email."
            )

            return

        save_post(
            category,
            purpose,
            title,
            description,
            city,
            activity_date,
            activity_time,
            email,
            photo
        )

        st.success(
            "Post created successfully!"
        )



# ==========================================================
# OFFERING / WANTED
# ==========================================================

def choose_purpose(category):


    col1, col2 = st.columns(2)


    if "purpose" not in st.session_state:

        st.session_state.purpose = None



    with col1:

        if st.button(
            "🔵 Offering",
            key=f"{category}_offer"
        ):

            st.session_state.purpose = "Offering"



    with col2:

        if st.button(
            "🟢 Wanted",
            key=f"{category}_wanted"
        ):

            st.session_state.purpose = "Wanted"



    if st.session_state.purpose:


        action = st.radio(

            "Choose Action",

            [
                "Post",
                "View Listings"
            ],

            key=f"{category}_action"

        )


        if action == "Post":

            post_form(

                category,

                st.session_state.purpose

            )


        else:

            show_posts(
                category
            )



# ==========================================================
# ACTIVITY TABS
# ==========================================================

coffee, lunch, walk, exercise, study, movie, shopping, sports, gaming, music, dogwalk, other = st.tabs(

    [

        "☕ Coffee",

        "🍽 Lunch",

        "🚶 Walk",

        "🏃 Exercise",

        "📚 Study",

        "🎬 Movie",

        "🛍 Shopping",

        "🎾 Sports",

        "🎮 Gaming",

        "🎵 Music",

        "🐕 Dog Walk",

        "➕ Other"

    ]

)



# ==========================================================
# TABS
# ==========================================================

activities = [

    (coffee, "Coffee"),

    (lunch, "Lunch"),

    (walk, "Walk"),

    (exercise, "Exercise"),

    (study, "Study"),

    (movie, "Movie"),

    (shopping, "Shopping"),

    (sports, "Sports"),

    (gaming, "Gaming"),

    (music, "Music"),

    (dogwalk, "Dog Walk"),

    (other, "Other")

]


for tab, activity in activities:

    with tab:

        st.header(activity)

        choose_purpose(
            activity
        )
