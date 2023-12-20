#Import Modules
from art.attacks.poisoning import PoisoningAttackBackdoor, PoisoningAttackCleanLabelBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.utils import to_categorical

class Backdoor:
    def __init__(self, dataset_struct, dataset_stats, params):
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.model = model
        self.params = params