import cv2
import numpy as np

# ==========================
# CAMERA
# ==========================

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# ==========================
# ROI SETTINGS
# ==========================

roi_x = 200
roi_y = 150
roi_w = 250
roi_h = 150

# ==========================
# CONTROL WINDOW
# ==========================

cv2.namedWindow("Controls")

cv2.createTrackbar(
    "Threshold",
    "Controls",
    100,
    255,
    lambda x: None
)

# ==========================
# MAIN LOOP
# ==========================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera Error")
        break

    # ROI

    cv2.rectangle(
        frame,
        (roi_x, roi_y),
        (roi_x + roi_w, roi_y + roi_h),
        (255, 0, 0),
        2
    )

    roi = frame[
        roi_y:roi_y + roi_h,
        roi_x:roi_x + roi_w
    ]

    # ==========================
    # PREPROCESSING
    # ==========================

    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # Live threshold value

    threshold_value = cv2.getTrackbarPos(
        "Threshold",
        "Controls"
    )

    _, thresh = cv2.threshold(
        blur,
        threshold_value,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Morphological cleanup

    kernel = np.ones((3,3), np.uint8)

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ==========================
    # CONTOURS
    # ==========================

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    quality = "NO PART"
    orientation = "NONE"

    area = 0
    aspect_ratio = 0
    angle = 0

    if len(contours) > 0:

        cnt = max(
            contours,
            key=cv2.contourArea
        )

        area = cv2.contourArea(cnt)

        if area > 500:

            x, y, w, h = cv2.boundingRect(cnt)

            # Draw contour box

            cv2.rectangle(
                frame,
                (x + roi_x, y + roi_y),
                (x + w + roi_x, y + h + roi_y),
                (0,255,0),
                2
            )

            # ==========================
            # ORIENTATION
            # ==========================

            rect = cv2.minAreaRect(cnt)

            (_, _), (rw, rh), angle = rect

            if rw < rh:
                angle = angle + 90

            if abs(angle) < 20:

                orientation = "HORIZONTAL"
                aspect_ratio = w / h

            elif 70 < angle < 110:

                orientation = "VERTICAL"
                aspect_ratio = h / w

            else:

                orientation = "TILTED"
                aspect_ratio = max(w, h) / min(w, h)

            # ==========================
            # QUALITY CHECK
            # ==========================

            area_ok = (
                1200 < area < 2500
            )

            aspect_ok = (
                2.0 < aspect_ratio < 6.0
            )

            orientation_ok = (
                orientation == "VERTICAL"
                or
                orientation == "HORIZONTAL"
            )

            if (
                area_ok
                and aspect_ok
                and orientation_ok
            ):

                quality = "GOOD"

            else:

                quality = "DEFECT"

    # ==========================
    # DISPLAY
    # ==========================

    color = (
        (0,255,0)
        if quality == "GOOD"
        else (0,0,255)
    )

    cv2.putText(
        frame,
        f"QUALITY: {quality}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.putText(
        frame,
        f"Area: {int(area)}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Aspect: {aspect_ratio:.2f}",
        (20,140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,0),
        2
    )

    cv2.putText(
        frame,
        f"Orientation: {orientation}",
        (20,190),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Threshold: {threshold_value}",
        (20,240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,0,255),
        2
    )

    # Windows

    cv2.imshow(
        "Threshold",
        thresh
    )

    cv2.imshow(
        "Defect Detection System",
        frame
    )

    # ESC key

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==========================
# CLEANUP
# ==========================

cap.release()
cv2.destroyAllWindows()