#! /usr/bin/python3
import logging
from ctypes import c_short, c_char, c_byte, c_int, c_void_p, c_bool, Structure, Union, byref, CDLL, create_string_buffer
from ctypes.util import find_library
from enum import Enum, auto

logger = logging.getLogger('mc-magewell-signal')


class MW_RESULT(Enum):
    MW_SUCCEEDED = 0x00
    MW_FAILED = auto()
    MW_ENODATA = auto()
    MW_INVALID_PARAMS = auto()


class MWCAP_VIDEO_SIGNAL_STATE(Enum):
    MWCAP_VIDEO_SIGNAL_NONE = 0x00           # No signal detectd
    MWCAP_VIDEO_SIGNAL_UNSUPPORTED = auto()  # Video signal status not valid
    MWCAP_VIDEO_SIGNAL_LOCKING = auto()      # Video signal status valid but not locked yet
    MWCAP_VIDEO_SIGNAL_LOCKED = auto()       # Every thing OK


class MWCAP_VIDEO_FRAME_TYPE(Enum):
    MWCAP_VIDEO_FRAME_2D = 0x00
    MWCAP_VIDEO_FRAME_3D_TOP_AND_BOTTOM_FULL = 0x01
    MWCAP_VIDEO_FRAME_3D_TOP_AND_BOTTOM_HALF = 0x02
    MWCAP_VIDEO_FRAME_3D_SIDE_BY_SIDE_FULL = 0x03
    MWCAP_VIDEO_FRAME_3D_SIDE_BY_SIDE_HALF = 0x04


class MWCAP_VIDEO_COLOR_FORMAT(Enum):
    MWCAP_VIDEO_COLOR_FORMAT_UNKNOWN = 0x00
    MWCAP_VIDEO_COLOR_FORMAT_RGB = 0x01
    MWCAP_VIDEO_COLOR_FORMAT_YUV601 = 0x02
    MWCAP_VIDEO_COLOR_FORMAT_YUV709 = 0x03
    MWCAP_VIDEO_COLOR_FORMAT_YUV2020 = 0x04
    MWCAP_VIDEO_COLOR_FORMAT_YUV2020C = 0x05  # Constant luminance not supported yet.


class MWCAP_VIDEO_QUANTIZATION_RANGE(Enum):
    MWCAP_VIDEO_QUANTIZATION_UNKNOWN = 0x00
    MWCAP_VIDEO_QUANTIZATION_FULL = 0x01     # Black level: 0 White level: 255/1023/4095/65535
    MWCAP_VIDEO_QUANTIZATION_LIMITED = 0x02  # Black level: 16/64/256/4096 White level: 235(240)/940(960)/3760(3840)/60160(61440)


class MWCAP_VIDEO_SATURATION_RANGE(Enum):
    MWCAP_VIDEO_SATURATION_UNKNOWN = 0x00
    MWCAP_VIDEO_SATURATION_FULL = 0x01            # Min: 0 Max: 255/1023/4095/65535
    MWCAP_VIDEO_SATURATION_LIMITED = 0x02         # Min: 16/64/256/4096 Max: 235(240)/940(960)/3760(3840)/60160(61440)
    MWCAP_VIDEO_SATURATION_EXTENDED_GAMUT = 0x03  # Min: 1/4/16/256 Max: 254/1019/4079/65279


class MWCAP_VIDEO_SIGNAL_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('state', c_int),             # MWCAP_VIDEO_SIGNAL_STATE
                ('x', c_int),
                ('y', c_int),
                ('cx', c_int),
                ('cy', c_int),
                ('cxTotal', c_int),
                ('cyTotal', c_int),
                ('bInterlaced', c_bool),
                ('dwFrameDuration', c_int),
                ('nAspectX', c_int),
                ('nAspectY', c_int),
                ('bSegmentedFrame', c_bool),
                ('frameType', c_int),         # MWCAP_VIDEO_FRAME_TYPE
                ('colorFormat', c_int),       # MWCAP_VIDEO_COLOR_FORMAT
                ('quantRange', c_int),        # MWCAP_VIDEO_QUANTIZATION_RANGE
                ('satRange', c_int),          # MWCAP_VIDEO_SATURATION_RANGE
                ]


class MWCAP_CHANNEL_INFO(Structure):
    MW_SERIAL_NO_LEN = 16
    MW_FAMILY_NAME_LEN = 64
    MW_PRODUCT_NAME_LEN = 64
    MW_FIRMWARE_NAME_LEN = 64

    _pack_ = 1
    _fields_ = [('wFamilyID', c_short),
                ('wProductID', c_short),
                ('chHardwareVersion', c_char),
                ('byFirmwareID', c_byte),
                ('dwFirmwareVersion', c_int),
                ('dwDriverVersion', c_int),
                ('szFamilyName', c_char * MW_FAMILY_NAME_LEN),
                ('szProductName', c_char * MW_PRODUCT_NAME_LEN),
                ('szFirmwareName', c_char * MW_FIRMWARE_NAME_LEN),
                ('szBoardSerialNo', c_char * MW_SERIAL_NO_LEN),
                ('byBoardIndex', c_byte),
                ('byChannelIndex', c_byte),
                ]


class SDI_TYPE(Enum):
    SDI_TYPE_SD = 0x00
    SDI_TYPE_HD = auto()
    SDI_TYPE_3GA = auto()
    SDI_TYPE_3GB_DL = auto()
    SDI_TYPE_3GB_DS = auto()
    SDI_TYPE_DL_CH1 = auto()
    SDI_TYPE_DL_CH2 = auto()
    SDI_TYPE_6G_MODE1 = auto()
    SDI_TYPE_6G_MODE = auto()


class SDI_SCANNING_FORMAT(Enum):
    SDI_SCANING_INTERLACED = 0
    SDI_SCANING_SEGMENTED_FRAME = 1
    SDI_SCANING_PROGRESSIVE = 3


class SDI_BIT_DEPTH(Enum):
    SDI_BIT_DEPTH_8BIT = 0
    SDI_BIT_DEPTH_10BIT = 1
    SDI_BIT_DEPTH_12BIT = 2


class SDI_SAMPLING_STRUCT(Enum):
    SDI_SAMPLING_422_YCbCr = 0x00
    SDI_SAMPLING_444_YCbCr = 0x01
    SDI_SAMPLING_444_RGB = 0x02
    SDI_SAMPLING_420_YCbCr = 0x03
    SDI_SAMPLING_4224_YCbCrA = 0x04
    SDI_SAMPLING_4444_YCbCrA = 0x05
    SDI_SAMPLING_4444_RGBA = 0x06
    SDI_SAMPLING_4224_YCbCrD = 0x08
    SDI_SAMPLING_4444_YCbCrD = 0x09
    SDI_SAMPLING_4444_RGBD = 0x0A
    SDI_SAMPLING_444_XYZ = 0x0E


class MWCAP_SDI_SPECIFIC_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('sdiType', c_int),            # SDI_TYPE
                ('sdiScanningFormat', c_int),  # SDI_SCANNING_FORMAT
                ('sdiBitDepth', c_int),        # SDI_BIT_DEPTH
                ('sdiSamplingStruct', c_int),  # SDI_SAMPLING_STRUCT
                ('bST352DataValid', c_bool),
                ('dwST352Data', c_int),
                ]


class HDMI_PIXEL_ENCODING(Enum):
    HDMI_ENCODING_RGB_444 = 0
    HDMI_ENCODING_YUV_422 = 1
    HDMI_ENCODING_YUV_444 = 2
    HDMI_ENCODING_YUV_420 = 3


class MWCAP_HDMI_VIDEO_TIMING(Structure):
    _pack_ = 1
    _fields_ = [('bInterlaced', c_bool),
                ('dwFrameDuration', c_int),
                ('wHSyncWidth', c_short),
                ('wHFrontPorch', c_short),
                ('wHBackPorch', c_short),
                ('wHActive', c_short),
                ('wHTotalWidth', c_short),
                ('wField0VSyncWidth', c_short),
                ('wField0VFrontPorch', c_short),
                ('wField0VBackPorch', c_short),
                ('wField0VActive', c_short),
                ('wField0VTotalHeight', c_short),
                ('wField1VSyncWidth', c_short),
                ('wField1VFrontPorch', c_short),
                ('wField1VBackPorch', c_short),
                ('wField1VActive', c_short),
                ('wField1VTotalHeight', c_short),
                ]


class MWCAP_HDMI_SPECIFIC_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('bHDMIMode', c_bool),
                ('bHDCP', c_bool),
                ('byBitDepth', c_byte),
                ('pixelEncoding', c_int),  # HDMI_PIXEL_ENCODING
                ('byVIC', c_byte),
                ('bITContent', c_bool),
                ('b3DFormat', c_bool),
                ('by3DStructure', c_byte),
                ('bySideBySideHalfSubSampling', c_byte),
                ('videoTiming', MWCAP_HDMI_VIDEO_TIMING),
                ]


class MWCAP_VIDEO_SYNC_INFO(Structure):
    _pack_ = 1
    _fields_ = [('bySyncType', c_byte),
                ('bHSPolarity', c_bool),
                ('bVSPolarity', c_bool),
                ('bInterlaced', c_bool),
                ('dwFrameDuration', c_int),
                ('wVSyncLineCount', c_short),
                ('wFrameLineCount', c_short),
                ]


class MWCAP_VIDEO_TIMING(Structure):
    _pack_ = 1
    _fields_ = [('dwType', c_int),
                ('dwPixelClock', c_int),
                ('bInterlaced', c_bool),
                ('bySyncType', c_byte),
                ('bHSPolarity', c_bool),
                ('bVSPolarity', c_bool),
                ('wHActive', c_short),
                ('wHFrontPorch', c_short),
                ('wHSyncWidth', c_short),
                ('wHBackPorch', c_short),
                ('wVActive', c_short),
                ('wVFrontPorch', c_short),
                ('wVSyncWidth', c_short),
                ('wVBackPorch', c_short),
                ]


class MWCAP_VIDEO_TIMING_SETTINGS(Structure):
    _pack_ = 1
    _fields_ = [('wAspectX', c_short),
                ('wAspectY', c_short),
                ('x', c_short),
                ('y', c_short),
                ('cx', c_short),
                ('cy', c_short),
                ('cxTotal', c_short),
                ('byClampPos', c_byte),
                ]


class MWCAP_COMPONENT_SPECIFIC_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('syncInfo', MWCAP_VIDEO_SYNC_INFO),
                ('bTriLevelSync', c_bool),
                ('videoTiming', MWCAP_VIDEO_TIMING),  # Not valid for custom video timing
                ('videoTimingSettings', MWCAP_VIDEO_TIMING_SETTINGS),
                ]


class MWCAP_SD_VIDEO_STANDARD(Enum):
    MWCAP_SD_VIDEO_NONE = 0x00
    MWCAP_SD_VIDEO_NTSC_M = auto()
    MWCAP_SD_VIDEO_NTSC_433 = auto()
    MWCAP_SD_VIDEO_PAL_M = auto()
    MWCAP_SD_VIDEO_PAL_60 = auto()
    MWCAP_SD_VIDEO_PAL_COMBN = auto()
    MWCAP_SD_VIDEO_PAL_BGHID = auto()
    MWCAP_SD_VIDEO_SECAM = auto()
    MWCAP_SD_VIDEO_SECAM_60 = auto()


class MWCAP_CVBS_YC_SPECIFIC_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('standard', c_int),  # MWCAP_SD_VIDEO_STANDARD
                ('b50Hz', c_bool),
                ]


class MWCAP_SPECIFIC_UNION(Union):
    _pack_ = 1
    _fields_ = [('sdiStatus', MWCAP_SDI_SPECIFIC_STATUS),
                ('hdmiStatus', MWCAP_HDMI_SPECIFIC_STATUS),
                ('vgaComponentStatus', MWCAP_COMPONENT_SPECIFIC_STATUS),
                ('cvbsYcStatus', MWCAP_CVBS_YC_SPECIFIC_STATUS),
                ]


class MWCAP_INPUT_SPECIFIC_STATUS(Structure):
    _pack_ = 1
    _fields_ = [('bValid', c_bool),
                ('dwVideoInputType', c_int),
                ('status', MWCAP_SPECIFIC_UNION),
                ]


class MWCapture():
    LIBMWCAPTURE_NAME = 'MWCapture'
    FILTER_FAMILY_NAME = b'USB Capture'
    FILTER_PRODUCT_NAME = b'Seneca USB Capture HDMI'

    def __init__(self):
        self._libMWCapture = None
        self._h_channel = None
        self._info = MWCAP_CHANNEL_INFO()
        self._signal_status = MWCAP_VIDEO_SIGNAL_STATUS()
        self._input_status = MWCAP_INPUT_SPECIFIC_STATUS()

    def start(self):
        if not self._libMWCapture:
            libmwcapture_so_name = find_library(self.LIBMWCAPTURE_NAME)
            if libmwcapture_so_name:
                try:
                    libMWCapture = CDLL(libmwcapture_so_name)
                except Exception:
                    libMWCapture = None
                if libMWCapture:
                    self._libMWCapture = libMWCapture
                    self._libMWCapture.MWOpenChannelByPath.restype = c_void_p
                    self._libMWCapture.MWGetChannelInfo.argtypes = [c_void_p, c_void_p]
                    self._libMWCapture.MWGetVideoSignalStatus.argtypes = [c_void_p, c_void_p]
                    self._libMWCapture.MWGetInputSpecificStatus.argtypes = [c_void_p, c_void_p]
                    self._libMWCapture.MWCloseChannel.argtypes = [c_void_p]
                    if not self._libMWCapture.MWCaptureInitInstance():
                        self._libMWCapture = None
                        logger.error('MWCaptureInitInstance failed')
                else:
                    logger.error(f'{self.LIBMWCAPTURE_NAME} load failed')
            else:
                logger.error(f'{self.LIBMWCAPTURE_NAME} find failed')

    def stop(self):
        if self._libMWCapture:
            self._libMWCapture.MWCaptureExitInstance()
            self._libMWCapture = None

    def _format_locked_signal(self, info, signal_status, input_status):
        result = ""
        hdmi_dvi = 'HDMI' if input_status.status.hdmiStatus.bHDMIMode else 'DVI'
        hdpc = ' (HDCP)' if input_status.status.hdmiStatus.bHDCP else ''

        fps = None
        interlaced = None
        if signal_status.bInterlaced:
            fps = 10000000 / (signal_status.dwFrameDuration / 2)
            interlaced = 'i'
        else:
            fps = 10000000 / signal_status.dwFrameDuration
            interlaced = 'p'

        colorspace = None
        if signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_UNKNOWN.value:
            colorspace = 'UNKNOWN_COLORSPACE'
        elif signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_RGB.value:
            colorspace = 'RGB'
        elif signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_YUV601.value \
                or signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_YUV709.value \
                or signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_YUV2020.value \
                or signal_status.colorFormat == MWCAP_VIDEO_COLOR_FORMAT.MWCAP_VIDEO_COLOR_FORMAT_YUV2020C.value:
            colorspace = 'YUV'

        result = f'{info.szBoardSerialNo.decode()} {hdmi_dvi}{hdpc} {signal_status.cx}x{signal_status.cy}{interlaced} {fps:.2f} Hz {colorspace}\n'

        return result

    def get_locked_signal(self):
        result = ""
        if self._libMWCapture:
            self._libMWCapture.MWRefreshDevice()
            channel_count = self._libMWCapture.MWGetChannelCount()
            dev_channels = []

            for i in range(channel_count):
                self._libMWCapture.MWGetChannelInfoByIndex(i, byref(self._info))
                if self._info.szFamilyName != self.FILTER_FAMILY_NAME:
                    continue
                if self._info.szProductName != self.FILTER_PRODUCT_NAME:
                    continue
                dev_channels.append(i)

            if not dev_channels:
                logger.error('cannot find usb channels')

            for dev_channel in dev_channels:
                if self._libMWCapture.MWGetChannelInfoByIndex(dev_channel, byref(self._info)) != MW_RESULT.MW_SUCCEEDED.value:
                    logger.error('cannot get channel info')
                    continue

                path = create_string_buffer(b'\0', 128)
                self._libMWCapture.MWGetDevicePath(dev_channel, path)

                self._h_channel = self._libMWCapture.MWOpenChannelByPath(path)

                if self._h_channel:
                    if self._libMWCapture.MWGetChannelInfo(self._h_channel, byref(self._info)) == MW_RESULT.MW_SUCCEEDED.value:
                        self._libMWCapture.MWGetVideoSignalStatus(self._h_channel, byref(self._signal_status))
                        if self._signal_status.state == MWCAP_VIDEO_SIGNAL_STATE.MWCAP_VIDEO_SIGNAL_NONE.value \
                           or self._signal_status.state == MWCAP_VIDEO_SIGNAL_STATE.MWCAP_VIDEO_SIGNAL_UNSUPPORTED.value \
                           or self._signal_status.state == MWCAP_VIDEO_SIGNAL_STATE.MWCAP_VIDEO_SIGNAL_LOCKING.value:
                            result += f'{self._info.szBoardSerialNo.decode()} No signal\n'
                        elif self._signal_status.state == MWCAP_VIDEO_SIGNAL_STATE.MWCAP_VIDEO_SIGNAL_LOCKED.value:
                            self._libMWCapture.MWGetInputSpecificStatus(self._h_channel, byref(self._input_status))
                            result += self._format_locked_signal(self._info, self._signal_status, self._input_status)
                    else:
                        logger.error('cannot get channel info')
                    self._libMWCapture.MWCloseChannel(self._h_channel)
                    self._h_channel = None
                else:
                    logger.error('cannot open channel')
        return result
