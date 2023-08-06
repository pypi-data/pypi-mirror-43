# -*- coding: utf-8 -*-
import pytest

from apispec import utils
from apispec.exceptions import APISpecError


class TestOpenAPIVersion:
    @pytest.mark.parametrize("version", ("1.0", "4.0"))
    def test_openapi_version_invalid_version(self, version):
        with pytest.raises(APISpecError) as excinfo:
            utils.OpenAPIVersion(version)
        assert "Not a valid OpenAPI version number:" in str(excinfo)

    @pytest.mark.parametrize("version", ("3.0.1", utils.OpenAPIVersion("3.0.1")))
    def test_openapi_version_string_or_openapi_version_param(self, version):
        assert utils.OpenAPIVersion(version) == utils.OpenAPIVersion("3.0.1")

    def test_openapi_version_digits(self):
        ver = utils.OpenAPIVersion("3.0.1")
        assert ver.major == 3
        assert ver.minor == 0
        assert ver.patch == 1
        assert ver.vstring == "3.0.1"
        assert str(ver) == "3.0.1"
