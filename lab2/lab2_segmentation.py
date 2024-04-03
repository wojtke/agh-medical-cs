import cv2
import numpy as np


def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(f"Seed point: {[x, y]}")
        # print(f"Intensity at seed: {im_gray[y, x]}")
        threshold = 3
        segmented_mask = region_growing(im_gray, (x, y), threshold)
        display_image = overlay_mask(im_color, segmented_mask)
        cv2.imshow("Segmentation", display_image)


def region_growing(img, seed, thresh):
    seg_mask = np.zeros_like(img)
    list = []
    list.append((seed[1], seed[0]))
    seg_mask[seed[1], seed[0]] = 1

    while len(list) > 0:
        y, x = list.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < img.shape[1] and 0 <= ny < img.shape[0]:
                    if seg_mask[ny, nx] == 0 and abs(int(img[ny, nx]) - int(img[y, x])) < thresh:
                        seg_mask[ny, nx] = 1
                        list.append((ny, nx))
    return seg_mask


def overlay_mask(image, mask, opacity=0.5):
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    red_mask = np.zeros_like(image)
    red_mask[:, :, 2] = 255  # Create a red mask
    overlay_img = np.where(mask[:, :, np.newaxis], cv2.addWeighted(image, 1 - opacity, red_mask, opacity, 0), image)
    return overlay_img


def load_img(path):
    im = cv2.imread(path)
    im_color = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.medianBlur(im_gray, 5)
    im_gray = cv2.GaussianBlur(im_gray, (3, 3), 0)
    return im_color, im_gray


if __name__ == "__main__":
    im_color, im_gray = load_img("abdomen.png")
    cv2.imshow("Segmentation", im_color)
    cv2.setMouseCallback("Segmentation", mouse_callback)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
