import subprocess

retval = subprocess.run(["cwltool", "test.cwl", "input_test.yml"])
print(retval)