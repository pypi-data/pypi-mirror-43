#   Copyright 2019 SiLeader and Cerussite.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import subprocess
import typing
import sys
import re


LICENSE = "Apache License 2.0"

DRY_RUN = False


def __which(name, default):
    res = subprocess.run("which {}".format(name), stdout=subprocess.PIPE, shell=True)
    if res.returncode != 0:
        return default
    out = res.stdout.decode(encoding="utf8")
    return out.strip()


CERTBOT = __which("certbot", "/usr/bin/certbot")


def __certbot(args):
    commands = [CERTBOT]
    commands.extend(args)
    if DRY_RUN:
        commands.append("--dry-run")
    res = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print("certbot error", file=sys.stderr)
        print(res.stderr.decode(encoding="utf8"), file=sys.stderr)
        exit(res.returncode)
    return res


def __std_out_err(res: subprocess.CompletedProcess) -> typing.Union[str, str]:
    return res.stdout.decode(encoding="utf8"), res.stderr.decode(encoding="utf8")


def get_certified(stdout=None):
    if stdout is None:
        stdout, _ = __std_out_err(__certbot(["certificates"]))
    domains = []
    for so in stdout.split("\n"):
        match = re.fullmatch("\\s*Domains\\s*:\\s*([\\w.]+)\\s*", so)
        if match is not None:
            domains.append(match.group(1))
    return domains


def main():
    global CERTBOT, DRY_RUN

    parser = argparse.ArgumentParser(
        prog="certify",
        description="certbot support tool",
        epilog="Copyright 2019 SiLeader and Cerussite.\nLicensed under {}.".format(LICENSE),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--certbot",
        help="name or path of certbot command (default: {})".format(CERTBOT),
        default=CERTBOT
    )
    parser.add_argument("--dry-run", help="test commands without saving any certificates", action="store_true")

    sub = parser.add_subparsers()

    _new = sub.add_parser("new")
    _new.set_defaults(handler=__new)
    _new.add_argument("--webroot", "-w", help="web root path", required=True)
    _new.add_argument("--agree-tos", help="Agree tp the ACME server's Subscriber Agreement", action="store_true")
    _new.add_argument("domain", help="domain name")

    _renew = sub.add_parser("renew")
    _renew.set_defaults(handler=__renew)
    _renew.add_argument("--reload", help="reload service after renewal", default=None)
    _renew.add_argument("--restart", help="restart service after renewal", default=None)
    _renew.add_argument("--force", help="force renewal", action="store_true")
    service = __which("service", "/usr/sbin/service")
    _renew.add_argument("--service", help="path of 'service' command (default: {})".format(service), default=service)

    lst = sub.add_parser("list")
    lst.set_defaults(handler=__list)
    lst.add_argument("--detail", action="store_true")

    _delete = sub.add_parser("delete")
    _delete.set_defaults(handler=__delete)
    _delete.add_argument("domain", help="domain name", choices=get_certified())

    args = parser.parse_args()
    CERTBOT = args.certbot
    DRY_RUN = args.dry_run
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


def new(domain, webroot, agree_tos=False):
    arg = ["certonly", "-d", domain, "--webroot", "-w", webroot]
    if agree_tos:
        arg.append("--agree-tos")
    __certbot(arg)


def renew(reload=None, restart=None, service=None, force=False):
    def __service():
        if service is None:
            return __which("service", "/usr/sbin/service")
        else:
            return service
    arg = ["renew"]
    if reload is not None:
        service = __service()
        arg.extend(["--post-hook", "{} {} reload".format(service, reload)])
    if restart is not None:
        service = __service()
        arg.extend(["--post-hook", "{} {} restart".format(service, reload)])
    if force:
        arg.append("--force-renewal")
    __certbot(arg)


def delete(domain):
    assert domain not in get_certified(), "{} not found".format(domain)
    __certbot(["delete", "-d", domain])


def __new(args):
    new(args.domain, args.webroot, args.agree_tos)


def __renew(args):
    renew(args.reload, args.restart, args.service, args.force)


def __list(args):
    res = __certbot(["certificates"])
    stdout, _ = __std_out_err(res)
    if args.detail:
        for so in stdout.split("\n"):
            if re.fullmatch("-*\\s*", so) is None:
                print(so)
    else:
        print("\n".join(get_certified(stdout)))


def __delete(args):
    delete(args.domain)


if __name__ == '__main__':
    main()
