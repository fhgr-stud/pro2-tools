#!/usr/bin/env python
import subprocess
import shutil
import sys


def check_command(name, version_args):
    """
    Prüft, ob ein Kommando existiert und gibt dessen Version aus.
    Funktioniert unter Linux, macOS und Windows.
    """
    print(f"Prüfe {name} ...")

    path = shutil.which(name)
    if path is None:
        print(f"  FEHLER: {name} nicht gefunden")
        return False

    try:
        result = subprocess.run(
            [name] + version_args,
            capture_output=True,
            text=True,
            shell=False,  # wichtig fuer Windows
        )

        output = (result.stdout or result.stderr).strip()

        if result.returncode != 0:
            print(f"  FEHLER: {name} vorhanden, aber Rückgabecode {result.returncode}")
            print(f"  Ausgabe: {output}")
            return False

        print(f"  OK: {name} gefunden")
        print(f"  Version: {output}")
        return True

    except FileNotFoundError:
        print(f"  FEHLER: {name} konnte nicht gestartet werden")
        return False
    except Exception as e:
        print(f"  FEHLER: Unerwarteter Fehler bei {name}")
        print(f"  {e}")
        return False


if __name__ == "__main__":
    CHECKS = [
        ("uv", ["self", "version"]),
        ("git", ["--version"]),
    ]

    print("=== Installations-Check ===\n")

    failed = False
    for check in CHECKS:
        failed = failed or not check_command(*check)
        print()

    print("\n=== Zusammenfassung ===")
    if not failed:
        print("OK: Alle benötigten Programme sind installiert.")
        sys.exit(0)
    else:
        print("FEHLER: Installation unvollständig.")
        print(
            "Bitte prüfen Sie die Installationsanleitungen auf der Webseite der Software und führe die Installation erneut durch."
        )
        sys.exit(1)
