# Research record

This record separates observations from proposed work. Research date: November 10, 2026.

## Actual target

The owner supplied the software values recorded in [the target file](../targets/WD90F53AVS.json). The operating system is reported as Tizen 7.1.9, correcting the initial assumption that the display ran Android. No firmware image or source tree has been extracted from this unit.

Bounded read-only LAN checks established reachability but did not provide an accessible web interface, debugging interface, authenticated local session or firmware image. Selected TCP ports refused connections. Directed service discovery and plaintext OCF reads received no reply. A stateless DTLS first-flight check to one standard secure port received no reply. A separate limited UDP check reported several candidate high ports closed and the standard OCF ports as open-or-filtered; the latter means no conclusive service response, not a confirmed open service. This was not a full port scan and does not rule out another endpoint or network filtering. Network addresses and hardware addresses are omitted from this public record.

## Same-model local-control evidence

[LocalThings issue #786](https://github.com/mbillow/localthings/issues/786) contains an owner's diagnostics for WD90F53AVS. This is evidence from another unit, not validation against this project's appliance.

[Pull request #790](https://github.com/mbillow/localthings/pull/790) was open when inspected. It identifies the same model family and proposes drying-temperature, dry-time and wrinkle-prevent controls. Its author explicitly marks those three writes as needing hardware confirmation. Do not describe them as verified working commands.

The PR's [pinned diagnostic fixture](https://github.com/mbillow/localthings/blob/b1f36f5f01e7b46b6927a9db5291bf85e146a1b0/tests/fixtures/washer_dryer_awm_m64_25_device.json) reports separate WIFI and Micom update entries. It also reports speaker output, voice/tone/mute modes, volume levels and a list of preset tones. That supports investigating these controls. It does not establish arbitrary audio upload, a speaker-file path, firmware write access, or a rollback procedure.

## Protocol and Hubitat

[LocalThings](https://github.com/mbillow/localthings) and the [smartthings-local protocol library](https://github.com/QuiteYellow/SmartThings-Local) provide relevant local OCF/CoAP/DTLS research. Compatibility and authentication vary by device and firmware. Runtime local access, credential acquisition, firmware modification and successful restoration are separate milestones.

Hubitat supports [custom drivers](https://docs2.hubitat.com/en/developer/driver/overview). No Hubitat driver is implemented here. Direct Hubitat transport versus a LAN-side adapter remains undecided until this appliance's protocol and Hubitat's needed transport support are verified. Any adapter must be described explicitly; it must not be presented as direct hub-to-appliance support.

## Samsung source and recovery material

Samsung's public Release Center returned no results for `WD90F53` or `AWM-US-M64` in the browser searches performed for this project. This describes those searches, not proof that no relevant source exists.

The model manual's [open-source announcement link](https://opensource.samsung.com/opensource/SMART_AT_051/seq/0) was accessible in the browser. It lists open-source license material and directs corresponding-source inquiries to Samsung's [Inquiry page](https://opensource.samsung.com/requestInquiry). A later catalog search for `SMART_AT_051` located an official U-Boot source archive, which was downloaded and inspected. See [firmware acquisition findings](firmware-acquisition.md) and its [provenance record](../sources/SMART_AT_051.json). This is not a matching complete washer image. The proprietary laundry application source, board map, installation route and recovery package have not been obtained. No request has been sent on the owner's behalf.

The next blocking dependency for firmware modification is acquisition of matching software and a verified way to recover test hardware. Neither a generic Tizen/TizenRT checkout nor a version string substitutes for that evidence.
