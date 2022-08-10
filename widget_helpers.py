class WidgetHelper:
    def center_widget(self):
        # Center window
        self.update()

        w = self.winfo_width()
        h = self.winfo_height()

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))