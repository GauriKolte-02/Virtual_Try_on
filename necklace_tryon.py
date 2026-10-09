# =========================
# necklace_tryon.py
# =========================

import cv2
import mediapipe as mp
import numpy as np
import os
import sys


INPUT_IMAGE = sys.argv[1] if len(sys.argv) > 1 else "input/test.png"
OUTPUT_IMAGE = sys.argv[2] if len(sys.argv) > 2 else "output/necklace_tryon.jpg"
NECKLACE_IMAGE = "jewellery/necklaces/necklace1.png"


# ---------------------------------------------------------
# LOAD PERSON
# ---------------------------------------------------------

person = cv2.imread(INPUT_IMAGE)

if person is None:
    print("ERROR: Cannot load:", INPUT_IMAGE)
    sys.exit(1)


# ---------------------------------------------------------
# LOAD NECKLACE
# ---------------------------------------------------------

necklace = cv2.imread(
    NECKLACE_IMAGE,
    cv2.IMREAD_UNCHANGED
)

if necklace is None:
    print("ERROR: Cannot load:", NECKLACE_IMAGE)
    sys.exit(1)


# ---------------------------------------------------------
# ALPHA
# ---------------------------------------------------------

if necklace.shape[2] == 4:

    necklace_bgr = necklace[:, :, :3]
    alpha = necklace[:, :, 3]

else:

    necklace_bgr = necklace

    gray = cv2.cvtColor(
        necklace_bgr,
        cv2.COLOR_BGR2GRAY
    )

    # Background connected to borders
    flood = np.zeros_like(gray)

    for seed in [
        (0, 0),
        (gray.shape[1]-1, 0),
        (0, gray.shape[0]-1),
        (gray.shape[1]-1, gray.shape[0]-1)
    ]:

        temp = gray.copy()

        mask = np.zeros(
            (
                gray.shape[0] + 2,
                gray.shape[1] + 2
            ),
            np.uint8
        )

        cv2.floodFill(
            temp,
            mask,
            seed,
            255,
            loDiff=15,
            upDiff=15
        )

        flood = cv2.bitwise_or(
            flood,
            mask[1:-1, 1:-1]
        )

    alpha = np.where(
        flood > 0,
        0,
        255
    ).astype(np.uint8)


# ---------------------------------------------------------
# CROP
# ---------------------------------------------------------

points = cv2.findNonZero(alpha)

if points is None:
    print("ERROR: Empty necklace.")
    sys.exit(1)

x, y, w, h = cv2.boundingRect(points)

necklace_bgr = necklace_bgr[
    y:y+h,
    x:x+w
]

alpha = alpha[
    y:y+h,
    x:x+w
]


# ---------------------------------------------------------
# FACE LANDMARKS
# ---------------------------------------------------------

mp_face_mesh = mp.solutions.face_mesh

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as mesh:

    rgb = cv2.cvtColor(
        person,
        cv2.COLOR_BGR2RGB
    )

    result = mesh.process(rgb)


if not result.multi_face_landmarks:
    print("ERROR: Face not detected.")
    sys.exit(1)


face = result.multi_face_landmarks[0]

img_h, img_w = person.shape[:2]


# ---------------------------------------------------------
# FACE WIDTH
# ---------------------------------------------------------

left_face = face.landmark[234]
right_face = face.landmark[454]

left_x = int(
    left_face.x * img_w
)

right_x = int(
    right_face.x * img_w
)

face_width = abs(
    right_x - left_x
)

center_x = (
    left_x + right_x
) // 2


# ---------------------------------------------------------
# CHIN
# ---------------------------------------------------------

chin = face.landmark[152]

chin_y = int(
    chin.y * img_h
)


# ---------------------------------------------------------
# SIZE
# ---------------------------------------------------------

original_h, original_w = alpha.shape

target_width = int(
    face_width * 0.65
)

target_width = max(
    190,
    min(
        target_width,
        300
    )
)

target_height = int(
    original_h *
    target_width /
    original_w
)

necklace_bgr = cv2.resize(
    necklace_bgr,
    (
        target_width,
        target_height
    ),
    interpolation=cv2.INTER_AREA
)

alpha = cv2.resize(
    alpha,
    (
        target_width,
        target_height
    ),
    interpolation=cv2.INTER_AREA
)


# ---------------------------------------------------------
# POSITION
# ---------------------------------------------------------

necklace_x = int(
    center_x -
    target_width / 2
)

necklace_y = int(
    chin_y +
    face_width * 0.08
)


# ---------------------------------------------------------
# OVERLAY
# ---------------------------------------------------------

x1 = max(
    0,
    necklace_x
)

y1 = max(
    0,
    necklace_y
)

x2 = min(
    img_w,
    necklace_x + target_width
)

y2 = min(
    img_h,
    necklace_y + target_height
)

sx1 = x1 - necklace_x
sy1 = y1 - necklace_y

sx2 = sx1 + (x2 - x1)
sy2 = sy1 + (y2 - y1)

fg = necklace_bgr[
    sy1:sy2,
    sx1:sx2
]

a = (
    alpha[
        sy1:sy2,
        sx1:sx2
    ].astype(np.float32)
    / 255.0
)

a = a[:, :, None]

bg = person[
    y1:y2,
    x1:x2
].astype(np.float32)

fg = fg.astype(np.float32)

person[
    y1:y2,
    x1:x2
] = (
    a * fg +
    (1 - a) * bg
).astype(np.uint8)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_IMAGE) or ".",
    exist_ok=True
)

cv2.imwrite(
    OUTPUT_IMAGE,
    person
)

print("NECKLACE TRY-ON SUCCESS")
print("Saved:", OUTPUT_IMAGE)