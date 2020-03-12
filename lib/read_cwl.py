from cwltool.load_tool import load_tool
from cwltool.workflow import default_make_tool

basic_cwl_path = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/data/workflows/basic_example_v2.cwl"
# basic_cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example_v2.cwl"
cwl_path = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/data/workflows/rp2-to-rp2path_modified.cwl"
# cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/rp2-to-rp2path_modified.cwl"

cwl_document = load_tool(basic_cwl_path)
inputs_record_schema = cwl_document.inputs_record_schema["fields"]
outputs_record_schema = cwl_document.outputs_record_schema["fields"]
print("INPUT RECORD SCHEMA: {}".format(inputs_record_schema))
print("OUTPUT RECORD SCHEMA: {}".format(outputs_record_schema))

for inputs in inputs_record_schema:
    print(inputs)

for outputs in outputs_record_schema:
    print(outputs)
    # for item in outputs.items():
    #     print(item)
