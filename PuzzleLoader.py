import json
import random

class Loader():
    def __init__(self, filePath) -> None:
        self.puzzleFile = './puzzles.json'

    def tryFile(self) -> bool:
        try:
            open(self.puzzleFile)
        except FileNotFoundError:
            print("File could not be opened")
            return False
        return True

    def loadBoard(self, difficulty: str):
        with open('./puzzles.json') as f:
            data = json.load(f)
            puzzles = []
            for i in data['puzzles']:
                if(i['difficulty'] == difficulty):
                    puzzles.append(i['board'])
            return random.choice(puzzles)