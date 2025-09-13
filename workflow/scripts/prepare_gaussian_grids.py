#!/usr/bin/env python3
"""
Script to prepare Gaussian grid files for OpenIFS processing.
Part of the OCP-tool Snakemake workflow.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import ocp_tool modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import yaml

# Get snakemake object if running through Snakemake
try:
    snakemake  # noqa: F821
except NameError:
    # If not running through Snakemake, create a mock object for testing
    class MockSnakemake:
        class Output:
            grid_info = "output/gaussian_grids/grid_info.pkl"
        output = Output()
    snakemake = MockSnakemake()

from ocp_tool.ocp_tool import extract_grid_data, read_grid_file


def main():
    # Load configuration
    with open("workflow/config/config.yaml") as f:
        config = yaml.safe_load(f)

    # Extract parameters
    res_num = config['res_num']
    truncation_type = config['truncation_type']
    exp_name_oifs = config['exp_name_oifs']

    # Set grid paths
    input_path_full_grid = "input/gaussian_grids_full/"
    if truncation_type == 'cubic-octahedral':
        input_path_reduced_grid = "input/gaussian_grids_octahedral_reduced/"
    else:
        input_path_reduced_grid = "input/gaussian_grids_linear_reduced/"

    # Read grid file
    print(f"Processing Gaussian grids for T{res_num}")
    lines, NN = read_grid_file(
        res_num,
        input_path_reduced_grid,
        input_path_full_grid,
        truncation_type,
        exp_name_oifs=exp_name_oifs,
        verbose=True
    )

    # Extract grid data
    lons_list, lats_list, numlons_list, dlon_list, lat_list = extract_grid_data(
        lines, verbose=True
    )

    # Save grid info to output file
    output_file = snakemake.output.grid_info  # type: ignore[name-defined]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save processed data
    import pickle
    grid_data = {
        'lines': lines,
        'NN': NN,
        'lons_list': lons_list,
        'lats_list': lats_list,
        'numlons_list': numlons_list,
        'dlon_list': dlon_list,
        'lat_list': lat_list
    }

    with open(output_file.replace('.txt', '.pkl'), 'wb') as f:
        pickle.dump(grid_data, f)

    # Create marker file
    with open(output_file, 'w') as f:
        f.write(f"Gaussian grid processing completed for T{res_num}\n")
        f.write(f"NN = {NN}\n")
        f.write(f"Grid points = {len(lons_list)}\n")

if __name__ == "__main__":
    main()
