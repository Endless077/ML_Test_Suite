# Import Modules
from pydantic import BaseModel, conint, conbool, constr

class ModelParams(BaseModel):
    is_trained_model: bool
    default_model: bool
    epochs: conint(ge=1)
    batch_size: conint(ge=32)

class Path(BaseModel):
    vulnerable_model_path: constr(min_length=1, regex=r".*(\.h5|saved_model.pb|variables|assets)$") = "../model/vulnerable_models/"
    robust_model_path: constr(min_length=1, regex=r".*(\.h5|saved_model.pb|variables|assets)$") = "../model/robust_models/"
    model_path: constr(min_length=1, regex=r".*(\.h5|saved_model.pb|variables|assets)$") = "../model/model.h5"
    dataset_path_train: constr(min_length=1, regex=r".*(\.h5|saved_model.pb|variables|assets)$") = "../dataset/train"
    dataset_path_test: constr(min_length=1, regex=r".*(\.h5|saved_model.pb|variables|assets)$") = "../dataset/test"

class Payload(BaseModel):
    function: constr(strip_whitespace=True, min_length=1, regex=r'^(attack|defense)$')
    method: constr(strip_whitespace=True, min_length=1)
    dataset_type: constr(strip_whitespace=True, min_length=1, regex=r'^(mnist|cifar10|cifar100|personal)$')
    model_params: ModelParams
    path: Path
