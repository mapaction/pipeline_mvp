# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Please maintain both this file AND the README.md file.

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [v0.3]

### Added

* Initial GitHub Actions for Continuous Integration (CI)
* New osm datasets: rivers, lakes, airports, seaports, seas, places.
* New admin2 and amdin3 polygon boundaries datasets.
* Allowed dag creation by countries rather than only data types.
* Created new folder structure that includes airflow_logic, map_action_logic, auxiliary_modules, configs.
* Implemented 9 tests for request API. No problems found.
* Implemented 21 tests for Fallback Dictionary class. An important error that leads to incorrect behavior of config parser was revealed by one of the tests.
* Implemented a test for yaml api. No problems found.
* Implemented 87 tests for config parser. 10 of them fail, revealing various bugs that exist in config parser code.

### Changed
* Separated output format validation schemas from the overpass request configs (they were both called schemas, which brought inconsistency to the code).
* Optimized config_parser.py by generalizing most of the function there(reduced 523 strings of code to 250)
* Refactored operators: combined all (except for adm0 and adm1) transform operators into generic DefaultTransformOperator and all admin transform operators into generic admin transform operator.
* Refactored transforms (combined most of the transforms into generic default_transform)
* Refactored osm dags. Defined a united procedure to create osm dags (now there is only one file for osm dags).
* Fixed osm extract and made it robust. Previously, osm extracts often failed reaching the quota of osm overpass api requests. Now upon failing the extract tasks will be launched multiple times with an exponential delay.
* Rewrote osm_query to support more sophisticated queries. Previously, only simple OR queries were supported. Now it is possible to create AND queries as well.
* Rewrote docker-compose and Dockerfile to make new structure accessible to airflow server.

* Refactored dags and operators and moved them, as well as the files associated with them, to airflow_logic.
* Moved files related to MapAction specific logic, such as transform and extract logic implementation, to map_action_logic.
* Edited flake8 scripts as well as github CI to cover new entities.
* Refactored requests api module and moved it to auxiliary_modules folder.
* Refactored requests storage access and moved it to auxiliary_modules folder.
* Refactored requests gcp access and moved it to auxiliary_modules folder.
* Refactored requests config access module and moved it to auxiliary_modules folder.
### Deprecated
### Removed
### Fixed
### Security

## [v0.2] - 2021-06-30
### Added
- Introduced code standards and contribution workflow.
- Airflow is used for pipeline management
  * Deploys to Google Cloud Platform (using GCP Composer service) using Docker images built using GitHub Actions.
  * Can deploy to local Airflow instance for development purposes using Docker Compose.
- Added these datasets:
  * Rail from OSM
  * Roads from OSM
  * Roads from HDX
  * Admin 1 & 2 from HDX
- Expanded from just Yemen to 14 countries. Additional countries are automatically from config files.
- Various changes to align the output with MapAction default Crash Move Folder structure and data schema.
- Added a pipeline architecture visualization for both current status and future proposed status, in the docs folder.

### Changed
- n/a
### Deprecated
- n/a
### Removed
- All use of Dagster
### Fixed
- n/a
### Security
- n/a

## [v0.1] - 2020-11-23
### Added
- Initial exploration using Dagster.
### Changed
- n/a
### Deprecated
- n/a
### Removed
- n/a
### Fixed
- n/a
### Security
- n/a
