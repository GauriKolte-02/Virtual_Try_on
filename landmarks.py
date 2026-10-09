import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Read image
image = cv2.imread("input/test.png")

if image is None:
    print("ERROR: Could not find input/test.png")
    exit()

# Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect facial landmarks
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as face_mesh:

    results = face_mesh.process(rgb_image)

# Check if face was detected
if results.multi_face_landmarks:

    print("Face landmarks detected!")

    for face_landmarks in results.multi_face_landmarks:

        # Draw all 468 landmarks
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style()
        )

    # Save output
    cv2.imwrite("output/landmarks.jpg", image)

    print("Result saved to output/landmarks.jpg")

else:
    print("No face landmarks detected.")