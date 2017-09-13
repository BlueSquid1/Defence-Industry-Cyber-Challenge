# this script is used to read the CSV files and format the dataset in a way that is friendly to tensorflow

import numpy


class CSVReader:
    # columns in the dataset

    datetime_length = 0
    browser_language = 1
    device_id = 2
    device_first_seen_length = 3
    os = 4
    os_anomaly = 5
    ua_os = 6
    browser_language_anomaly = 7
    fuzzy_device_id = 8
    true_ip_geo = 9
    proxy_ip_geo = 10
    page_time_on = 11
    transaction_amount = 12
    frd = 13


    """
    # origional columns in the dataset (before cleanup)
    datetime = 0
    browser_language = 1
    device_id = 2
    device_first_seen = 3
    os = 4
    os_anomaly = 5
    ua_os = 6
    browser_language_anomaly = 7
    fuzzy_device_id = 8
    fuzzy_device_first_seen = 9
    true_ip = 10
    true_ip_geo = 11
    proxy_ip = 12
    proxy_ip_geo = 13
    page_time_on = 14
    transaction_amount = 15
    frd = 16
    """

    # mapping strings to numbers
    osDictionary = {
        'ANDROID': 1,
        'BLACKBERRY': 2,
        'IOS': 3,
        'WINDOWS': 4,
        'OS X': 5,
        'LINUX': 6,
        'WINDOWS MOBILE': 7,
        'OTHER': 8,
        'UNKNOWN': 0,
        '': 0,
    }

    browLanDictionary = {
        'ar-ae': 1,
        'bg': 2,
        'bg-BG': 3,
        'bn-IN': 4,
        'cs': 5,
        'cs-CZ': 6,
        'cy': 7,
        'da': 8,
        'da-dk': 9,
        'de': 10,
        'de-CH': 11,
        'de-DE': 12,
        'el': 13,
        'el-GR': 14,
        'en': 15,
        'en_US': 16,
        'en-150': 17,
        'en-AE': 18,
        'en-AU': 19,
        'en-ca': 20,
        'en-gb': 21,
        'en-ie': 22,
        'en-NZ': 23,
        'en-securid': 24,
        'en-sg': 25,
        'en-US': 26,
        'en-ZA': 27,
        'en-ZW': 28,
        'es': 29,
        'es-AR': 30,
        'es-ES': 31,
        'es-UY': 32,
        'fi-FI': 33,
        'fr': 34,
        'fr-CA': 35,
        'fr-FR': 36,
        'ga-ie': 37,
        'gd': 38,
        'hr-HR': 39,
        'hu': 40,
        'hu-HU': 41,
        'id': 42,
        'is-is': 43,
        'it-IT': 44,
        'ja': 45,
        'ja-jp': 46,
        'ko-KR': 47,
        'lt': 48,
        'lt-LT': 49,
        'lv': 50,
        'lv-LV': 51,
        'nb': 52,
        'nb-NO': 53,
        'nl': 54,
        'nl-NL': 55,
        'pl': 56,
        'pl-PL': 57,
        'pt-BR': 58,
        'pt-PT': 59,
        'ro': 60,
        'ro-ro': 61,
        'ru': 62,
        'ru-RU': 63,
        'sk-SK': 64,
        'sr-RS': 65,
        'sv-SE': 66,
        'th': 67,
        'th-TH': 68,
        'tr-tr': 69,
        'vi': 70,
        'vi-VN': 71,
        'zh-cn': 72,
        'zh-Hans-CN': 73,
        'zh-Hant-TW': 74,
        'zh-HK': 75,
        'zh-TW': 76,
        '': 0
    }

    uaDictionary = {
        'Android': 1,
        'Android 4.0.3': 2,
        'Android 4.4.3': 3,
        'Android 5.1.1': 4,
        'Android 6.0': 5,
        'Android 6.0.1': 6,
        'Android 7.0': 7,
        'BlackBerry 10.3.2.2876': 8,
        'Chrome OS': 9,
        'chromeos': 10,
        'ios': 11,
        'iOS 10.0.1': 12,
        'iOS 10.1.1': 13,
        'iOS 10.2': 14,
        'iOS 10.2.1': 15,
        'iOS 10.3': 16,
        'iOS 10.3.1': 17,
        'iOS 7.0.4': 18,
        'iOS 8.1': 19,
        'iOS 9.0.2': 20,
        'iOS 9.3.2': 21,
        'iOS 9.3.3': 22,
        'iOS 9.3.5': 23,
        'java': 24,
        'linux': 25,
        'Linux x86_64': 26,
        'Mac OS X': 27,
        'Mac OS X 10.10.0': 28,
        'Mac OS X 10.10.5': 29,
        'Mac OS X 10.11': 30,
        'Mac OS X 10.11.4': 31,
        'Mac OS X 10.11.6': 32,
        'Mac OS X 10.6.8': 33,
        'Mac OS X 10.7': 34,
        'Mac OS X 10.7.5': 35,
        'Mac OS X 10.9': 36,
        'Mac OS X 10.9.5': 37,
        'macOS 10.12': 38,
        'macOS 10.12.1': 39,
        'macOS 10.12.3': 40,
        'macOS 10.12.4': 41,
        'macOS 10.12.5': 42,
        'macosx': 43,
        'rim os': 44,
        'win10': 45,
        'win7': 46,
        'win8': 47,
        'win8.1': 48,
        'Windows': 49,
        'Windows 10': 50,
        'Windows 7': 51,
        'Windows 8.1': 52,
        'Windows Phone OS': 53,
        'Windows RT': 54,
        'Windows Vista': 55,
        'Windows XP': 56,
        'winphone10': 57,
        'winphone8.1': 58,
        'winrt8': 59,
        'winvista': 60,
        'winxp': 61,
        'Xbox OS': 62,
        '' : 0
    }

    csvTrainFilePath = ""
    csvTestFilePath = ""

    # constructor
    def __init__(self, mCsvTrainFilePath, mCsvTestFilePath):
        self.csvTrainFilePath = mCsvTrainFilePath
        self.csvTestFilePath = mCsvTestFilePath

    # returns the malious test cases
    def getTestingCases(self):
        return self.fileToFormattedList(self.csvTestFilePath)

    # returns the malious training cases
    def getTrainingCases(self):
        return self.fileToFormattedList(self.csvTrainFilePath)

    # returns a list containing all the entries in a CSV file
    def fileToFormattedList(self, mCsvFileName):
        formatedOutput = []
        formatedInput = []
        with open(mCsvFileName, "r") as file:
            print("reading from file " + str(mCsvFileName))

            # for each entry in the file
            lineCount = 0
            for line in file:
                # skip the header
                if lineCount == 0:
                    lineCount += 1
                    continue

                # might contain unwanted windows carradge returns "\n\r" or linux news lines "\n"
                line = line.replace('\r', '')
                line = line.replace('\n', '')

                entry = line.split(',')

                entryInput, entryOutput = self.formatEntryForTensorflow(entry)

                formatedInput.append(entryInput)
                formatedOutput.append(entryOutput)
                lineCount += 1
                if lineCount % 10000 == 0:
                    print("read: " + str(lineCount) + " lines")

            print("finished proccessing: " + str(lineCount) + " lines")

        return formatedInput, formatedOutput

    def formatEntryForTensorflow(self, entry):
        # as mentioned in the report number ranges were normalized to be between 0 and 1.
        # this is done by dividing each input by the max value see from the dataset.
        formatedInput = []
        formatedOutput = []

        # datetime_length
        maxDateTimeLength = 1489768105.0
        formatedInput.append(self.string2Float(entry[self.datetime_length]) / maxDateTimeLength)

        # browser_language
        maxBrowserLanguage = 76.0
        browLang = 0.0
        if entry[self.browser_language] in self.browLanDictionary:
            browLang = float(self.browLanDictionary[entry[self.browser_language]])

        formatedInput.append( browLang / maxBrowserLanguage)

        # device_id
        maxDeviceId = 268423845.0
        formatedInput.append(self.string2Float(entry[self.device_id]) / maxDeviceId)

        # device_first_seen_length
        maxDeviceFirstSeen = 1498176000.0
        formatedInput.append(self.string2Float(entry[self.device_first_seen_length]) / maxDeviceFirstSeen)

        # os
        osNum = 0
        if entry[self.os].upper() in self.osDictionary:
            osNum = self.osDictionary[entry[self.os].upper()]

        maxOs = 9
        formatedInput += self.oneHotEncoding(osNum, maxOs)

        # os_anomaly
        if entry[self.os_anomaly].upper() == "TRUE":
            formatedInput.append(1.0)
        else:
            formatedInput.append(-1.0)

        # ua_os
        maxUaOs = 62.0
        usOsNum = 0.0
        if entry[self.ua_os] in self.uaDictionary:
            usOsNum = float(self.uaDictionary[entry[self.ua_os]])
        formatedInput.append(usOsNum / maxUaOs)

        # browser_language_anomaly
        if entry[self.browser_language_anomaly].upper() == "TRUE":
            formatedInput.append(1.0)
        else:
            formatedInput.append(-1.0)

        # fuzzy_device_id
        maxFuzzyDeviceId = 268430955.0
        formatedInput.append(self.string2Float(entry[self.fuzzy_device_id]) / maxFuzzyDeviceId)

        # true_ip_geo
        maxIpGeo = self.convertToNumber("ZW")
        formatedInput.append(self.convertToNumber(entry[self.true_ip_geo]) / maxIpGeo)

        # proxy_ip_geo
        maxProxyIpGeo = self.convertToNumber("US")
        formatedInput.append(self.convertToNumber(entry[self.proxy_ip_geo]) / maxProxyIpGeo)

        # page_time_on
        maxPageTimeOn = 1073264.0
        formatedInput.append(self.string2Float(entry[self.page_time_on]) / maxPageTimeOn)

        # transaction_amount
        maxTransAmount = 20185.0
        formatedInput.append(self.string2Float(entry[self.transaction_amount]) / maxTransAmount)

        # frd
        isMalicious = 0
        if entry[self.frd] == "1":
            isMalicious = 1

        numOutputLabels = 2
        formatedOutput += self.oneHotEncoding(isMalicious, numOutputLabels)

        return formatedInput, formatedOutput

    # my super smart string to float converter
    def string2Float(self, inputString):
        if inputString == "" or inputString == None:
            return 0.0

        return float(inputString)

    def oneHotEncoding(self, num, maxNum):
        if num < 0 or num >= maxNum:
            print("failed to generate onehot encoding")
            return

        # create list of output size
        retList = [0.0] * maxNum

        # put a 1 at the correct output
        retList[num] = 1
        return retList

    # need a way to convert a string to a number. Do it based on the bytes that make up the string
    def convertToNumber(self, stringValue):
        return int.from_bytes(stringValue.encode(), byteorder='big', signed=False)