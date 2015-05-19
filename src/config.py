#
# space_weather configuration file
#

PROGRAM_DISABLED = False

####

NOAA_FTP_ADDRESS = 'ftp.sec.noaa.gov'
NOAA_ACE_DIR = '/pub/lists/ace'
NOAA_XRAY_DIR = '/pub/lists/xray'
NOAA_GEOMAG_DIR = '/pub/lists/geomag'

####

PROTON_FLUX_FILE_SUFFIX = '_ace_sis_5m.txt'
PROTON_FLUX_OUT_FILE = 'proton_flux.png'

XRAY_FILE_SUFFIX = '_Gs_xr_5m.txt'
XRAY_OUT_FILE = 'xray.png'

GEOMAG_FILE = 'AK.txt'
GEOMAG_WEEKLY_FILE = '7day_AK.txt'
GEOMAG_OUT_FILE = 'geomag.png'

####

FILES_WORK_DIR = '/tmp/space_weather'

####

PLOT_XTICKS_ROTATION = 55
PLOT_DPI = 85

####

UPLOAD_FTP_ADDRESS = 'astrotourist.info'
UPLOAD_FTP_LOGIN = 'user'
UPLOAD_FTP_PASSWORD = 'password'
UPLOAD_FTP_DIR = '/'

