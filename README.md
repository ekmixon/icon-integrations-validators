
# InsightConnect Integrations Validators

Tooling with a bundled suite of validator rules for
ensuring quality across
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integrations.

## Installation

```
pip install insightconnect-integrations-validators
```

## Use

Simple!

### Command

```
icon-validate my_plugin_directory/
```

or

```
icon-validate my_plugin_directory/ --all
```

to run entire set of validators used in our CI.
Omitting `--all` is often helpful when developing.

### Python

```
from icon_validator.validate import validate


validate("/path/to/plugin/directory")
```

or

```
validate("/path/to/plugin/directory", run_all=True)
```

to simulate the `--all` flag.

## Changelog

* 2.1.6 - Fix issue where ID was an acronym
* 2.1.5 - Fix issue where confidential validator was not checking against provided whitelist
* 2.1.4 - Fix issue where confidential validator was triggering on remediated findings and updated formatting
* 2.1.3 - Update Exception Validator to throw warning
* 2.1.2 - Fix issue where resources validator would always raise an exception
* 2.1.1 - Update RequiredKeysValidator to validate the correct products key and empty resources keys
* 2.1.0 - Update Golang RegenerationValidator
* 2.0.2 - Update HelpValidator to fix error messaging
* 2.0.1 - Update UseCaseValidator valid use case list
* 2.0.0 - Update Help Validator to use new help format |
Update RequiredKeys Validator for new spec fields |
Add validator rule: use case validation
* 1.3.0 - Add --all flag to run entire set of validators,
add Confidential Validator, Regeneration Validator clean up
* 1.2.0 - Add regeneration validator jenkins support
* 1.1.8 - Add regeneration validator
* 1.1.7 - Remove false positive "SPAM" entry from the Acronym Validator
* 1.1.6 - Improved Output validator
* 1.1.5 - Remove Makefile validator rule, fix rules import
* 1.1.4 - Move `rules` package inside `icon_validator`
* 1.1.3 - Ignore unit test directories (/unit_test & /unit_tests) in Exception Validator
* 1.1.2 - Fix for Acronym and Output validators
* 1.1.1 - Removed breaking changes to Makefile validator
* 1.1.0 - Add validator rules: check for help.md, profanity check,
acronym capitalization check,
`print` usage check, JSON tests, exceptions, credentials, passwords
| Updated rules: Makefiles, logging
* 1.0.0 - Initial release

PyPi.org link: [https://pypi.org/project/insightconnect-integrations-validators/](https://pypi.org/project/insightconnect-integrations-validators/)
