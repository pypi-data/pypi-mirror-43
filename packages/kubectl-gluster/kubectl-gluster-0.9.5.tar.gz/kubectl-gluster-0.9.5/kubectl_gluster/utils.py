#
# Copyright (c) 2019 Red Hat, Inc.
#
# This file is part of gluster-health-report project which is a
# subproject of GlusterFS ( www.gluster.org)
#
# This file is licensed to you under your choice of the GNU Lesser
# General Public License, version 3 or any later version (LGPLv3 or
# later), or the GNU General Public License, version 2 (GPLv2), in all
# cases as published by the Free Software Foundation.

import os
import sys
import subprocess
import time
from datetime import datetime
from contextlib import contextmanager

import requests
from jinja2 import Template


kubectl_cmd = "kubectl"


def _msg(prefix, msg, **kwargs):
    message = "[%7s] %s " % (prefix,
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message += "%s" % msg
    for k, v in kwargs.items():
        if v:
            message += "  %s=%s" % (k, v)

    return message


def info(msg, **kwargs):
    msg = _msg("INFO", msg, **kwargs)
    if kwargs.get("newline", True):
        msg += "\n"

    sys.stdout.write(msg)
    sys.stdout.flush()


def warn(msg, **kwargs):
    print(_msg("WARNING", msg, **kwargs))


def error(msg, **kwargs):
    print(_msg("ERROR", msg, **kwargs))
    sys.exit(1)


class GlusterCSException(Exception):
    def __init__(self, message, **kwargs):
        self.kwargs = kwargs
        self.message = message

        if sys.version_info >= (3,):
            super().__init__(message)
        else:
            super(GlusterCSException, self).__init__(message)

    def __str__(self):
        error(self.message, **self.kwargs)


class CmdException(GlusterCSException):
    pass


class TemplateException(GlusterCSException):
    pass


def execute(cmd, retries=0, delay=2, out_expect="", out_expect_fn=None,
            shell=False, label=""):
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         shell=shell)
    out, err = p.communicate()
    if sys.version_info >= (3,):
        out = out.decode("utf-8").strip()
        err = err.decode("utf-8").strip()
    else:
        out = out.strip()
        err = err.strip()

    cmd_print = cmd if shell else " ".join(cmd)

    if p.returncode == 0:
        if out_expect and out.strip() == out_expect:
            return out

        if out_expect_fn is not None and out_expect_fn(out):
            return out

        if not out_expect and out_expect_fn is None:
            return out

    if retries > 0:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)
        return execute(cmd, retries=(retries-1), delay=delay,
                       out_expect=out_expect, out_expect_fn=out_expect_fn,
                       shell=shell, label=label)

    if p.returncode != 0:
        raise CmdException(
            "command failed",
            cmd=cmd_print,
            return_code=p.returncode,
            error=err
        )

    if out_expect and out_expect != out:
        raise CmdException("command output didn't match",
                           cmd=cmd_print,
                           return_code=p.returncode,
                           expected=out_expect,
                           actual=out)

    if out_expect_fn is not None and not out_expect_fn(out):
        raise CmdException("command output didn't match",
                           cmd=cmd_print,
                           return_code=p.returncode,
                           actual=out)

    return out


def kubectl_exec(namespace, podname, command, retries=0, delay=2,
                 out_expect="", out_expect_fn=None, label=""):
    if retries > 0 and label:
        info(label, newline=False)

    cmd = (kubectl_cmd + " exec -it " + podname + " /bin/bash -n" +
           namespace + " -- -c '%s'" % command)
    out = execute(
        cmd,
        retries=retries,
        delay=delay,
        out_expect=out_expect,
        out_expect_fn=out_expect_fn,
        shell=True,
        label=label
    )

    if retries > 0 and label:
        print(".")

    return out


def kubectl_create(config, filename, retries=0, delay=2, label=""):
    if retries > 0 and label:
        info(label, newline=False)

    out = execute([
        kubectl_cmd,
        "create",
        "-f",
        config["workdir"] + "/" + filename
    ], retries=retries, delay=delay, label=label)

    if retries > 0 and label:
        print(".")

    return out


def kubectl_get(namespace, jsonpath, gettype, name, retries=0, delay=2,
                out_expect="", out_expect_fn=None, extra_args=[], label=""):
    if retries > 0 and label:
        info(label, newline=False)

    cmd = [kubectl_cmd]
    if namespace:
        cmd += ["-n", namespace]

    if jsonpath:
        cmd += ["-ojsonpath={.%s}" % jsonpath]

    cmd += ["get", gettype]

    if name:
        cmd += [name]

    if extra_args:
        cmd += extra_args

    out = execute(cmd, retries=retries, delay=delay, out_expect=out_expect,
                  out_expect_fn=out_expect_fn, label=label)

    if retries > 0 and label:
        print(".")

    return out


def template(config, filename, template_file=None):
    tmpl_url = config["manifests-dir"] + "/" + filename + ".j2"
    dest = os.path.join(config["workdir"], filename)

    if template_file is not None:
        tmpl_url = config["manifests-dir"] + "/" + template_file + ".j2"

    content = ""
    if tmpl_url.startswith("http"):
        resp = requests.get(tmpl_url)
        if resp.status_code != 200:
            raise TemplateException("failed to fetch template",
                                    template=tmpl_url,
                                    status_code=resp.status_code)

        if sys.version_info >= (3,):
            content = resp.content.decode('utf-8')
        else:
            content = resp.content
    else:
        try:
            with open(tmpl_url) as f:
                content = f.read()
        except IOError as err:
            raise TemplateException("failed to open template file",
                                    template=tmpl_url,
                                    error=err)

    if not content:
        raise TemplateException("failed to generate template",
                                template=tmpl_url)

    try:
        Template(content).stream(
            **config["template-args"]).dump(dest)
        return
    except IOError as err:
        raise TemplateException("failed to save template output",
                                template=tmpl_url,
                                error=err)


def template_kube_apply(config, filename, retries=0, delay=2,
                        template_file=None, label=""):
    template(config, filename, template_file=template_file)
    kubectl_create(config, filename, retries=retries, delay=delay)


@contextmanager
def kubectl_context_run(cmd):
    cmd = [kubectl_cmd] + cmd
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    try:
        # Give some time to run the given command
        time.sleep(5)
        yield p
    finally:
        p.terminate()
