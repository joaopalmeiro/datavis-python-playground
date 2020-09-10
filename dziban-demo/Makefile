.PHONY: init clean clone draco dziban nb remove

CONDA_BASE=$(shell conda info --base)

init: new_env 
    
new_env:
	conda create --name dzyban-demo python=3.6

clone_draco:
	git clone --single-branch --branch multi-vis https://github.com/uwdata/draco.git

clone_dziban:
	git clone https://github.com/uwdata/dziban.git

draco_fe:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dzyban-demo && \
	cd draco && \
	conda install -c potassco clingo && \
	yarn install && \
	cd js && \
	yarn install && \
	cd .. && \
	yarn build

draco_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dzyban-demo && \
	cd draco && \
	while read requirement; do \
        conda install --yes $$requirement || pip install $$requirement; \
    done < requirements.txt

dziban_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dzyban-demo && \
	cd dziban && \
	while read requirement; do \
        conda install --yes $$requirement || pip install $$requirement; \
    done < requirements.txt

draco_local_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dzyban-demo && \
	cd draco && \
	pip install -e .

dziban_local_py:
	source $(CONDA_BASE)/etc/profile.d/conda.sh && \
	conda activate dzyban-demo && \
	cd dziban && \
	pip install -e .

remove_env: clean
	conda remove -n dzyban-demo --all

clean_draco:
	rm -rf draco

clean_dziban:
	rm -rf dziban

nb:
	jupyter notebook

draco: clean_draco clone_draco draco_fe draco_py draco_local_py

dziban: clean_dziban clone_dziban dziban_py dziban_local_py

clean: clean_draco clean_dziban

clone: clone_draco clone_dziban
