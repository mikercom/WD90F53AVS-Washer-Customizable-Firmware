# Recovery evidence and current limits

**Rollback status: unverified.** This repository contains no flasher, recovery image, board pinout or restore procedure.

## What must be established

- Physical board identifiers and revisions for the actual test appliance.
- The relationship between the screen/network firmware and each appliance-controller component.
- Storage technology, partition map, image formats and update dependencies.
- A repeatable read-only extraction or an authoritative matching original image.
- Which per-device configuration, calibration and identity data are needed for restoration, and how they will be kept private.
- Boot verification, signing and rollback restrictions for this exact target. These remain unknown; behavior from Samsung phones or another appliance does not establish them.
- A recovery interface that remains usable when the modified application fails to boot.
- A restore rehearsal on appropriate test hardware with recorded results. No unverified offsets, erase commands or wiring instructions should be used.

## Image inventory

The offline image catalog is one preparation step. It associates supplied files with a target record and records their sizes and hashes. Repeating a read and comparing the independent files can help detect an inconsistent extraction, but identical reads still do not prove that every required region was captured.

A successful `verify` command means the supplied files match the supplied manifest and target record. It does not identify partitions, verify manufacturer signatures, defeat boot protection, or test restoration. The tool always preserves `recovery_status: unverified`.

Keep at least one trusted copy of the original images and manifest outside the development workspace. Firmware and captures may contain private device or account data; they do not belong in this public repository. Ignore rules are a convenience, not a substitute for inspecting files before publishing.

## Future restore acceptance

Before calling rollback verified, record the target hardware, original images and trusted hashes, recovery entry method, exact restored regions, power requirements, read-back results, startup behavior and retained calibration/configuration. Test the failure cases that the procedure is intended to recover from.

A factory settings reset, a network reconnection or a successful normal update is not a demonstrated restoration of a failed custom firmware installation.
