from copy import deepcopy
from pathlib import Path

from fontTools.misc.fixedTools import otRound
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont


SCALE = 0.66
COPYRIGHT = 'Small triangle glyphs copyright (c) 2026 AlphaPrime.'


def main():
    root = Path(__file__).resolve().parent.parent
    for path in sorted((root / 'Original').glob('*.ttf')):
        add_small_triangles(path)


def add_small_triangles(path):
    font = TTFont(path, recalcTimestamp=False)
    cmap = font.getBestCmap()
    zero = font['glyf'][cmap[ord('0')]]
    source_advance = font['hmtx'][cmap[0x25B2]][0]
    advance = otRound(source_advance * 0.676)
    x_offset = (advance - source_advance * SCALE) / 2
    glyph_set = font.getGlyphSet()
    pen = TTGlyphPen(glyph_set)
    glyph_set[cmap[0x25B2]].draw(
        TransformPen(pen, (SCALE, 0, 0, SCALE, x_offset, 0))
    )
    up = pen.glyph()
    up.recalcBounds(font['glyf'])

    # Match parity so integer coordinates can share zero's exact half-unit center.
    if (zero.yMin + zero.yMax - up.yMin - up.yMax) % 2:
        for index, (x, y) in enumerate(up.coordinates):
            if y == up.yMax:
                up.coordinates[index] = (x, y + 1)
        up.recalcBounds(font['glyf'])

    # Align the ink bounds with the vertical center of the digit zero.
    y_offset = otRound((zero.yMin + zero.yMax - up.yMin - up.yMax) / 2)
    for index, (x, y) in enumerate(up.coordinates):
        up.coordinates[index] = (x, y + y_offset)
    up.recalcBounds(font['glyf'])

    # Mirror the rounded coordinates to keep both triangles exactly the same size.
    down = deepcopy(up)
    flip_y = up.yMin + up.yMax
    for index, (x, y) in enumerate(down.coordinates):
        down.coordinates[index] = (advance - x, flip_y - y)

    for codepoint, glyph in ((0x25B4, up), (0x25BE, down)):
        name = f'uni{codepoint:04X}'
        font['glyf'][name] = glyph
        glyph.recalcBounds(font['glyf'])
        font['hmtx'][name] = (advance, glyph.xMin)
        for table in font['cmap'].tables:
            if table.isUnicode() and table.format in (4, 12):
                table.cmap[codepoint] = name

    font['head'].fontRevision = 1.101
    for record in font['name'].names:
        if record.nameID == 5:
            record.string = 'Version 1.101'.encode(record.getEncoding())
        elif record.nameID == 0:
            text = record.toUnicode()
            if COPYRIGHT not in text:
                record.string = (text + '\n' + COPYRIGHT).encode(record.getEncoding())
    font.save(path)
    print(f'Added U+25B4/U+25BE: {path.name}')


if __name__ == '__main__':
    main()
