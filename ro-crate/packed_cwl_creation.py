import json
import os

from distutils.version import StrictVersion
from pkg_resources import get_distribution

# TODO change print to logger


def pack_cwl(cwl_url):
    """

    :param cwl_url:
    :type cwl_url: str
    :return:
    :rtype: Workflow
    """

    print("CWL URL: {}".format(cwl_url))

    from cwltool.load_tool import fetch_document
    from cwltool.main import print_pack

    cwltool_version = get_distribution("cwltool").version
    print("cwltool version: {}".format(cwltool_version))

    try:

        if StrictVersion(cwltool_version) > StrictVersion("1.0.20181201184214"):
            from cwltool.load_tool import resolve_and_validate_document

            loadingContext, workflowobj, uri = fetch_document(cwl_url)
            print("workflow: {}".format(workflowobj))
            loadingContext.do_update = False

            # validate CWL
            loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)

            processobj = loadingContext.loader.resolve_ref(uri)[0]
            print("process object: {}".format(processobj))

            # create packed cwl
            packed_cwl = json.loads(print_pack(loadingContext.loader, processobj, uri, loadingContext.metadata))

        else:   # TODO the condition needs to be tested
            from cwltool.load_tool import validate_document
            document_loader, workflowobj, uri = fetch_document(cwl_url)

            # validate CWL
            document_loader, _, processobj, metadata, uri = validate_document(document_loader, workflowobj, uri, [], {})

            # create packed cwl
            packed_cwl = json.loads(print_pack(document_loader, processobj, uri, metadata))

        return packed_cwl

    except Exception as error:
        errstr = "Unable to pack the CWL: {}. Error: {}".format(cwl_url, error)
        raise Exception(errstr)


def create_pack_cwl(cwl_url):
    """

    :param cwl_url:
    :type cwl_url: str
    :return:
    :rtype: Workflow
    """
    # create directory for packed.cwl
    # cwl_filename = cwl_url.replace(".cwl", "").split('/')[-1]
    # cwl_file_path = os.path.join(os.path.curdir, cwl_filename)
    # if not os.path.exists(cwl_file_path):
    #     try:
    #         os.makedirs(cwl_file_path)
    #     except IOError as error:
    #         errstr = "Unable to create intermediate directory. Error: {}".format(error)
    #         raise Exception(errstr)
    #
    try:

        # pack CWL
        packed_cwl = pack_cwl(cwl_url)
        print("CWL packed")

        # write packed.cwl
        # packed_cwl_path = os.path.join(cwl_file_path, "packed.cwl")
        packed_cwl_file = open("packed.cwl", 'w')
        json.dump(packed_cwl, packed_cwl_file, indent=4, sort_keys=True)
        print("packed CWL created")

    except Exception as error:
        errstr = "Unable to create the packed CWL: {}. Error: {}".format(cwl_url, error)
        raise Exception(errstr)

    # cwl_document = read_config_from_cwl_file(packed_cwl_path)
    # print(cwl_document)


def read_config_from_cwl_file(cwl_file):
    print(cwl_file)
    print_pref = "[read_cwl_file]:"
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
        raise AssertionError( print_pref + "failed to read cwl file \"" + cwl_file + "\": does not exist or is invalid")
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
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
    # packed_cwl = pack_cwl(cwl_url)
    # print("CWL packed: {}".format(packed_cwl))

    create_pack_cwl(cwl_url)

    # import_cwl("https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl")
    # import_cwl("https://raw.githubusercontent.com/CompEpigen/ATACseq_workflows/1.2.0/CWL/workflows/ATACseq.cwl")