#!/usr/bin/env python3

DEVELOPER = 'developer'
TRANSLATOR = 'translator'

class Logger(object):
    def __init__(self, categories):
        self.categories = set(categories)

    def error(self, code, lines):
        from sys import stderr
        from sys import exit

        if type(lines) is str:
            print(lines, file=stderr)
        else:
            for line in lines:
                print(line, file=stderr)

        exit(code)

    def warning(self, category, lines):
        if category in self.categories:
            from sys import stderr

            if type(lines) is str:
                print(lines, file=stderr)
            else:
                for line in lines:
                    print(line, file=stderr)


class TextValidator(object):
    def __init__(self, logger):
        from collections import namedtuple

        CultureScripts = namedtuple('CultureScripts', ('primary', 'allowed'))

        self.logger = logger
        self.culture_ranges = {
            'en-Latn-US': CultureScripts(
                set(['Basic Latin']),
                set(['Basic Latin'])),
            'ru-Cyrl-RU': CultureScripts(
                set(['Cyrillic']),
                set(['Cyrillic', 'Basic Latin'])),
            'ka-Geor-GE': CultureScripts(
                set(['Georgian']),
                set(['Georgian', 'Basic Latin'])),
            'uz-Latn-UZ': CultureScripts(
                set(['Basic Latin', 'Spacing Modifier Letters']),
                set(['Basic Latin', 'Spacing Modifier Letters']))
        }

    def get_symbol_range(self, symbol):
        symbol = ord(symbol)

        if 0x000000 <= symbol <= 0x00007F: return 'Basic Latin'
        if 0x000080 <= symbol <= 0x0000FF: return 'C1 Controls and Latin-1 Supplement'
        if 0x000100 <= symbol <= 0x00017F: return 'Latin Extended-A'
        if 0x000180 <= symbol <= 0x00024F: return 'Latin Extended-B'
        if 0x000250 <= symbol <= 0x0002AF: return 'IPA Extensions'
        if 0x0002B0 <= symbol <= 0x0002FF: return 'Spacing Modifier Letters'
        if 0x000300 <= symbol <= 0x00036F: return 'Combining Diacritical Marks'
        if 0x000370 <= symbol <= 0x0003FF: return 'Greek/Coptic'
        if 0x000400 <= symbol <= 0x0004FF: return 'Cyrillic'
        if 0x000500 <= symbol <= 0x00052F: return 'Cyrillic Supplement'
        if 0x000530 <= symbol <= 0x00058F: return 'Armenian'
        if 0x000590 <= symbol <= 0x0005FF: return 'Hebrew'
        if 0x000600 <= symbol <= 0x0006FF: return 'Arabic'
        if 0x000700 <= symbol <= 0x00074F: return 'Syriac'
        # if 0x000750 <= symbol <= 0x00077F: return 'Undefined'
        if 0x000780 <= symbol <= 0x0007BF: return 'Thaana'
        # if 0x0007C0 <= symbol <= 0x0008FF: return 'Undefined'
        if 0x000900 <= symbol <= 0x00097F: return 'Devanagari'
        if 0x000980 <= symbol <= 0x0009FF: return 'Bengali/Assamese'
        if 0x000A00 <= symbol <= 0x000A7F: return 'Gurmukhi'
        if 0x000A80 <= symbol <= 0x000AFF: return 'Gujarati'
        if 0x000B00 <= symbol <= 0x000B7F: return 'Oriya'
        if 0x000B80 <= symbol <= 0x000BFF: return 'Tamil'
        if 0x000C00 <= symbol <= 0x000C7F: return 'Telugu'
        if 0x000C80 <= symbol <= 0x000CFF: return 'Kannada'
        if 0x000D00 <= symbol <= 0x000DFF: return 'Malayalam'
        if 0x000D80 <= symbol <= 0x000DFF: return 'Sinhala'
        if 0x000E00 <= symbol <= 0x000E7F: return 'Thai'
        if 0x000E80 <= symbol <= 0x000EFF: return 'Lao'
        if 0x000F00 <= symbol <= 0x000FFF: return 'Tibetan'
        if 0x001000 <= symbol <= 0x00109F: return 'Myanmar'
        if 0x0010A0 <= symbol <= 0x0010FF: return 'Georgian'
        if 0x001100 <= symbol <= 0x0011FF: return 'Hangul Jamo'
        if 0x001200 <= symbol <= 0x00137F: return 'Ethiopic'
        # if 0x001380 <= symbol <= 0x00139F: return 'Undefined'
        if 0x0013A0 <= symbol <= 0x0013FF: return 'Cherokee'
        if 0x001400 <= symbol <= 0x00167F: return 'Unified Canadian Aboriginal Syllabics'
        if 0x001680 <= symbol <= 0x00169F: return 'Ogham'
        if 0x0016A0 <= symbol <= 0x0016FF: return 'Runic'
        if 0x001700 <= symbol <= 0x00171F: return 'Tagalog'
        if 0x001720 <= symbol <= 0x00173F: return 'Hanunoo'
        if 0x001740 <= symbol <= 0x00175F: return 'Buhid'
        if 0x001760 <= symbol <= 0x00177F: return 'Tagbanwa'
        if 0x001780 <= symbol <= 0x0017FF: return 'Khmer'
        if 0x001800 <= symbol <= 0x0018AF: return 'Mongolian'
        # if 0x0018B0 <= symbol <= 0x0018FF: return 'Undefined'
        if 0x001900 <= symbol <= 0x00194F: return 'Limbu'
        if 0x001950 <= symbol <= 0x00197F: return 'Tai Le'
        # if 0x001980 <= symbol <= 0x0019DF: return 'Undefined'
        if 0x0019E0 <= symbol <= 0x0019FF: return 'Khmer Symbols'
        # if 0x001A00 <= symbol <= 0x001CFF: return 'Undefined'
        if 0x001D00 <= symbol <= 0x001D7F: return 'Phonetic Extensions'
        # if 0x001D80 <= symbol <= 0x001DFF: return 'Undefined'
        if 0x001E00 <= symbol <= 0x001EFF: return 'Latin Extended Additional'
        if 0x001F00 <= symbol <= 0x001FFF: return 'Greek Extended'
        if 0x002000 <= symbol <= 0x00206F: return 'General Punctuation'
        if 0x002070 <= symbol <= 0x00209F: return 'Superscripts and Subscripts'
        if 0x0020A0 <= symbol <= 0x0020CF: return 'Currency Symbols'
        if 0x0020D0 <= symbol <= 0x0020FF: return 'Combining Diacritical Marks for Symbols'
        if 0x002100 <= symbol <= 0x00214F: return 'Letterlike Symbols'
        if 0x002150 <= symbol <= 0x00218F: return 'Number Forms'
        if 0x002190 <= symbol <= 0x0021FF: return 'Arrows'
        if 0x002200 <= symbol <= 0x0022FF: return 'Mathematical Operators'
        if 0x002300 <= symbol <= 0x0023FF: return 'Miscellaneous Technical'
        if 0x002400 <= symbol <= 0x00243F: return 'Control Pictures'
        if 0x002440 <= symbol <= 0x00245F: return 'Optical Character Recognition'
        if 0x002460 <= symbol <= 0x0024FF: return 'Enclosed Alphanumerics'
        if 0x002500 <= symbol <= 0x00257F: return 'Box Drawing'
        if 0x002580 <= symbol <= 0x00259F: return 'Block Elements'
        if 0x0025A0 <= symbol <= 0x0025FF: return 'Geometric Shapes'
        if 0x002600 <= symbol <= 0x0026FF: return 'Miscellaneous Symbols'
        if 0x002700 <= symbol <= 0x0027BF: return 'Dingbats'
        if 0x0027C0 <= symbol <= 0x0027EF: return 'Miscellaneous Mathematical Symbols-A'
        if 0x0027F0 <= symbol <= 0x0027FF: return 'Supplemental Arrows-A'
        if 0x002800 <= symbol <= 0x0028FF: return 'Braille Patterns'
        if 0x002900 <= symbol <= 0x00297F: return 'Supplemental Arrows-B'
        if 0x002980 <= symbol <= 0x0029FF: return 'Miscellaneous Mathematical Symbols-B'
        if 0x002A00 <= symbol <= 0x002AFF: return 'Supplemental Mathematical Operators'
        if 0x002B00 <= symbol <= 0x002BFF: return 'Miscellaneous Symbols and Arrows'
        # if 0x002C00 <= symbol <= 0x002E7F: return 'Undefined'
        if 0x002E80 <= symbol <= 0x002EFF: return 'CJK Radicals Supplement'
        if 0x002F00 <= symbol <= 0x002FDF: return 'Kangxi Radicals'
        # if 0x002FE0 <= symbol <= 0x002FEF: return 'Undefined'
        if 0x002FF0 <= symbol <= 0x002FFF: return 'Ideographic Description Characters'
        if 0x003000 <= symbol <= 0x00303F: return 'CJK Symbols and Punctuation'
        if 0x003040 <= symbol <= 0x00309F: return 'Hiragana'
        if 0x0030A0 <= symbol <= 0x0030FF: return 'Katakana'
        if 0x003100 <= symbol <= 0x00312F: return 'Bopomofo'
        if 0x003130 <= symbol <= 0x00318F: return 'Hangul Compatibility Jamo'
        if 0x003190 <= symbol <= 0x00319F: return 'Kanbun (Kunten)'
        if 0x0031A0 <= symbol <= 0x0031BF: return 'Bopomofo Extended'
        # if 0x0031C0 <= symbol <= 0x0031EF: return 'Undefined'
        if 0x0031F0 <= symbol <= 0x0031FF: return 'Katakana Phonetic Extensions'
        if 0x003200 <= symbol <= 0x0032FF: return 'Enclosed CJK Letters and Months'
        if 0x003300 <= symbol <= 0x0033FF: return 'CJK Compatibility'
        if 0x003400 <= symbol <= 0x004DBF: return 'CJK Unified Ideographs Extension A'
        if 0x004DC0 <= symbol <= 0x004DFF: return 'Yijing Hexagram Symbols'
        if 0x004E00 <= symbol <= 0x009FAF: return 'CJK Unified Ideographs'
        # if 0x009FB0 <= symbol <= 0x009FFF: return 'Undefined'
        if 0x00A000 <= symbol <= 0x00A48F: return 'Yi Syllables'
        if 0x00A490 <= symbol <= 0x00A4CF: return 'Yi Radicals'
        # if 0x00A4D0 <= symbol <= 0x00ABFF: return 'Undefined'
        if 0x00AC00 <= symbol <= 0x00D7AF: return 'Hangul Syllables'
        # if 0x00D7B0 <= symbol <= 0x00D7FF: return 'Undefined'
        if 0x00D800 <= symbol <= 0x00DBFF: return 'High Surrogate Area'
        if 0x00DC00 <= symbol <= 0x00DFFF: return 'Low Surrogate Area'
        if 0x00E000 <= symbol <= 0x00F8FF: return 'Private Use Area'
        if 0x00F900 <= symbol <= 0x00FAFF: return 'CJK Compatibility Ideographs'
        if 0x00FB00 <= symbol <= 0x00FB4F: return 'Alphabetic Presentation Forms'
        if 0x00FB50 <= symbol <= 0x00FDFF: return 'Arabic Presentation Forms-A'
        if 0x00FE00 <= symbol <= 0x00FE0F: return 'Variation Selectors'
        # if 0x00FE10 <= symbol <= 0x00FE1F: return 'Undefined'
        if 0x00FE20 <= symbol <= 0x00FE2F: return 'Combining Half Marks'
        if 0x00FE30 <= symbol <= 0x00FE4F: return 'CJK Compatibility Forms'
        if 0x00FE50 <= symbol <= 0x00FE6F: return 'Small Form Variants'
        if 0x00FE70 <= symbol <= 0x00FEFF: return 'Arabic Presentation Forms-B'
        if 0x00FF00 <= symbol <= 0x00FFEF: return 'Halfwidth and Fullwidth Forms'
        if 0x00FFF0 <= symbol <= 0x00FFFF: return 'Specials'
        if 0x010000 <= symbol <= 0x01007F: return 'Linear B Syllabary'
        if 0x010080 <= symbol <= 0x0100FF: return 'Linear B Ideograms'
        if 0x010100 <= symbol <= 0x01013F: return 'Aegean Numbers'
        # if 0x010140 <= symbol <= 0x0102FF: return 'Undefined'
        if 0x010300 <= symbol <= 0x01032F: return 'Old Italic'
        if 0x010330 <= symbol <= 0x01034F: return 'Gothic'
        if 0x010380 <= symbol <= 0x01039F: return 'Ugaritic'
        if 0x010400 <= symbol <= 0x01044F: return 'Deseret'
        if 0x010450 <= symbol <= 0x01047F: return 'Shavian'
        if 0x010480 <= symbol <= 0x0104AF: return 'Osmanya'
        # if 0x0104B0 <= symbol <= 0x0107FF: return 'Undefined'
        if 0x010800 <= symbol <= 0x01083F: return 'Cypriot Syllabary'
        # if 0x010840 <= symbol <= 0x01CFFF: return 'Undefined'
        if 0x01D000 <= symbol <= 0x01D0FF: return 'Byzantine Musical Symbols'
        if 0x01D100 <= symbol <= 0x01D1FF: return 'Musical Symbols'
        # if 0x01D200 <= symbol <= 0x01D2FF: return 'Undefined'
        if 0x01D300 <= symbol <= 0x01D35F: return 'Tai Xuan Jing Symbols'
        # if 0x01D360 <= symbol <= 0x01D3FF: return 'Undefined'
        if 0x01D400 <= symbol <= 0x01D7FF: return 'Mathematical Alphanumeric Symbols'
        # if 0x01D800 <= symbol <= 0x01FFFF: return 'Undefined'
        if 0x020000 <= symbol <= 0x02A6DF: return 'CJK Unified Ideographs Extension B'
        # if 0x02A6E0 <= symbol <= 0x02F7FF: return 'Undefined'
        if 0x02F800 <= symbol <= 0x02FA1F: return 'CJK Compatibility Ideographs Supplement'
        # if 0x02FAB0 <= symbol <= 0x0DFFFF: return 'Unused'
        if 0x0E0000 <= symbol <= 0x0E007F: return 'Tags'
        # if 0x0E0080 <= symbol <= 0x0E00FF: return 'Unused'
        if 0x0E0100 <= symbol <= 0x0E01EF: return 'Variation Selectors Supplement'
        # if 0x0E01F0 <= symbol <= 0x0EFFFF: return 'Unused'
        if 0x0F0000 <= symbol <= 0x0FFFFD: return 'Supplementary Private Use Area-A'
        # if 0x0FFFFE <= symbol <= 0x0FFFFF: return 'Unused'
        if 0x100000 <= symbol <= 0x10FFFD: return 'Supplementary Private Use Area-B'

        return 'Undefined'

    def validate(self, text_cell, text_data, culture_name):
        from collections import defaultdict
        from unicodedata import category
        from unicodedata import name

        if len(text_data) == 0:
            self.logger.warning(TRANSLATOR, '\033[33mText specified at \033[92m{0}\033[33m is empty.\033[0m'.format(text_cell))
        else:
            if category(text_data[0]) == 'Zs':
                self.logger.warning(TRANSLATOR, '\033[33mText specified at \033[92m{0}\033[33m starts with space.\033[0m'.format(text_cell))

            if category(text_data[-1]) == 'Zs':
                self.logger.warning(TRANSLATOR, '\033[33mText specified at \033[92m{0}\033[33m ends with space.\033[0m'.format(text_cell))

            if category(text_data[0]) == 'Cc':
                self.logger.warning(TRANSLATOR, '\033[33mText specified at \033[92m{0}\033[33m starts with control character.\033[0m'.format(text_cell))

            if category(text_data[-1]) == 'Cc':
                self.logger.warning(TRANSLATOR, '\033[33mText specified at \033[92m{0}\033[33m ends with control character.\033[0m'.format(text_cell))

            culture_ranges = self.culture_ranges.get(culture_name)

            if culture_ranges:
                counter = 0

                for index, symbol in enumerate(text_data):
                    symbol_range = self.get_symbol_range(symbol)

                    if symbol_range in culture_ranges.primary:
                        counter += 1

                    if not symbol_range in culture_ranges.allowed:
                        self.logger.warning(
                            TRANSLATOR, 
                            '\033[33mText "\033[93m{0}\033[4m{1}\033[24m{2}\033[33m" specified at \033[92m{3}\033[33m contains invalid symbol "{4}" ({5}).\033[0m'.format(
                                text_data[:index],
                                text_data[index],
                                text_data[index + 1:],
                                text_cell,
                                symbol,
                                name(symbol)))

                        return

                if counter < len(text_data) / 2:
                    self.logger.warning(
                        TRANSLATOR, 
                        '\033[33mText "\033[93m{0}\033[33m" specified at \033[92m{1}\033[33m contains many allowed, but not culture specific symbols.\033[0m'.format(
                            text_data,
                            text_cell))


class GoogleSheetDataReader(object):
    def __init__(self, logger, sheet_id, culture_name, path_column_index, code_column_index):
        from googleapiclient.discovery import build

        self.logger = logger
        self.sheet_id = sheet_id
        self.culture_name = culture_name
        self.path_column_index = path_column_index
        self.code_column_index = code_column_index
        self._text_validator = TextValidator(self.logger)
        self._sheets_service = build('sheets', 'v4', developerKey='AIzaSyD5t2N0Z5lrOGg08xW0xcw6san8cb2lKn0').spreadsheets()

    def read(self):
        from collections import defaultdict
        from collections import namedtuple
        from random import seed
        from random import randint
        from re import compile

        TranslatioinItem = namedtuple('TranslatioinItem', ('text_cell', 'text_data', 'is_first_in_group'))
        code_pattern = compile('[A-Za-z][A-Za-z0-9_]*')

        print('Looking for spreadsheet ID = "{0}"'.format(self.sheet_id))
        print()

        spreadsheet_meta = self._sheets_service.get(spreadsheetId=self.sheet_id).execute()

        print('Found spreadsheet ID = "{0}".'.format(spreadsheet_meta['spreadsheetId']))
        print('    URL = \033[94m{0}\033[0m'.format(spreadsheet_meta['spreadsheetUrl']))
        print('    Title = "{0}"'.format(spreadsheet_meta['properties']['title']))
        print()

        texts_sheet_propeties = None

        for sheet_meta in spreadsheet_meta['sheets']:
            sheet_propeties = sheet_meta['properties']

            if (sheet_propeties['title'] == 'Texts') and (sheet_propeties['sheetType'] == 'GRID'):
                texts_sheet_propeties = sheet_propeties

        if not texts_sheet_propeties:
            self.logger.error(10, '\033[91mSheet with name "Texts" is missing.\033[0m')

        row_count = texts_sheet_propeties['gridProperties']['rowCount']
        column_count = texts_sheet_propeties['gridProperties']['columnCount']
        column_names = [chr(ord('A') + i) if i < 26 else chr(ord('A') + (i - 26) // 26) + chr(ord('A') + i % 26) for i in range(column_count)]

        headers_range = 'Texts!A1:{0}2'.format(column_names[column_count - 1])
        header_values = self._sheets_service.values().get(spreadsheetId=self.sheet_id, range=headers_range).execute().get('values', [])

        try:
            text_column_index = header_values[1].index(self.culture_name)

            if text_column_index < 9:
                raise ValueError()
        except ValueError:
            self.logger.error(20, '\033[91mCulture with name "{0}" is missing.\033[0m'.format(self.culture_name))

        print('Processing culture "{0}"'.format(self.culture_name))
        print('    ' + header_values[0][text_column_index].replace('\n', '\n    '))
        print()

        path_column_name = column_names[self.path_column_index]
        code_column_name = column_names[self.code_column_index]
        text_column_name = column_names[text_column_index]

        path_range = 'Texts!{0}1:{0}{1}'.format(path_column_name, row_count - 1)
        code_range = 'Texts!{0}1:{0}{1}'.format(code_column_name, row_count - 1)
        text_range = 'Texts!{0}1:{0}{1}'.format(text_column_name, row_count - 1)
        path_values = self._sheets_service.values().get(spreadsheetId=self.sheet_id, range=path_range).execute().get('values', [])
        code_values = self._sheets_service.values().get(spreadsheetId=self.sheet_id, range=code_range).execute().get('values', [])
        text_values = self._sheets_service.values().get(spreadsheetId=self.sheet_id, range=text_range).execute().get('values', [])

        result = defaultdict(dict)

        prev_row_index = 0

        for row_index in range(3, row_count - 1):
            path_cell = '{0}{1}'.format(path_column_name, row_index + 1)
            code_cell = '{0}{1}'.format(code_column_name, row_index + 1)
            text_cell = '{0}{1}'.format(text_column_name, row_index + 1)
            path_data = path_values[row_index][0] if (len(path_values) > row_index) and (len(path_values[row_index]) == 1) else None
            code_data = code_values[row_index][0] if (len(code_values) > row_index) and (len(code_values[row_index]) == 1) else None
            text_data = text_values[row_index][0] if (len(text_values) > row_index) and (len(text_values[row_index]) == 1) else None

            seed(path_cell + code_cell)

            mask_text = str(randint(1000, 9999))

            if code_data == mask_text:
                continue

            if text_data:
                if not code_data:
                    self.logger.warning(
                        DEVELOPER,
                        '\033[33mText is specified at \033[92m{0}\033[33m, but corresponding code is not specified at \033[92m{1}\033[33m. Use code "\033[93m{2}\033[33m" to suppress this warning.\033[0m'.format(
                            text_cell,
                            code_cell,
                            mask_text))
                    continue

                if not path_data:
                    self.logger.warning(
                        DEVELOPER,
                        '\033[33mText is specified at \033[92m{0}\033[33m, but corresponding path is not specified at \033[92m{1}\033[33m.\033[0m'.format(
                            text_cell,
                            path_cell))
                    continue

                if not code_pattern.fullmatch(code_data):
                    self.logger.warning(
                        DEVELOPER,
                        '\033[33mCode specified at \033[92m{0}\033[33m has invalid value "{1}".\033[0m'.format(
                            code_cell,
                            code_data))
                    continue

                previous_item = result[path_data].get(code_data)

                if previous_item and (previous_item.text_data != text_data):
                    self.logger.warning(
                        DEVELOPER,
                        '\033[33mText "\033[93m{0}\033[33m" is specified at \033[92m{1}\033[33m for code "\033[93m{2}\033[33m", but different text "\033[93m{3}\033[33m" was previously specified at \033[92m{4}\033[33m for the same code.\033[0m'.format(
                            text_data,
                            text_cell,
                            code_data,
                            previous_item.text_data,
                            previous_item.text_cell))
                else:
                    self._text_validator.validate(text_cell, text_data, self.culture_name)
                    result[path_data][code_data] = TranslatioinItem(text_cell, text_data, prev_row_index + 1 != row_index)
                    prev_row_index = row_index
            else:
                if code_data:
                    self.logger.warning(
                        TRANSLATOR,
                        '\033[33mCode is specified at \033[92m{0}\033[33m, but corresponding text is not specified at \033[92m{1}\033[33m.\033[0m'.format(
                            code_cell,
                            text_cell))
                    continue

        return result


class AndroidDataWriter(object):
    def __init__(self, logger, base_path, culture_name):
        self.logger = logger
        self.base_path = base_path
        self.culture_name = culture_name

    def write(self, translation_data):
        from os import makedirs
        from os.path import abspath
        from os.path import dirname
        from os.path import expandvars
        from os.path import join
        from xml.sax.saxutils import XMLGenerator

        if len(translation_data.items()) == 0:
            self.logger.error(31, '\033[91mNo files will be generated.\033[0m')

        for file_name, file_data in translation_data.items():
            file_path = abspath(join(self.base_path, expandvars(file_name)))

            makedirs(dirname(file_path), exist_ok=True)

            print()
            print('Writing contents to "{0}"'.format(file_path))

            with open(file_path, 'w') as xml_file:
                generator = XMLGenerator(out=xml_file, encoding='utf-8')
                generator.startDocument()
                generator.startElement('resources', {})
                
                for code, item in file_data.items():
                    if item.is_first_in_group:
                        generator.ignorableWhitespace('\r\n')

                    generator.ignorableWhitespace('\r\n    <!-- Defined at {0} -->\r\n    '.format(item.text_cell))
                    generator.startElement('string', {'name': code})
                    generator.characters(item.text_data)
                    generator.endElement('string')

                generator.ignorableWhitespace('\r\n')
                generator.endElement('resources')
                generator.endDocument()


class IosDataWriter(object):
    def __init__(self, logger, base_path, culture_name):
        self.logger = logger
        self.base_path = base_path
        self.culture_name = culture_name

    def write(self, translation_data):
        from os import makedirs
        from os.path import abspath
        from os.path import dirname
        from os.path import expandvars
        from os.path import join

        if len(translation_data.items()) == 0:
            self.logger.error(32, '\033[91mNo files will be generated.\033[0m')

        for file_name, file_data in translation_data.items():
            file_path = abspath(join(self.base_path, expandvars(file_name)))

            makedirs(dirname(file_path), exist_ok=True)

            print()
            print('Writing contents to "{0}"'.format(file_path))

            with open(file_path, 'w') as strings_file:
                for code, item in file_data.items():
                    if item.is_first_in_group:
                        strings_file.write('\r\n')

                    strings_file.write('// Defined at {0}\r\n'.format(item.text_cell))
                    strings_file.write('"{0}" = "{1}";\r\n'.format(code, item.text_data))


class TranslationBuilder(object):
    def __init__(self, logger, platform, sheet_id, base_path, culture_name):
        self.platform = platform
        self.sheet_id = sheet_id
        self.base_path = base_path
        self.culture_name = culture_name

        if platform == 'android':
            self.reader = GoogleSheetDataReader(logger, sheet_id, culture_name, 0, 1)
            self.writer = AndroidDataWriter(logger, self.base_path, self.culture_name)
        elif platform == 'ios':
            self.reader = GoogleSheetDataReader(logger, sheet_id, culture_name, 2, 3)
            self.writer = IosDataWriter(logger, self.base_path, self.culture_name)

    def build(self):
        data = self.reader.read()
        self.writer.write(data)


def main(prog_name=None):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog=prog_name,
        description='Generate Space Mobile App Translation Files based on Google Sheet.')

    os_parser = parser.add_mutually_exclusive_group(required=True)
    os_parser.add_argument(
        '--android',
        action='store_const',
        const='android',
        dest='platform',
        help='Generate XML files for Android.')
    os_parser.add_argument(
        '--ios',
        action='store_const',
        const='ios',
        dest='platform',
        help='Generate Strings files for iOS.')

    parser.add_argument(
        '--sheet',
        nargs='?',
        required=True,
        metavar='"1nTGePbXdQ5ma58GBoZsjScLGBF-lsm1qpJNMzrYUecA"',
        help='Google Sheet ID.')
    parser.add_argument(
        '--path',
        nargs='?',
        required=True,
        metavar='"/some/path/to/files/"',
        help='Base path for generated files, if relative path was specified.')
    parser.add_argument(
        '--culture',
        nargs='?',
        required=True,
        metavar='"en-Latn-US"',
        help='ISO compatible specification of language-Script-COUNTRY.')
    parser.add_argument(
        '--warnings',
        nargs='+',
        choices=[DEVELOPER, TRANSLATOR],
        default=[DEVELOPER, TRANSLATOR],
        help='Type of warning to output.')

    args = parser.parse_args()

    logger = Logger(args.warnings)

    builder = TranslationBuilder(logger, args.platform, args.sheet, args.path, args.culture)
    builder.build()
