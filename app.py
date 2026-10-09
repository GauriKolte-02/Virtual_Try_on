# =========================
# app.py
# =========================

import streamlit as st
import os
import subprocess
import sys
from PIL import Image


st.set_page_config(
    page_title="AI Virtual Jewellery Try-On",
    page_icon="💎",
    layout="wide"
)


st.title("💎 AI Virtual Jewellery Try-On")

st.write(
    "Upload your photo and virtually try on jewellery."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

choice = st.sidebar.selectbox(
    "Choose Jewellery",
    [
        "Earrings",
        "Necklace",
        "Earrings + Necklace"
    ]
)


# ---------------------------------------------------------
# UPLOAD
# ---------------------------------------------------------

uploaded = st.file_uploader(
    "Upload your photo",
    type=["jpg", "jpeg", "png"]
)


if uploaded is not None:

    image = Image.open(
        uploaded
    ).convert("RGB")


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Original Photo"
        )

        st.image(
            image,
            use_container_width=True
        )


    if st.button(
        "✨ TRY ON",
        use_container_width=True
    ):

        os.makedirs(
            "input",
            exist_ok=True
        )

        os.makedirs(
            "output",
            exist_ok=True
        )


        # -------------------------------------------------
        # ALWAYS SAVE THE ORIGINAL IMAGE
        # -------------------------------------------------

        original_path = (
            "input/test.png"
        )

        image.save(
            original_path
        )


        # -------------------------------------------------
        # DELETE OLD OUTPUTS
        # -------------------------------------------------

        for file in [
            "output/earring_tryon.jpg",
            "output/necklace_tryon.jpg",
            "output/final_tryon.jpg"
        ]:

            if os.path.exists(file):

                os.remove(file)


        final_output = None
        error = ""


        # =================================================
        # EARRINGS
        # =================================================

        if choice == "Earrings":

            p = subprocess.run(
                [
                    sys.executable,
                    "earring_tryon.py",
                    original_path,
                    "output/earring_tryon.jpg"
                ],
                capture_output=True,
                text=True
            )

            if p.returncode == 0:

                final_output = (
                    "output/earring_tryon.jpg"
                )

            else:

                error = (
                    p.stdout +
                    "\n" +
                    p.stderr
                )


        # =================================================
        # NECKLACE
        # =================================================

        elif choice == "Necklace":

            p = subprocess.run(
                [
                    sys.executable,
                    "necklace_tryon.py",
                    original_path,
                    "output/necklace_tryon.jpg"
                ],
                capture_output=True,
                text=True
            )

            if p.returncode == 0:

                final_output = (
                    "output/necklace_tryon.jpg"
                )

            else:

                error = (
                    p.stdout +
                    "\n" +
                    p.stderr
                )


        # =================================================
        # EARRINGS + NECKLACE
        # =================================================

        else:

            earring_result = (
                "output/earring_tryon.jpg"
            )

            necklace_result = (
                "output/final_tryon.jpg"
            )


            # ---------------------------------------------
            # FIRST: EARRINGS
            # ---------------------------------------------

            p1 = subprocess.run(
                [
                    sys.executable,
                    "earring_tryon.py",
                    original_path,
                    earring_result
                ],
                capture_output=True,
                text=True
            )


            if p1.returncode != 0:

                error = (
                    p1.stdout +
                    "\n" +
                    p1.stderr
                )

            else:

                # -----------------------------------------
                # SECOND: NECKLACE
                #
                # IMPORTANT:
                # Use earring result as input.
                # NEVER overwrite test.png.
                # -----------------------------------------

                p2 = subprocess.run(
                    [
                        sys.executable,
                        "necklace_tryon.py",
                        earring_result,
                        necklace_result
                    ],
                    capture_output=True,
                    text=True
                )


                if p2.returncode != 0:

                    error = (
                        p2.stdout +
                        "\n" +
                        p2.stderr
                    )

                else:

                    final_output = (
                        necklace_result
                    )


        # =================================================
        # SHOW RESULT
        # =================================================

        if (
            final_output is not None
            and
            os.path.exists(final_output)
        ):

            with col2:

                st.subheader(
                    "✨ Virtual Try-On"
                )

                st.image(
                    final_output,
                    use_container_width=True
                )


            st.success(
                "Jewellery applied successfully!"
            )


            with open(
                final_output,
                "rb"
            ) as f:

                st.download_button(
                    "⬇️ Download Result",
                    f,
                    file_name="virtual_jewellery_tryon.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )


        else:

            st.error(
                "Processing failed."
            )

            st.code(
                error
            )


else:

    st.info(
        "👆 Upload a front-facing photo to begin."
    )


st.divider()

st.caption(
    "AI Virtual Jewellery Try-On | "
    "MediaPipe + OpenCV + Streamlit"
)