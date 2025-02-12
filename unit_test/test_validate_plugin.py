import unittest
from icon_validator.validate import validate
from icon_plugin_spec.plugin_spec import KomandPluginSpec

# Import plugin validators to pass to tests
from icon_validator.rules.plugin_validators.title_validator import TitleValidator
from icon_validator.rules.plugin_validators.profanity_validator import ProfanityValidator
from icon_validator.rules.plugin_validators.help_input_output_validator import HelpInputOutputValidator
from icon_validator.rules.plugin_validators.version_validator import VersionValidator
from icon_validator.rules.plugin_validators.version_pin_validator import VersionPinValidator
from icon_validator.rules.plugin_validators.encoding_validator import EncodingValidator
from icon_validator.rules.plugin_validators.example_input_validator import ExampleInputValidator
from icon_validator.rules.plugin_validators.cloud_ready_connection_credential_token_validator import CloudReadyConnectionCredentialTokenValidator
from icon_validator.rules.plugin_validators.use_case_validator import UseCaseValidator
from icon_validator.rules.plugin_validators.help_validator import HelpValidator
from icon_validator.rules.plugin_validators.confidential_validator import ConfidentialValidator
from icon_validator.rules.plugin_validators.description_validator import DescriptionValidator
from icon_validator.rules.plugin_validators.cloud_ready_validator import CloudReadyValidator
from icon_validator.rules.plugin_validators.acronym_validator import AcronymValidator
from icon_validator.rules.plugin_validators.unapproved_keywords_validator import UnapprovedKeywordsValidator
from icon_validator.rules.plugin_validators.help_example_validator import HelpExampleValidator
from icon_validator.rules.plugin_validators.version_bump_validator import VersionBumpValidator
from icon_validator.rules.plugin_validators.supported_version_validator import SupportedVersionValidator

import requests
from unittest.mock import MagicMock
import os


class TestPluginValidate(unittest.TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertEqual(result, 0)

    def test_plugin_validate_with_task(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_with_task"
        file_to_test = "plugin.spec.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertEqual(result, 0)

    def test_title_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/title_tests"
        file_to_test = "plugin_no_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 1)

    def test_title_validator_with_number_in_title(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_number_title"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 0)

    def test_title_validator_validator_capitalized_word_where_should_not_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_example_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 1)

    def test_profanity_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/profanity_tests"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ProfanityValidator()])
        self.assertEqual(result, 1)

    def test_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpInputOutputValidator()])
        self.assertEqual(result, 0, "Result should be success")

    def test_bad_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_array_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpInputOutputValidator()])
        # TODO this clear violations for other tests
        HelpInputOutputValidator.violations = []
        HelpInputOutputValidator.violated = 0
        self.assertEqual(result, 1, "Result should be failed")

    def test_encoding_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/encoding_tests"
        file_to_test = "plugin_good_encoding.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [EncodingValidator()])
        self.assertEqual(result, 0)

    def test_encoding_validator(self):
        directory_to_test = "plugin_examples/encoding_tests"
        file_to_test = "plugin_bad_encoding.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [EncodingValidator()])
        self.assertEqual(result, 1)

    def test_version_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 0)

    def test_version_validator_should_faile_when_version_same_in_api(self):
        # example workflow in plugin_examples directory. Run tests with these files
        version = requests.get(
            url=f"https://extensions-api.rapid7.com/v1/public/extensions/active_directory_ldap",
            timeout=3
        ).json()["version"]

        f = open("plugin_examples/version_validator/plugin.spec_bad.yaml", 'w')
        f.write(f"plugin_spec_version: v2\nname: active_directory_ldap\nversion: {version}")
        f.close()
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec_bad.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_test"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_fail_when_question_mark(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "?ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_one_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3=2.6")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin_in_one_of_multiple_version_first_test(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3===1.2.3,ldap3xxxx1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin_in_one_of_multiple_version_second_test(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3xxxx1.2.3,ldap3===1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_success_when_three_equal(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3===1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_minority_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3<1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_minority_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3<=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_git(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "git+git://github.com/komand/pycrits@1.0.0#egg=pycrits")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_majority_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3>1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_majority_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3>=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_not_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3!=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_tilda_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3~=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_many_versions(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3<1.2.3,ldap3==1-2-3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_plugin_with_false_for_required_on_output(self):
        # TODO This validator is not correctly made: fix
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_required_key_in_output"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True)
        self.assertEqual(result, 1)

    def test_example_input_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_test"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 0)

    def test_example_input_validator_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_example_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 1)

    def test_example_input_validator_should_fail_when_not_all_exists(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_array_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 1)

    def test_example_input_validator_should_success_when_example_are_0_false(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_example_in_spec_0_false"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 0)

    def test_cloud_ready_connection_credential_token_validator_should_fail(self):
        directory_to_test = "plugin_examples/cloud_ready_connection_credential_token_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyConnectionCredentialTokenValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 0)

    def test_use_case_validator_use_case_not_from_list_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_bad_use_case_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_use_case_empty_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_use_case_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_keywords_from_use_case_list_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_keywords_from_use_case_list_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_duplicate_headings_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 0)

    def test_help_validator_duplicate_headings_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_duplicate_headings_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_help_headers_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 0)

    def test_help_validator_help_headers_missing_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_missing_headings_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_help_headers_not_found_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_headings_not_found_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_confidential_validator_validate_email_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_validate_email"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ConfidentialValidator()])
        self.assertEqual(result, 1)

    def test_confidential_validator_validate_email_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_validate_email"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ConfidentialValidator()])
        self.assertEqual(result, 0)

    def test_description_validator_validate_existed_description_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_description"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [DescriptionValidator()])
        self.assertEqual(result, 1)

    def test_description_validator_validate_existed_description_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [DescriptionValidator()])
        self.assertEqual(result, 0)

    def test_cloud_ready_validator_bad_python_image_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_bad_docker_image"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_user_root_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_user_root"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_dockerfile_apt_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_dockerfile_apt_apk"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_enable_cache_true_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_enable_cache_true"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_system_command_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_system_command"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_cloud_ready"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 0)

    def test_acronym_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 0)

    def test_acronym_validator_lower_acronym_help_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/acronym_validator_help_bad"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 1)

    def test_acronym_validator_lower_acronym_plugin_spec_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/acronym_validator_spec_bad"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 1)

    def test_unapproved_keywords_validator_should_success_without_warning(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UnapprovedKeywordsValidator()])
        self.assertEqual(result, 0)

    def test_unapproved_keywords_validator_should_print_warning(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_warning_keywords"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UnapprovedKeywordsValidator()])
        self.assertEqual(result, 0)

    def test_help_example_spaces_and_json_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpExampleValidator()])
        self.assertEqual(result, 0)

    def test_help_example_spaces_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_help_example_wrong_spaces"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpExampleValidator()])
        self.assertEqual(result, 1)

    def test_help_example_json_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_help_example_wrong_json"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpExampleValidator()])
        self.assertEqual(result, 1)

    def test_major_version_action_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.action.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_action_title_changed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.action.title.changed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_connection_input_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.connection.input.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_input_now_required_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.now.required.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_input_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_title_changes_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.title.changes.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_change_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.type.change.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_new_required_connection_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.new.input.required.connection.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_new_required_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.new.required.input.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_output_nolonger_required_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.output.nolonger.required.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_trigger_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.trigger.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_trigger_renamed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.trigger.renamed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_changed_connection_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.changed.connection.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_subtype_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.subtype.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_action_removed_bump_applied_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.good.action.removedandbumped.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    def test_major_version_new_optional_connection_input_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.good.new.connection.input.optional.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    def test_version_new_optional_action_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.input.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_action_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.action.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_trigger_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.trigger.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_output_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.output.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_output_bumped_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.good.new.output.bumped.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    def test_supported_version_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 0)

    def test_supported_version_validator_sup_vers_null(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    def test_supported_version_validator_spec_empty(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad_empty.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    def test_supported_version_validator_sup_vers_empty(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad_missing_value.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    @staticmethod
    def replace_requirements(path, text):
        f = open(path, 'w')
        f.write(text)
        f.close()


class MockRepoSpecResponse:
    @staticmethod
    def mock_patch_remote_spec_major_version(directory):
        final_name = "plugin.spec.remote.yaml"
        # if the "remote" spec exists, use that
        if os.path.exists(os.path.join(directory, final_name)):
            spec = KomandPluginSpec(directory, final_name)
        # otherwise, just use a copy of the existing spec
        else:
            spec = KomandPluginSpec(directory, "plugin.spec.yaml")
        spec_dict = spec.spec_dictionary()
        return spec_dict
