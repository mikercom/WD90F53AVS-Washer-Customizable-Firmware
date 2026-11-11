# Firmware acquisition findings

Research date: November 10, 2026. No modified firmware has been installed.

## Material actually obtained

Samsung's Release Center has one result for `SMART_AT_051`, the identifier referenced by the washer's open-source announcement. The result provides `uboot-903575a.tar.gz`. The downloaded archive was inspected without executing its build scripts or extracting files into the project.

The [source record](../sources/SMART_AT_051.json) preserves its size, SHA-256, archive root and observed configurations. Its root Makefile identifies U-Boot 2017.01. Vendor configurations include ARTIK051, ARTIK051DA and ARTIK053. The only archive member with a `.bin` suffix is a U-Boot test fixture. No `.img`, `.fw`, `.rpm`, `.wgt`, `.tpk`, `.wav` or `.mp3` members were found.

This is bootloader source. It does not supply the target's complete Tizen filesystem, laundry application, sound assets or matching controller images. Its relationship to the installed M64 hardware has not been established. Addresses, boot commands and recovery behavior in these ARTIK configurations must not be applied to the washer on the strength of a shared manual link.

Source location: [Samsung Open Source](https://opensource.samsung.com/main), search `SMART_AT_051`. The archive is not mirrored in this repository. Its software retains the licenses supplied in the archive; this project's MIT license does not relicense it.

## Model-specific download and service documentation

The [Samsung model support download list](https://www.samsung.com/us/support/model/WD90F53AVSUS/#download-popup) showed manuals and troubleshooting links, with no standalone firmware image.

The Samsung-authored [WD90F/27 service manual](https://manuals.plus/m/386e4f3bd834f59d6df1f71d43411881ffd5f802e7ae5fcb92d3916ec23762e1_optim.pdf) covers WD90F53AVSUS. Printed pages 39 and 48 illustrate the LCD assembly and main PCB. Printed pages 69-71 cover diagnostic tests. No labeled USB/UART/JTAG recovery connector or firmware-upload procedure was found in the text or these board photos. The photos do not establish the identity of unmarked connectors. The manual is linked, not redistributed here.

## Local access

An additional bounded multicast OCF discovery attempt sent three discovery requests and accepted no response from the intended appliance. No pairing, ownership changes, appliance-control commands, firmware writes or security-resource writes were performed. This negative result does not rule out an interface that requires another network path, credentials or physical access.

## Remaining acquisition routes

1. Ask Samsung for matching available source, original service/recovery images and the supported installation/recovery process. A [prepared materials request](samsung-materials-request.md) records the exact target. It has not been sent.
2. Identify the physical LCD/network module and appliance-controller boards, including storage and connector markings. The current service illustrations do not provide sufficient detail to choose a reader or cable.
3. If a compatible read-only service interface or storage reader is established, obtain and compare independent reads, preserve required per-device data privately, and demonstrate restoration on suitable test hardware.

The exact original firmware and a usable recovery path remain blocking dependencies. Rebuilding or modifying an unverified ARTIK bootloader would not implement the requested washer customizations or establish a rollback method.
