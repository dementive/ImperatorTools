import json


class Location:
    def __init__(self, column, origin, fullpath, length, line, linenr, path, tag=None):
        self.column = column
        self.origin = origin  # Renamed to avoid conflict with 'from' keyword
        self.fullpath = fullpath
        self.length = length
        self.line = line
        self.linenr = linenr
        self.path = path
        self.tag = tag


class JsonObject:
    def __init__(self, confidence, info, key, locations, message, severity):
        self.confidence = confidence
        self.info = info
        self.key = key
        locations_list = list()
        for i in locations:
            locations_list.append(
                Location(
                    i["column"],
                    i["from"],
                    i["fullpath"],
                    i["length"],
                    i["line"],
                    i["linenr"],
                    i["path"],
                    i["tag"],
                )
            )
        self.locations = locations_list
        self.message = message
        self.severity = severity
        self._max_line_num_length = 0

    def display(self):
        print(f"{self.severity}({self.key}): {self.message}")
        count = 0
        for i in self.locations:
            line_num_padding = " "
            column_padding = ""
            arrows = ""

            low_num_padding = ""
            line_len = len(str(i.linenr))
            if line_len < self._max_line_num_length:
                for j in range(line_len):
                    low_num_padding += " "
            if line_len > self._max_line_num_length:
                self._max_line_num_length = line_len

            for j in range(line_len):
                line_num_padding += " "
            for j in range(i.column - 1):
                column_padding += " "
            for j in range(i.length):
                arrows += "^"

            line = i.line.replace("\t", " ")

            tag = ""
            if i.tag:
                tag = "<-- " + i.tag

            added_arrow = "--> " if count < 1 else "     "
            print(f"{line_num_padding}{added_arrow}[{i.origin}] {i.path}")
            print(f"{low_num_padding}{i.linenr} |{line}")
            print(f"{low_num_padding}{line_num_padding}|{column_padding}{arrows} {tag}")
            count += 1


with open("tiger.json", "r", encoding="utf-16") as file:
    data = json.load(file)

x = JsonObject(
    data[1]["confidence"],
    data[1]["info"],
    data[1]["key"],
    data[1]["locations"],
    data[1]["message"],
    data[1]["severity"],
)

x.display()
