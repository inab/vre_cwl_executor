# Usage cosifer test

- Change value from `execution` argument in [config.json](https://github.com/inab/vre_cwl_executor/blob/master/tests/cosifer/config.json).
- Change `file_path` value from [in_metadata.json](https://github.com/inab/vre_cwl_executor/blob/master/tests/cosifer/in_metadata.json).
- Download example input file from <https://raw.githubusercontent.com/PhosphorylatedRabbits/cosifer/master/examples/interactive/data_matrix.csv>.
```bash
cd tests/cosifer/
wget https://raw.githubusercontent.com/PhosphorylatedRabbits/cosifer/master/examples/interactive/data_matrix.csv
```
- Run the test:
```bash
./test_VRE_RUNNER.sh
```
- See the results in `run000` folder.
