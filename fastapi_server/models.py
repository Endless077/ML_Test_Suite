# Models
from pydantic import Field, field_validator, BaseModel
from typing import List, Dict, Union

class Params(BaseModel):
    epochs: int = Field(default=1, ge=1, description="Number of epochs for training.")
    batch_size: int = Field(default=32, ge=32, description="Batch size for training.")

    filename: str = Field(default="model", description="Model filename.")
    dataset_type: str = Field(default=None, description="Type of dataset used.")
    dataset_name: str = Field(default=None, description="Name of dataset used.")

    @field_validator('dataset_type')
    def dataset_type_validation(cls, value):
        if value.strip() not in ['mnist', 'cifar10', 'cifar100', 'personal']:
            raise ValueError("Dataset type must be 'mnist', 'cifar10', 'cifar100', or 'personal'.")
        return value.strip()

###################################################################################################

class EvasionModel(Params):
    eps: float = Field(default=0.3, ge=0.3, description="Epsilon value for the attack.")
    eps_step: float = Field(default=0.1, ge=0.1, description="Step size for epsilon.")
    norm: Union[int, float, str] = Field(default="inf", description="Norm for the attack.")

    @field_validator("norm")
    def norm_validation(cls, v):
        if isinstance(v, str):
            if v.lower() == "inf":
                return "inf"
            else:
                raise ValueError("String norm value must be 'inf'.")
        elif int(v) == 1 or int(v) == 2:
            return v
        else:
            raise ValueError("Norm value must be 'inf', 1, or 2.")

class ExtractionModel(Params):
    steal_percentage: float = Field(default=0.5, ge=0.1, le=0.7, description="Percentage of information to steal.")
    use_probability: bool = Field(default=False, description="Indicates whether to use probability.")

class InferenceModel(Params):
    max_iter: int = Field(default=10000, ge=1, description="Maximum number of iterations.")
    window_length: int = Field(default=100, ge=1, description="Length of the window.")
    threshold: float = Field(default=0.99, ge=0.1, le=1, description="Decision threshold.")
    learning_rate: float = Field(default=0.1, ge=0.1, description="Learning rate.")

class PoisoningModel(Params):
    poisoned_percentage: float = Field(default=0.3, ge=0.1, le=0.7, description="Percentage of poisoning.")
    target_labels: List[Union[int, str]] = Field(default=[], description="Target Labels to poisoning.")

###################################################################################################

class DetectorModel(Params):
    poison_attack: str = Field(..., description="Type of poisoning attack.")
    
    poisoned_percentage: float = Field(default=0.3, ge=0.1, le=0.7, description="Percentage of poisoning.")

    cluster_analysis: str = Field(..., description="Type of cluster analysis.")
    reduce: str = Field("PCA", description="Type of reduction.")
    nb_clusters: int = Field(default=2, ge=2, description="Number of clusters.")
    nb_dims: int = Field(default=10, ge=1, description="Number of dimensions.")

    @field_validator('poison_attack')
    def poison_attack_validation(cls, value):
        if value.strip() not in ['cleanlabel', 'simple']:
            raise ValueError("Poison attack type must be 'cleanlabel' or 'simple'.")
        return value.strip()

    @field_validator('reduce')
    def reduce_validation(cls, value):
        if value.strip() not in ['FastICA', 'TSNE', 'PCA']:
            raise ValueError("Reduce type must be 'FastICA', 'TSNE' or 'PCA'.")
        return value.strip()

    @field_validator('cluster_analysis')
    def cluster_analysis_validation(cls, value):
        if value.strip() not in ['smaller', 'distance']:
            raise ValueError("Cluster Analysis type must be 'smaller' or 'distance'.")
        return value.strip()

class PostprocessorModel(Params):
    beta: float = Field(default=1.0, ge=0.1, description="Value of beta.")
    gamma: float = Field(default=0.1, ge=0.1, description="Value of gamma.")
    
    steal_percentage: float = Field(default=0.5, ge=0.1, le=0.7, description="Percentage of information to steal.")
    use_probability: bool = Field(default=False, description="Indicates whether to use probability.")
    
class PreprocessorModel(Params):
    evasion_attack: str = Field(..., description="Type of evasion attack.")
    samples_percentage: float = Field(default=0.1, ge=0.1, le=1, description="Percentage of samples to use.")

    eps: float = Field(default=0.3, ge=0.3, description="Epsilon value for the attack.")
    eps_step: float = Field(default=0.1, ge=0.1, description="Step size for epsilon.")
    norm: Union[int, float, str] = Field("inf", description="Norm for the attack.")

    prob: float = Field(default=0.3, ge=0.1, le=1, description="Probability value.")
    norm_value: int = Field(default=2, ge=1, description="Norm value.")
    lamb_value: float = Field(default=0.5, ge=0.1, description="Lambda value.")
    solver: str = Field(..., description="Type of solver.")
    max_iter: int = Field(default=10, ge=1, description="Maximum number of iterations.")

    @field_validator('evasion_attack')
    def evasion_attack_validation(cls, value):
        if value.strip() not in ['fgm', 'pgd']:
            raise ValueError("Evasion attack type must be 'fgm' or 'pgd'.")
        return value.strip()

    @field_validator('solver')
    def solver_validation(cls, value):
        if value.strip() not in ['L-BFGS-B', 'CG', 'Newton-CG']:
            raise ValueError("Solver type must be 'L-BFGS-B', 'CG' or 'Newton-CG'.")
        return value.strip()

class TrainerModel(Params):
    evasion_attack: str = Field(..., description="Type of evasion attack.")
    samples_percentage: float = Field(default=0.1, ge=0.1, le=1, description="Percentage of samples to use.")
    
    eps: float = Field(default=0.3, ge=0.3, description="Epsilon value for the attack.")
    eps_step: float = Field(default=0.1, ge=0.1, description="Step size for epsilon.")
    norm: Union[int, float, str] = Field("inf", description="Norm for the attack.")
    
    ratio: float = Field(default=0.5, ge=0.1, le=1, description="Value of ratio.")

    @field_validator('evasion_attack')
    def evasion_attack_validation(cls, value):
        if value.strip() not in ['fgm', 'pgd']:
            raise ValueError("Evasion attack type must be 'fgm' or 'pgd'.")
        return value.strip()

class TransformerModel(Params):
    poison_attack: str = Field(..., description="Type of poisoning attack.")
    poisoned_percentage: float = Field(default=0.3, ge=0.1, le=0.7, description="Percentage of poisoning.")

    @field_validator('poison_attack')
    def poison_attack_validation(cls, value):
        if value.strip() not in ['cleanlabel', 'simple']:
            raise ValueError("Poison attack type must be 'cleanlabel' or 'simple'.")
        return value.strip()

###################################################################################################
