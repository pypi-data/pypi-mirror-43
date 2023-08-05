import inspect
import logging
import re
from functools import wraps


class GenerateLogs(object):
    def __init__(self, logger=None):
        """
        Initialing the logger

        Args:
            logger (Logger): logger instance to use

        """
        self.logger = logger if logger else logging.getLogger(__name__)

    def generate_logs(self, info=True, error=True, warn=False):
        """
        Decorator to generate log info and log error for function.
        The log contain the first line from the function docstring and resolve
        names from function docstring by function args, any args that not
        resolved from the docstring will be printed after.
        In some cases only info or error log is needed, the decorator can be
        called with @generate_logs(error=False) to get only log INFO and vice versa

        Example:
            from autologs.autologs import GenerateLogs
            logger = logging.getLoger(""NAME)
            gl = GenerateLogs(logger=logger)

            @gl.generate_logs()
            def my_test(test, cases):
                '''
                Run test with cases
                '''
                return

        call my_test(test='my-test-name', cases=['case01', 'case02']
        Will generate:
            INFO Run test my-test-name with cases case01, case02
            ERROR Failed to Run test my-test-name with cases case01, case02
            if step is True:
                Test Step   1: Run test my-test-name with cases case01, case02

        Args:
            info (bool): True to get INFO log
            error (bool): True to get ERROR log
            warn (bool): True to get WARN log

        Returns:
            any: The function return
        """

        def generate_logs_decorator(func):
            """
            The real decorator

            Args:
                func (Function): Function

            Returns:
                any: The function return
            """

            @wraps(func)
            def inner(*args, **kwargs):
                """
                The call for the function
                """
                kwargs_for_log = kwargs.copy()
                stack = inspect.stack()
                called_from, _ = self.get_called_from_test(stack=stack)
                func_doc = inspect.getdoc(func)
                func_argspec = inspect.getfullargspec(func)

                # Get function default args
                func_argspec_default = dict(
                    zip(
                        func_argspec.args[-len(func_argspec.defaults or list()):],
                        func_argspec.defaults or list()
                    )
                )

                # Get actual function args
                func_args = dict(zip(func_argspec.args, [kwargs.get(i) for i in func_argspec.args]))

                # Filter missing args from default if not sent by user
                missing_args = dict(
                    (k, v) for k, v in func_argspec_default.items() if
                    k not in func_args.keys()
                )

                # Update func_args with missing args
                for k, v in missing_args.items():
                    if k == "self":
                        continue

                    if k not in func_args.keys():
                        func_args[k] = v

                # Update kwargs_for_log with all args
                for k, v in func_args.items():
                    if k == "self":
                        continue

                    if k not in kwargs_for_log.keys():
                        kwargs_for_log[k] = v

                log_action = func_doc.split("\n")[0]
                log_info, log_err = self.get_log_msg(log_action=log_action, **kwargs_for_log)
                if called_from:
                    called_from_log = "[{called_from}]".format(called_from=called_from)
                    log_info = "{called_from_log} {log_info}".format(
                        called_from_log=called_from_log, log_info=log_info
                    )

                if info:
                    self.logger.info(log_info)
                try:
                    res = func(*args, **kwargs)
                except Exception:
                    self.logger.error(log_err)
                    raise

                if not res:
                    if warn:
                        self.logger.warning(log_err)
                    elif error:
                        self.logger.error(log_err)
                return res

            return inner
        return generate_logs_decorator

    def prepare_kwargs_for_log(self, **kwargs):
        """
        Prepare kwargs for get_log_msg()

        Args:
            kwargs (dict): kwargs to prepare

        Returns:
            dict: kwargs after prepare
        """
        new_kwargs = {}
        for k, v in kwargs.items():
            if v is None:
                continue

            elif isinstance(v, list):
                new_kwargs[k] = self.convert_list(items_list=v)

            elif isinstance(v, dict):
                new_kwargs[k] = self.convert_dict(items_dict=v)

            else:
                new_kwargs[k] = getattr(v, "name", getattr(v, "id", v))
        return new_kwargs

    def convert_list(self, items_list):
        """
        Convert objects in the list to names/ids

        Args:
            items_list (list): List to convert

        Returns:
            list: Converted list
        """
        new_list = []
        for i in items_list:
            if isinstance(i, dict):
                new_list.append(self.convert_dict(items_dict=i))
            else:
                new_list.append(getattr(i, "name", getattr(i, "id", i)))
        return new_list

    def convert_dict(self, items_dict):
        """
        Convert objects in the dict to names/ids

        Args:
            items_dict (dict): dict to convert

        Returns:
            dict: Converted dict
        """
        new_dict = {}
        for k, v in items_dict.items():
            if v is None:
                continue

            if isinstance(v, list):
                new_dict[k] = self.convert_list(items_list=v)
            else:
                new_dict[k] = getattr(v, "name", getattr(v, "id", v))
        return new_dict

    def get_log_msg(self, log_action, obj_type="", obj_name="", extra_txt="", **kwargs):
        """
        Generate info and error logs for log_action on object.

        Args:
            log_action (str): The log_action to perform on the object
                (create, update, remove)
            obj_type (str): Object type
            obj_name (str): Object name
            extra_txt (str): Extra text to add to the log
            kwargs (dict): Parameters for the log_action if any

        Returns:
            tuple: Log info and log error text
        """
        kwargs = self.prepare_kwargs_for_log(**kwargs)
        kwargs_to_pop = []
        kwargs_to_log = {}
        log = [re.sub('[^0-9a-zA-Z|_]+', "", i) for i in log_action.lower().split()]
        for k, v in kwargs.items():

            if k == "self":
                kwargs_to_pop.append(k)

            if " object " in str(v):
                kwargs_to_pop.append(k)

            if k.lower() in log:
                if isinstance(v, bool):
                    continue

                key = re.findall(r'\b%s\b' % k, log_action, re.IGNORECASE)[0]
                v = ", ".join(v) if isinstance(v, list) and all([isinstance(i, str) for i in v]) else v
                log_action = log_action.replace(key, "{key} {val}".format(key=key, val=v))
                kwargs_to_pop.append(k)

        for k in kwargs_to_pop:
            kwargs.pop(k)

        for k, v in kwargs.items():
            if isinstance(v, list):
                kwargs_to_log[k] = [getattr(i, "name", getattr(i, "id", i)) for i in v]
            else:
                kwargs_to_log[k] = getattr(
                    v, "name", getattr(v, "id", getattr(v, "fqdn", v))
                )

        with_kwargs = "with %s" % kwargs_to_log if kwargs_to_log else ""
        info_text = (
            "{log_action} {obj_type} {obj_name} {with_kwargs} {extra_txt}".format(
                log_action=log_action, obj_type=obj_type, obj_name=obj_name,
                with_kwargs=with_kwargs, extra_txt=extra_txt
            )
        ).strip()
        info_text = info_text.replace("  ", "")

        log_error_txt = "Failed to %s" % (info_text.lower())
        return info_text, log_error_txt

    def get_called_from_test(self, stack):
        """
        Check if function was called from test or from fixture

        Args:
            stack (list): stack (inspect.stack()) list

        Returns:
            tuple: From where the function called (step (test), setup or teardown)
                and if called from fixture the fixture scope as well
        """
        scope = ""
        call_args = [i[3] for i in stack]
        frames = [i[0] for i in stack]
        if "pytest_runtest_call" in call_args:
            return "step", scope

        if "pytest_fixture_setup" in call_args:
            for f in frames:
                fixture_def = f.f_locals.get("fixturedef", None)
                if fixture_def:
                    try:
                        scope = fixture_def.scope
                    except AttributeError:
                        scope = ""
            return "setup", scope

        if "pytest_runtest_teardown" in call_args:
            for f in frames:
                fixture_fin = f.f_locals.get("fin", None)
                if fixture_fin:
                    try:
                        if getattr(fixture_fin, "func", None):
                            scope = fixture_fin.func.im_self.scope
                        else:
                            scope = fixture_fin.im_self.scope
                    except AttributeError:
                        scope = ""
            return "teardown", scope
        return "", scope
