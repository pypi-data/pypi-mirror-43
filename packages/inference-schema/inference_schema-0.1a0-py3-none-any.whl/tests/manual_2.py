# import sklearn
# from azureml.core.model import Model
# from sklearn.externals import joblib

import json
import numpy as np
from inference_schema.schema_decorators import input_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType

sample_data = np.array([[1.8]])
# sample_data = np.asarray(json.dumps({"data":[[1.8]]}).replace(" ", "").replace('"', r'\"'))


def init():
    global model

    model_file = Model.get_model_path('Salary_Predictor')
    with open(model_file, 'rb') as f:
        model = joblib.load(f)


@input_schema('data', NumpyParameterType(sample_data))
def run(data):
    # try:
    #     res = model.predict(data)
    #     return res.tolist()
    # except Exception as e:
    #     return str(e)
    print(type(data))
    return data


print(run([[1.8]]))
