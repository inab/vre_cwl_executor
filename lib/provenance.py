import argparse
import logging
import os
import sys
import time

from cwltool.stdfsaccess import StdFsAccess
from cwltool.provenance import ResearchObject
from cwltool.context import RuntimeContext, getdefault

from typing import (
    IO,
    List,
    Optional,
    cast,
)

METADATA = "metadata"
PROVENANCE = os.path.join(METADATA, "provenance")


def setup_provenance(
        args,  # type: str
        argsl,  # type: List[str]
        runtimeContext,  # type: RuntimeContext
):  # type: (...) -> Optional[int]
    ro = ResearchObject(
        getdefault(runtimeContext.make_fs_access, StdFsAccess),
        temp_prefix_ro="",
        orcid="",
        full_name="",
    )
    runtimeContext.research_obj = ro
    log_file_io = ro.open_log_file_for_activity(ro.engine_uuid)
    prov_log_handler = logging.StreamHandler(cast(IO[str], log_file_io))

    class ProvLogFormatter(logging.Formatter):
        """Enforce ISO8601 with both T and Z."""

        def __init__(self):  # type: () -> None
            super(ProvLogFormatter, self).__init__("[%(asctime)sZ] %(message)s")

        def formatTime(self, record, datefmt=None):
            # type: (logging.LogRecord, Optional[str]) -> str
            record_time = time.gmtime(record.created)
            formatted_time = time.strftime("%Y-%m-%dT%H:%M:%S", record_time)
            with_msecs = "%s,%03d" % (formatted_time, record.msecs)
            return with_msecs

    prov_log_handler.setFormatter(ProvLogFormatter())
    # _logger.addHandler(prov_log_handler)
    print("[provenance] Logging to %s", log_file_io)
    if argsl is not None:
        # Log cwltool command line options to provenance file
        print("[cwltool] %s %s", sys.argv[0], " ".join(argsl))
    print("[cwltool] Arguments: %s", args)
    return None


if __name__ == '__main__':
    setup_provenance(PROVENANCE, ["hehe.cwl", "hehe.yml"], RuntimeContext)
