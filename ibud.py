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
# TITLE
# ==========================================================

st.title(
    "🤝 iBud"
)

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

# ==========================================================
# POST FORM
# ==========================================================

def post_form(category, purpose):

    st.subheader(
        f"{purpose}: {category}"
    )

    description = st.text_area(
        "What do you want to do?",
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
        "Image (1 image only)",
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
# APPLY TO WANTED POST
# ==========================================================

def apply_post(post_id):


    name = st.text_input(
        "Your Name",
        key=f"name_{post_id}"
    )


    email = st.text_input(
        "Your Email",
        key=f"email_{post_id}"
    )


    image = st.file_uploader(
        "Your Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key=f"image_{post_id}"
    )


    if st.button(
        "Apply",
        key=f"apply_{post_id}"
    ):


        if not valid_email(email):

            st.error(
                "Invalid email."
            )

            return


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


        if len(response.data) >= 5:

            st.error(
                "Maximum 5 applicants reached."
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
                    width=150,
                    caption="Image"
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


                    supabase.table(
                        "ibud_applicants"
                    ).update({

                        "status": "accepted"

                    }).eq(

                        "id",
                        applicant["id"]

                    ).execute()


                    st.success(
                        "Applicant accepted"
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

                        "status": "rejected"

                    }).eq(

                        "id",
                        applicant["id"]

                    ).execute()


                    st.success(
                        "Applicant rejected"
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
                    width=200,
                    caption="Image"
                )


            st.write(
                "## " + category
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


            # Only Wanted posts get applicants

            if post["purpose"] == "Wanted":


                show_applicants(
                    post["id"]
                )


                apply_post(
                    post["id"]
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
