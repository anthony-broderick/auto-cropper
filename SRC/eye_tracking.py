import cv2
from ultralytics import YOLO

# load the face and eye classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# toggle for debugging visuals
DEBUGGING = False

def track_eyes(image, aspect_width=4, aspect_height=5):
    image = image.copy()
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    eye_centers = []
    # x, y = coordinates of the top-left corner of face
    # w, h = width and height of the face 
    for (x, y, w, h) in faces:
        # draw rectangle around the face
        if DEBUGGING:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # extract the face region of interest (ROI)
        roi_gray = gray[y:y+h, x:x+w]
        # extract the color face ROI
        roi_color = image[y:y+h, x:x+w]
        
        # detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye_center_x = x + ex + ew / 2
            eye_center_y = y + ey + eh / 2
            eye_centers.append((eye_center_x, eye_center_y))

            # draw rectangles around detected eyes
            if DEBUGGING:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # calculate average eye center position (height and horizontal position)
    if eye_centers:
        x_eye_center = sum([ec[0] for ec in eye_centers]) / len(eye_centers)
        avg_eye_height = sum([ec[1] for ec in eye_centers]) / len(eye_centers)
    else:
        x_eye_center = image.shape[1] / 2
        avg_eye_height = image.shape[0] / 2

    return center_image(image, avg_eye_height, x_eye_center, aspect_width, aspect_height)


def center_image(image, avg_eye_height, x_eye_center, aspect_width, aspect_height):
    image_height, image_width = image.shape[:2]

    # maximum width constrained by horizontal edges
    max_width_left = x_eye_center * 2
    max_width_right = (image_width - x_eye_center) * 2
    crop_width = min(max_width_left, max_width_right)
    
    # corresponding height for given aspect ratio
    crop_height = int(crop_width * aspect_height / aspect_width)
    
    # check if height exceeds image height, if so, scale down
    # place vertical 2/3 point at avg_eye_height (ideal for photography, could add option to make 1/3 later for different compositions)
    max_height_top = avg_eye_height / (1/3)
    max_height_bottom = (image_height - avg_eye_height) / (2/3)
    max_crop_height = min(crop_height, max_height_top, max_height_bottom)
    
    # adjust width according to new height if height was constrained
    crop_height = int(max_crop_height)
    crop_width = int(crop_height * aspect_width / aspect_height)
    
    # final coordinates
    x_left = int(x_eye_center - crop_width / 2)
    x_right = int(x_eye_center + crop_width / 2)
    y_top = int(avg_eye_height - (1/3) * crop_height)
    y_bottom = int(y_top + crop_height)
    
    # clamp to image boundaries
    x_left = max(0, x_left)
    y_top = max(0, y_top)
    x_right = min(image_width, x_right)
    y_bottom = min(image_height, y_bottom)

    cropped_image = image[y_top:y_bottom, x_left:x_right]

    # draw guide lines
    if DEBUGGING:
        cropped_image = print_guide_lines(cropped_image, avg_eye_height - y_top, x_eye_center - x_left)

    return cropped_image

def print_guide_lines(image, avg_eye_height=None, x_eye_center=None):
    h, w = image.shape[:2]

    # green lines
    green = (0, 255, 0)  # BGR
    # vertical lines at 1/3 and 2/3 width
    cv2.line(image, (w // 3, 0), (w // 3, h), green, 1)
    cv2.line(image, (2 * w // 3, 0), (2 * w // 3, h), green, 1)
    # horizontal lines at 1/3 and 2/3 height
    cv2.line(image, (0, h // 3), (w, h // 3), green, 1)
    cv2.line(image, (0, 2 * h // 3), (w, 2 * h // 3), green, 1)

    # cyan lines
    cyan = (255, 255, 0)  # BGR
    if avg_eye_height is not None:
        cv2.line(image, (0, int(avg_eye_height)), (w, int(avg_eye_height)), cyan, 1)
    if x_eye_center is not None:
        cv2.line(image, (int(x_eye_center), 0), (int(x_eye_center), h), cyan, 1)

    return image