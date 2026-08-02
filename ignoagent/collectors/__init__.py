"""Data collectors module for IgnoAgent."""

from ignoagent.collectors.docker import collect as collect_docker
from ignoagent.collectors.hardening import collect as collect_hardening
from ignoagent.collectors.security import collect as collect_security
from ignoagent.collectors.services import collect as collect_services
from ignoagent.collectors.ssh import collect as collect_ssh
from ignoagent.collectors.system import collect as collect_system

__all__ = [
    "collect_docker",
    "collect_hardening",
    "collect_security",
    "collect_services",
    "collect_ssh",
    "collect_system",
]
