# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.6.22](https://github.com/Esukhia/pybo/releases/tag/v0.6.22) - 20200710
### Added
 * #5 Add optional "--tags" to tok command to select and order token tags

## [0.6.21](https://github.com/Esukhia/pybo/releases/tag/v0.6.21) - 20191215
### Added
 * add profile-update to CLI
### Changed
 * use Token.text_cleaned whenever possible, fallback to Token.text otherwise
 * output of `pybo rdr` and `pybo profile-report`

## [0.6.20](https://github.com/Esukhia/pybo/releases/tag/v0.6.20) - 20191213
### Added
 * Support for `object.suffixL<X>` in CQL rule creation.

## [0.6.19](https://github.com/Esukhia/pybo/releases/tag/v0.6.19) - 20191210
### Fixed
 * import bug fixed

## [0.6.18](https://github.com/Esukhia/pybo/releases/tag/v0.6.18) - 20191210
### Added
 * botok profile report: `pybo profile-report <path>`
 Finds out all duplicates over all the folders and files.

## [0.6.17](https://github.com/Esukhia/pybo/releases/tag/v0.6.17) - 20191122
### Fixed
 * bad setup

## [0.6.16](https://github.com/Esukhia/pybo/releases/tag/v0.6.16) - 20191122
### Fixed
 * bad imports

## [0.6.15](https://github.com/Esukhia/pybo/releases/tag/v0.6.15) - 20191122
### Fixed
 * reference to bo_sorted() not removed

## [0.6.14](https://github.com/Esukhia/pybo/releases/tag/v0.6.14) - 20191122
### Fixed
 * piycu for Windows from third-party website
 * temporarily remove bo_sorted() + CLI command
 * fixed rdr_2_replace_matcher bug on first line of rules
### Added
 * cwd CLI command

## [0.6.13](https://github.com/Esukhia/pybo/releases/tag/v0.6.13) - 20191109
### Fixed
 * removed pyicu dependency

## [0.6.12](https://github.com/Esukhia/pybo/releases/tag/v0.6.12) - 20191109
### Added
 * added rdr_2_replace_matcher in utils

## [0.6.11](https://github.com/Esukhia/pybo/releases/tag/v0.6.11) - 20191030
### Added
 * added bo_sort() and the corresponding kakha CLI option

## [0.6.10](https://github.com/Esukhia/pybo/releases/tag/v0.6.10) - 20190901
### Added
 * added pyewts to pybo

## [0.6.9](https://github.com/Esukhia/pybo/releases/tag/v0.6.9) - 20190901
### Added
 * the tokenizer's codebase is extracted from pybo and now lives in botok. All the related history is brought out to that project.
