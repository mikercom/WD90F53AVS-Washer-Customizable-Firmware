import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.image_catalog import CatalogError, create_catalog, verify_catalog


ROOT = Path(__file__).resolve().parents[1]
TARGET_PATH = ROOT / "targets" / "WD90F53AVS.json"


class ImageCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "images"
        self.root.mkdir()
        self.image = self.root / "sample.bin"
        self.image.write_bytes(b"abc")
        self.target = json.loads(TARGET_PATH.read_text(encoding="utf-8"))

    def catalog(self):
        return create_catalog(self.root, self.target, {"sample": "sample.bin"})

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / "image_catalog.py"), *args],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )

    def test_known_digest_and_round_trip(self):
        catalog = self.catalog()
        self.assertEqual(
            catalog["images"][0]["sha256"],
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )
        self.assertEqual(catalog["images"][0]["bytes"], 3)
        self.assertEqual(verify_catalog(self.root, self.target, catalog), ["sample"])
        self.assertEqual(catalog["recovery_status"], "unverified")

    def test_changed_image_is_rejected(self):
        catalog = self.catalog()
        self.image.write_bytes(b"abd")
        with self.assertRaisesRegex(CatalogError, "SHA-256"):
            verify_catalog(self.root, self.target, catalog)

    def test_truncated_image_is_rejected(self):
        catalog = self.catalog()
        self.image.write_bytes(b"ab")
        with self.assertRaisesRegex(CatalogError, "size"):
            verify_catalog(self.root, self.target, catalog)

    def test_other_firmware_build_is_rejected(self):
        catalog = self.catalog()
        other = copy.deepcopy(self.target)
        other["identity"]["firmware_build"] = "different-build"
        with self.assertRaisesRegex(CatalogError, "target"):
            verify_catalog(self.root, other, catalog)

    def test_other_model_is_rejected(self):
        catalog = self.catalog()
        other = copy.deepcopy(self.target)
        other["model"] = "DIFFERENT-MODEL"
        with self.assertRaisesRegex(CatalogError, "target"):
            verify_catalog(self.root, other, catalog)

    def test_parent_path_is_rejected(self):
        (self.root.parent / "outside.bin").write_bytes(b"abc")
        with self.assertRaisesRegex(CatalogError, "relative"):
            create_catalog(self.root, self.target, {"sample": "../outside.bin"})

    def test_catalog_path_escape_is_rejected(self):
        catalog = self.catalog()
        catalog["images"][0]["file"] = "../outside.bin"
        with self.assertRaisesRegex(CatalogError, "relative"):
            verify_catalog(self.root, self.target, catalog)

    def test_windows_absolute_path_is_rejected_on_every_platform(self):
        with self.assertRaisesRegex(CatalogError, "relative"):
            create_catalog(self.root, self.target, {"sample": "C:\\private\\image.bin"})

    def test_symlink_escape_is_rejected_when_available(self):
        outside = self.root.parent / "outside.bin"
        outside.write_bytes(b"abc")
        link = self.root / "link.bin"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("Creating symlinks is unavailable on this platform/account")
        with self.assertRaisesRegex(CatalogError, "outside"):
            create_catalog(self.root, self.target, {"sample": "link.bin"})

    def test_empty_image_is_rejected(self):
        self.image.write_bytes(b"")
        with self.assertRaisesRegex(CatalogError, "empty"):
            self.catalog()

    def test_duplicate_catalog_entry_is_rejected(self):
        catalog = self.catalog()
        catalog["images"].append(copy.deepcopy(catalog["images"][0]))
        with self.assertRaisesRegex(CatalogError, "duplicate"):
            verify_catalog(self.root, self.target, catalog)

    def test_manifest_cannot_claim_verified_recovery(self):
        catalog = self.catalog()
        catalog["recovery_status"] = "verified"
        with self.assertRaisesRegex(CatalogError, "recovery"):
            verify_catalog(self.root, self.target, catalog)

    def test_cli_creates_and_verifies_a_private_catalog(self):
        manifest = self.root / "sample.manifest.json"
        result = self.cli(
            "create", "--image-root", str(self.root),
            "--component", "sample=sample.bin", "--manifest", str(manifest),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli(
            "verify", "--image-root", str(self.root), "--manifest", str(manifest),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("recovery remain unverified", result.stdout)

    def test_cli_never_overwrites_an_existing_file(self):
        existing = self.root / "existing.manifest.json"
        existing.write_text("keep this", encoding="utf-8")
        result = self.cli(
            "create", "--image-root", str(self.root),
            "--component", "sample=sample.bin", "--manifest", str(existing),
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(existing.read_text(encoding="utf-8"), "keep this")

    def test_cli_rejects_duplicate_component_names(self):
        result = self.cli(
            "create", "--image-root", str(self.root),
            "--component", "sample=sample.bin", "--component", "sample=sample.bin",
            "--manifest", str(self.root / "duplicate.manifest.json"),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_cli_reports_invalid_json_without_traceback(self):
        manifest = self.root / "broken.manifest.json"
        manifest.write_text("{", encoding="utf-8")
        result = self.cli(
            "verify", "--image-root", str(self.root), "--manifest", str(manifest),
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
