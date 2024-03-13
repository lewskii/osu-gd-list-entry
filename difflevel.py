from enum import Enum
from ossapi import Beatmap

class DiffLevel(Enum):
    EASY = 'Easy'
    NORMAL = 'Normal'
    HARD = 'Hard'
    INSANE = 'Insane'
    EXPERT = 'Expert'
    EXPERTPLUS = 'Expert+'

    def image_url(self):
        match self:
            case DiffLevel.EASY:
                return 'https://i.ppy.sh/e4046437c0d195a3f2bed4b4140a41d696bdf7f0/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f656173792d6f2e706e673f3230323131323135'
            case DiffLevel.NORMAL:
                return 'https://i.ppy.sh/20d7052354c61f8faf3a4828d9ff7751bb6776b1/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f6e6f726d616c2d6f2e706e673f3230323131323135'
            case DiffLevel.HARD:
                return 'https://i.ppy.sh/0ad2e280f5a26c7f202b3dff711b723045662b37/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f686172642d6f2e706e673f3230323131323135'
            case DiffLevel.INSANE:
                return 'https://i.ppy.sh/f6eabcfbacdfe85e520106702ec3a382a0430d40/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f696e73616e652d6f2e706e673f3230323131323135'
            case DiffLevel.EXPERT:
                return 'https://i.ppy.sh/cd145e0f3cf7039d72cb7cfe58f3931585f8e7a7/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f6578706572742d6f2e706e673f3230323131323135'
            case DiffLevel.EXPERTPLUS:
                return 'https://i.ppy.sh/3b561ef8a73118940b59e79f3433bfa98c26cbf1/68747470733a2f2f6f73752e7070792e73682f77696b692f696d616765732f7368617265642f646966662f657870657274706c75732d6f2e706e673f3230323131323135'

    def from_str(diff_str: str):
        DIFF_INPUT_TABLE = {
            DiffLevel.EASY: ['e', 'easy'],
            DiffLevel.NORMAL: ['n', 'normal'],
            DiffLevel.HARD: ['h', 'hard'],
            DiffLevel.INSANE: ['i', 'insane'],
            DiffLevel.EXPERT: ['x', 'ex', 'expert', 'extra'],
            DiffLevel.EXPERTPLUS: ['+', 'p', 'plus', 'expert+'],
        }
        for (diff, names) in DIFF_INPUT_TABLE.items():
            if diff_str in names:
                return diff
        return None


DIFFNAME_TABLE = {
    DiffLevel.EASY: ['easy'],
    DiffLevel.NORMAL: ['normal', 'advanced'],
    DiffLevel.HARD: ['hard', 'hyper'],
    DiffLevel.INSANE: ['insane', 'lunatic', 'another'],
    DiffLevel.EXPERT: ['expert', 'extra'],
}

EXPERT_PLUS_CUTOFF = 6.5

def expected_diff(map: Beatmap) -> DiffLevel | None:
    sr = map.difficulty_rating
    diffname = map.version.lower()

    if sr >= EXPERT_PLUS_CUTOFF:
        return DiffLevel.EXPERTPLUS
    else:
        for (diff, names) in DIFFNAME_TABLE.items():
            for name in names:
                if name in diffname:
                    return diff
        else:
            return None
