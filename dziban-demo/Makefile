.PHONY: init clean clone draco dziban nb new_env remove_env

CONDA_BASE=$(shell conda info --base)

init: clean new_env draco dziban enable_vega_nbextension

clean: clean_draco clean_dziban

draco: clone_draco draco_fe draco_py draco_local_py

dziban: clone_dziban dziban_py dziban_local_py
    
new_env:
	conda create --yes --name dziban-demo python=3.6

remove_env: clean
	conda remove -n dziban-demo --all

nb:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	jupyter notebook

clone: clone_draco clone_dziban

clone_draco:
	git clone --single-branch --branch multi-vis https://github.com/uwdata/draco.git

clone_dziban:
	git clone https://github.com/uwdata/dziban.git

draco_fe:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	cd draco && \
	conda install --yes -c potassco clingo && \
	yarn install && \
	cd js && \
	yarn install && \
	cd .. && \
	yarn build

draco_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	cd draco && \
	while read requirement; do \
        conda install --yes $$requirement || pip install $$requirement; \
    done < requirements.txt

dziban_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	cd dziban && \
	while read requirement; do \
        conda install --yes $$requirement || pip install $$requirement; \
    done < requirements.txt

draco_local_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	cd draco && \
	pip install -e .

dziban_local_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	cd dziban && \
	pip install -e .

clean_draco:
	rm -rf draco

clean_dziban:
	rm -rf dziban

enable_vega_nbextension:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dziban-demo && \
	jupyter nbextension install --py vega --sys-prefix && \
	jupyter nbextension enable --py vega --sys-prefix
