import os
import sys
import subprocess


# =========================================================
# MASTER TRY-ON PIPELINE
# =========================================================

INPUT_IMAGE = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "input/test.png"
)

MODE = (
    sys.argv[2]
    if len(sys.argv) > 2
    else "both"
)


# =========================================================
# OUTPUT FILES
# =========================================================

EARRING_OUTPUT = (
    "output/earring_tryon.jpg"
)

NECKLACE_OUTPUT = (
    "output/necklace_tryon.jpg"
)

FINAL_OUTPUT = (
    "output/final_tryon.jpg"
)

INTERMEDIATE_OUTPUT = (
    "output/earring_result.jpg"
)


# =========================================================
# CREATE OUTPUT FOLDER
# =========================================================

os.makedirs(
    "output",
    exist_ok=True
)


# =========================================================
# CHECK INPUT
# =========================================================

if not os.path.exists(INPUT_IMAGE):

    print(
        "ERROR: Input image not found:"
    )

    print(INPUT_IMAGE)

    sys.exit(1)


# =========================================================
# CLEAN OLD OUTPUTS
# =========================================================

for file in [

    EARRING_OUTPUT,
    NECKLACE_OUTPUT,
    FINAL_OUTPUT,
    INTERMEDIATE_OUTPUT

]:

    if os.path.exists(file):

        try:

            os.remove(file)

        except:

            pass


# =========================================================
# EARRINGS
# =========================================================

def apply_earrings(
    input_image,
    output_image
):

    print()
    print(
        "Applying earrings..."
    )

    process = subprocess.run(

        [
            sys.executable,

            "earring_tryon.py",

            input_image,

            output_image

        ],

        capture_output=True,

        text=True

    )


    print(
        process.stdout
    )


    if process.returncode != 0:

        print(
            process.stderr
        )

        return False


    return os.path.exists(
        output_image
    )


# =========================================================
# NECKLACE
# =========================================================

def apply_necklace(
    input_image,
    output_image
):

    print()
    print(
        "Applying necklace..."
    )

    process = subprocess.run(

        [
            sys.executable,

            "necklace_tryon.py",

            input_image,

            output_image

        ],

        capture_output=True,

        text=True

    )


    print(
        process.stdout
    )


    if process.returncode != 0:

        print(
            process.stderr
        )

        return False


    return os.path.exists(
        output_image
    )


# =========================================================
# EARRINGS ONLY
# =========================================================

if MODE.lower() == "earrings":

    success = apply_earrings(
        INPUT_IMAGE,
        FINAL_OUTPUT
    )


    if success:

        print()
        print(
            "======================================"
        )

        print(
            "      EARRING TRY-ON SUCCESS"
        )

        print(
            "======================================"
        )

        print(
            "Saved:"
        )

        print(
            FINAL_OUTPUT
        )

    else:

        print(
            "Earring try-on failed."
        )

        sys.exit(1)


# =========================================================
# NECKLACE ONLY
# =========================================================

elif MODE.lower() == "necklace":

    success = apply_necklace(
        INPUT_IMAGE,
        FINAL_OUTPUT
    )


    if success:

        print()
        print(
            "======================================"
        )

        print(
            "     NECKLACE TRY-ON SUCCESS"
        )

        print(
            "======================================"
        )

        print(
            "Saved:"
        )

        print(
            FINAL_OUTPUT
        )

    else:

        print(
            "Necklace try-on failed."
        )

        sys.exit(1)


# =========================================================
# BOTH
# =========================================================

else:

    print()
    print(
        "======================================"
    )

    print(
        "      AI JEWELLERY TRY-ON"
    )

    print(
        "======================================"
    )


    # -----------------------------------------------------
    # STEP 1: EARRINGS
    # -----------------------------------------------------

    earrings_success = apply_earrings(

        INPUT_IMAGE,

        INTERMEDIATE_OUTPUT

    )


    if not earrings_success:

        print(
            "Earring step failed."
        )

        sys.exit(1)


    # -----------------------------------------------------
    # STEP 2: NECKLACE
    #
    # IMPORTANT:
    # Use the earring result as input.
    #
    # Original input_image is NEVER modified.
    # -----------------------------------------------------

    necklace_success = apply_necklace(

        INTERMEDIATE_OUTPUT,

        FINAL_OUTPUT

    )


    if not necklace_success:

        print(
            "Necklace step failed."
        )

        sys.exit(1)


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    print()
    print(
        "======================================"
    )

    print(
        "     JEWELLERY TRY-ON SUCCESS"
    )

    print(
        "======================================"
    )

    print()
    print(
        "Original:"
    )

    print(
        INPUT_IMAGE
    )

    print()
    print(
        "Final result:"
    )

    print(
        FINAL_OUTPUT
    )

    print()
    print(
        "Earrings + Necklace applied."
    )