# Lab: rooted Android emulator as a Linux sandbox

This is a *sandbox*, not a kernel replacement factory.

## Android Studio AVD (recommended)

1. Install Android Studio and SDK platform-tools (`adb` on PATH).
2. Create an x86_64 AVD with a Google APIs system image (API 34+).
3. Cold-boot it once. Confirm:

```bash
adb devices
adb shell uname -a
```

You should see a Linux kernel string (Goldfish or Ranchu).

4. Root the AVD with a maintained tool such as rootAVD or a Magisk-patched image.
5. Then:

```bash
adb root
adb shell id
adb shell cat /proc/version
```

`uid=0` means you have userspace root on the guest. That is the ceiling for "slowly replacing Linux" from inside the emulator: you can change userspace, not the running kernel.

## Genymotion

Genymotion can enable root on many virtual devices. Same story: `adb shell` is Linux userspace. Use it if you want a faster GUI device, not if you want to author a kernel.

## Host-side control plane

Keep Aether on the host so a bad policy cannot brick the only copy of the code:

```bash
python3 control_plane.py
# then, inside the REPL:
adb devices
adb shell uname -a
```

## If you actually want a new OS

Separate track, do not mix with Magisk:

- QEMU + Limine or multiboot
- a tiny kernel that prints to serial
- then drivers, then a scheduler, then an agent in userspace

That is years of work. The control plane in this repo is the part you can run *today* so the machine already *behaves* like an AI OS.
