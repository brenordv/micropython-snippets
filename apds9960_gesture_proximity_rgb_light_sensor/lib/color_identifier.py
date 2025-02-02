class ColorIdentifier:
    def __init__(self):
        self.colors = [
            ((0, 0, 0), "Black"),
            ((255, 255, 255), "White"),
            ((255, 0, 0), "Red"),
            ((0, 255, 0), "Green"),
            ((0, 0, 255), "Blue"),
            ((255, 255, 0), "Yellow"),
            ((255, 0, 255), "Magenta"),
            ((0, 255, 255), "Cyan"),
            ((128, 128, 128), "Gray"),
            ((128, 0, 0), "Maroon"),
            ((128, 128, 0), "Olive"),
            ((0, 128, 0), "Dark Green"),
            ((128, 0, 128), "Purple"),
            ((0, 128, 128), "Teal"),
            ((0, 0, 128), "Navy"),
            ((255, 165, 0), "Orange"),
            ((165, 42, 42), "Brown"),
            ((255, 192, 203), "Pink")
        ]

    def color_distance(self, color1, color2):
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2))

    def get_closest_color(self, r, g, b):
        return min(self.colors, key=lambda color: self.color_distance(color[0], (r, g, b)))

    def get_hue(self, r, g, b):
        if r > g and r > b:
            return "Red"
        elif g > r and g > b:
            return "Green"
        elif b > r and b > g:
            return "Blue"
        elif r > b and g > b and abs(r - g) < 30:
            return "Yellow"
        elif r > g and b > g and abs(r - b) < 30:
            return "Purple"
        elif g > r and b > r and abs(g - b) < 30:
            return "Cyan"
        else:
            return "Gray"

    def get_brightness_modifier(self, brightness):
        if brightness < 64:
            return "Dark"
        elif brightness < 128:
            return "Medium"
        elif brightness < 192:
            return "Light"
        else:
            return "Bright"

    def get_color_name(self, r, g, b):
        closest_color = self.get_closest_color(r, g, b)

        if self.color_distance(closest_color[0], (r, g, b)) < 5000:
            return closest_color[1]

        brightness = sum((r, g, b)) / 3
        saturation = max(r, g, b) - min(r, g, b)

        if saturation < 20:
            if brightness < 32:
                return "Black"
            elif brightness > 224:
                return "White"
            else:
                return f"{self.get_brightness_modifier(brightness)} Gray"

        hue = self.get_hue(r, g, b)
        modifier = self.get_brightness_modifier(brightness)

        return f"{modifier} {hue}"
