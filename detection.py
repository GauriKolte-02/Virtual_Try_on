import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Read input image
image = cv2.imread("input/test.png")

# Check if image was loaded
if image is None:
    print("ERROR: Could not find input/test.png")
    exit()

# Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect face
with mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
) as face_detection:

    results = face_detection.process(rgb_image)

# Check whether face was detected
if results.detections:

    print("Face detected!")

    height, width, _ = image.shape

    for detection in results.detections:

        # Get face bounding box
        bbox = detection.location_data.relative_bounding_box

        x = int(bbox.xmin * width)
        y = int(bbox.ymin * height)

        w = int(bbox.width * width)
        h = int(bbox.height * height)

        # Keep coordinates inside image
        x = max(0, x)
        y = max(0, y)

        # Draw rectangle around face
        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    # Save result
    cv2.imwrite("output/face_detected.jpg", image)

    print("Result saved to output/face_detected.jpg")

else:
    print("No face detected.")