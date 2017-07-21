import random
from PIL import Image, ImageDraw
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import math

def factorize(num):
    factors = list()
    for i in range(1, int(num / 6)):
        if num % i == 0 and i != 1 and i != num:
            factors.append(i)
    return factors


# Finds the average color tuple of a bounded partition of the image
def partitionAvg(colors):
    pixel_count = 0
    avg_color = list()
    for i in range(len(colors[0][1])):
        avg_color.append(0)

    for entry in colors:
        count = entry[0]
        color = entry[1]

        pixel_count += count
        for i in range(len(color)):
            avg_color[i] += (count * color[i])

    for i in range(len(avg_color)):
        avg_color[i] = int(avg_color[i] / pixel_count)

    return tuple(avg_color)

def img_to_avg(img, rows, columns):
    row_step = float(img.height / rows)
    column_step = float(img.width / columns)

    for r in range(rows):
        for c in range(columns):
            left = math.ceil(c * column_step)
            upper = math.ceil(r * row_step)
            right = math.ceil((c + 1) * column_step)
            lower = math.ceil((r + 1) * row_step)

            partition = img.crop((left, upper, right, lower))

            colors = partition.getcolors(pow(2, 24))

            avg_color = partitionAvg(colors)

            partition = Image.new(partition.mode, partition.size, avg_color)

            img.paste(partition, (left, upper, right, lower))
    return img

def main(argv):
    # Tweet object is passed into this module
    tweet = argv

    # Open the image from the URL
    response = requests.get(tweet['entities']['media'][0]['media_url'])
    img = Image.open(BytesIO(response.content))

    # Strip out the bot mention in the tweet text, and strip the extra whitespace
    tweet_text = str(tweet['text']).replace("@imgavgbot", "").strip()

    pattern = re.compile("[0-9]+[x][0-9]+")

    if pattern.match(tweet_text):
        # Parse out the rows/columns from the tweet text if the pattern matches
        size_string = tweet_text.split()[0]
        rows = int(size_string.split("x")[0])
        columns = int(size_string.split("x")[1])
    else:
        row_factors = factorize(img.height)
        column_factors = factorize(img.width)
        if len(row_factors) > 0:
            rows = random.choice(row_factors)
        else:
            rows = random.randint(3, 15)
        if len(column_factors) > 0:
            columns = random.choice(column_factors)
        else:
            columns = random.randint(3, 15)
    img = img_to_avg(img, rows, columns)
    return img


def original():
    img_size = random.choice([(1920, 1080), (1080, 1920), (2000, 2000), (2560, 2048), (2048, 2560)])
    palette = list()
    for z in range(random.randint(500, 1000)):
        palette.append((random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 100)))

    img = Image.new('RGB', img_size, 0)
    draw = ImageDraw.Draw(img)

    points = list()
    for x in range(-int(img.width / 2), int(img.width * 2), random.randint(20, 50)):
        for y in range(-int(img.height / 2), int(img.height * 2), random.randint(20, 50)):
            points.append((x, y))
    for i in range(random.randint(50, 100)):
        start_degrees = random.randint(0, 180)
        end_degrees = random.randint(start_degrees, 360)
        point_sample = random.sample(points, 2)
        draw.pieslice(xy=point_sample, start=start_degrees, end=end_degrees, fill=random.choice(palette))

    row_factors = factorize(img.height)
    column_factors = factorize(img.width)
    if len(row_factors) > 0:
        rows = random.choice(row_factors)
    else:
        rows = random.randint(3, 15)
    if len(column_factors) > 0:
        columns = random.choice(column_factors)
    else:
        columns = random.randint(3, 15)

    img = img_to_avg(img, rows, columns)
    img.save("/out/" + str(random.randint(int(sys.maxsize / 4), sys.maxsize)) + ".png")
    return img


if __name__ == "__main__":
    main()
