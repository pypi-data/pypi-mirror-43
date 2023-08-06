import re
import logging
import json
from typing import Dict


class Log:
    __logger = logging.getLogger(__name__)

    @classmethod
    def warn(cls, message: str):
        Log.__logger.warning(message)


class AnalyzerHelpers:
    # Constants

    SWIFT_FILE_EXTENSION = '.swift'

    APPLE_FRAMEWORKS = [
        'AGL',
        'AppKit',
        'ARKit',
        'AVFoundation',
        'AVKit',
        'Accelerate',
        'Accounts',
        'AdSupport',
        'AddressBook',
        'AddressBookUI',
        'ApplicationServices',
        'AssetsLibrary',
        'AudioToolbox',
        'AudioUnit',
        'AuthenticationServices',
        'BusinessChat',
        'CFNetwork',
        'CallKit',
        'CarPlay',
        'ClassKit',
        'ClockKit',
        'CloudKit',
        'Collaboration',
        'ColorSync',
        'Compression',
        'Contacts',
        'ContactsUI',
        'CoreAnimation',
        'CoreAudio',
        'CoreAudioKit',
        'CoreBluetooth',
        'CoreData',
        'CoreFoundation',
        'CoreGraphics',
        'CoreImage',
        'CoreLocation',
        'CoreMIDI',
        'CoreML',
        'CoreMedia',
        'CoreMotion',
        'CoreNFC',
        'CoreServices',
        'CoreSpotlight',
        'CoreTelephony',
        'CoreText',
        'CoreVideo',
        'CoreWLAN',
        'CreateML',
        'CryptoTokenKit',
        'DarwinNotify',
        'DeviceCheck',
        'DiskArbitration',
        'Dispatch',
        'EventKit',
        'EventKitUI',
        'ExceptionHandling',
        'ExternalAccessory',
        'FWAUserLib',
        'FileProvider',
        'FileProviderUI',
        'FinderSync',
        'ForceFeedback',
        'Foundation',
        'FxPlug',
        'GLKit',
        'GSS',
        'GameController',
        'GameKit',
        'GameplayKit',
        'HTTPLiveStreaming',
        'HealthKit',
        'HomeKit',
        'Hypervisor',
        'IOBluetooth',
        'IOBluetoothUI',
        'IOKit',
        'IOSurface',
        'InputMethodKit',
        'JavaScriptCore',
        'Kernel',
        'LatentSemanticMapping',
        'LocalAuthentication',
        'MapKit',
        'MediaAccessibility',
        'MediaLibrary',
        'MediaPlayer',
        'MessageUI',
        'Messages',
        'MetalKit',
        'MobileCoreServices',
        'MultipeerConnectivity',
        'NaturalLanguage',
        'Network',
        'NetworkExtension',
        'NewsstandKit',
        'NotificationCenter',
        'ObjectiveC',
        'OpenDirectory',
        'OpenGL',
        'PDFKit',
        'PassKit',
        'PhotoKit',
        'PushKit',
        'QTKit',
        'QuartzCore',
        'QuickLook',
        'ReplayKit',
        'SMS',
        'SafariServices',
        'SceneKit',
        'ScreenSaver',
        'Security',
        'SecurityFoundation',
        'SecurityInterface',
        'ServiceManagement',
        'SiriKit',
        'Social',
        'Speech',
        'SpriteKit',
        'StoreKit',
        'SystemConfiguration',
        'TVML',
        'TVMLKit JS',
        'TVMLKit',
        'TVServices',
        'TVUIKit',
        'UIKit',
        'UserNotifications',
        'UserNotificationsUI',
        'VideoToolbox',
        'Vision',
        'WatchConnectivity',
        'WatchKit',
        'WebKit',
        'XPC',
        'XCTest',
        'dnssd',
        'iAd',
        'iTunesLibrary',
        'os',
        'simd',
        'vmnet'
    ]

    @staticmethod
    def is_path_in_list(subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False


class ParsingHelpers:
    # Constants

    DEFAULT_FRAMEWORK_NAME = 'AppTarget'
    DEFAULT_TEST_FRAMEWORK_SUFFIX = '_Test'
    TEST_METHOD_PREFIX = 'test'
    FRAMEWORK_STRUCTURE_OVERRIDE_FILE = 'scm.json'

    # Constants - Regex patterns

    BEGIN_COMMENT = '^//*'
    END_COMMENT = '\*/$'
    SINGLE_COMMENT = '^//'

    IMPORTS = '(?<=^import )(?:\\b\w+\s|)([^.; ]+)'

    PROTOCOLS = '.*protocol (.*?)[:|{|\s]'
    STRUCTS = '.*struct (.*?)[:|{|\s]'
    CLASSES = '.*class (.*?)[:|{|\s]'
    FUNCS = '.*func (.*?)[:|\(|\s]'

    # Static helpers

    @staticmethod
    def check_existence(regex_pattern, trimmed_string):
        regex = re.compile(regex_pattern)
        if re.search(regex, trimmed_string.strip()) is not None:
            return True
        else:
            return False

    @staticmethod
    def extract_substring_with_pattern(regex_pattern, trimmed_string):
        try:
            return re.search(regex_pattern, trimmed_string).group(1)
        except AttributeError:
            return ''


class ReportingHelpers:

    @staticmethod
    def decimal_format(number, decimal_places=3):
        format_string = "{:." + str(decimal_places) + "f}"
        return float(format_string.format(number))


class JSONReader:

    @staticmethod
    def read_json_file(path: str) -> Dict:
        with open(path, 'r') as fp:
            return json.load(fp)
