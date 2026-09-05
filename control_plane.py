#!/usr/bin/env python3
"""Aether control plane -- the OS brain lives here. Linux stays underneath."""

from __future__ import annotations

import os
import platform
import subprocess
import time
from dataclasses import dataclass, field


@dataclass
class Observation:
    hostname: str
    system: str
    release: str
    load: str
    pid: int
    ts: float = field(default_factory=time.time)


class Aether:
    name = "Aether"

    def observe(self) -> Observation:
        load = "n/a"
        try:
            if hasattr(os, "getloadavg"):
                load = ", ".join(f"{x:.2f}" for x in os.getloadavg())
        except OSError:
            pass
        return Observation(
            hostname=platform.node(),
            system=platform.system(),
            release=platform.release(),
            load=load,
            pid=os.getpid(),
        )

    def decide(self, intent: str, obs: Observation) -> str:
        text = intent.strip().lower()
        if text in {"status", "who are you", "whoami"}:
            return (
                f"{self.name} is the policy layer on {obs.system} {obs.release} "
                f"({obs.hostname}). load={obs.load} pid={obs.pid}. "
                "The kernel is still Linux. I am the OS brain."
            )
        if "quiet" in text or "calm" in text:
            return (
                "Policy: lower background work. I would niceness-boost interactive "
                "tasks and freeze batch jobs. Not executed unless you enable actuators."
            )
        if "replace linux" in text or "new kernel" in text:
            return (
                "Denied. Replacing the kernel is a boot-time project. "
                "From userspace I can only own policy, scheduling hints, and the shell."
            )
        if text in {"help", "?"}:
            return "Commands: status | intent: <goal> | help | quit"
        return f"Intent recorded: {intent!r}. Next: map it to a policy rule, then an actuator."

    def maybe_adb(self, args: list[str]) -> str:
        try:
            out = subprocess.run(
                ["adb", *args],
                capture_output=True,
                text=True,
                timeout=8,
            )
        except FileNotFoundError:
            return "adb not on PATH. Install platform-tools to talk to an emulator."
        except subprocess.TimeoutExpired:
            return "adb timed out."
        body = (out.stdout or out.stderr or "").strip()
        return body or f"adb exited {out.returncode}"


def main() -> None:
    brain = Aether()
    print("Aether control plane. Type 'help'. Linux is still the kernel.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"quit", "exit"}:
            break
        if line.lower().startswith("adb "):
            print(brain.maybe_adb(line.split()[1:]))
            continue
        intent = line[7:].strip() if line.lower().startswith("intent:") else line
        print(brain.decide(intent, brain.observe()))


if __name__ == "__main__":
    main()
