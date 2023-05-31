#!/bin/bash
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2020 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

set -e

export DEVICE=violet
export DEVICE_COMMON=sm6150-common
export VENDOR=xiaomi

export DEVICE_BRINGUP_YEAR=2020

# Load extract_utils and do some sanity checks
MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

function blob_fixup() {
    case "${1}" in
    vendor/lib64/hw/camera.qcom.so)
            sed -i "s|libc++.so|libc29.so|g" "${2}"
            ;;
    vendor/etc/camera/camxoverridesettings.txt )
        sed -i "s|0x10080|0|g" "${2}"
        sed -i "s|0x1F|0x0|g" "${2}"
    ;;
    vendor/lib64/libvendor.goodix.hardware.interfaces.biometrics.fingerprint@2.1.so)
        "${PATCHELF_0_8}" --remove-needed "libhidlbase.so" "${2}"
        sed -i "s/libhidltransport.so/libhidlbase-v32.so\x00/" "${2}"
    ;;
    esac
}

# If we're being sourced by the common script that we called,
# stop right here. No need to go down the rabbit hole.
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return
fi

"./../../${VENDOR}/${DEVICE_COMMON}/extract-files.sh" "$@"
