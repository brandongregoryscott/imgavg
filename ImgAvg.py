import random
from PIL import Image
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import botconfig
import math

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

def main(argv):
    # Tweet object is passed into this module
    tweet = argv

    # Open the image from the URL
    response = requests.get(tweet['entities']['media'][0]['media_url'])
    img = Image.open(BytesIO(response.content))

    # Strip out the bot mention in the tweet text, and strip the extra whitespace
    tweet_text = str(tweet['text']).replace(botconfig.botMention, "").strip()

    pattern = re.compile("[0-9]+[x][0-9]+")

    if pattern.match(tweet_text):
        # Parse out the rows/columns from the tweet text if the pattern matches
        size_string = tweet_text.split()[0]
        rows = int(size_string.split("x")[0])
        columns = int(size_string.split("x")[1])

    else:
        rows = random.randint(3, 12)
        columns = random.randint(3, 12)

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

if __name__ == "__main__":
    main()
