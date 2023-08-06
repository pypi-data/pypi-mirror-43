import numpy as np
from inference_schema.schema_decorators import input_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.schema_util import get_input_schema

data = [('Sarah', (8.0, 7.0)), ('John', (6.0, 7.0))]
sample = np.array(data, dtype=np.dtype([('name', np.unicode_, 16), ('grades', np.float64, (2,))]))
data_2 = [(0, 1), (2, 3)]
sample_2 = np.array(data_2, dtype='int32, float64')
print("sample: ", sample)

# data_3 = [{'f0': 0, 'f1': 1.0}, {'f0': 2, 'f1': 3.0}]
# sample_3 = np.array(data_3, dtype='int32, float64')


@input_schema('input', NumpyParameterType(sample))
def run(input):
    print(type(input), input.dtype)
    return input


print("run sample: ", run(sample))

example = get_input_schema(run)['example']
print("swagger example: ", example)
print("run data: ", run(data))
print("run args: ", run(example['input']))
print("run kwargs: ", run(**example))
