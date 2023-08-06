#! /bin/bash
set -e
export package_version="${1:-$(date +'%Y.%m.%d.%H.%M.%S')}"

wheelhouse="${HOME}/Research/Temp/wheelhouse"

/bin/rm -rf "${wheelhouse}"
mkdir -p "${wheelhouse}"

CONDA_ENVS=( py27 py35 py36 py37 )

# Update conda envs
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    conda activate "${CONDA_ENV}"
    conda update -y --all
    conda install -y fftw
    pip install --upgrade pip
    source deactivate
done

# Compile wheels
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    source activate "${CONDA_ENV}"
    ### NOTE: The path to the requirements file is specialized for spinsfast
    pip install -r ./python/dev-requirements.txt
    pip wheel ./ -w "${wheelhouse}/"
    source deactivate
done

# Bundle external shared libraries into the wheels
for whl in $(ls $(echo "${wheelhouse}/*.whl")); do
    echo
    delocate-listdeps --depending "$whl"
    delocate-wheel -v "$whl"
    delocate-listdeps --depending "$whl"
    echo
done


### NOTE: These lines are specialized for spinsfast
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    source activate "${CONDA_ENV}"
    # Install packages and test ability to import and run simple command
    pip install --upgrade spinsfast --no-index -f "${wheelhouse}"
    (cd "$HOME"; python -c 'import spinsfast; print(spinsfast.__version__); print("N_lm(8) = {0}".format(spinsfast.N_lm(8)))')
    source deactivate
done


# Upload to pypi
pip install twine
twine upload "${wheelhouse}"/*macosx*.whl
