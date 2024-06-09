# Logging System
from server import LOG_SYS

# Models
from models import *

# Stuff
import json

# Classes
from utils.classes.ImageSerializer import ImageSerializer
from utils.classes.AttackClass import *
from utils.classes.DefenseClass import *

# ML_Attacks
from utils.ml_attacks.evasion.FGM import FGM
from utils.ml_attacks.evasion.PGD import PGD
from utils.ml_attacks.extraction.CopycatCNN import CopycatCNN
from utils.ml_attacks.inference.MIFace import MIFace
from utils.ml_attacks.poisoning.CleanLabelBackdoor import CleanLabelBackdoor
from utils.ml_attacks.poisoning.SimpleBackdoor import SimpleBackdoor

# ML_Defenses
from utils.ml_defenses.detector.ActivationDefense import ActivationDefense
from utils.ml_defenses.postprocessor.ReverseSigmoid import ReverseSigmoid
from utils.ml_defenses.preprocessor.TotalVarMin import TotalVarMin
from utils.ml_defenses.trainer.AdversarialTrainer import AdversarialTrainer
from utils.ml_defenses.transformer.STRongIntentionalPerturbation import STRongIntentionalPerturbation

# Utils
from utils.load_dataset import *
from utils.load_model import *
from utils.model import *

###################################################################################################

def to_JSON(param: str):
    return json.loads(param)

def to_dict(params: Params) -> dict:
    return params.model_dump()

def load_dataset():
    pass

def load_model():
    pass

def perform_attack(params: Params, attack_type: str):
    pass

def perform_defense(params: Params, defense_type: str):
    pass