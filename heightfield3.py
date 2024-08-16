import numpy as np
from PIL import Image

def save_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1} {face[3]+1}\n")

def generate_tile(heightmap_path, output_path, tile_size=100, base_thickness=3):
    # Load and downsample the heightmap image to 10x10
    im = Image.open(heightmap_path).convert('L')
    #im_resized = im.resize((100, 100))
    z = np.asarray(im) / 255.0  # Normalize pixel values between 0 and 1
    h, w = z.shape
    
    # Scale heightmap to desired tile size
    scale_x = tile_size / w
    scale_y = tile_size / h
    z *= base_thickness

    # Generate vertices for the top surface
    vertices = []
    for y in range(h):
        for x in range(w):
            vertices.append((x * scale_x, y * scale_y, z[y, x]))

    # Generate vertices for the base, using the same grid as the top surface
    base_vertices = [(x * scale_x, y * scale_y, -base_thickness) for y in range(h) for x in range(w)]
    vertices.extend(base_vertices)

    # Add the four corner vertices for the bottom face
    bottom_corners = [
        (0, 0, -base_thickness),
        (tile_size, 0, -base_thickness),
        (tile_size, tile_size, -base_thickness),
        (0, tile_size, -base_thickness)
    ]

    # Generate quads for the top surface
    faces = []
    for y in range(h - 1):
        for x in range(w - 1):
            i = y * w + x
            faces.append((i, i + 1, i + w + 1, i + w))

    print("Surface done")

    # Generate quads for the sides
    for y in range(h - 1):
        for x in range(w - 1):
            i = y * w + x
            base_i = i + h * w

            # Front side
            if y == 0:
                faces.append((i, i + 1, base_i + 1, base_i))

            # Back side
            if y == h - 2:
                faces.append((i + w, i + w + 1, base_i + w + 1, base_i + w))

            # Left side
            if x == 0:
                faces.append((i, i + w, base_i + w, base_i))

            # Right side
            if x == w - 2:
                faces.append((i + 1, i + w + 1, base_i + w + 1, base_i + 1))

    print("Sides done")

    # Add a single quad for the bottom using the corner vertices
    bottom_quad = (
        len(vertices) - len(base_vertices) + 0,  # Bottom left
        len(vertices) - len(base_vertices) + w - 1,  # Bottom right
        len(vertices) - 1,  # Top right
        len(vertices) - w   # Top left
    )
    faces.append(bottom_quad)

    print("Bottom done")
    
    # Save to OBJ file
    save_obj(output_path, vertices, faces)

if __name__ == "__main__":
    heightmap_path = "/Users/maxine/Downloads/1_casino_navy_stitched.jpg"  # Replace with your heightmap path
    output_path = "output6.obj"
    generate_tile(heightmap_path, output_path)
