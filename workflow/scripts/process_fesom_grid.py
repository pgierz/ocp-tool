#!/usr/bin/env python3
"""
Script to process FESOM ocean grid.
Part of the OCP-tool Snakemake workflow.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import ocp_tool modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ocp_tool.ocp_tool import read_fesom_grid
import yaml

def main():
    # Load configuration
    with open("workflow/config/config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    # Extract parameters
    grid_name_oce = config['grid_name_oce']
    interp_res = config['interp_res']
    cavity = config['cavity']
    fesom_grid_file_path = config['fesom_grid_file_path']
    exp_name_oifs = config['exp_name_oifs']
    
    # Set paths
    input_path_oce = "input/fesom_mesh/"
    
    print(f"Processing FESOM grid: {grid_name_oce}")
    
    # Read FESOM grid
    fesom_grid_sorted = read_fesom_grid(
        input_path_oce,
        grid_name_oce, 
        fesom_grid_file_path,
        interp_res,
        cavity=cavity,
        force_overwrite_griddes=True,
        verbose=True
    )
    
    # Save processed grid
    output_file = snakemake.output.processed_grid
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    import numpy as np
    import netCDF4 as nc
    
    # Create output NetCDF file
    with nc.Dataset(output_file, 'w') as ds:
        ds.createDimension('npoints', len(fesom_grid_sorted))
        
        var = ds.createVariable('cell_area', 'f8', ('npoints',))
        var[:] = fesom_grid_sorted
        var.long_name = "FESOM grid cell areas"
        var.units = "dimensionless"
        
        ds.title = f"Processed FESOM grid: {grid_name_oce}"
        ds.description = "Grid processed for OpenIFS coupling"

    print(f"Processed FESOM grid saved to: {output_file}")

if __name__ == "__main__":
    main()