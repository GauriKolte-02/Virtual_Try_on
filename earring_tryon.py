import cv2
import numpy as np
import os
import sys

# ============================================================
# FILES
# ============================================================

INPUT_IMAGE = sys.argv[1] if len(sys.argv) > 1 else "input/test.png"
OUTPUT_IMAGE = sys.argv[2] if len(sys.argv) > 2 else "output/earring_test.jpg"

EARRING_IMAGE = "jewellery/earrings/earring1.png"


# ============================================================
# LOAD CUSTOMER IMAGE
# ============================================================

person = cv2.imread(INPUT_IMAGE)

if person is None:
    print("ERROR: Cannot load:", INPUT_IMAGE)
    sys.exit(1)

H, W = person.shape[:2]

print("Customer image:", W, "x", H)


# ============================================================
# LOAD EARRING PAIR IMAGE
# ============================================================

pair = cv2.imread(
    EARRING_IMAGE,
    cv2.IMREAD_COLOR
)

if pair is None:
    print("ERROR: Cannot load:", EARRING_IMAGE)
    sys.exit(1)

pair_h, pair_w = pair.shape[:2]

print("Jewellery image:", pair_w, "x", pair_h)


# ============================================================
# IMPORTANT
#
# YOUR JEWELLERY IMAGE CONTAINS TWO EARRINGS.
#
# We take ONLY THE RIGHT EARRING.
#
# Approximate crop based on the uploaded jewellery image:
#
#        LEFT EARRING     RIGHT EARRING
#             |                 |
#             ↓                 ↓
#        -----------------------------
#        |             |             |
#        |             |    ONE      |
#        |             |   EARRING   |
#        |             |             |
#        -----------------------------
#
# ============================================================

# Right earring crop
x1 = int(pair_w * 0.50)
x2 = int(pair_w * 0.80)

y1 = int(pair_h * 0.20)
y2 = int(pair_h * 0.88)

single = pair[
    y1:y2,
    x1:x2
]


# ============================================================
# CREATE TRANSPARENCY
#
# White background becomes transparent.
# Gold earring remains.
# ============================================================

gray = cv2.cvtColor(
    single,
    cv2.COLOR_BGR2GRAY
)

alpha = np.where(
    gray < 245,
    255,
    0
).astype(np.uint8)


# Smooth the mask slightly
kernel = np.ones(
    (2, 2),
    np.uint8
)

alpha = cv2.morphologyEx(
    alpha,
    cv2.MORPH_OPEN,
    kernel
)


# ============================================================
# REMOVE EMPTY BORDER
# ============================================================

points = cv2.findNonZero(alpha)

if points is None:
    print("ERROR: Could not isolate single earring.")
    sys.exit(1)

x, y, w, h = cv2.boundingRect(points)

single = single[
    y:y+h,
    x:x+w
]

alpha = alpha[
    y:y+h,
    x:x+w
]


# ============================================================
# RESIZE ONE EARRING
# ============================================================

original_h, original_w = alpha.shape

target_h = int(H * 0.10)

target_h = max(
    40,
    min(target_h, 65)
)

target_w = int(
    original_w *
    target_h /
    original_h
)


single = cv2.resize(
    single,
    (target_w, target_h),
    interpolation=cv2.INTER_AREA
)

alpha = cv2.resize(
    alpha,
    (target_w, target_h),
    interpolation=cv2.INTER_AREA
)


# ============================================================
# OVERLAY FUNCTION
# ============================================================

def put_earring(
    background,
    jewellery,
    alpha,
    center_x,
    top_y,
    mirror=False
):

    if mirror:

        jewellery = cv2.flip(
            jewellery,
            1
        )

        alpha = cv2.flip(
            alpha,
            1
        )


    eh, ew = alpha.shape

    x = int(
        center_x - ew / 2
    )

    y = int(top_y)


    x1 = max(0, x)
    y1 = max(0, y)

    x2 = min(
        background.shape[1],
        x + ew
    )

    y2 = min(
        background.shape[0],
        y + eh
    )


    if x1 >= x2 or y1 >= y2:
        return background


    sx1 = x1 - x
    sy1 = y1 - y

    sx2 = sx1 + (x2 - x1)
    sy2 = sy1 + (y2 - y1)


    fg = jewellery[
        sy1:sy2,
        sx1:sx2
    ].astype(np.float32)

    bg = background[
        y1:y2,
        x1:x2
    ].astype(np.float32)

    a = alpha[
        sy1:sy2,
        sx1:sx2
    ].astype(np.float32) / 255.0

    a = a[:, :, None]


    result = (
        fg * a +
        bg * (1.0 - a)
    )


    background[
        y1:y2,
        x1:x2
    ] = result.astype(np.uint8)


    return background


# ============================================================
# POSITIONS
#
# For your current 430 x 501 customer image.
# ============================================================

scale_x = W / 430.0
scale_y = H / 501.0


LEFT_X = int(155 * scale_x)
RIGHT_X = int(275 * scale_x)

TOP_Y = int(205 * scale_y)


# ============================================================
# EXACTLY ONE EARRING — LEFT
# ============================================================

person = put_earring(
    person,
    single,
    alpha,
    LEFT_X,
    TOP_Y,
    mirror=False
)


# ============================================================
# EXACTLY ONE EARRING — RIGHT
# ============================================================

person = put_earring(
    person,
    single,
    alpha,
    RIGHT_X,
    TOP_Y,
    mirror=True
)


# ============================================================
# SAVE
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_IMAGE) or ".",
    exist_ok=True
)

cv2.imwrite(
    OUTPUT_IMAGE,
    person
)


print()
print("========================================")
print(" SUCCESS")
print("========================================")
print("ONE earring  -> LEFT EAR")
print("ONE earring  -> RIGHT EAR")
print("TOTAL        -> ONE PAIR / 2")
print("========================================")
print("Saved:", OUTPUT_IMAGE)
print("========================================")