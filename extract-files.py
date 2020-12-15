#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/violet',
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
    'vendor/xiaomi/sm6150-common',
]

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib64/hw/camera.qcom.so',
        'vendor/lib64/libvidhance.so',
    ): blob_fixup()
        .add_needed('libcomparetf2_shim.so'),
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10080', '0')
        .regex_replace('0x1F', '0'),
    'vendor/lib64/libvendor.goodix.hardware.interfaces.biometrics.fingerprint@2.1.so': blob_fixup()
        .patchelf_version('0_8')
        .remove_needed('libhidlbase.so')
        .binary_regex_replace(b'libhidltransport.so', b'libhidlbase-v32.so\x00'),
}  # fmt: skip

module = ExtractUtilsModule(
    'violet',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sm6150-common', module.vendor)
    utils.run()
