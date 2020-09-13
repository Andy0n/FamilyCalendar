from PIL import Image, ImageDraw, ImageFont

from config import *


def get_min_max(data):
    min = 24
    max = 0

    for name in data:
        for day in data[name]:
            for event in data[name][day]:
                if event[1] - event[0] < 23:
                    min = event[0] if event[0] < min else min
                    max = event[1] if event[1] > max else max

    return min, max


def _draw_bars(draw, data, user_count, min, max, col_width, row_height):
    current_user = user_count - 1

    for name in data:
        current_day = 1

        for day in data[name]:
            for event in data[name][day]:
                start = event[0] - min if event[0] - min > 0 else 0
                end = event[1] - min if event[1] - min < max - min + 1 else max - min + 1

                x1 = col_width * current_day * user_count - current_user * col_width + 1
                y1 = row_height * (1 + start)
                x2 = col_width * (user_count * current_day + 1) - current_user * col_width
                y2 = row_height * (1 + end)

                shape = [(x1, y1), (x2, y2)]

                draw.rectangle(shape, fill=MATES[name]['config']['color'], width=0)
            current_day += 1
        current_user -= 1


def _draw_grid(draw, data, user_count, min, max, col_width, row_height, cols, rows, width, height):
    for row in range(1, rows):
        x1 = 0
        y1 = row_height * row
        x2 = width
        y2 = row_height * row
        shape = [(x1, y1), (x2, y2)]

        draw.line(shape, fill=BLACK, width=1)

        hour = str(int(min + row - 1))

        font = ImageFont.truetype(FONT, size=FONT_SIZE_HOUR)
        w, h = draw.textsize(hour, font=font)
        x = (col_width - w) / 2
        y = row_height * row + (row_height - h) / 2

        draw.text((x, y), hour, fill=BLACK, font=font)

    for col in range(1, cols):
        if (col - 1) % user_count == 0:
            x1 = col_width * col
            y1 = 0
            x2 = col_width * col
            y2 = height
            shape = [(x1, y1), (x2, y2)]

            draw.line(shape, fill=BLACK, width=2)

            weekday = DAYS_FULL[list(data[list(data)[0]])[int((col - 1) / user_count)]]

            font = ImageFont.truetype(FONT, size=FONT_SIZE_DAYS)
            w, h = draw.textsize(weekday, font=font)
            x = col_width * col + (col_width * user_count - w) / 2
            y = (row_height - h) / 2

            draw.text((x, y), weekday, fill=BLACK, font=font)


def create_picture(data, width, height):
    img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(img)

    min, max = get_min_max(data)
    user_count = len(data)

    cols = user_count * 5 + 1
    rows = round((max - min + 1) + 1)

    col_width = width / cols
    row_height = height / rows

    _draw_bars(draw, data, user_count, min, max, col_width, row_height)
    _draw_grid(draw, data, user_count, min, max, col_width, row_height, cols, rows, width, height)

    return img
