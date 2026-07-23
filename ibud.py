import streamlit as st
from supabase import create_client, Client
import re


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

st.title(
    "🤝 iBud"
)

st.caption(
    "Find someone to share an activity with today."
)



# ==========================================================
# UPLOAD IMAGE
# ==========================================================

def upload_image(image):

    if image is None:

        return None


    file_name = image.name


    supabase.storage.from_(
        "ibud_images"
    ).upload(
        file_name,
        image.getvalue()
    )


    image_url = (

        SUPABASE_URL

        + "/storage/v1/object/public/ibud_images/"

        + file_name

    )


    return image_url



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
    image_url

):

    data = {

        "category": category,

        "purpose": purpose,

        "description": description,

        "city": city,

        "activity_date": str(activity_date),

        "activity_time": str(activity_time),

        "email": email,

        "image_url": image_url

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
# POST FORM
# ==========================================================

def post_form(category, purpose):


    st.subheader(
        f"{purpose}: {category}"
    )


    description = st.text_area(
        "Description"
    )


    city = st.text_input(
        "City"
    )


    activity_date = st.date_input(
        "Date"
    )


    activity_time = st.time_input(
        "Time"
    )


    email = st.text_input(
        "Email"
    )


    image = st.file_uploader(
        "Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )


    if st.button(
        "Post"
    ):


        if not valid_email(email):

            st.error(
                "Please enter a valid email."
            )

            return



        image_url = upload_image(
            image
        )


        save_post(

            category,

            purpose,

            description,

            city,

            activity_date,

            activity_time,

            email,

            image_url

        )


        st.success(
            "Post created successfully!"
        )



# ==========================================================
# SHOW POSTS
# ==========================================================

def show_posts(category):


    st.subheader(
        f"📋 {category} Posts"
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


                if post.get("image_url"):

                    st.image(
                        post["image_url"],
                        width=200,
                        caption="Image"
                    )


                st.write(
                    "### " + category
                )


                st.write(
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
                    "🗑 Delete Post",
                    key=f"delete_{post['id']}"
                ):


                    delete_post(
                        post["id"]
                    )

                    st.rerun()


                st.divider()



    else:

        st.info(
            "No posts found."
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

            st.session_state.purpose = "Offering"



    with col2:

        if st.button(
            "🟢 Wanted",
            key=f"{category}_wanted"
        ):

            st.session_state.purpose = "Wanted"



    if "purpose" in st.session_state:


        action = st.radio(
            "Action",
            [
                "Post",
                "View Posts"
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


        category = activity.split(
            " ",
            1
        )[1]


        st.header(
            activity
        )


        choose_purpose(
            category
        )

# ==========================================================
# POST FORM
# ==========================================================
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


    image = st.file_uploader(
        "Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key=f"{category}_{purpose}_image"
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



        image_url = upload_image(
            image
        )


        data = {

            "category": category,

            "purpose": purpose,

            "description": description,

            "city": city,

            "activity_date": str(activity_date),

            "activity_time": str(activity_time),

            "email": email,

            "image_url": image_url

        }


        supabase.table(
            "ibud_posts"
        ).insert(
            data
        ).execute()



        st.success(
            "Post created successfully!"
        )



# ==========================================================
# APPLY TO WANTED POST
# ==========================================================

def apply_to_post(post_id):


    st.subheader(
        "🙋 Apply"
    )


    name = st.text_input(
        "Name",
        key=f"apply_name_{post_id}"
    )


    email = st.text_input(
        "Email",
        key=f"apply_email_{post_id}"
    )


    image = st.file_uploader(
        "Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key=f"apply_image_{post_id}"
    )



    if st.button(
        "Apply",
        key=f"apply_button_{post_id}"
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
                "Maximum 5 applicants."
            )

            return



        image_url = upload_image(
            image
        )



        supabase.table(
            "ibud_applicants"
        ).insert({

            "post_id": post_id,

            "name": name,

            "email": email,

            "image_url": image_url,

            "status": "pending"

        }).execute()



        st.success(
            "Application sent!"
        )

        st.rerun()



# ==========================================================
# SHOW APPLICANTS
# ==========================================================

def show_applicants(post_id):


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
            post_id
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



            if applicant.get("image_url"):


                st.image(
                    applicant["image_url"],
                    width=150
                )



            st.write(
                "👤",
                applicant["name"]
            )


            st.write(
                "📧",
                applicant["email"]
            )



            col1, col2 = st.columns(2)



            with col1:

                if st.button(

                    "✅ Accept",

                    key=f"accept_{applicant['id']}"

                ):


                    supabase.table(
                        "ibud_applicants"
                    ).update({

                        "status":"accepted"

                    }).eq(

                        "id",
                        applicant["id"]

                    ).execute()


                    st.success(
                        "Accepted"
                    )

                    st.rerun()



            with col2:

                if st.button(

                    "❌ Reject",

                    key=f"reject_{applicant['id']}"

                ):


                    supabase.table(
                        "ibud_applicants"
                    ).update({

                        "status":"rejected"

                    }).eq(

                        "id",
                        applicant["id"]

                    ).execute()


                    st.success(
                        "Rejected"
                    )

                    st.rerun()



        else:


            st.info(
                "Empty position"
            )



# ==========================================================
# SHOW POSTS
# ==========================================================

def show_posts(category):


    st.subheader(
        f"📋 {category} Posts"
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



    for post in posts:


        with st.container():


            if post.get("image_url"):


                st.image(
                    post["image_url"],
                    width=200
                )



            st.write(
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



            # Wanted gets applicants

            if post["purpose"] == "Wanted":


                show_applicants(
                    post["id"]
                )


                apply_to_post(
                    post["id"]
                )



            if st.button(

                "🗑 Delete Post",

                key=f"delete_{post['id']}"

            ):


                supabase.table(
                    "ibud_posts"
                ).delete().eq(

                    "id",

                    post["id"]

                ).execute()


                st.rerun()



            st.divider()
