# WD90F53AVS Washer Customizable Firmware

Research and development for owner-customizable Samsung WD90F53AVS firmware and local Hubitat integration.

**Current status: research foundation. There is no flashable custom firmware, working Hubitat driver, firmware extraction tool, or verified rollback procedure in this repository.** The included image catalog tool works offline on files already obtained separately.

## Project goals

- Modify the appliance's existing firmware, with a verified recovery path.
- Upload personal completion sounds and configure ordinary notifications and behaviors.
- Save custom wash/dry profiles and expose finer control over supported settings and durations.
- Explore steam/dewrinkle profiles where the hardware supports them.
- Operate through Hubitat over the local network without a required internet connection during normal operation.

Door, heater, water-level, motor and other hardware protections remain enforced. Timing and temperature granularity require evidence from the actual controller; unlimited heating or steam operation is not a project feature.

See [requirements](docs/requirements.md), [research findings](docs/research.md), and [recovery requirements](docs/recovery.md).

An official `SMART_AT_051` U-Boot source archive has now been obtained and inspected. It targets ARTIK051/053 and has not been matched to the installed M64 hardware. See the [acquisition findings](docs/firmware-acquisition.md); it is not the complete firmware needed for the requested modifications.

## Target baseline

The owner reported these values from the appliance screen on November 10, 2026:

| Field | Value |
| --- | --- |
| Model | WD90F53AVS |
| Interface | One UI 7.0 Laundry combo |
| Operating system | Tizen 7.1.9 |
| Firmware family | AWM-US-M64-25-WD80MU |
| Firmware build | 20250328.161953 |
| Additional version lines | `25052649 24120301`; `25021204 25021204` |

The machine-readable [target record](targets/WD90F53AVS.json) preserves the additional lines without assigning them to an unverified board or function. These values are owner observations, not a firmware-image extraction.

## What works now

`tools/image_catalog.py` records file sizes and SHA-256 hashes for supplied image files and checks them against the target record. It rejects changed or truncated files, target mismatches, duplicate entries, empty images and paths that escape the chosen image directory. It creates a new manifest without overwriting an existing file.

Python 3.11 or newer is sufficient; no third-party packages are required. From the repository root:

```text
python -m unittest discover -s tests -v
python tools/image_catalog.py --help
```

If a firmware image is obtained independently, keep it in a private directory. For example, with `original.bin` already present in an ignored `private` directory:

```text
python tools/image_catalog.py create --image-root private --component original=original.bin --manifest private/original.manifest.json
python tools/image_catalog.py verify --image-root private --manifest private/original.manifest.json
```

`original` is a user-supplied file label, not a known partition name. A passing hash check establishes file integrity against the manifest. It does not establish that a file is authentic, complete, compatible, flashable or recoverable. A manifest can itself be edited, so keep a trusted, separate copy of it.

## Next engineering milestone

Obtain the matching original firmware or a repeatable read-only extraction, identify the physical boards and partition layout, and demonstrate restoration on appropriate test hardware. That evidence determines the build target, installation method and rollback design. Samsung's source offer is not a promise that its proprietary laundry applications or a complete flashable image are publicly available.

## Public contributions

Publish sanitized observations and code you have the right to share. Keep appliance serial numbers, network details, account data, credentials, raw captures and proprietary firmware images private. The MIT license applies to this project's original code and documentation, not to Samsung firmware or third-party projects.
