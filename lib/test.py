import itertools

outputs = {'bam_file': [
    {'location': 'file:///Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/A.bam', 'basename': 'A.bam',
     'class': 'File', 'checksum': 'sha1$b3481bf8e778e5c33a52c8e7a2a787185c7ac565', 'size': 765904,
     'path': '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/A.bam'},
    {'location': 'file:///Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/B.bam', 'basename': 'B.bam',
     'class': 'File', 'checksum': 'sha1$1058bf8642e0063f09963a1123bd9ba39970851f', 'size': 752260,
     'path': '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/B.bam'},
    {'location': 'file:///Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/C.bam', 'basename': 'C.bam',
     'class': 'File', 'checksum': 'sha1$df12ecaaad576c44467aa3b4c8d05e527347dc97', 'size': 795785,
     'path': '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/C.bam'}]}

output_files = {'bam_file': None}
output_path = list()

for k in output_files.keys():
    if k in outputs.keys():
        for x in outputs[k]:
            output_path.append(x["path"])
        output_files[k] = output_path

print(output_path)
print(output_files)

x = {'bam_files': ['/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/A.bam', '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/B.bam', '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/C.bam']}

for key, value in (
        itertools.chain.from_iterable(
            [itertools.product((k, ), v) for k, v in x.items()])):
    print(value)

