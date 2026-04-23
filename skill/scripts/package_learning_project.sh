#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/package_learning_project.sh <output-dir> [version]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PACKAGES_DIR="$(cd "${SKILL_DIR}/.." && pwd)"
STARTER_DIR="${PACKAGES_DIR}/learning-project-starter-workspace"
OUTPUT_DIR="$1"
VERSION="${2:-$(date +%Y%m%d)}"

mkdir -p "${OUTPUT_DIR}"

SKILL_ARCHIVE="${OUTPUT_DIR}/learning-project-tutor-${VERSION}.zip"
STARTER_ARCHIVE="${OUTPUT_DIR}/learning-project-starter-workspace-${VERSION}.zip"

(
  cd "${PACKAGES_DIR}"
  zip -qr "${SKILL_ARCHIVE}" "learning-project-tutor"
  zip -qr "${STARTER_ARCHIVE}" "learning-project-starter-workspace"
)

echo "${SKILL_ARCHIVE}"
echo "${STARTER_ARCHIVE}"
