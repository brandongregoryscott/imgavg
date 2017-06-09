import random
from PIL import Image
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import botconfig
import math

def partitionAvg(colors):
    pixelCount = 0
    avgColor = list()
    for i in range(len(colors[0][1])):
        avgColor.append(0)

    for entry in colors:
        count = entry[0]
        color = entry[1]

        pixelCount += count
        for i in range(len(color)):
            avgColor[i] += (count * color[i])

    for i in range(len(avgColor)):
        avgColor[i] = int(avgColor[i] / pixelCount)

    return tuple(avgColor)

def main(argv):
    tweet = argv
    # tweet = {}
    # Open the image from the URL
    response = requests.get(tweet['entities']['media'][0]['media_url'])

    img = Image.open(BytesIO(response.content))

    tweet_text = str(tweet['text']).replace(botconfig.botMention, "").strip()

    pattern = re.compile("[0-9]+[x][0-9]+")

    if pattern.match(tweet_text):
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

            avgColor = partitionAvg(colors)

            partition = Image.new(partition.mode, partition.size, avgColor)

            img.paste(partition, (left, upper, right, lower))
    #img.show()

    return img

if __name__ == "__main__":
    main()
