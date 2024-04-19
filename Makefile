SHELL := /bin/bash


# BUILD

define build
	$(eval $@_SNAP = $(1))
	@echo "Building ${$@_SNAP} snap..."
	cd ${$@_SNAP}
	snapcraft --debug
endef

.PHONY: control
.ONESHELL:
control:
	@$(call build, "control")

.PHONY: reporting
.ONESHELL:
reporting:
	@$(call build, "reporting")

.PHONY: server
.ONESHELL:
server:
	@$(call build, "server")

.PHONY: vpn
.ONESHELL:
vpn:
	@$(call build, "vpn")

.PHONY: all
all: control reporting server vpn

.DEFAULT_GOAL := all


# INSTALL
# To use the make targets below, make sure you have yq installed.
# You can install it using Homebrew or as a snap:
# 	$ brew install yq
# 	$ snap install yq

define install
    $(eval $@_SNAP = $(1))
	@echo "Installing ${$@_SNAP} snap..."
	$(eval VERSION=$(shell yq ".version" ${$@_SNAP}/snap/snapcraft.yaml))
	sudo snap install --devmode ${$@_SNAP}/aspects-poc-${$@_SNAP}_$(VERSION)_amd64.snap
	snap connections aspects-poc-${$@_SNAP} | awk '{print $$2}' | \
		tail -n +2 | xargs -I {} sudo snap connect {}
endef

.PHONY: install-control
install-control:
	@$(call install, "control")

.PHONY: install-reporting
install-reporting:
	@$(call install, "reporting")

.PHONY: install-server
install-server:
	@$(call install, "server")

.PHONY: install-vpn
install-vpn:
	@$(call install, "vpn")

.PHONY: install-all
install-all: install-server install-control install-vpn install-reporting


# CLEAN UP

define clean
	$(eval $@_SNAP = $(1))
	sudo snap remove aspects-poc-${$@_SNAP}
	rm ${$@_SNAP}/*.snap
endef

.PHONY: clean-all
clean-all:
	@$(call clean, "control")
	@$(call clean, "reporting")
	@$(call clean, "server")
	@$(call clean, "vpn")


# TESTING

.PHONY: format
format:
	ruff format .

.PHONY: check
check:
	ruff check . && \
	mypy control/ && mypy reporting/ && mypy server/ && mypy vpn/

.PHONY: depends
depends:
	pip install -r test-requirements.txt

.PHONY: test
test:
	# test each component individually and combine the coverage results
	COVERAGE_FILE=.coverage_control pytest --cov=control control/tests
	COVERAGE_FILE=.coverage_reporting pytest --cov=reporting reporting/tests
	COVERAGE_FILE=.coverage_server pytest --cov=server server/tests
	COVERAGE_FILE=.coverage_vpn pytest --cov=vpn vpn/tests
	coverage combine --keep .coverage_*
	coverage report --precision=1 --show-missing --skip-empty
	rm .coverage_*
