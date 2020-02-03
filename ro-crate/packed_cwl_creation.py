import json

from distutils.version import StrictVersion
from pkg_resources import get_distribution


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

        else:  # TODO the condition needs to be tested
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
        json.dump(packed_cwl, packed_cwl_file, indent=4)
        print("packed CWL created")

    except Exception as error:
        errstr = "Unable to create the packed CWL: {}. Error: {}".format(cwl_url, error)
        raise Exception(errstr)


if __name__ == '__main__':
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
    cwl_url_2 = "https://raw.githubusercontent.com/CompEpigen/ATACseq_workflows/1.2.0/CWL/workflows/ATACseq.cwl"
    # packed_cwl = pack_cwl(cwl_url)
    # print("CWL packed: {}".format(packed_cwl))

    create_pack_cwl(cwl_url)
