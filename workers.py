from hashlib import md5

class Worker:
    def __init__(self, TO_FIND, START_RANGE, DPC) -> None:
        self.STRING_TO_FIND = TO_FIND.lower()
        self.DISTANCE_PER_CPU = DPC
        self.START_RANGE = START_RANGE
        self.END_RANGE = self.START_RANGE + self.DISTANCE_PER_CPU
    
    def find_all(self):
        string = ""

        for i in range(self.START_RANGE, self.END_RANGE):
            hashed_str = md5(str(i).encode()).hexdigest()

            if hashed_str == self.STRING_TO_FIND:
                print(hashed_str)

                string = i

                return string

        print('Worker done')
        return -1
