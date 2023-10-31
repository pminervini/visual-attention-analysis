import os
import csv
import random
import numpy as np
from PIL import Image, ImageDraw
import argparse

def draw_star(draw, center, size, angle=0):
    # Star generation with rotation
    points = []
    for i in range(5):
        points.append((center[0] + size * np.cos(2 * np.pi * i / 5 + angle),
                       center[1] + size * np.sin(2 * np.pi * i / 5 + angle)))
        points.append((center[0] + size/2 * np.cos(2 * np.pi * i / 5 + np.pi / 5 + angle),
                       center[1] + size/2 * np.sin(2 * np.pi * i / 5 + np.pi / 5 + angle)))
    draw.polygon(points, fill="black")

def draw_shape(draw, shape, position, size, angle):
    if shape == 'circle':
        bounding_box = [position[0] - size, position[1] - size, position[0] + size, position[1] + size]
        draw.ellipse(bounding_box, fill="black")
    elif shape == 'square':
        angle_rad = np.deg2rad(angle)
        points = [
            (position[0] + size * np.cos(angle_rad), position[1] + size * np.sin(angle_rad)),
            (position[0] - size * np.sin(angle_rad), position[1] + size * np.cos(angle_rad)),
            (position[0] - size * np.cos(angle_rad), position[1] - size * np.sin(angle_rad)),
            (position[0] + size * np.sin(angle_rad), position[1] - size * np.cos(angle_rad)),
        ]
        draw.polygon(points, fill="black")
    elif shape == 'triangle':
        points = [
            (position[0], position[1] - size),
            (position[0] - size * np.sin(np.deg2rad(angle)), position[1] + size * np.cos(np.deg2rad(angle))),
            (position[0] + size * np.sin(np.deg2rad(angle)), position[1] + size * np.cos(np.deg2rad(angle))),
        ]
        draw.polygon(points, fill="black")
    elif shape == 'star':
        draw_star(draw, position, size, np.deg2rad(angle))

def create_random_shape_image(img_size):
    img = Image.new('RGB', (img_size, img_size), color = 'white')
    draw = ImageDraw.Draw(img)

    shape = random.choice(SHAPES)
    size = random.randint(15, 30)
    position = (random.randint(size, img_size - size), random.randint(size, img_size - size))
    angle = random.randint(0, 360) if ROTATE_SHAPES else 0

    draw_shape(draw, shape, position, size, angle)
    return img, shape

def main():
    parser = argparse.ArgumentParser(description='Generate images with random shapes.')
    parser.add_argument('--output', type=str, default='generated_images', help='Output directory for images')
    parser.add_argument('--size', type=int, default=224, help='Size of the images (square)')
    parser.add_argument('--num', type=int, default=100, help='Number of images to generate')
    args = parser.parse_args()

    output_dir = args.output
    img_size = args.size
    num_images = args.num

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, 'shapes.csv'), 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image', 'Shape'])

        for i in range(num_images):
            img, shape = create_random_shape_image(img_size)
            img_path = os.path.join(output_dir, f'image_{i+1}.png')
            img.save(img_path)
            csvwriter.writerow([img_path, shape])

    print(f"{num_images} images generated in '{output_dir}' directory with accompanying CSV.")

if __name__ == "__main__":
    SHAPES = ['star', 'triangle', 'square', 'circle']
    ROTATE_SHAPES = True  # Set to False to disable rotation
    main()
