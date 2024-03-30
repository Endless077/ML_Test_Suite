# Utils
from utils.load_dataset import *
from utils.load_model import *
from utils.model import *
from utils.utils import *

from server import LOG_SYS

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

# Models
from models import *

# Stuff
import json

###################################################################################################

def to_JSON(param: str):
    return json.loads(param)

def to_dict(params: Params):
    return params.model_dump()

def load_dataset():
    pass

def load_model():
    pass

def perform_attack_defense():
    pass