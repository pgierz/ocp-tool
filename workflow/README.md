# OCP-tool Snakemake Workflow
This directory contains a Snakemake workflow for automating the OpenIFS coupling preparation (OCP-tool) pipeline.

## Overview

The workflow automates the main tasks of OCP-tool:
1. **Land-sea mask modification** - Adapting OpenIFS input files to ocean model grids
2. **OASIS3-MCT file generation** - Creating coupling interface files  
3. **Runoff mapper modifications** - Adjusting drainage basins and arrival points
4. **Paleoclimate processing** - Optional paleoclimate data integration
5. **Visualization** - Generating diagnostic plots

## Quick Start

### 1. Setup Environment

```bash
# Create conda environment
conda env create -f environment.yaml
conda activate ocp-tool

# Install Snakemake
mamba install snakemake>=7.0
```

### 2. Configure Workflow

Edit `workflow/config/config.yaml` to match your setup:

```yaml
# OpenIFS Configuration
res_num: 159                    # Truncation number (T159, T255, etc.)
truncation_type: "linear"       # linear or cubic-octahedral  
exp_name_oifs: "abda"          # 4-digit experiment name
num_fields: 50                  # Number of GRIB fields

# Ocean Model  
grid_name_oce: "CORE2"         # Ocean grid name
fesom_grid_file_path: "/path/to/mesh.nc"
```

### 3. Run Workflow

```bash
# Local execution
snakemake --cores 4 --use-conda

# With custom config
snakemake --cores 4 --configfile my_config.yaml

# Dry run to check rules
snakemake --dry-run
```

## Workflow Structure

```
workflow/
├── Snakefile              # Main workflow definition
├── config/
│   └── config.yaml        # Configuration parameters
├── scripts/               # Python scripts for each step
├── envs/                  # Conda environment files
├── profiles/              # Execution profiles (local, SLURM)
├── containers/            # Docker/Singularity definitions
└── logs/                  # Execution logs (created at runtime)
```

## Execution Profiles

### Local Execution
```bash
snakemake --profile workflow/profiles/default
```

### SLURM Cluster
```bash
snakemake --profile workflow/profiles/slurm
```

## Container Usage

### Docker
```bash
# Build containers
cd workflow/containers && ./build.sh

# Run workflow in container
docker run --rm -v $(pwd):/app/data ocp-tool:latest snakemake --cores 4

# Development with Jupyter
docker run --rm -p 8888:8888 ocp-tool:latest-dev
```

### Singularity/Apptainer
```bash
# Build container
BUILD_SINGULARITY=true ./workflow/containers/build.sh

# Run workflow
singularity exec --bind /data:/app/data ocp-tool.sif snakemake --cores 4
```

## Key Rules

- **all**: Complete workflow execution
- **setup_environment**: Environment preparation
- **prepare_gaussian_grids**: Process OpenIFS grid files  
- **process_fesom_grid**: Read ocean model grid
- **modify_land_sea_mask**: Core LSM modification
- **generate_oasis_files**: Create OASIS coupling files
- **modify_runoff_maps**: Adjust runoff routing
- **generate_plots**: Create diagnostic visualizations
- **run_notebook**: Execute validation notebook

## Configuration Options

### Required Parameters
- `res_num`: OpenIFS truncation number (e.g., 159, 255)
- `exp_name_oifs`: 4-character experiment identifier
- `grid_name_oce`: Ocean model grid identifier
- `fesom_grid_file_path`: Path to ocean grid file

### Optional Parameters
- `do_paleo`: Enable paleoclimate processing
- `manual_basin_removal`: Runoff basin modifications
- `cavity`: Ice cavity support for ocean grid
- `threads`, `memory_mb`: Resource limits

## Outputs

The workflow produces:
- Modified OpenIFS input files (`output/openifs_input_modified/`)
- OASIS3-MCT coupling files (`output/oasis_mct3_input/`)
- Modified runoff maps (`output/runoff_map_modified/`)
- Diagnostic plots (`output/plots/`)
- Executed notebooks (`output/executed_notebooks/`)

## Troubleshooting

### Common Issues

1. **Missing input files**: Ensure all required input data is in `input/` subdirectories
2. **GRIB field count**: Verify `num_fields` matches your OpenIFS file
3. **Grid file paths**: Check ocean grid file exists and is accessible
4. **Memory errors**: Increase memory limits in cluster profile

### Debugging

```bash
# Verbose output
snakemake --verbose

# Keep intermediate files
snakemake --notemp

# Unlock after interruption  
snakemake --unlock
```

### Log Files

Execution logs are stored in:
- `workflow/logs/` for rule-specific logs
- `workflow/logs/slurm/` for SLURM job logs

## Development

### Adding New Rules

1. Define rule in `Snakefile`
2. Create script in `workflow/scripts/`
3. Add dependencies to environment file
4. Update configuration schema
5. Test with `snakemake --dry-run`

### Contributing

Please follow these guidelines:
- Use descriptive rule names
- Include resource requirements
- Add logging and error handling
- Update documentation
- Test on multiple configurations