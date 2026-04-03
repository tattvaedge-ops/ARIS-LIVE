from PIL import Image, ImageDraw, ImageFont


def add_labels(image_path, labels):

    try:

        image = Image.open(image_path)

        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        width, height = image.size

        x = int(width * 0.02)
        y = int(height * 0.05)

        for label in labels:

            draw.text((x, y), label, fill="white", font=font)

            y += 40

        output_file = image_path.replace(".png", "_labeled.png")

        image.save(output_file)

        print("LABELLED IMAGE CREATED:", output_file)

        return output_file

    except Exception as e:

        print("LABEL ENGINE ERROR:", e)

        return image_path