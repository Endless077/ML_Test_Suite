# Input Validation
from pydantic import Field, validator, BaseModel

# Main Params Payload
class Params(BaseModel):
    is_trained_model: bool
    default_model: bool
    dataset_type: str
    
    epochs: int = Field(default=1, ge=1)
    batch_size: int = Field(default=32, ge=32)
    
    @validator('dataset_type', pre=True, always=True)
    def dataset_type_validation(cls, value):
        if value.strip() not in ['mnist', 'cifar10', 'cifar100', 'personal']:
            raise ValueError("Dataset type must be 'mnist', 'cifar10', 'cifar100', or 'personal'.")
        return value.strip()

###################################################################################################

class EvasionModel(Params):
    norm: int | float | str = float('inf')
    eps: float = Field(default=0.3, ge=0.3)
    eps_step: float = Field(default=0.1, ge=0.1)
    
    @validator("norm", pre=True, always=True)
    def norm_validation(cls, v):
        if isinstance(v, str):
            if v.lower() == "inf":
                return float('inf')
            else:
                raise ValueError("String norm value must be 'inf'.")
        elif v == 1 or v == 2:
            return v
        else:
            raise ValueError("Norm value must be 'inf', 1, or 2.")

###

class ExtractionModel(Params):
    use_probability: bool = False
    steal_percentage: float = Field(default=0.5, ge=0.1, le=0.7)

###
    
class InferenceModel(Params):
    max_iter: int = Field(default=10000, ge=1)
    window_length: int = Field(default=100, ge=1)
    threshold: float = Field(default=0.99, ge=0.1, le=1)
    learning_rate: float = Field(default=0.1, ge=0.1)

###

class PoisoningModel(Params):
    poison_percentage: float = Field(default=0.3, ge=0.1, le=0.7)
    
###################################################################################################

class DetectorModel(Params):
    poison_attack: str
    poison_percentage: float = Field(default=0.3, ge=0.1, le=0.7)

    poison_params: PoisoningModel
    
    nb_clusters: int = Field(default=2, ge=2)
    reduce: str = "PCA"
    nb_dims: int = Field(default=10, ge=1)
    cluster_analysis: str
            
    @validator('poison_attack', pre=True, always=True)
    def poison_attack_validation(cls, value):
        if value.strip() not in ['cleanlabels', 'simple']:
            raise ValueError("Poison attack type must be 'cleanlabels' or 'simple'.")
        return value.strip()
    
    @validator('reduce', pre=True, always=True)
    def reduce_validation(cls, value):
        if value.strip() not in ['FastICA', 'TSNE', 'PCA']:
            raise ValueError("Reduce type must be 'FastICA', 'TSNE' or 'PCA'.")
        return value.strip()

    @validator('cluster_analysis', pre=True, always=True)
    def cluster_analysis_validation(cls, value):
        if value.strip() not in ['smaller', 'distance']:
            raise ValueError("Cluster Analysis type must be 'smaller ' or 'distance'.")
        return value.strip()

###

class PostprocessorModel(Params):
    beta: float = Field(default=1.0, ge=0.1)
    gamma: float = Field(default=0.1, ge=0.1)

###

class PreprocessorModel(Params):
    evasion_attack: str
    samples_percentage: float = Field(default=0.1, ge=0.1)
    
    evasion_params: EvasionModel
    
    prob: float = Field(default=0.3, ge=0.1, le=1)
    norm: int = Field(default=2, ge=1)
    lamb: float = Field(default=0.5, ge=0.1)
    solver: str
    max_iter: int = Field(default=10, ge=1)

    @validator('evasion_attack', pre=True, always=True)
    def evasion_attack_validation(cls, value):
        if value.strip() not in ['fgm', 'pgd']:
            raise ValueError("Evasion attack type must be 'fgm' or 'pgd'.")
        return value.strip()
    
    @validator('solver', pre=True, always=True)
    def solver_validation(cls, value):
        if value.strip() not in ['L-BFGS-B', 'CG', 'Newton-CG']:
            raise ValueError("Solverk type must be 'L-BFGS-B', 'CG' or 'Newton-CG'.")
        return value.strip()

###

class TrainerModel(Params):
    evasion_attack: str
    samples_percentage: float = Field(default=0.1, ge=0.1)
    
    evasion_params: EvasionModel
    
    ratio: float = Field(default=0.5, ge=0.1, le=1)
    
    @validator('evasion_attack', pre=True, always=True)
    def evasion_attack_validation(cls, value):
        if value.strip() not in ['fgm', 'pgd']:
            raise ValueError("Evasion attack type must be 'fgm' or 'pgd'.")
        return value.strip()

###
   
class TransformerModel(Params):
    poison_attack: str
    poison_percentage: float = Field(default=0.3, ge=0.1, le=0.7)
    
    poison_params: PoisoningModel
    
    @validator('poison_attack', pre=True, always=True)
    def poison_attack_validation(cls, value):
        if value.strip() not in ['cleanlabels', 'simple']:
            raise ValueError("Poison attack type must be 'cleanlabels' or 'simple'.")
        return value.strip()

###################################################################################################
