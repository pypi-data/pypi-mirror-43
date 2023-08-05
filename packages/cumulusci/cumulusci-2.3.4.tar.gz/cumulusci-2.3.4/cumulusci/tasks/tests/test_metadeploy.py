import io
import json
import unittest
import zipfile

import mock
import requests
import responses
import yaml

from cumulusci.core.config import ServiceConfig
from cumulusci.core.config import TaskConfig
from cumulusci.tasks.github.tests.util_github_api import GithubApiTestMixin
from cumulusci.tasks.metadeploy import BaseMetaDeployTask
from cumulusci.tasks.metadeploy import Publish
from cumulusci.tests.util import create_project_config


class TestBaseMetaDeployTask(unittest.TestCase):
    @responses.activate
    def test_call_api__400(self):
        responses.add("GET", "https://metadeploy/rest", status=400, body=b"message")

        project_config = create_project_config()
        project_config.keychain.set_service(
            "metadeploy", ServiceConfig({"url": "https://metadeploy", "token": "TOKEN"})
        )
        task_config = TaskConfig()
        task = BaseMetaDeployTask(project_config, task_config)
        task._init_task()
        with self.assertRaises(requests.exceptions.HTTPError):
            task._call_api("GET", "/rest")

    @responses.activate
    def test_call_api__collect_pages(self):
        responses.add(
            "GET",
            "https://metadeploy/rest",
            json={"data": [1], "links": {"next": "https://metadeploy/rest?page=2"}},
        )
        responses.add(
            "GET",
            "https://metadeploy/rest",
            json={"data": [2], "links": {"next": None}},
        )

        project_config = create_project_config()
        project_config.keychain.set_service(
            "metadeploy", ServiceConfig({"url": "https://metadeploy", "token": "TOKEN"})
        )
        task_config = TaskConfig()
        task = BaseMetaDeployTask(project_config, task_config)
        task._init_task()
        results = task._call_api("GET", "/rest", collect_pages=True)
        self.assertEqual([1, 2], results)


class TestPublish(unittest.TestCase, GithubApiTestMixin):
    @responses.activate
    def test_run_task(self):
        project_config = create_project_config()
        project_config.keychain.set_service(
            "metadeploy", ServiceConfig({"url": "https://metadeploy", "token": "TOKEN"})
        )
        project_config.keychain.set_service(
            "github",
            ServiceConfig(
                {"username": "foo", "password": "bar", "email": "foo@example.com"}
            ),
        )

        responses.add(
            "GET",
            "https://api.github.com/repos/TestOwner/TestRepo",
            json=self._get_expected_repo("TestOwner", "TestRepo"),
        )
        responses.add(
            "GET",
            "https://api.github.com/repos/TestOwner/TestRepo/git/refs/tags/release/1.0",
            json=self._get_expected_tag_ref("release/1.0", "tag_sha"),
        )
        responses.add(
            "GET",
            "https://api.github.com/repos/TestOwner/TestRepo/git/tags/tag_sha",
            json=self._get_expected_tag("release/1.0", "commit_sha"),
        )
        f = io.BytesIO()
        zf = zipfile.ZipFile(f, "w")
        zfi = zipfile.ZipInfo("toplevel/")
        zf.writestr(zfi, "")
        zf.writestr(
            "toplevel/cumulusci.yml",
            yaml.dump(
                {
                    "project": {
                        "package": {"name_managed": "Test Product", "namespace": "ns"}
                    }
                }
            ),
        )
        zf.close()
        responses.add(
            "GET",
            "https://api.github.com/repos/TestOwner/TestRepo/zipball/commit_sha",
            body=f.getvalue(),
            content_type="application/zip",
        )
        responses.add(
            "GET",
            "https://api.github.com/repos/TestOwner/TestRepo/releases/latest",
            json=self._get_expected_release("release/1.0"),
        )
        responses.add(
            "GET", "https://metadeploy/versions?product=abcdef&label=1.0", status=400
        )
        responses.add(
            "POST",
            "https://metadeploy/versions",
            json={"url": "https:/metadeploy/versions/1", "id": 1},
        )
        responses.add(
            "POST",
            "https://metadeploy/plans",
            json={"url": "https://metadeploy/plans/1"},
        )
        responses.add(
            "POST",
            "https://metadeploy/planslug",
            json={"url": "https://metadeploy/planslug/1"},
        )
        responses.add("PATCH", "https://metadeploy/versions/1", json={})

        task_config = TaskConfig(
            {
                "options": {
                    "flow": "install_prod",
                    "product_id": "abcdef",
                    "tag": "release/1.0",
                    "title": "Test Product",
                    "slug": "test",
                    "tier": "primary",
                    "preflight_message": "preflight",
                    "post_install_message": "post-install",
                }
            }
        )
        task = Publish(project_config, task_config)
        task()

        steps = json.loads(responses.calls[-3].request.body)["steps"]
        self.assertEqual(
            [
                {
                    "is_required": True,
                    "kind": "managed",
                    "name": "Install Test Product 1.0",
                    "path": "install_managed",
                    "step_num": "2",
                    "task_class": "cumulusci.tasks.salesforce.InstallPackageVersion",
                    "task_config": {
                        "options": {
                            "activateRSS": True,
                            "namespace": "ns",
                            "retries": 5,
                            "retry_interval": 5,
                            "retry_interval_add": 30,
                            "version": "1.0",
                        }
                    },
                },
                {
                    "is_required": True,
                    "kind": "other",
                    "name": "Update Admin Profile",
                    "path": "config_managed.update_admin_profile",
                    "step_num": "3.2",
                    "task_class": "cumulusci.tasks.salesforce.UpdateAdminProfile",
                    "task_config": {
                        "options": {"managed": True, "namespaced_org": False}
                    },
                },
            ],
            steps,
        )

    @responses.activate
    def test_find_or_create_version__already_exists(self):
        responses.add(
            "GET",
            "https://metadeploy/versions?product=abcdef&label=1.0",
            json={"data": [{"url": "http://EXISTING_VERSION"}]},
        )

        project_config = create_project_config()
        project_config.keychain.set_service(
            "metadeploy", ServiceConfig({"url": "https://metadeploy", "token": "TOKEN"})
        )
        task_config = TaskConfig(
            {
                "options": {
                    "flow": "install_prod",
                    "product_id": "abcdef",
                    "tag": "release/1.0",
                    "title": "Test Product",
                    "slug": "test",
                    "tier": "primary",
                }
            }
        )
        task = Publish(project_config, task_config)
        task._init_task()
        version = task._find_or_create_version()
        self.assertEqual("http://EXISTING_VERSION", version["url"])
