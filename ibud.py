import streamlit as st
from supabase import create_client, Client
import uuid
import re


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="iBud",
    page_icon="👥",
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
# TITLE
# ==========================================================

st.title("👥 iBud")

st.caption(
    "Find someone to share an activity with today."
)


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(
        pattern,
        email
    )


# ==========================================================
# UPLOAD PHOTO
# ==========================================================

def upload_photo(photo):

    if photo is None:

        return None


    file_name = (
        str(uuid.uuid4())
        + ".jpg"
    )


    supabase.storage.from_(
        "ibud_photos"
    ).upload(
        file_name,
        photo.getvalue()
    )


    public_url = (
        SUPABASE_URL
        + "/storage/v1/object/public/ibud_photos/"
        + file_name
    )


    return public_url



# ==========================================================
# SAVE POST
# ==========================================================

def save_post(
    category,
    purpose,
    description,
    city,
    activity_date,
    activity_time,
    email,
    photo
):


    if purpose == "Offering":

        title = (
            f"I am available for {category} today"
        )

    else:

        title = (
            f"Looking for someone for {category} today"
        )


    photo_url = upload_photo(
        photo
    )


    data = {

        "category": category,

        "purpose": purpose,

        "title": title,

        "description": description,

        "city": city,

        "activity_date": str(activity_date),

        "activity_time": str(activity_time),

        "email": email,

        "photo_url": photo_url,

        "status": "active"

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
# APPLY TO WANTED POST
# ==========================================================

def apply_to_post(
    post_id,
    name,
    email,
    photo
):


    existing = (

        supabase.table(
            "ibud_applicants"
        )

        .select("*")

        .eq(
            "post_id",
            post_id
        )

        .execute()

    )


    if len(existing.data) >= 5:

        st.error(
            "This iBud request is full."
        )

        return



    photo_url = upload_photo(
        photo
    )


    data = {

        "post_id": post_id,

        "name": name,

        "email": email,

        "photo_url": photo_url,

        "status": "pending"

    }


    supabase.table(
        "ibud_applicants"
    ).insert(
        data
    ).execute()


    st.success(
        "Application sent!"
    )



# ==========================================================
# DELETE APPLICANT
# ==========================================================

def delete_applicant(applicant_id):

    supabase.table(
        "ibud_applicants"
    ).delete().eq(
        "id",
        applicant_id
    ).execute()



# ==========================================================
# UPDATE APPLICANT STATUS
# ==========================================================

def update_applicant(
    applicant_id,
    status
):

    supabase.table(
        "ibud_applicants"
    ).update(
        {
            "status": status
        }
    ).eq(
        "id",
        applicant_id
    ).execute()

# ==========================================================
# POST FORM
# ==========================================================

def post_form(category, purpose):


    st.subheader(
        f"{purpose}: {category}"
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
        "Your Photo (1 picture)",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key=f"{category}_{purpose}_photo"
    )


    if st.button(
        "Post Ad",
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
            description,
            city,
            activity_date,
            activity_time,
            email,
            photo
        )


        st.success(
            "iBud posted successfully!"
        )



# ==========================================================
# SHOW APPLICANTS
# ==========================================================
# ==========================================================
# SHOW APPLICANTS
# ==========================================================

def show_applicants(post):

    st.subheader(
        "👥 Applicants"
    )


    response = (

        supabase.table(
            "ibud_applicants"
        )

        .select("*")

        .eq(
            "post_id",
            post["id"]
        )

        .execute()

    )


    applicants = response.data


    for i in range(5):

        st.write(
            f"### Applicant {i+1}"
        )


        if i < len(applicants):

            applicant = applicants[i]


            # Applicant photo
            if (
                applicant.get("photo_url")
                and applicant["photo_url"].startswith("http")
            ):

                st.image(
                    applicant["photo_url"],
                    width=150,
                    caption="Applicant Photo"
                )


            st.write(
                "👤",
                applicant["name"]
            )


            st.write(
                "📧",
                applicant["email"]
            )


            st.write(
                "Status:",
                applicant["status"]
            )


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✅ Accept",
                    key=f"accept_{applicant['id']}"
                ):

                    update_applicant(
                        applicant["id"],
                        "accepted"
                    )

                    st.success(
                        "Applicant accepted"
                    )

                    st.rerun()


            with col2:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{applicant['id']}"
                ):

                    update_applicant(
                        applicant["id"],
                        "rejected"
                    )

                    st.success(
                        "Applicant rejected"
                    )

                    st.rerun()


        else:

            st.info(
                "Empty position"
            )



# ==========================================================
# SHOW LISTINGS
# ==========================================================

def show_posts(category):


    st.subheader(
        f"📋 {category} Listings"
    )


    response = (

        supabase.table(
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


                if post["photo_url"]:

                    st.image(
                        post["photo_url"],
                        width=200
                    )


                st.write(
                    "## " + post["title"]
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


                if post["purpose"] == "Wanted":


                    show_applicants(
                        post
                    )


                    st.subheader(
                        "Apply"
                    )


                    name = st.text_input(
                        "Your Name",
                        key=f"name_{post['id']}"
                    )


                    apply_email = st.text_input(
                        "Your Email",
                        key=f"apply_email_{post['id']}"
                    )


                    apply_photo = st.file_uploader(
                        "Your Photo",
                        type=[
                            "jpg",
                            "jpeg",
                            "png"
                        ],
                        key=f"apply_photo_{post['id']}"
                    )


                    if st.button(
                        "Apply",
                        key=f"apply_{post['id']}"
                    ):


                        if valid_email(
                            apply_email
                        ):

                            apply_to_post(
                                post["id"],
                                name,
                                apply_email,
                                apply_photo
                            )

                        else:

                            st.error(
                                "Invalid email"
                            )



                if st.button(
                    "🗑 Delete Ad",
                    key=f"delete_{post['id']}"
                ):


                    delete_post(
                        post["id"]
                    )


                    st.success(
                        "Ad deleted"
                    )


                    st.rerun()



                st.divider()


    else:


        st.info(
            "No iBud listings yet."
        )



# ==========================================================
# OFFERING / WANTED
# ==========================================================

def choose_purpose(category):


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔵 Offering",
            key=f"{category}_offering"
        ):

            st.session_state[
                "purpose"
            ] = "Offering"



    with col2:

        if st.button(
            "🟢 Wanted",
            key=f"{category}_wanted"
        ):

            st.session_state[
                "purpose"
            ] = "Wanted"



    if "purpose" in st.session_state:


        action = st.radio(
            "Action",
            [
                "Post",
                "View Listings"
            ],
            key=f"{category}_action"
        )


        if action == "Post":

            post_form(
                category,
                st.session_state["purpose"]
            )


        else:

            show_posts(
                category
            )



# ==========================================================
# ACTIVITY TABS
# ==========================================================

activities = [

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


tabs = st.tabs(
    activities
)


for tab, activity in zip(
    tabs,
    activities
):

    with tab:

        clean_name = (
            activity
            .split(" ",1)[1]
        )


        st.header(
            activity
        )


        choose_purpose(
            clean_name
        )
