# Multi-stage Dockerfile for OCP-tool climate modeling

# Base stage with conda environment
FROM condaforge/mambaforge:latest as base

LABEL maintainer="OCP-tool developers"
LABEL description="Climate modeling tools for OpenIFS coupling preparation"

# Set environment variables
ENV CONDA_ENV_NAME=ocp-tool
ENV PATH="/opt/conda/envs/${CONDA_ENV_NAME}/bin:${PATH}"

# Copy environment file
COPY workflow/envs/ocp_tool.yaml /tmp/environment.yaml

# Create conda environment
RUN mamba env create -f /tmp/environment.yaml -n ${CONDA_ENV_NAME} && \
    mamba clean -afy && \
    conda clean -afy

# Activate environment
SHELL ["conda", "run", "-n", "ocp-tool", "/bin/bash", "-c"]

# Production stage
FROM base as production

# Install system dependencies for netCDF and GRIB processing
RUN apt-get update && apt-get install -y \
    libeccodes-dev \
    libeccodes-tools \
    libnetcdf-dev \
    libhdf5-dev \
    cdo \
    nco \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source code
COPY ocp_tool/ ./ocp_tool/
COPY workflow/ ./workflow/
COPY input/ ./input/
COPY *.py ./
COPY *.ipynb ./
COPY environment.yaml ./
COPY setup.py ./
COPY README.md ./

# Install OCP-tool package
RUN conda run -n ${CONDA_ENV_NAME} pip install -e .

# Create output directories
RUN mkdir -p output/{openifs_input_modified,oasis_mct3_input,runoff_map_modified,plots,executed_notebooks}

# Set entrypoint
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ocp-tool"]
CMD ["snakemake", "--help"]

# Development stage with jupyter
FROM production as development

# Expose Jupyter port
EXPOSE 8888

# Development entrypoint
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]