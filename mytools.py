def time_converter(s):
    m, s = divmod(s, 60)
    if m >= 60:
        h, m = divmod(m, 60)
        if h >= 24:
            d, h = divmod(h, 24)
            if d >= 30:
                M, d = divmod(d, 30)
                if M >= 12:
                    y, M = divmod(M, 12)
                    return f'{y}y:{M}M:{d}d:{h}h:{m}m:{s}s'
                return f'{M}M:{d}d:{h}h:{m}m:{s}s'
            return f'{d}d:{h}h:{m}m:{s}s'
        return f'{h}h:{m}m:{s}s'
    return f'{m}m:{s}s'


def multiple_replace(remaps, text):
    import re
    regex = re.compile(f"({"|".join(map(re.escape, remaps.keys()))})" )
    return regex.sub(lambda mo: remaps[mo.string[mo.start():mo.end()]], text)