from rocrate import rocrate_api
from ruamel import yaml

def create_rocrate(cwl_wf_url, input_files, output_path):
    """"
    """
    # Create base
    ro_crate = rocrate_api.make_workflow_rocrate(workflow_path=cwl_wf_url, wf_type="CWL", include_files=input_files)

    # write RO-Crate to output_path
    ro_crate.write_crate(output_path)


if __name__ == '__main__':
    wf = "https://raw.githubusercontent.com/kids-first/kf-alignment-workflow/dm-ipc-fixes/workflows/kfdrc_alignment_wf_cyoa.cwl"
    files_list = ["/Users/laurarodrigueznavas/BSC/vre_cwl_executor/ro/lib/sample_file.txt"]
    out_path = "/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000"

    create_rocrate(wf, files_list, out_path)

    with open("/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/kfdrc_alignment/kf_alignment_cyoa_wf.yaml", "r") as fp:
        data = yaml.safe_load(fp)
        for elem in data:
            print(data[elem])
