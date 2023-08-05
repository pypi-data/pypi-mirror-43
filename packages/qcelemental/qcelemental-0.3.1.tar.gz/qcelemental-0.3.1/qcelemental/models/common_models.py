from enum import Enum
from typing import Any, Dict, Optional

import numpy as np
from pydantic import BaseModel

ndarray_encoder = {np.ndarray: lambda v: v.flatten().tolist()}


class Provenance(BaseModel):
    creator: str
    version: Optional[str] = None
    routine: Optional[str] = None

    class Config:
        extra = "allow"


class Model(BaseModel):
    method: str
    basis: Optional[str] = None

    # basis_spec: BasisSpec = None  # This should be exclusive with basis, but for now will be omitted

    class Config:
        allow_mutation = False
        extra = "allow"


class DriverEnum(str, Enum):
    energy = 'energy'
    gradient = 'gradient'
    hessian = 'hessian'
    properties = 'properties'


class ComputeError(BaseModel):
    """The type of error message raised"""
    error_type: str  # Error enumeration not yet strict
    error_message: str
    extras: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"


class FailedOperation(BaseModel):
    id: str = None
    input_data: Any = None
    success: bool = False
    error: ComputeError
    extras: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"
        allow_mutation = False
        json_encoders = {**ndarray_encoder}


qcschema_input_default = "qcschema_input"
qcschema_output_default = "qcschema_output"
qcschema_optimization_input_default = "qcschema_optimization_input"
qcschema_optimization_output_default = "qcschema_optimization_output"
qcschema_molecule_default = "qcschema_molecule"
