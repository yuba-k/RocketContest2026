import configparser
import os

class Config_reader:
    def __init__(self):
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            ini_path = os.path.join(base, "..", "config", "cansat.ini")
            self.config = configparser.ConfigParser()
            self.config.read(ini_path, encoding="utf-8")
        except FileNotFoundError as e:
            print(f"FIleNotFoudError\n{e}")

    def reader(self, key, value, style):
        var = self.config.get(key, value)
        if style == "intenger16":
            var = int(var, 0)
        elif style == "intenger":
            var = int(var)
        elif style == "character":
            var = str(var)
        elif style == "float":
            var = float(var)
        return var
