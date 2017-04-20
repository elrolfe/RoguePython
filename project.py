import rp

def main():
    display = rp.display()
    display.put_text('Testing', 5, 5)
    
    display.put_character('E', 5, 6)
    display.put_character('S', 5, 7)
    display.put_character('T', 5, 8)

    display.put_text('This %c{BLACK}%b{WHITE}is%c{}%b{} a %c{GOLD}%b{BLUE}Test', 5, 10)

    display.put_text_centered('-=> %c{YELLOW}RoguePython Library%c{} <=-', 2)

    display.start()

if __name__ == '__main__':
    main()