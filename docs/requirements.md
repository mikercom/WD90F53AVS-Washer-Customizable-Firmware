# Customization requirements

All appliance features below are requested or proposed work, not implemented capabilities. Firmware modification is the owner's preferred approach. A companion-only integration is an alternative to evaluate explicitly, not an assumed replacement for that goal.

| Feature | Intended behavior | Evidence needed |
| --- | --- | --- |
| Uploaded completion sounds | Import personal audio, preview it, select completion events, and adjust ordinary notification volume and quiet hours. | Access to the screen/audio software, supported codecs, storage limits, speaker controls and event hooks. Critical alarms must remain effective. |
| Configurable behaviors | Configure completion reminders, notifications and other ordinary event-driven actions. | Documented events and actions, persistence behavior and restart handling. No automatic cycle start after a restart. |
| Custom cycles | Name, save, import and export wash/dry profiles; edit supported stage sequences. | The controller's real stage model, parameter ranges and valid transitions. A stored profile is not evidence that the appliance can execute it. |
| More timing control | Choose wash, rinse, soak, spin and drying durations where supported. | Verified lower/upper bounds, cancellation behavior and the controller's response to each requested setting. No unbounded actuator or heater operation. |
| Temperature control | Offer the finest verified temperature choices for each supported stage. | Whether the controller accepts numeric targets or only named presets, plus verified operating limits. Do not infer degree-by-degree control from a preset selector. |
| Steam/dewrinkle profiles | Provide suitable refresh profiles where the hardware and controller support them. | Confirmed steam capability, water handling, temperature and exposure limits. Steam wash support alone does not establish a dry-garment refresh function. |
| Local Hubitat integration | Publish state/events and accept verified, permitted commands over the LAN during an internet outage. | Authentication, protocol mapping, Hubitat transport support, reconnect behavior and a real offline test. Initial credential acquisition must be documented separately from normal operation. |
| Rollback | Restore the matching original software and required per-device state after a failed modification. | Complete images, board/partition mapping, recovery access independent of the modified application and a demonstrated restore. |

## Acceptance criteria

1. The device identity and firmware build match the chosen target before any future installation.
2. Each exposed setting has a hardware observation or authoritative source supporting its meaning, range and writable state.
3. The interface distinguishes a requested value, an accepted value and the appliance's reported state. Failed commands are visible.
4. Heating, steam, water and motor operations remain subject to the appliance's protections. A local API does not add unlock overrides or arbitrary resource writes.
5. A saved profile validates against the connected appliance's verified capabilities and refuses unsupported values. It cannot silently extend operating limits.
6. Network loss or a restart does not replay stale commands, extend heating, or automatically restart a cycle.
7. The audio feature has size/duration limits and preserves critical alarms. Uploaded files are parsed and validated before playback.
8. Offline Hubitat behavior is demonstrated with the internet path unavailable; a working cloud integration is not that test.
9. Rollback is called verified only after a restore on suitable test hardware passes defined checks. Image hashing alone does not satisfy this criterion.

## Work order

1. Obtain original firmware and recovery evidence; identify all relevant boards.
2. Establish a reproducible analysis/build environment for that exact software.
3. Implement a small UI/audio change and test restore before broader changes.
4. Map permitted cycle parameters and implement profile validation.
5. Add a local Hubitat integration using verified commands and events.
6. Validate startup, power loss, network loss, update compatibility and recovery.

No schedule or compatibility guarantee is attached to these steps while the firmware and hardware interfaces remain unavailable.
