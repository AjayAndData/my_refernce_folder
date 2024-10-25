from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

# Convert PDF to images
pdf_path = 'invoice.pdf'
pages = convert_from_path(pdf_path, 300)

# Iterate over each page
for page_number, page in enumerate(pages):
    # Convert PIL image to OpenCV format
    open_cv_image = np.array(page)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Perform OCR on the image
    data = pytesseract.image_to_data(open_cv_image, output_type=pytesseract.Output.DICT)

    # Iterate over each detected word
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        text = data['text'][i]
        
        # Draw bounding box if text is detected
        if int(data['conf'][i]) > 60:  # Confidence threshold
            cv2.rectangle(open_cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(open_cv_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Save or display the result
    output_path = f'output_page_{page_number + 1}.png'
    cv2.imwrite(output_path, open_cv_image)
    print(f"Processed page {page_number + 1}, saved as {output_path}")
