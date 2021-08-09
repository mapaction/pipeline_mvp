# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Please maintain both this file AND the README.md file.

## [Unreleased]

### Added

* initial GitHub Actions for Continuous Integration (CI)

### Changed
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
