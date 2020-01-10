# import subprocess
#
# retval = subprocess.run(["cwltool", "example.cwl", "input_example.yml"])
# print(retval)

import json
import os
import zipfile
from re import match
from shutil import copyfile

from distutils.version import StrictVersion
from pkg_resources import get_distribution


def unzip_dir(zip_path, target_dir):
    """
    Unzip directory specified by target_dir
    """
    zip_path = os.path.abspath(zip_path)
    assert zipfile.is_zipfile(zip_path), "The provided file is not a zip."
    assert os.path.isdir(target_dir), "The provided target dir does not exist or is not a dir."
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)


def pack_cwl(cwl_path):
    """
    cwltool needs to be imported on demand since repeatedly calling functions on a document named with same name
    caused errors.

    :param cwl_path:
    :type cwl_path: str
    """
    from cwltool.load_tool import fetch_document
    from cwltool.main import print_pack
    cwltool_version = get_distribution("cwltool").version
    if StrictVersion(cwltool_version) > StrictVersion("1.0.20181201184214"):
        from cwltool.load_tool import resolve_and_validate_document
        loadingContext, workflowobj, uri = fetch_document(cwl_path)
        loadingContext.do_update = False
        loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)
        processobj = loadingContext.loader.resolve_ref(uri)[0]
        packed_cwl = json.loads(print_pack(loadingContext.loader, processobj, uri, loadingContext.metadata))
    else:
        from cwltool.load_tool import validate_document
        document_loader, workflowobj, uri = fetch_document(cwl_path)
        document_loader, _, processobj, metadata, uri = validate_document(document_loader, workflowobj, uri, [], {})
        packed_cwl = json.loads(print_pack(document_loader, processobj, uri, metadata))
    return packed_cwl


def import_cwl(wf_path, name):
    cwl_filename = "{}.{}".format(name, "cwl")
    print(cwl_filename)

    cwl_file_path = os.path.join(os.path.curdir, cwl_filename)
    if not os.path.exists(cwl_file_path):
        try:
            os.makedirs(cwl_file_path)
        except IOError as error:
            errstr = "ERROR: Unable to create intermediate directories. Error: {}".format(error)
            raise Exception(errstr)

    print(cwl_file_path)

    try:
        packed_cwl = pack_cwl(wf_path)

    except Exception as e:
        raise Exception("The loaded CWL document is not valid. Error: {}".format(str(e)))

    # temp_dir = make_temp_dir()
    wf_temp_path = os.path.join(os.path.curdir, "packed.cwl")
    # try:
    #     with open(wf_temp_path, 'w') as cwl_file:
    #         json.dump(packed_cwl, cwl_file)
    # except Exception as e:
    #     raise AssertionError("Could not write CWL file. Error: %s" % e)
    # job_templ_path = os.path.join(temp_dir, "job_templ.xlsx")
    # generate_job_template_from_cwl(
    #     workflow_file=wf_temp_path,
    #     wf_type="CWL",
    #     output_file=job_templ_path,
    #     show_please_fill=True
    # )
    #copyfile(wf_temp_path, wf_target_path)
    # job_templ_target_path = get_path("job_templ", wf_target=cwl_filename)
    # copyfile(job_templ_path, job_templ_target_path)
    # rmtree(temp_dir)


def fetch_files_in_dir(dir_path,  # searches for files in dir_path
                       file_exts,  # match files with extensions in this list
                       search_string="",  # match files that contain this string in the name
                       # "" to disable
                       regex_pattern="",  # matches files by regex pattern
                       ignore_subdirs=False,  # if true, ignores subdirectories
                       return_abspaths=False
                       ):
    # searches for files in dir_path
    # onyl hit that fullfill following criteria are return:
    #   - file extension matches one entry in the file_exts list
    #   - search_string is contained in the file name ("" to disable)
    file_exts = ["." + e for e in file_exts]
    hits = []
    abs_dir_path = os.path.abspath(dir_path)
    for root, dir_, files in os.walk(abs_dir_path):
        for file_ in files:
            file_ext = os.path.splitext(file_)[1]
            if file_ext not in file_exts:
                continue
            if search_string != "" and search_string not in file_:
                continue
            if search_string != "" and not match(regex_pattern, file_):
                continue
            if ignore_subdirs and os.path.abspath(root) != abs_dir_path:
                continue
            file_reldir = os.path.relpath(root, abs_dir_path)
            file_relpath = os.path.join(file_reldir, file_)
            file_nameroot = os.path.splitext(file_)[0]
            file_dict = {
                "file_name": file_,
                "file_nameroot": file_nameroot,
                "file_relpath": file_relpath,
                "file_reldir": file_reldir
                # "file_ext":file_ext
            }
            if return_abspaths:
                file_dict["file_abspath"] = os.path.join(abs_dir_path, file_)
            hits.append(file_dict)
    return hits


if __name__ == '__main__':
    # pack = pack_cwl("/home/laura/PycharmProjects/vre-process_cwl-executor/cwl_wrapper_test/tests/data"
    #                 "/samtools_split.cwl")
    #
    # print(pack)
    #
    # files = fetch_files_in_dir(
    #     dir_path="/home/laura/PycharmProjects/vre-process_cwl-executor/cwl_wrapper_test/tests/data",
    #     file_exts=["cwl"],
    #     ignore_subdirs=True)
    # print(files)
    #
    import_cwl("/cwl_wrapper_test/tests/data/workflows/example.cwl", "caca")
    # import_cwl("https://raw.githubusercontent.com/CompEpigen/ATACseq_workflows/1.2.0/CWL/workflows/ATACseq.cwl", "test")

