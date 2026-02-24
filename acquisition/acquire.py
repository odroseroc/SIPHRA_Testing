import argparse
import subprocess
import json
from pathlib import Path
import time
from datetime import datetime, timezone

def parse_args():
    parser = argparse.ArgumentParser(
        description="Acquire data from SIPHRA ASIC using dma_to_raw_file and store metadata."
    )

    parser.add_argument("-o", "--output",
                        required=True,
                        help="Base name for output files (without extension).")
    parser.add_argument("-c", "--counts", type=int, default=100_000)
    parser.add_argument("-s", "--size", type=int, default=4095)
    parser.add_argument("--device", default="/dev/D2A_DMA")
    parser.add_argument("--active-chs", nargs="*", default=[])
    parser.add_argument("--sipm-chs", nargs="*", default='')
    parser.add_argument("--source", type=str, default='[NOT SPECIFIED]')
    parser.add_argument("--source-description", type=str, default='[NOT SPECIFIED]')

    return parser.parse_args()

def run_acquisition(args):
    output_base = Path(args.output).resolve()
    dat_file = output_base.with_suffix(".dat")

    cmd = [
        "./dma_to_raw_file",
        "-i", args.device,
        "-o", str(dat_file),
        "-s", str(args.size),
        "-v",
        "-c", str(args.counts),
        "-b"
    ]

    start = time.time()
    subprocess.run(cmd, check=True)
    end = time.time()

    exposure = end - start
    return exposure, output_base

def write_metadata(output_base, exposure, args):
    metadata = {
        "schema-version": "1.0",

        "acquisition": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "exposure_sec": exposure,
            "counts": args.counts,
            "active_chs": args.active_chs,
            "sipm_chs": args.sipm_chs,
        },

        "source": {
            "type": args.source,
            "description": args.source_description,
        },

        "file_info": {
            "data_file": str(output_base.with_suffix(".dat")),
            "format": "raw_binary"
        }
    }

    json_file = output_base.with_suffix(".json")
    with open(json_file, "w") as f:
        json.dump(metadata, f, indent=4)

def main():
    args = parse_args()
    exposure, output_base = run_acquisition(args)
    write_metadata(output_base, exposure, args)

if __name__ == "__main__":
    main()

