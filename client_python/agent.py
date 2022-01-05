class Agent:
    def __init__(self, info: dict):
        self.id = int(info['id'])
        self.value = float(info['value'])
        self.src = int(info['src'])
        self.dest = int(info['dest'])
        self.speed = float(info['speed'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.x = float(loc[0])
        self.y = float(loc[1])
        self.target = None

    def id(self):
        return self.id