import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


def oil_pastel(image, brush_size=7, detail=0.20):
    if not hasattr(cv2, "xphoto"):
        raise RuntimeError(
            "Install opencv-contrib-python first."
        )

    # Create oil-painting base
    painted = cv2.xphoto.oilPainting(
        image, brush_size, 1
    )

    # Preserve original fine details
    smooth = cv2.GaussianBlur(
        image, (0, 0), 2.0
    )

    fine_detail = cv2.subtract(image, smooth)

    result = cv2.addWeighted(
        painted, 1.0,
        fine_detail, detail,
        0
    )

    # Gentle sharpening
    blurred = cv2.GaussianBlur(
        result, (0, 0), 1.0
    )

    result = cv2.addWeighted(
        result, 1.12,
        blurred, -0.12,
        0
    )

    return result


root = tk.Tk()
root.withdraw()

input_path = filedialog.askopenfilename(
    title="Choose Your Photo",
    filetypes=[
        ("Images", "*.jpg *.jpeg *.png *.webp *.bmp")
    ]
)

if not input_path:
    root.destroy()
    raise SystemExit

image = cv2.imread(input_path)

if image is None:
    messagebox.showerror(
        "Error", "Could not open this image."
    )
    root.destroy()
    raise SystemExit

try:
    result = oil_pastel(
        image,
        brush_size=7,
        detail=0.20
    )

    output_path = filedialog.asksaveasfilename(
        title="Save Oil Painting",
        defaultextension=".png",
        initialfile="oil_pastel.png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg")
        ]
    )

    if output_path:
        saved = cv2.imwrite(output_path, result)

        if saved:
            messagebox.showinfo(
                "Success",
                "Oil painting saved successfully!"
            )

    # Resize only the preview, not the saved image
    height, width = result.shape[:2]
    scale = min(1.0, 1000 / max(height, width))

    preview = cv2.resize(
        result, None,
        fx=scale, fy=scale,
        interpolation=cv2.INTER_AREA
    )

    cv2.imshow("Oil Painting Preview", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

except Exception as error:
    messagebox.showerror("Error", str(error))

root.destroy()