import urwid

superscript_map = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


class TextWithLinks(urwid.WidgetWrap):
    def __init__(self, markup, on_link_click):
        self.markup = markup
        self.on_link_click = on_link_click
        self.text = urwid.Text(markup)
        self.focused_item_index = 0
        self.focusable_items = self.get_focusable_items(markup)
        self.update_focus(markup)
        super().__init__(self.text)

    def update_focus(self, markup):
        rewrite = []
        index = 0
        for item in markup:
            if isinstance(item, tuple) and item[0].startswith("http"):
                if index == self.focused_item_index:
                    rewrite.append(
                        ("link_focused", f"{item[1]} {superscript_map[str(index+1)]}")
                    )
                else:
                    rewrite.append(
                        ("link", f"{item[1]} {superscript_map[str(index+1)]}")
                    )
                index += 1
            else:
                rewrite.append(item)
        self.text.set_text(rewrite)

    def get_focusable_items(self, markup):
        return [
            item
            for item in markup
            if isinstance(item, tuple) and item[0].startswith("http")
        ]

    def keypress(self, size, key):
        max_position = len(self.focusable_items) - 1
        if key == "up" or key == "left":
            self.focused_item_index = max(0, self.focused_item_index - 1)
        elif key == "down" or key == "right":
            self.focused_item_index = min(max_position, self.focused_item_index + 1)
        elif key == "enter":
            self.on_link_click(self.focusable_items[self.focused_item_index][0])
        else:
            return key
        self.update_focus(self.markup)

    def selectable(self):
        return True


palette = [
    ("link", "underline", ""),
    ("link_focused", "yellow", "black"),
    ("italics", "italics", ""),
]

markup = [
    "I am Thejaswi Puthraya, the owner of this ",
    ("http://thejaswi.info/", "website"),
    " and a freelance software developer. I was born in ",
    ("https://en.wikipedia.org/wiki/Hyderabad", "Hyderabad"),
    " the city of pearls and the capital of Telangana, India. Ever since I have been living in this city famous for ",
    ("italics", "Irani Chai and"),
    ("italics", " Chalta Hai"),
    " attitude.",
]


def on_link_click(link):
    print(f"Link clicked: {link}")


txt = TextWithLinks(markup, on_link_click)
fill = urwid.Filler(txt, valign="top")
loop = urwid.MainLoop(urwid.Padding(fill, left=2, right=2), palette)
loop.run()
