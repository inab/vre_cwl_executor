import json
import os

from cwltool.load_tool import fetch_document
from cwltool.main import print_pack
from cwltool.load_tool import resolve_and_validate_document

os.chdir(os.path.dirname(__file__))


def resolve_and_validate(cwl_path):
    """

    """
    try:
        loadingContext, workflowobj, uri = fetch_document(cwl_path)
        loadingContext.do_update = False
        loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)
        processobj = loadingContext.loader.resolve_ref(uri)[0]
        packed_cwl = json.loads(print_pack(loadingContext.loader, processobj, uri, loadingContext.metadata))
        return packed_cwl

    except Exception as error:
        errstr = "Unable to pack CWL. ERROR: {}".format(error)
        raise Exception(errstr)


def pack_cwl(wf_path):
    """

    """
    cwl_filename = os.path.basename(wf_path)
    cwl_file_path = os.path.join(os.path.curdir, cwl_filename.split(".")[0])
    if not os.path.exists(cwl_file_path):
        os.makedirs(cwl_file_path)

    try:
        packed_cwl = resolve_and_validate(wf_path)
        packed_cwl_path = os.path.join(cwl_file_path, "pack_" + cwl_filename)
        with open(packed_cwl_path, 'w') as cwl_file:
            json.dump(packed_cwl, cwl_file)

    except Exception as error:
        errstr = "Unable to create CWL packed. ERROR: {}".format(error)
        raise Exception(errstr)

    # cwl_document = read_config_from_cwl_file(packed_cwl_path)


def read_config_from_cwl_file(cwl_file):
    print(cwl_file)
    print_pref = "[read_cwl_file]:"
    configs = {}
    metadata = {
        "doc": "",
        "workflow_name": os.path.basename(cwl_file),
        "workflow_path": os.path.abspath(cwl_file),
        "workflow_type": "CWL"
    }
    print(os.path.basename(cwl_file))
    print(os.path.abspath(cwl_file))
    # cwltool needs to be imported on demand since
    # repeatedly calling functions on a document named
    # with same name caused errors.
    from cwltool.context import LoadingContext
    from cwltool.load_tool import load_tool
    from cwltool.workflow import default_make_tool
    loadingContext = LoadingContext({"construct_tool_object": default_make_tool, "disable_js_validation": True})
    try:
        cwl_document = load_tool(cwl_file, loadingContext)
    except AssertionError as e:
        raise AssertionError(print_pref + "failed to read cwl file \"" + cwl_file + "\": does not exist or is invalid")
    inp_records = cwl_document.inputs_record_schema["fields"]
    outp_records = cwl_document.outputs_record_schema["fields"]
    print(inp_records)
    print(outp_records)
    if "doc" in cwl_document.tool:
        metadata["doc"] = cwl_document.tool["doc"]
    # for inp_rec in inp_records:
    #     name = clean_string( inp_rec["name"] )
    #     is_array = False
    #     null_allowed = False
    #     null_items_allowed = False
    #     default_value = [""]
    #     # read type:
    #     try:
    #         type_, null_allowed, is_array, null_items_allowed = read_inp_rec_type_field(inp_rec["type"])
    #     except Exception as e:
    #         raise AssertionError( print_pref + "E: reading type of param \"{}\": {}".format(name, str(e)))
    #     # get the default:
    #     if "default" in inp_rec:
    #         if is_basic_type_instance(inp_rec["default"]):
    #             default_value = [clean_string(inp_rec["default"])]
    #         else:
    #             if is_array and isinstance(inp_rec["default"], list):
    #                 default_value = []
    #                 for entry in inp_rec["default"]:
    #                     if is_basic_type_instance(inp_rec["default"]):
    #                         default_value.append(clean_string(entry))
    #                     else:inp_records = cwl_document.inputs_record_schema["fields"]
    if "doc" in cwl_document.tool:
        metadata["doc"] = cwl_document.tool["doc"]
    # for inp_rec in inp_records:
    #     name = clean_string( inp_rec["name"] )
    #     is_array = False
    #                         print(print_pref + "W: invalid default value for parameter " + name +
    #                             ": will be ignored", file=sys.stderr)
    #                         default_value = [""]
    #             elif type_ == "File" and isinstance(inp_rec["default"], dict):
    #                 print(print_pref + "W: invalid default value for parameter " + name +
    #                     ": defaults for File class are not supported yet; will be ignored", file=sys.stderr)
    #                 default_value = [""]
    #             else:
    #                 print(print_pref + "W: invalid default value for parameter " + name +
    #                     ": will be ignored", file=sys.stderr)
    #                 default_value = [""]
    #     else:
    #         default_value = [""]
    #     # read secondary files:
    #     if type_ == "File" and "secondaryFiles" in inp_rec:
    #         if isinstance(inp_rec["secondaryFiles"], str):
    #             secondary_files = [ inp_rec["secondaryFiles"] ]
    #         elif isinstance(inp_rec["secondaryFiles"], list):
    #             secondary_files = inp_rec["secondaryFiles"]
    #         else:
    #             raise AssertionError( print_pref + "E: invalid secondaryFiles field for parameter " + name )
    #     else:
    #         secondary_files = [ "" ]
    #     # read doc:
    #     if "doc" in inp_rec:
    #         doc = inp_rec["doc"]
    #     else:
    #         doc = ""
    #     # assemble config parameters:
    #     inp_configs = {
    #         "type": type_,
    #         "is_array": is_array,
    #         "null_allowed": null_allowed,
    #         "null_items_allowed": null_items_allowed,
    #         "secondary_files": secondary_files,
    #         "default_value": default_value,
    #         "doc": doc
    #     }
    #     # add to configs dict:
    #     configs[ name ] = inp_configs
    # return configs, metadata
    return cwl_document, metadata


if __name__ == '__main__':
    basic_cwl_path = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/data/workflows/basic_example_test.cwl"
    cwl_path = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/data/workflows/rp2-to-rp2path_modified.cwl"
    # resolve_and_validate(basic_cwl_path)
    pack_cwl(basic_cwl_path)
