from .autologs import generate_logs
import logging
import pytest


import yaml
import logging
import urllib3
from kubernetes import config as kube_config
from openshift.dynamic import DynamicClient
from openshift.dynamic.exceptions import NotFoundError

LOGGER = logging.getLogger(__name__)
TIMEOUT = 120
SLEEP = 1


class OcpClient(object):
    def __init__(self):
        urllib3.disable_warnings()
        try:
            self.dyn_client = DynamicClient(kube_config.new_client_from_config())
        except (kube_config.ConfigException, urllib3.exceptions.MaxRetryError):
            LOGGER.error('You need to be login to cluster')
            raise

    def get_resource(self, name, api_version, kind, **kwargs):
        """
        Get resource

        Args:
            name (str): Resource name.
            api_version (str): API version of the resource.
            kind (str): The kind on the resource.

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            dict: Resource dict.
        """

    def get_resources(self, api_version, kind, **kwargs):
        """
        Get resources

        Args:
            api_version (str): API version of the resource.
            kind (str): The kind on the resource.

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            list: Resources.
        """

    @generate_logs()
    def wait_for_resource(self, name, api_version, kind, timeout=TIMEOUT, sleep=SLEEP, **kwargs):
        """
        Wait for resource

        Args:
            name (str): Resource name.
            api_version (str): API version of the resource.
            kind (str): The kind on the resource.
            timeout (int): Time to wait for the resource.
            sleep (int): Time to sleep between retries.

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            bool: True if resource exists, False if timeout reached.
        """

    @generate_logs()
    def wait_for_resource_to_be_gone(self, name, api_version, kind, timeout=TIMEOUT, sleep=SLEEP, **kwargs):
        """
        Wait until resource is not exists

        Args:
            name (str): Resource name.
            api_version (str): API version of the resource.
            kind (str): The kind on the resource.
            timeout (int): Time to wait for the resource.
            sleep (int): Time to sleep between retries.

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            bool: True if resource exists, False if timeout reached.
        """

    @generate_logs()
    def wait_for_resource_status(self, name, api_version, kind, status, timeout=TIMEOUT, sleep=SLEEP, **kwargs):
        """
        Wait for resource to be in desire status

        Args:
            name (str): Resource name.
            api_version (str): API version of the resource.
            kind (str): The kind on the resource.
            status (str): Expected status.
            timeout (int): Time to wait for the resource.
            sleep (int): Time to sleep between retries.

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            bool: True if resource in desire status, False if timeout reached.
        """

    @generate_logs()
    def create_resource(self, yaml_file=None, resource_dict=None, namespace=None, wait=False):
        """
        Create resource from given yaml file or from dict

        Args:
            yaml_file (str): Path to yaml file.
            resource_dict (dict): Dict to create resource from.
            namespace (str): Namespace name for the object
            wait (bool) : True to wait for resource status.

        Raises:
            AssertionError: If missing parameter.

        Returns:
            bool: True if create succeeded, False otherwise.
        """

    def delete_resource(self, name, namespace, api_version, kind, wait=False):
        """
        Delete resource

        Args:
            name (str): Pod name.
            namespace (str): Namespace name.
            api_version (str): API version.
            kind (str): Resource kind.
            wait (bool): True to wait for pod to be deleted.

        Returns:

        """

    @generate_logs()
    def delete_resource_from_yaml(self, yaml_file, wait=False):
        """
        Delete resource from given yaml file or from dict

        Args:
            yaml_file (str): Path to yaml file.
            wait (bool) : True to wait for resource status.

        Raises:
            AssertionError: If missing parameter

        Returns:
            bool: True if delete succeeded, False otherwise.
        """

    @generate_logs()
    def get_namespace(self, namespace):
        """
        Get namespace

        Args:
            namespace (str): Namespace name.

        Returns:
            dict: Namespace dict.
        """

    @generate_logs()
    def create_namespace(self, namespace, wait=False, switch=False):
        """
        Create a namespace

        Args:
            namespace (str): Namespace name.
            wait (bool) : True to wait for resource status.
            switch (bool): Switch to created namespace (project)

        Returns:
            bool: True if create succeeded, False otherwise
        """

    @generate_logs()
    def delete_namespace(self, namespace, wait=False):
        """
        Delete namespace

        Args:
            namespace (str): Namespace name to delete.
            wait (bool) : True to wait for resource status.

        Returns:
            bool: True if delete succeeded, False otherwise
        """

    @generate_logs()
    def get_nodes(self, label_selector=None):
        """
        Get nodes

        Args:
            label_selector (str): Node label to filter with

        Returns:
            list: List of nodes
        """

    @generate_logs()
    def get_pods(self, label_selector=None):
        """
        Get pods

        Args:
            label_selector (str): Pod label to filter with

        Returns:
            list: List of pods
        """

    @generate_logs()
    def get_vmis(self):
        """
        Return List with all the VMI objects

        Returns:
            list: List of VMIs
        """

    @generate_logs()
    def get_vmi(self, vmi):
        """
        Get VMI

        Returns:
            dict: VMI
        """

    @generate_logs()
    def get_vm(self, vm):
        """
        Get VM

        Returns:
            dict: VM
        """

    @generate_logs()
    def delete_pod(self, pod, namespace, wait=False):
        """
        Delete Pod

        Args:
            pod (str): Pod name.
            namespace (str): Namespace name.
            wait (bool): True to wait for pod to be deleted.

        Returns:
            bool: True if delete succeeded, False otherwise.
        """

    @generate_logs()
    def switch_project(self, project):
        """
        Set working project

        Args:
            project (str): Project name

        Returns:
            bool: True if switch succeeded, False otherwise
        """

    @generate_logs()
    def delete_vm(self, vm, namespace, wait=False):
        """
        Delete VM

        Args:
            vm (str): VM name.
            namespace (str): Namespace name.
            wait (bool): True to wait for pod to be deleted.

        Returns:
            bool: True if delete succeeded, False otherwise.
        """

    @generate_logs()
    def wait_for_vmi_status(self, vmi, status):
        """
        Wait for VM status

        Args:
            vmi (str): VMI name
            status (str): Desire status.

        Returns:
            bool: True if resource in desire status, False if timeout reached.
        """

    @generate_logs()
    def wait_for_pod_status(self, pod, status):
        """
        Wait for Pod status

        Args:
            pod (str): Pod name
            status (str): Desire status.

        Returns:
            bool: True if resource in desire status, False if timeout reached.
        """


@generate_logs()
def full_log(name, version='1', **kwargs):
    """
    Get version by name
    """
    return


# def test1():
#     full_log(name='test1')



def test2():
    api = OcpClient()
    api.delete_vm(vm="name", namespace="namespace")
    api.get_pods()

