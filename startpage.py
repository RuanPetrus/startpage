import sys
from io import TextIOWrapper

BACKGROUND = "#2E3440"
TITLE_COLOR = "#5E81AC"
ITEM_COLOR = "#ECEFF4"


class Frame():
    name: str
    links: list[tuple[str, str]]


def usage():
    print("USAGE: python3 startpage.py <input_file>")


def generate_css(out: TextIOWrapper):
    # Body
    out.write('body {\n')
    out.write('margin: 0;\n')
    out.write("font-family: 'Oswald', sans-serif;\n")
    out.write('height: 100%;\n')
    out.write('width: 100%;\n')
    out.write(f'background-color: {BACKGROUND};\n')
    out.write('}')

    # H1
    out.write('h1 { \n')
    out.write('text-align: center;\n')
    out.write(f'color: {TITLE_COLOR};\n')
    out.write('font-size: 70px;\n')
    out.write('margin-top: 20px;\n')
    out.write('margin-bottom: 20px;\n')
    out.write('font-weight: bold;\n')
    out.write('}')

    # H2
    out.write('h2 {\n')
    out.write('text-align: center;\n')
    out.write(f'color: {TITLE_COLOR};\n')
    out.write('}\n')

    # UL
    out.write('ul {\n')
    out.write('list-style-type: none;\n')
    out.write('margin: 0;\n')
    out.write('padding: 0;\n')
    out.write('text-align: center;\n')
    out.write(f'color: {ITEM_COLOR} ;\n')
    out.write('}\n')

    # A
    out.write('a {\n')
    out.write('display: block;\n')
    out.write('padding: 10px 0px;\n')
    out.write('text-decoration: none;\n')
    out.write(f'color: {ITEM_COLOR};\n')
    out.write('font-size: 1.2em;\n')
    out.write('}\n')

    # div
    out.write('div {\n')
    out.write('display: inline;\n')
    out.write('margin: 5px;\n')
    out.write('border-color: #FF0000;\n')
    out.write('border-width: 5px;\n')
    out.write('float: left;\n')
    out.write('}\n')

    # Container
    out.write('.container {\n')
    out.write('display: flex;\n')
    out.write('width: 100%;\n')
    out.write('justify-content: space-evenly;\n')
    out.write('}\n')


def generate_html(file_path: str, frames: list[Frame]):
    index: int = file_path[::-1].find('.')
    output_name: str = file_path[:len(file_path) - index] + "html"
    try:
        with open(output_name, "w") as out:
            out.write("")
            out.write('<!DOCTYPE html>\n')
            out.write('<html lang="en">\n')
            out.write('<head>\n')
            out.write('<title>StartPage</title>\n')
            out.write('<meta charset="UTF-8">\n')
            out.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
            out.write('</head>\n')
            out.write('<body>\n')
            out.write('<style type="text/css">\n')

            generate_css(out)

            out.write('</style>\n')
            out.write('<h1>Start page</h1>\n')
            out.write('<div class="container">\n')

            for frame in frames:
                out.write('<div>\n')
                out.write(f'<h2>{frame.name}</h2>\n')
                out.write('<ul>\n')

                for item in frame.links:
                    out.write(f'<li><a href="{item[1]}">{item[0]}</a></li>\n')

                out.write('</ul>\n')
                out.write('</div>\n')

            out.write('</div>\n')
            out.write('</body>\n')
            out.write('</html>\n')
            print(f"{output_name} created with success")

    except IOError:
        print(f"Fail to write to file: {output_name}")
        exit()


def parse_file(file_path: str) -> list[Frame]:
    try:
        with open(file_path, "r") as input:
            content: str = input.read()
            lines: str = content.strip().split('\n')
            frames: list[Frame] = []
            link_mode: bool = False

            for i in range(len(lines)):
                line: str = lines[i]
                if (line.strip() != ''):
                    if line[0] == '#':
                        frame: Frame = Frame()
                        frame.name = line[1:].strip()
                        frame.links = []
                        frames.append(frame)
                        link_mode = True

                    elif link_mode:
                        names_links = line.split('*')
                        if len(names_links) < 2:
                            print("ERROR: link in not in the right format <name> * <link>")
                            exit()

                        frames[-1].links.append((names_links[0],
                                                 names_links[1].strip()))
            if len(frames) == 0:
                print("Empty Content")
                exit()

            print(f"Succeful to read file: {file_path}")
            return frames

    except IOError:
        print(f"Fail to read file: {file_path}")
        exit()


def main():
    if len(sys.argv) < 2:
        print("Not enough number of arguments")
        usage()
        exit()

    input_file: str = sys.argv[1]
    frames: list[Frame] = parse_file(input_file)
    generate_html(input_file, frames)


if __name__ == "__main__":
    main()
