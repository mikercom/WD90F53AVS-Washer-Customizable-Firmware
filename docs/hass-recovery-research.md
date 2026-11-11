# Recovery and flashing leads: HASS research

Research date: November 11, 2026. No matching WD90F53AVS/M64 recovery image or verified restore procedure has been obtained. Nothing was written to the appliance.

## New primary research sources

- [HASS archive unpacker](https://github.com/doitaljosh/samsung-hass-fw-unpacker/tree/8e028337096a802973a57306d8e0cc7f737592bf): custom compressed controller update archives, metadata and checksum tooling. The author traces the decoder to a Samsung HART-M320 / ABOV A33G527 bootloader.
- [HASS UART tool](https://github.com/doitaljosh/samsung-hass-uart-playground/tree/9f42ffc29ba8157905f16d3eaf783992841753bb): source implements bus logging, messaging, erase, write and checksum verification. Its command parser does not implement flash readback. It was inspected statically and was not run against hardware.

These are useful protocol leads, not evidence that either tool supports this washer. UART settings, electrical connections, target addresses, bootloader entry, erase regions and recovery after interruption remain unverified for this unit. The write implementation erases by default. No commands or wiring from these generic examples should be applied to the washer without establishing compatibility.

## Sample archives actually checked

Four example TARs were downloaded from the pinned unpacker revision and inspected locally without running downloaded code. An independent offline decoder checked all six payload occurrences (five unique payloads) against their XML metadata. All compressed sizes, compressed CRCs, decoded sizes and decoded CRCs matched. Decoded payloads range from 244,584 to 424,904 bytes. SHA-256 records are in [HASS sample verification](../sources/HASS-sample-verification.json).

| Archive | Payload board identifiers |
| --- | --- |
| DE92-04721A_DE92-04768A_240208.tar | DE92-04721A, DE92-04768A |
| DE92-04768A_240131.tar | DE92-04768A |
| DE92-04769A_DE92-04770A_240525.tar | DE92-04769A, DE92-04770A |
| FG_DA92-01156A_241204.tar | DA92-01156A; payload name includes RS5300T |

Neither the inspected XML nor the targeted ASCII string scan established WD90F53AVS or AWM-US-M64 compatibility. Absence of those strings is not proof of incompatibility; there is simply no positive match. These small controller updates do not establish a complete Tizen/display recovery image, a bootloader backup or a means to recover a board that cannot enter its update routine. CRC agreement establishes internal integrity, not provenance, model compatibility, signature acceptance or successful restoration. The binaries are not redistributed in this repository.

## Physical board identifiers for follow-up

Parts sellers provide narrower search leads:

- [Display assembly DC92-03822A](https://impactcomputers.com/index.php/miscellaneous/samsung-washer-dc92-03822a) lists WD90F53AVSUS compatibility.
- [Control assembly DC94-15980A](https://www.shopjimmy.com/samsung-dc94-15980a-washer-dryer-control-board-assy-pcb-eeprom/) lists WD90F53AVSUS and visible PCB number DC92-03695G.

These are seller records, not a verified bill of materials for the owner's actual revision. The [ShopJimmy display listing](https://www.shopjimmy.com/samsung-dc92-03822a-washer-dryer-display-module-screen/) has inconsistent part-number text, so its title alone must not be used to select hardware. A matched spare board could support bench research and preserve the original, but neither drop-in restoration, pairing requirements nor firmware cloning has been demonstrated. No purchase was made.

## What would establish a usable restore path

1. Match the actual display and controller board labels/revisions, processor and storage.
2. Obtain a matching complete service image or independently repeated storage reads. Preserve device-specific data privately.
3. Establish the documented or measured recovery entry and read/write transport, power requirements, image layout, signing restrictions and downgrade rules.
4. Demonstrate recovery on suitable spare hardware, including verification after reboot, before changing the installed appliance.

Samsung's [consumer update guide](https://www.samsung.com/us/support/answer/ANS10001022/) describes SmartThings updates. Its physical update dongle procedure is for a specific 2021/2022 top-loader campaign; it does not establish a WD90F53AVS recovery route. An update package, factory settings reset and full firmware restoration are separate capabilities.

This research advances controller-format understanding but leaves matching original images and model-specific recovery as unresolved dependencies.
