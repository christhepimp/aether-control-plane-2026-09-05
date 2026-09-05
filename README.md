# Aether Control Plane

**Repo:** https://github.com/christhepimp/aether-control-plane-2026-09-05

This is the honest version of the "AI OS from a rooted Android emulator" idea.

## What you asked for

1. Find an Android emulator with root.
2. Get inside its Linux.
3. Slowly replace Linux with a new OS you make.
4. That OS should *be* an AI.

## What is actually possible

Android **is already Linux**. The emulator kernel is typically Goldfish/Ranchu (AOSP). Root lets you inspect and change *userspace* and some device nodes. It does **not** let you hot-swap the running kernel for a brand-new OS while the guest is up.

Replacing Linux means writing a kernel (or a unikernel / hypervisor guest) and booting it. That is a different project from "adb root and start editing /system".

The viable path: **keep Linux as the kernel. Make the AI the OS brain.**

```
[ you / apps ]
       |
[ Aether control plane  <- this repo ]
       |
[ Linux kernel -- Android Goldfish, Linux desktop, or a VM ]
       |
[ hardware or emulator ]
```

The control plane:
- watches processes, files, network, battery
- decides policy (start, stop, isolate, explain)
- talks in natural language
- slowly *replaces the shell and init policy*, not the kernel

## Rooted Android emulator options (research, 2026)

| Path | Root? | Linux access | Notes |
|---|---|---|---|
| Android Studio AVD + rootAVD / Magisk | Yes, after patch | adb root + adb shell | Best free lab. Kernel is Goldfish/Ranchu. |
| Genymotion | Yes on many images (dynamic root) | adb shell | Fast. Good for app testing, not kernel work. |
| Android-x86 / Bliss OS in VirtualBox/QEMU | Yes if you enable it | Real-ish x86 Linux userspace | Closer to a PC Linux box than a phone. |
| Waydroid (on a Linux host) | Host is already root | Android in LXC | You already have a real Linux kernel on the host. |
| Termux / AnLinux / Podroid | Usually no host root | Userspace Linux or a VM | Useful sandbox. Not a kernel replacement. |

Recommended lab for *this* repo:

1. Install Android Studio.
2. Create an AVD (Google APIs, x86_64, API 34+).
3. Root it with rootAVD or a Magisk-patched system image.
4. `adb root && adb shell` -- you are now in Linux userspace on the guest.
5. Run `python3 control_plane.py` from this repo on the host, talking to the device over adb. Or copy it into `/data/local/tmp` and run it in the guest.

## Why we do not replace Linux slowly from inside the emulator

- The kernel is mapped in memory and owned by the hypervisor.
- Userspace cannot rewrite vmlinux and keep running.
- Android userspace (Bionic, init, zygote, binder) is glued to that kernel ABI.
- A real new OS boots from firmware/hypervisor, not from su.

If you later want a real custom kernel, the next step is QEMU + a tiny kernel (Limine + your code, or a research kernel), not Magisk.

## This repo

```
control_plane.py   # AI-shaped supervisor (rule + optional LLM hook)
policy.yaml        # what the OS-brain is allowed to do
docs/LAB.md        # emulator + adb lab notes
```

Run locally (no emulator required for the prototype):

```bash
python3 control_plane.py
```

Talk to it:

```
status
intent: I want a quiet machine
help
```

## You already have this idea many times

Your GitHub account already contains a pile of the same project under different names (AetherOS, SentientOS, synapse-aios, aios-self, ...). One working control plane is worth more than fifty empty repos. Build here.
