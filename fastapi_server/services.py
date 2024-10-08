# Logging Analytics System
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

def load_model_service(filename: str = "model.h5"):
    LOG_SYS.write(TAG, f"Loading model from server directory named: {filename}.")
    model_path = os.path.join(STORAGE_MODEL_DIR, filename)
    loaded_model = load_model(model_path)
    
    if not loaded_model:
        LOG_SYS.write(TAG, f"Failed to load model from {model_path}.")
        raise HTTPException(status_code=404, detail=f"Model not found at {model_path}")

    if loaded_model.optimizer is None:
        LOG_SYS.write(TAG, f"Model is not already compiled, compilation is started.")
        return compile_model(loaded_model)

    LOG_SYS.write(TAG, f"Loading model from server directory complete: {filename}.")
    return loaded_model

def load_dataset_service(dataset_type: str = "mnist", dataset_name = "dataset", path: dict = {"dataset_path_train":"../storage/dataset/train", "dataset_path_test":"../storage/dataset/test"}):
    LOG_SYS.write(TAG, f"Loading dataset from local server storage")
    train_data, test_data, min_, max_ = get_dataset(dataset_type, path)
    
    if not train_data or not test_data:
        LOG_SYS.write(TAG, f"Failed to load dataset from {dataset_type}.")
        raise HTTPException(status_code=500, detail=f"Impossible to load the dataset struct of type: {dataset_type}")
        
    LOG_SYS.write(TAG, f"Getting dataset info struct.")
    dataset_stats = get_dataset_info(train_data[0], test_data[0], dataset_type, dataset_name, path)
    
    if not train_data or not test_data:
        LOG_SYS.write(TAG, f"Failed to load dataset from {dataset_type}.")
        raise HTTPException(status_code=500, detail=f"Impossible to load the dataset stats of type: {dataset_type}")
    
    LOG_SYS.write(TAG, f"Building dataset struct.")
    dataset_struct = {
        "train_data": train_data,
        "test_data": test_data,
        "min": min_,
        "max": max_
    }

    LOG_SYS.write(TAG, f"Loading dataset from local server storage complete.")
    return dataset_struct, dataset_stats

###################################################################################################

async def perform_attack_service(params: Params, attack_type: str):
    LOG_SYS.write(TAG, "Loading local stored model.")
    filename = params.filename
    
    if not filename in LOCAL_MODELS.keys():
        LOCAL_MODELS[filename] = (load_model_service(filename), filename)

    model = LOCAL_MODELS[filename][0]
    
    LOG_SYS.write(TAG, "Loading local stored dataset.")
    dataset_type = params.dataset_type
    dataset_name = params.dataset_name
    dataset_path = {f"dataset_path_train":"../storage/dataset/{dataset_name}/train", f"dataset_path_test":"../storage/dataset/{dataset_name}/test"}
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
    params_dict = to_dict(params)

    LOG_SYS.write(TAG, "Fitting the stored model.")
    fitted_model = fit_model(dataset_struct["train_data"], model, params.batch_size, params.epochs)
    
    if attack_type == "fgm":
        LOG_SYS.write(TAG, "Selected FGM attack, building the attack class.")
        evasion_attack = FGM(fitted_model, dataset_struct, dataset_stats, params_dict)
    elif attack_type == "pgd":
        LOG_SYS.write(TAG, "Selected PGD attack, building the attack class.")
        evasion_attack = PGD(fitted_model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Evasion attack type: {attack_type} not supported.")
    
    LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
    LOG_SYS.write(TAG, "Create a Keras Classifier.")
    evasion_classifier = AttackClass.create_keras_classifier(self=None, model=fitted_model)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack.")
    attack_results = evasion_attack.perform_attack(evasion_classifier)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack evaluation.")
    score_clean, score_adv = evasion_attack.evaluate(attack_results)
    LOG_SYS.write(TAG, f"Return the {attack_type} attack results.")
    return evasion_attack.result(score_clean, score_adv)


async def handle_extraction_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Extraction attack chosen, starting the attack setup.")
    params_dict = to_dict(params)
    
    if attack_type == "copycatcnn":
        LOG_SYS.write(TAG, "Selected CopycatCNN attack, building the attack class.")
        extraction_attack = CopycatCNN(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Extraction attack type: {attack_type} not supported.")
    
    LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
    LOG_SYS.write(TAG, f"Stealing the dataset with a steal percentage: {(params.steal_percentage)*100}%")
    original_dataset, stolen_dataset = extraction_attack.steal_model(params.steal_percentage)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack.")
    classifier_original, classifier_stolen = extraction_attack.perform_attack(original_dataset, stolen_dataset)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack evaluation.")
    score_clean, score_adv = extraction_attack.evaluate(classifier_original, classifier_stolen)
    LOG_SYS.write(TAG, f"Return the {attack_type} attack results.")
    return extraction_attack.result(score_clean, score_adv)


async def handle_inference_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Inference attack chosen, starting the attack setup.")
    params_dict = to_dict(params)

    LOG_SYS.write(TAG, "Fitting the stored model.")
    fitted_model = fit_model(dataset_struct["train_data"], model, params.batch_size, params.epochs)
    
    if attack_type == "miface":
        LOG_SYS.write(TAG, "Selected MIFace attack, building the attack class.")
        inference_attack = MIFace(fitted_model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Inference attack type: {attack_type} not supported.")
    
    LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
    LOG_SYS.write(TAG, f"Creating the {attack_type} Keras Classifier.")
    inference_classifier = inference_attack.create_keras_classifier(model)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack.")
    miface_inverted_dataset = inference_attack.perform_attack(inference_classifier)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack evaluation.")
    miface_data = inference_attack.evaluate(miface_inverted_dataset)
    LOG_SYS.write(TAG, f"Return the {attack_type} attack results.")
    return inference_attack.result(miface_data)


async def handle_poisoning_attack(model, dataset_struct, dataset_stats, params, attack_type):
    LOG_SYS.write(TAG, "Poison attack chosen, starting the attack setup.")
    params_dict = to_dict(params)

    if attack_type == "cleanlabelbackdoor":
        LOG_SYS.write(TAG, "Selected Clean Label Backdoor attack, building the attack class.")
        poisoning_attack = CleanLabelBackdoor(model, dataset_struct, dataset_stats, params_dict)
    elif attack_type == "simplebackdoor":
        LOG_SYS.write(TAG, "Selected Simple Backdoor attack, building the attack class.")
        poisoning_attack = SimpleBackdoor(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported attack type: {attack_type}.")
        raise HTTPException(status_code=404, detail=f"Poisoning attack type: {attack_type} not supported.")

    LOG_SYS.write(TAG, f"Performing {attack_type}, scores evaluation and building result struct.")
    clean_test, poisoned_test, poison_struct, model_poisoned = poisoning_attack.perform_attack(params.target_labels)
    LOG_SYS.write(TAG, f"Starting {attack_type} attack evaluation.")
    score_clean, score_poisoned = poisoning_attack.evaluate(clean_test, poisoned_test, model_poisoned)
    poison_data = {
        "clean_test": clean_test,
        "poisoned_test": poisoned_test,
        "poison_struct": poison_struct,
        "model_poisoned": model_poisoned
    }
    LOG_SYS.write(TAG, f"Return the {attack_type} attack results.")
    return poisoning_attack.result(score_clean, score_poisoned, poison_data)

###################################################################################################

async def perform_defense_service(params: Params, defense_type: str):
    LOG_SYS.write(TAG, "Loading local stored model.")
    filename = params.filename
    
    if not filename in LOCAL_MODELS.keys():
        LOCAL_MODELS[filename] = (load_model_service(filename), filename)
    
    model = LOCAL_MODELS[filename][0]
    
    LOG_SYS.write(TAG, "Loading local stored dataset.")
    dataset_type = params.dataset_type
    dataset_name = params.dataset_name
    dataset_path = {f"dataset_path_train":"../storage/dataset/{dataset_name}/train", f"dataset_path_test":"../storage/dataset/{dataset_name}/test"}
    dataset_struct, dataset_stats = load_dataset_service(dataset_type, dataset_name, dataset_path)
    
    defense_type = defense_type.lower()
    
    if isinstance(params, DetectorModel):
        return await handle_detector_defense(model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, PostprocessorModel):
        return await handle_postprocessor_defense(model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, PreprocessorModel):
        return await handle_preprocessor_defense(model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, TrainerModel):
        return await handle_trainer_defense(model, dataset_struct, dataset_stats, params, defense_type)
    elif isinstance(params, TransformerModel):
        return await handle_transformer_defense(model, dataset_struct, dataset_stats, params, defense_type)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense param type: {type(params)}.")
        raise HTTPException(status_code=404, detail=f"Model type: {type(params)} not supported.")


async def handle_detector_defense(model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Detector defense chosen, starting the defense setup.")
    params_dict = to_dict(params)
     
    if defense_type == "activationdefense":
        LOG_SYS.write(TAG, "Selected Activation defense, building the defense class.")
        detector_defense = ActivationDefense(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Detector defense type: {defense_type} not supported.")

    LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
    clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense = detector_defense.perform_defense()
    LOG_SYS.write(TAG, f"Starting {defense_type} defense evaluation.")
    attack_metrics, defense_metrics = detector_defense.evaluate(clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense)
    LOG_SYS.write(TAG, f"Return the {defense_type} defense results.")
    return detector_defense.result(attack_metrics, defense_metrics)


async def handle_postprocessor_defense(model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Postprocessor defense chosen, starting the defense setup.")
    params_dict = to_dict(params)
    
    if defense_type == "reversesigmoid":
        LOG_SYS.write(TAG, "Selected Reverse Sigmoid defense, building the defense class.")
        postprocessor_defense = ReverseSigmoid(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Postprocessor defense type: {defense_type} not supported.")

    LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
    classifier_original, classifier_stolen = postprocessor_defense.perform_defense()
    LOG_SYS.write(TAG, f"Starting {defense_type} defense evaluation.")
    unprotected_classifier, protected_classifier = classifier_original
    unpotected_stolen, protected_stolen = classifier_stolen
    score_victim, score_stolen_unprotected, score_stolen_protected = postprocessor_defense.evaluate(unprotected_classifier, unpotected_stolen, protected_stolen)
    LOG_SYS.write(TAG, f"Return the {defense_type} defense results.")
    return postprocessor_defense.result(score_victim, score_stolen_unprotected, score_stolen_protected)


async def handle_preprocessor_defense(model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Preprocessor defense chosen, starting the defense setup.")
    params_dict = to_dict(params)
    
    if defense_type == "totalvarmin":
        LOG_SYS.write(TAG, "Selected Total Variance Minimization defense, building the defense class.")
        preprocessor_defense = TotalVarMin(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Preprocessor defense type: {defense_type} not supported.")
    
    LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
    test_images_attack, test_images_attack_cleaned, vulnerable_classifier = preprocessor_defense.perform_defense()
    LOG_SYS.write(TAG, f"Starting {defense_type} defense evaluation.")
    score_attack, score_attack_cleaned = preprocessor_defense.evaluate(test_images_attack, test_images_attack_cleaned, vulnerable_classifier)
    LOG_SYS.write(TAG, f"Return the {defense_type} defense results.")
    return preprocessor_defense.result(score_attack, score_attack_cleaned)


async def handle_trainer_defense(model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Trainer defense chosen, starting the defense setup.")
    params_dict = to_dict(params)
    
    if defense_type == "adversarialtrainer":
        LOG_SYS.write(TAG, "Selected Adversarial Trainer defense, building the attack class.")
        trainer_defense = AdversarialTrainer(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Trainer defense type: {defense_type} not supported.")

    LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
    test_images_attack, robust_classifier, vulnerable_classifier = trainer_defense.perform_defense()
    LOG_SYS.write(TAG, f"Starting {defense_type} defense evaluation.")
    score_clean, score_attack, score_robust_attack = trainer_defense.evaluate(test_images_attack, robust_classifier, vulnerable_classifier)
    LOG_SYS.write(TAG, f"Return the {defense_type} defense results.")
    return trainer_defense.result(score_clean, score_attack, score_robust_attack)


async def handle_transformer_defense(model, dataset_struct, dataset_stats, params, defense_type):
    LOG_SYS.write(TAG, "Transformer defense chosen, starting the defense setup.")
    params_dict = to_dict(params)
    
    if defense_type == "strip":
        LOG_SYS.write(TAG, "Selected STRong Intentional Perturbation defense, building the attack class.")
        transformer_defense = STRongIntentionalPerturbation(model, dataset_struct, dataset_stats, params_dict)
    else:
        LOG_SYS.write(TAG, f"Unsupported defense type: {defense_type}.")
        raise HTTPException(status_code=404, detail=f"Transformer defense type: {defense_type} not supported.")
    
    LOG_SYS.write(TAG, f"Performing {defense_type}, scores evaluation and building result struct.")
    clean_test, poisoned_test, model_poisoned, defense = transformer_defense.perform_defense()
    LOG_SYS.write(TAG, f"Starting {defense_type} defense evaluation.")
    num_abstained, num_clean, num_poison = transformer_defense.evaluate(clean_test, poisoned_test, model_poisoned, defense)
    LOG_SYS.write(TAG, f"Return the {defense_type} defense results.")
    return transformer_defense.result(num_abstained, num_clean, num_poison)
    
    ###############################################################################################