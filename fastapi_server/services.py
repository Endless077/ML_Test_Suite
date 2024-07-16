# Logging System
from server import LOG_SYS

# Server
from server import LOCAL_MODELS
from server import LOCAL_DATASET
from server import STORAGE_TEMP_DIR
from server import STORAGE_MODEL_DIR
from server import STORAGE_DATASET_DIR

# Models
from models import *

# Stuff
import json

# HTTPException
from fastapi import HTTPException

# Classes
from utils.classes.AttackClass import *
from utils.classes.DefenseClass import *

# ML Attacks
from utils.ml_attacks.evasion.FGM import FGM
from utils.ml_attacks.evasion.PGD import PGD
from utils.ml_attacks.extraction.CopycatCNN import CopycatCNN
from utils.ml_attacks.inference.MIFace import MIFace
from utils.ml_attacks.poisoning.CleanLabelBackdoor import CleanLabelBackdoor
from utils.ml_attacks.poisoning.SimpleBackdoor import SimpleBackdoor

# ML Defenses
from utils.ml_defenses.detector.ActivationDefense import ActivationDefense
from utils.ml_defenses.postprocessor.ReverseSigmoid import ReverseSigmoid
from utils.ml_defenses.preprocessor.TotalVarMin import TotalVarMin
from utils.ml_defenses.trainer.AdversarialTrainer import AdversarialTrainer
from utils.ml_defenses.transformer.STRongIntentionalPerturbation import STRongIntentionalPerturbation

# Utils
from utils.load_dataset import *
from utils.load_model import *
from utils.model import *

TAG = "Services"

###################################################################################################

def to_JSON(param: str):
    return json.loads(param)

def to_dict(params: Params) -> dict:
    return params.model_dump()

def load_dataset_service(dataset_type: str = "mnist", dataset_name = "dataset", path: dict = {"dataset_path_train":"../storage/dataset/train", "dataset_path_test":"../storage/dataset/test"}):
    LOG_SYS.write(TAG, f"Loading dataset from server storage at path: {path}")
    train_data, test_data, min_, max_ = get_dataset(dataset_type, path)
    
    if not train_data or test_data:
        LOG_SYS.write(TAG, f"Failed to load model from {dataset_type}.")
        raise HTTPException(status_code=500, detail=f"Impossible to load the dataset struct of type: {dataset_type}")
        
    LOG_SYS.write(TAG, f"Getting dataset info struct.")
    dataset_stats = get_dataset_info(train_data[0], test_data[0], dataset_type, dataset_name, path)
    
    if not train_data or test_data:
        LOG_SYS.write(TAG, f"Failed to load model from {dataset_type}.")
        raise HTTPException(status_code=500, detail=f"Impossible to load the dataset stats of type: {dataset_type}")
    
    LOG_SYS.write(TAG, f"Building dataset struct.")
    dataset_struct = {
        "train_data": train_data,
        "test_data": test_data,
        "min": min_,
        "max": max_
    }

    LOG_SYS.write(TAG, f"Loading dataset from server storage complete: {path}.")
    return dataset_struct, dataset_stats

def load_model_service(filename: str = "model.h5", alreadyCompiled: bool = True):
    LOG_SYS.write(TAG, f"Loading model from server directory named: {filename}.")
    model_path = STORAGE_MODEL_DIR.join(filename)
    loaded_model = load_model(model_path)
    
    if not loaded_model:
        LOG_SYS.write(TAG, f"Failed to load model from {model_path}.")
        raise HTTPException(status_code=404, detail=f"Model not found at {model_path}")

    if not alreadyCompiled:
        LOG_SYS.write(TAG, f"Model is not already compiled, compilation is started.")
        loaded_model = compile_model(loaded_model)

    LOG_SYS.write(TAG, f"Loading model from server directory complete: {filename}.")
    return loaded_model

###################################################################################################

async def perform_attack_service(params: Params, attack_type: str):
    LOG_SYS.write(TAG, "Loading local stored model.")
    iterator = iter(params.files.items())
    filename, alreadyCompiled = next(iterator)
    
    if not filename in LOCAL_MODELS.keys():
        LOCAL_MODELS[filename] = (load_model_service(filename, alreadyCompiled), STORAGE_MODEL_DIR.join(filename))

    model = LOCAL_MODELS[filename][0]
    
    LOG_SYS.write(TAG, "Loading local stored dataset.")
    dataset_type = params.dataset_type
    dataset_name = params.dataset_name
    dataset_path = params.dataset_path
    dataset_struct, dataset_stats = load_dataset_service(dataset_type, dataset_name, dataset_path)

    attack_type = attack_type.lower()
    
    if isinstance(params, EvasionModel):
        return await handle_evasion_attack(model, dataset_struct, dataset_stats, params, attack_type)
    elif isinstance(params, ExtractionModel):
        return await handle_extraction_attack(model, dataset_struct, dataset_stats, params, attack_type)
    elif isinstance(params, InferenceModel):
        return await handle_inference_attack(model, dataset_struct, dataset_stats, params, attack_type)
    elif isinstance(params, PoisoningModel):
        return await handle_poisoning_attack(model, dataset_struct, dataset_stats, params, attack_type)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack params type: {type(params)}.")
        raise HTTPException(status_code=404, detail=f"Model type: {type(params)} not supported.")

async def handle_evasion_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Evasion attack chosen, starting the attack setup.")
    evasion_attack = EvasionAttack(model, dataset_struct, dataset_stats, to_dict(params))
    evasion_classifier = evasion_attack.create_keras_classifier(model)
    
    if attack_type == "fgm":
        LOG_SYS.write(TAG, "Selected FGM attack, building the attack class.")
        evasion_attack = FGM(evasion_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        score_clean, score_adv = evasion_attack.evaluate(evasion_attack.perform_attack(evasion_classifier))
        return evasion_attack.result(score_clean, score_adv)
    elif attack_type == "pgd":
        LOG_SYS.write(TAG, "Selected PGD attack, building the attack class.")
        evasion_attack = PGD(evasion_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        score_clean, score_adv = evasion_attack.evaluate(evasion_attack.perform_attack(evasion_classifier))
        return evasion_attack.result(score_clean, score_adv)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Evasion attack type: {attack_type} not supported.")

async def handle_extraction_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Extraction attack chosen, starting the attack setup.")
    extraction_attack = ExtractionAttack(model, dataset_struct, dataset_stats, to_dict(params))
    original_dataset, stolen_dataset = extraction_attack.steal_model(params.steal_percentage)
    
    if attack_type == "copycatcnn":
        LOG_SYS.write(TAG, "Selected CopycatCNN attack, building the attack class.")
        extraction_attack = CopycatCNN(extraction_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        classifier_original, classifier_stolen = extraction_attack.perform_attack(original_dataset, stolen_dataset)
        score_clean, score_adv = extraction_attack.evaluate(classifier_original, classifier_stolen)
        return extraction_attack.result(score_clean, score_adv)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Extraction attack type: {attack_type} not supported.")

async def handle_inference_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Inference attack chosen, starting the attack setup.")
    inference_attack = EvasionAttack(model, dataset_struct, dataset_stats, to_dict(params))
    inference_classifier = inference_attack.create_keras_classifier(model)
    
    if attack_type == "miface":
        LOG_SYS.write(TAG, "Selected MIFace attack, building the attack class.")
        inference_attack = MIFace(inference_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        miface_data = inference_attack.evaluate(inference_attack.perform_attack(inference_classifier))
        return inference_attack.result(miface_data)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Inference attack type: {attack_type} not supported.")

async def handle_poisoning_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Poison attack chosen, starting the attack setup.")
    poisoning_attack = BackdoorAttack(model, dataset_struct, dataset_stats, to_dict(params))
    
    if attack_type == "cleanlabelbackdoor":
        LOG_SYS.write(TAG, "Selected Clean Label Backdoor attack, building the attack class.")
        poisoning_attack = CleanLabelBackdoor(poisoning_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        clean_test, poisoned_test, poison_struct, model_poisoned = poisoning_attack.perform_attack(model, params.target_labels)
        score_clean, score_poisoned = poisoning_attack.evaluate(clean_test, poisoned_test, model_poisoned)
        poison_data = {
            "clean_test": clean_test,
            "poisoned_test": poisoned_test,
            "poison_struct": poison_struct,
            "model_poisoned": model_poisoned
        }
        return poisoning_attack.result(score_clean, score_poisoned, poison_data)
    elif attack_type == "simplebackdoor":
        LOG_SYS.write(TAG, "Selected Simple Backdoor attack, building the attack class.")
        poisoning_attack = SimpleBackdoor(poisoning_attack)
        
        LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
        clean_test, poisoned_test, poison_struct, model_poisoned = poisoning_attack.perform_attack(model, params.target_labels)
        score_clean, score_poisoned = poisoning_attack.evaluate(clean_test, poisoned_test, model_poisoned)
        poison_data = {
            "clean_test": clean_test,
            "poisoned_test": poisoned_test,
            "poison_struct": poison_struct,
            "model_poisoned": model_poisoned
        }
        return poisoning_attack.result(score_clean, score_poisoned, poison_data)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Poisoning attack type: {attack_type} not supported.")

###################################################################################################

async def perform_defense_service(params: Params, defense_type: str):
    LOG_SYS.write(TAG, "Loading local stored vulnearble model.")
    iterator = iter(params.files.items())
    vulnerable_filename, vulnearble_alreadyCompiled = next(iterator)
    vulnerable_model = load_model_service(vulnerable_filename, vulnearble_alreadyCompiled)
    
    if not vulnerable_filename in LOCAL_MODELS.keys():
        LOCAL_MODELS[vulnerable_filename] = (load_model_service(vulnerable_filename, vulnearble_alreadyCompiled), STORAGE_MODEL_DIR.join(vulnerable_filename))
    
    vulnerable_model = LOCAL_MODELS[vulnerable_filename]
    
    LOG_SYS.write(TAG, "Loading local stored robust model.")
    robust_filename, robust_alreadyCompiled = next(iterator)
    robust_model = load_model_service(robust_filename, robust_alreadyCompiled)
    
    if not robust_filename in LOCAL_MODELS.keys():
        LOCAL_MODELS[robust_filename] = (load_model_service(robust_filename, robust_alreadyCompiled), STORAGE_MODEL_DIR.join(robust_filename))
    
    robust_model = LOCAL_MODELS[robust_filename]
    
    LOG_SYS.write(TAG, "Loading local stored dataset.")
    dataset_type = params.dataset_type
    dataset_name = params.dataset_name
    dataset_path = params.dataset_path
    dataset_struct, dataset_stats = load_dataset_service(dataset_type, dataset_name, dataset_path)

    defense_type = defense_type.lower()
    
    if isinstance(params, DetectorModel):
        return await handle_detector_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, PostprocessorModel):
        return await handle_postprocessor_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, PreprocessorModel):
        return await handle_preprocessor_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, TrainerModel):
        return await handle_trainer_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, TransformerModel):
        return await handle_transformer_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense param type: {type(params)}.")
        raise HTTPException(status_code=404, detail=f"Model type: {type(params)} not supported.")

async def handle_detector_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Detector defense chosen, starting the defense setup.")
    detector_defense = DetectorDefense(vulnerable_model, robust_model, dataset_struct, dataset_stats, to_dict(params))
    
    if defense_type == "activationdefense":
        LOG_SYS.write(TAG, "Selected Activation defense, building the defense class.")
        detector_defense = ActivationDefense(detector_defense)
        
        LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
        clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense = detector_defense.perform_defense()
        attack_metrics, defense_metrics = detector_defense.evaluate(clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense)
        return detector_defense.result(attack_metrics, defense_metrics)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Detector defense type: {defense_type} not supported.")

async def handle_postprocessor_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Postprocessor defense chosen, starting the defense setup.")
    postprocessor_defense = PostprocessorDefense(vulnerable_model, robust_model, dataset_struct, dataset_stats, to_dict(params))
    
    if defense_type == "reversesigmoid":
        LOG_SYS.write(TAG, "Selected Reverse Sigmoid defense, building the defense class.")
        postprocessor_defense = ReverseSigmoid(postprocessor_defense)
        
        LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
        classifiers, stolen_classifiers, stolen_classifiers_probabilistic = postprocessor_defense.perform_defense()
        raise NotImplementedError("Reverse Sigmoide not implemented ad-hoc yet.")
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Postprocessor defense type: {defense_type} not supported.")

async def handle_preprocessor_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Preprocessor defense chosen, starting the defense setup.")
    preprocessor_defense = PreprocessorDefense(vulnerable_model, robust_model, dataset_struct, dataset_stats, to_dict(params))
    
    if defense_type == "totalvarmin":
        LOG_SYS.write(TAG, "Selected Total Variance Minimization defense, building the defense class.")
        preprocessor_defense = TotalVarMin(preprocessor_defense)
        
        LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
        test_images_attack, test_images_attack_cleaned, vulnerable_classifier = preprocessor_defense.perform_defense()
        score_attack, score_attack_cleaned = preprocessor_defense.evaluate(test_images_attack, test_images_attack_cleaned, vulnerable_classifier)
        return preprocessor_defense.result(score_attack, score_attack_cleaned)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Preprocessor defense type: {defense_type} not supported.")

async def handle_trainer_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Trainer defense chosen, starting the defense setup.")
    trainer_defense = TrainerDefense(vulnerable_model, robust_model, dataset_struct, dataset_stats, to_dict(params))
    
    if defense_type == "adversarialtrainer":
        LOG_SYS.write(TAG, "Selected Adversarial Trainer defense, building the attack class.")
        trainer_defense = AdversarialTrainer(trainer_defense)
        
        LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
        test_images_attack, robust_classifier, vulnerable_classifier = trainer_defense.perform_defense()
        score_clean, score_attack, score_robust_attack = trainer_defense.evaluate(test_images_attack, robust_classifier, vulnerable_classifier)
        return trainer_defense.result(score_attack, score_clean, score_attack, score_robust_attack)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Trainer defense type: {defense_type} not supported.")

async def handle_transformer_defense(vulnerable_model, robust_model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Transformer defense chosen, starting the defense setup.")
    transformer_defense = TransformerDefense(vulnerable_model, robust_model, dataset_struct, dataset_stats, to_dict(params))
    
    if defense_type == "strip":
        LOG_SYS.write(TAG, "Selected STRong Intentional Perturbation defense, building the attack class.")
        transformer_defense = STRongIntentionalPerturbation(transformer_defense)
        
        LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
        clean_test, poisoned_test, model_poisoned, defense = transformer_defense.perform_defense()
        num_abstained, num_clean, num_poison = transformer_defense.evaluate(clean_test, poisoned_test, model_poisoned, defense)
        return transformer_defense.result(num_abstained, num_clean, num_poison)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Transformer defense type: {defense_type} not supported.")
    
    ###############################################################################################