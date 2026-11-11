"""Catalog and check local image files. Never connects to or flashes a device."""

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys


DEFAULT_TARGET = Path(__file__).resolve().parents[1] / "targets" / "WD90F53AVS.json"
PURPOSE = "file-integrity-only"
RECOVERY_STATUS = "unverified"


class CatalogError(ValueError):
    """The catalog, target, or input files could not be validated."""


def _target_identity(target):
    if not isinstance(target, dict) or target.get("schema_version") != 1:
        raise CatalogError("Unsupported target record")
    model = target.get("model")
    identity = target.get("identity")
    if not isinstance(model, str) or not model.strip() or not isinstance(identity, dict):
        raise CatalogError("Missing target identity")
    for key in ("firmware_family", "firmware_build", "platform", "platform_version"):
        if not isinstance(identity.get(key), str) or not identity[key].strip():
            raise CatalogError(f"Missing target identity field: {key}")
    return {"model": model, "identity": copy.deepcopy(identity)}


def _image_path(root, relative_name):
    if not isinstance(relative_name, str) or not relative_name:
        raise CatalogError("Image file must be a relative path")
    relative = PurePosixPath(relative_name.replace("\\", "/"))
    if (
        relative.is_absolute()
        or PureWindowsPath(relative_name).drive
        or ".." in relative.parts
        or ":" in relative_name
    ):
        raise CatalogError("Image file must be a relative path without parent traversal")
    resolved = root.joinpath(*relative.parts).resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise CatalogError("Image file resolves outside the image root")
    if not resolved.is_file():
        raise CatalogError("Image path is not a regular file")
    return resolved, relative.as_posix()


def _image_root(value):
    root = Path(value).resolve(strict=True)
    if not root.is_dir():
        raise CatalogError("Image root must be a directory")
    return root


def _measure(path):
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        before = path.stat()
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            total += len(block)
        after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (
        after.st_size, after.st_mtime_ns, after.st_ino
    ) or total != after.st_size:
        raise CatalogError("Image changed while being read")
    if total == 0:
        raise CatalogError("Image file is empty")
    return total, digest.hexdigest()


def create_catalog(image_root, target, components):
    """Hash supplied files; neither image authenticity nor backup completeness is proven."""
    identity = _target_identity(target)
    root = _image_root(image_root)
    if not isinstance(components, dict) or not components:
        raise CatalogError("At least one named image is required")
    images = []
    paths = set()
    for name, relative_name in components.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name):
            raise CatalogError("Invalid component name")
        path, relative = _image_path(root, relative_name)
        if path in paths:
            raise CatalogError("duplicate image path")
        paths.add(path)
        size, digest = _measure(path)
        images.append({"component": name, "file": relative, "bytes": size, "sha256": digest})
    return {
        "schema_version": 1,
        "purpose": PURPOSE,
        "recovery_status": RECOVERY_STATUS,
        "target": identity,
        "images": images,
    }


def verify_catalog(image_root, target, catalog):
    """Return matching component names or raise. Success only establishes file integrity."""
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1:
        raise CatalogError("Unsupported image catalog")
    if catalog.get("purpose") != PURPOSE:
        raise CatalogError("Unsupported catalog purpose")
    if catalog.get("recovery_status") != RECOVERY_STATUS:
        raise CatalogError("A file catalog cannot establish verified recovery")
    if catalog.get("target") != _target_identity(target):
        raise CatalogError("Catalog target does not match the supplied target record")
    images = catalog.get("images")
    if not isinstance(images, list) or not images:
        raise CatalogError("Image catalog is empty")
    root = _image_root(image_root)
    names, paths = set(), set()
    verified = []
    for entry in images:
        if not isinstance(entry, dict):
            raise CatalogError("Invalid image entry")
        name = entry.get("component")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name):
            raise CatalogError("Invalid component name")
        if name in names:
            raise CatalogError("duplicate component name")
        names.add(name)
        path, _ = _image_path(root, entry.get("file"))
        if path in paths:
            raise CatalogError("duplicate image path")
        paths.add(path)
        expected_size = entry.get("bytes")
        expected_digest = entry.get("sha256")
        if type(expected_size) is not int or expected_size <= 0:
            raise CatalogError("Invalid image size")
        if not isinstance(expected_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
            raise CatalogError("Invalid SHA-256 digest")
        size, digest = _measure(path)
        if size != expected_size:
            raise CatalogError(f"Image size mismatch: {name}")
        if digest != expected_digest:
            raise CatalogError(f"Image SHA-256 mismatch: {name}")
        verified.append(name)
    return verified


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--target", type=Path, default=DEFAULT_TARGET)
        command.add_argument("--image-root", type=Path, required=True)
        command.add_argument("--manifest", type=Path, required=True)
        if name == "create":
            command.add_argument("--component", action="append", required=True, metavar="NAME=RELATIVE_PATH")
    args = parser.parse_args(argv)
    try:
        target = json.loads(args.target.read_text(encoding="utf-8"))
        if args.command == "create":
            components = {}
            for item in args.component:
                if "=" not in item:
                    raise CatalogError("Use --component NAME=RELATIVE_PATH")
                name, relative = item.split("=", 1)
                if name in components:
                    raise CatalogError("duplicate component name")
                components[name] = relative
            catalog = create_catalog(args.image_root, target, components)
            # Exclusive creation prevents accidentally overwriting an image or prior catalog.
            with args.manifest.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(catalog, stream, indent=2, sort_keys=True)
                stream.write("\n")
            print(f"Cataloged {len(catalog['images'])} image file(s). Recovery remains unverified.")
        else:
            catalog = json.loads(args.manifest.read_text(encoding="utf-8"))
            names = verify_catalog(args.image_root, target, catalog)
            print(f"File integrity verified for {len(names)} image file(s).")
            print("Firmware authenticity, completeness and recovery remain unverified.")
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
