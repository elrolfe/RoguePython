import rp

def main():

    generator = rp.maps.GridMap()
    # generator.rng.set_seed(1492718583.865769)
    print(generator.rng.get_seed())
    level_map = generator.generate()

    width = generator.get_width()
    height = generator.get_height()
    display = rp.display(width, height, rp.font.ATI_8X8)

    for x in range(width):
        for y in range(height):
            if (level_map[x][y] == 1):
                display.put_character('.', x, y)
            else:
                display.put_character('#', x, y, rp.Color.GOLDENROD)

    display.start()

if __name__ == '__main__':
    main()