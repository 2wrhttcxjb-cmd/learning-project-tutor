#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/release.sh <output-dir> [version]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_DIR="$1"
VERSION="${2:-$(cat "${REPO_DIR}/VERSION")}"

mkdir -p "${OUTPUT_DIR}"

(
  cd "${REPO_DIR}"
  zip -qr "${OUTPUT_DIR}/learning-project-tutor-${VERSION}.zip" "skill"
  zip -qr "${OUTPUT_DIR}/learning-project-starter-workspace-${VERSION}.zip" "starter-workspace"
)

echo "${OUTPUT_DIR}/learning-project-tutor-${VERSION}.zip"
echo "${OUTPUT_DIR}/learning-project-starter-workspace-${VERSION}.zip"
