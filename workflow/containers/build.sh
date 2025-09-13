#!/bin/bash
# Container build script for OCP-tool

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Build options
BUILD_DOCKER=${BUILD_DOCKER:-true}
BUILD_SINGULARITY=${BUILD_SINGULARITY:-false}
PUSH_DOCKER=${PUSH_DOCKER:-false}

# Container tags
DOCKER_TAG=${DOCKER_TAG:-"ocp-tool:latest"}
REGISTRY=${REGISTRY:-""}

echo "Building OCP-tool containers..."
echo "Project root: ${PROJECT_ROOT}"

cd "${PROJECT_ROOT}"

# Build Docker container
if [[ "${BUILD_DOCKER}" == "true" ]]; then
    echo "Building Docker container..."
    
    # Production image
    docker build -f workflow/containers/Dockerfile \
        --target production \
        -t "${DOCKER_TAG}" \
        .
    
    # Development image  
    docker build -f workflow/containers/Dockerfile \
        --target development \
        -t "${DOCKER_TAG}-dev" \
        .
    
    echo "Docker build complete:"
    echo "  Production: ${DOCKER_TAG}"
    echo "  Development: ${DOCKER_TAG}-dev"
    
    # Push to registry if requested
    if [[ "${PUSH_DOCKER}" == "true" && -n "${REGISTRY}" ]]; then
        echo "Pushing to registry: ${REGISTRY}"
        docker tag "${DOCKER_TAG}" "${REGISTRY}/${DOCKER_TAG}"
        docker tag "${DOCKER_TAG}-dev" "${REGISTRY}/${DOCKER_TAG}-dev"
        docker push "${REGISTRY}/${DOCKER_TAG}"
        docker push "${REGISTRY}/${DOCKER_TAG}-dev"
    fi
fi

# Build Singularity container
if [[ "${BUILD_SINGULARITY}" == "true" ]]; then
    echo "Building Singularity container..."
    
    # Check if singularity is available
    if ! command -v singularity &> /dev/null; then
        echo "Error: singularity command not found"
        echo "Please install Singularity/Apptainer to build SIF containers"
        exit 1
    fi
    
    # Build from definition file
    singularity build \
        --force \
        ocp-tool.sif \
        workflow/containers/singularity.def
    
    echo "Singularity build complete: ocp-tool.sif"
fi

echo "Container build process finished!"
echo ""
echo "Usage examples:"
echo "  # Docker"
echo "  docker run --rm -v \$(pwd):/app/data ${DOCKER_TAG} snakemake --cores 4"
echo "  docker run --rm -p 8888:8888 ${DOCKER_TAG}-dev"
echo ""
if [[ "${BUILD_SINGULARITY}" == "true" ]]; then
echo "  # Singularity"
echo "  singularity exec --bind /data:/app/data ocp-tool.sif snakemake --cores 4"
echo ""
fi