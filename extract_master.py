import cv2

# Load master image
master = cv2.imread(
    "DefectDetectionSystem/images/master_part.png"
)

# Convert to grayscale
gray = cv2.cvtColor(
    master,
    cv2.COLOR_BGR2GRAY
)

# Blur
blur = cv2.GaussianBlur(
    gray,
    (5,5),
    0
)

# Threshold
_, thresh = cv2.threshold(
    blur,
    100,
    255,
    cv2.THRESH_BINARY_INV
)

# Find contours
contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Get largest contour
master_contour = max(
    contours,
    key=cv2.contourArea
)

# Draw contour
cv2.drawContours(
    master,
    [master_contour],
    -1,
    (0,255,0),
    2
)

print(
    "Master Area:",
    cv2.contourArea(master_contour)
)

cv2.imshow(
    "Master Contour",
    master
)

cv2.imshow(
    "Threshold",
    thresh
)

cv2.waitKey(0)
cv2.destroyAllWindows()