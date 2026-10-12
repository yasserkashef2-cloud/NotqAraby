# -*- coding: utf-8 -*-
"""Structure of the book: units, lessons, items, and how each item maps onto blocks of the supplied Word file.
All ranges are [start, end) block indices of data/source.json (see parse_docx.py)."""

# ---------------------------------------------------------------------------------------------------------------------
META = dict(
    title_ar='صوتي عربي',
    subtitle_ar='فصحى – عامية – دارجة',
    title_en='Ṣawtī ʿArabī — "My Arabic Voice"',
    subtitle_en='Modern Standard Arabic · Egyptian colloquial · Moroccan Darija — a pronunciation course',
    authors_ar=['إسراء توكل', 'سمر زايد', 'فاطمة الزهراء شكر', 'ندا عبد الفتاح'],   # names printed in the footer of the supplied Word file
    curator_line_ar='إعداد المادة: إسراء توكل · سمر زايد · فاطمة الزهراء شكر · ندا عبد الفتاح (كما في تذييل الوثيقة المصدرية)',
    curator_line_en='Course materials by the four authors named in the footer of the supplied Word file. Interactive book prepared from those materials.',
    term_line='صوتي عربي · وثيقة المقرر المؤرخة 2016',
    term_line_en='Course document dated 2016 (file properties)',
    copyright_line='© 2016 — course materials as credited above · Interactive edition: design carried out by AI',
    year='2016',
)

# colour rules (see css): listening titles dark blue, reading / recitation titles dark red.
UNITS = [
    dict(id='1', ar='الوحدة الأولى', en='Unit 1', sub_ar='الأصوات الخاصة باللغة العربية: منفردة وفي السياقات وفي أوزان الأفعال',
         sub_en='The sounds particular to Arabic — in isolation, in contexts and in verb patterns',
         lessons=['L1', 'L2', 'L3', 'L4', 'L5'], obj_row=1),
    dict(id='2', ar='الوحدة الثانية', en='Unit 2', sub_ar='النصوص الطويلة: الفصحى والعامية والدارجة',
         sub_en='Long texts — Standard Arabic, Egyptian colloquial and Moroccan Darija',
         lessons=['L6', 'L7', 'L8'], obj_row=2),
]

LESSONS = {
    'L1': dict(id='L1', unit='1', n=1, ar='الدرس الأول: المفخمات', en='Lesson 1 — The emphatics ص ض ط ظ', obj=(30, 40), items=['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7']),
    'L2': dict(id='L2', unit='1', n=2, ar='الدرس الثاني: الحلقيات ح و ق', en='Lesson 2 — ق and ح', obj=(40, 50), items=['2.1', '2.2']),
    'L3': dict(id='L3', unit='1', n=3, ar='الدرس الثالث: ع', en='Lesson 3 — ع', obj=(50, 60), items=['3.1']),
    'L4': dict(id='L4', unit='1', n=4, ar='الدرس الرابع: خ و غ', en='Lesson 4 — خ and غ', obj=(60, 70), items=['4.1', '4.2']),
    'L5': dict(id='L5', unit='1', n=5, ar='الدرس الخامس: ل و ر', en='Lesson 5 — ل and ر', obj=(70, 80), items=['5.1', '5.2']),
    'L6': dict(id='L6', unit='2', n=6, ar='الدرس السادس: بيان ثورة الثالث والعشرين من يوليو', en='Lesson 6 — The statement of 23 July (Standard Arabic)', obj=(1028, 1036), items=['6.1']),
    'L7': dict(id='L7', unit='2', n=7, ar='الدرس السابع: قصيدة «ماتزعليش»', en='Lesson 7 — A modern Egyptian colloquial poem', obj=(1036, 1044), items=['7.1']),
    'L8': dict(id='L8', unit='2', n=8, ar='الدرس الثامن: الغزال فاطمة', en='Lesson 8 — A Moroccan (Malhūn) poem', obj=(1044, 1052), items=['8.1']),
}

# type: 'listen' -> dark blue titles, 'read' -> dark red titles
ITEMS = [
 dict(id='1.1', lesson='L1', type='listen', kind='sound', ar='صوت الصاد /ص/', en='The sound ṣād /ṣ/ against sīn', target='ص', rng=(85, 138), verbs=False),
 dict(id='1.2', lesson='L1', type='listen', kind='sound', ar='صوت الضاد /ض/', en='The sound ḍād /ḍ/ against dāl', target='ض', rng=(138, 212), verbs=False),
 dict(id='1.3', lesson='L1', type='listen', kind='sound', ar='صوت الطاء /ط/', en='The sound ṭāʾ /ṭ/ against tāʾ', target='ط', rng=(212, 291), verbs=False),
 dict(id='1.4', lesson='L1', type='listen', kind='sound', ar='صوت الظاء /ظ/', en='The sound ẓāʾ /ẓ/ against dhāl, zāy, thāʾ', target='ظ', rng=(291, 373), verbs=False),
 dict(id='1.5', lesson='L1', type='listen', kind='verbs', ar='أوزان الأفعال مع المفخمات', en='Verb patterns with the emphatics (Standard → colloquial)', target='صضطظ', rng=(373, 394), verbs=True),
 dict(id='1.6', lesson='L1', type='listen', kind='listening', ar='نص الاستماع: عصير الكتب مع بلال فضل (الحلقة 12)', en='Listening: "Aṣīr al-Kutub", episode 12', target='صضطظ', rng=(394, 412), verbs=False),
 dict(id='1.7', lesson='L1', type='read', kind='poem', ar='أبيات أبي فراس الحمداني: عصي الدمع', en='Verses of Abū Firās al-Ḥamdānī', target='صضطظ', rng=(412, 419), verbs=False),
 dict(id='2.1', lesson='L2', type='listen', kind='sound', ar='صوت القاف /ق/', en='The sound qāf /q/ against kāf', target='ق', rng=(423, 497), verbs=True),
 dict(id='2.2', lesson='L2', type='listen', kind='sound', ar='صوت الحاء /ح/', en='The sound ḥāʾ /ħ/ against hāʾ', target='ح', rng=(497, 594), verbs=True),
 dict(id='3.1', lesson='L3', type='listen', kind='sound', ar='صوت العين /ع/', en='The sound ʿayn /ʕ/ against hamza', target='ع', rng=(597, 702), verbs=True),
 dict(id='4.1', lesson='L4', type='listen', kind='sound', ar='صوت الغين /غ/', en='The sound ghayn /ɣ/', target='غ', rng=(705, 768), verbs=True),
 dict(id='4.2', lesson='L4', type='listen', kind='sound', ar='صوت الخاء /خ/', en='The sound khāʾ /x/ against ghayn', target='خ', rng=(768, 831), verbs=True),
 dict(id='5.1', lesson='L5', type='listen', kind='sound', ar='اللام /ل/ المرققة والمفخمة', en='Lām — non-emphatic and emphatic', target='ل', rng=(835, 913), verbs=True),
 dict(id='5.2', lesson='L5', type='listen', kind='sound', ar='صوت الراء /ر/', en='The sound rāʾ /r/ — trilled, emphatic and not', target='ر', rng=(913, 1026), verbs=True),
 dict(id='6.1', lesson='L6', type='read', kind='speech', ar='بيان ثورة الثالث والعشرين من يوليو 1952', en='The statement of 23 July 1952 (Standard Arabic)', target='صضطظعحقخغ', rng=(1077, 1109), verbs=False),
 dict(id='7.1', lesson='L7', type='read', kind='poem', ar='قصيدة «ماتزعليش» لهشام الجخ', en='"Matzaʿalīsh" — Egyptian colloquial poem', target='صضطظعحقخغ', rng=(1109, 1142), verbs=False),
 dict(id='8.1', lesson='L8', type='read', kind='poem', ar='الغزال فاطمة: من تراث الملحون المغربي', en='"Al-Ghazāl Fāṭima" — Moroccan Malḥūn poem', target='صضطظعحقخغ', rng=(1142, 1176), verbs=False),
]

# Blocks of the Word file that are NOT reproduced in the book, and why.
#   'copyright'  : modern song lyrics / modern poem / modern spoken text — the author's text can be added through data/private_texts/
#   'transcript' : supplied listening transcript, deliberately not shown (students must develop listening strategies)
WITHHELD = {}
def _w(rng, kind, key, label_ar, label_en, slot=True):
    for i in rng: WITHHELD[i] = dict(kind=kind, key=key, label_ar=label_ar, label_en=label_en, slot=slot)
_w((406, 407), 'transcript', 'b406', 'نص الاستماع (مُورَّد في الملف لكنه غير معروض)', 'Listening transcript (supplied but deliberately not shown)', slot=False)
_w((586, 587, 588), 'copyright', 'b586', 'كلمات الأغنية «كل ما تكبر تحلى»', 'Lyrics of the song "Kull mā tikbar tiḥlā"')
_w((673,), 'copyright', 'b673', 'كلمات الأغنية «في الشارع»', 'Lyrics of the song "Fī ash-shāriʿ"')
_w((763,), 'copyright', 'b763', 'كلمات الأغنية «يا غالي»', 'Lyrics of the song "Yā ghālī"')
_w((909,), 'copyright', 'b909', 'كلمات الأغنية «يا لا لا لا»', 'Lyrics of the song "Yā lā lā lā"')
_w((1014, 1015, 1016, 1017), 'copyright', 'b1014', 'كلمات الأغنية «يا هلا يا هلا»', 'Lyrics of the song "Yā halā yā halā"')
_w((1122,), 'copyright', 'b1122', 'نص قصيدة «ماتزعليش»', 'Text of the poem "Matzaʿalīsh"')

TITLE_RED = {415, 416, 900, 1078, 1091, 1092, 1110, 1111, 1143, 1144, 1158}
TITLE_BLUE = {402, 403, 582, 583, 668, 669, 761, 762, 907, 908, 1011, 1012}

# YouTube links supplied in the Word file (block -> video id)
YOUTUBE = {404: 'efBDE3bPgjo', 584: 'hULNcLm7Pr8', 670: 'LFTSJrIZa5Y', 1013: 'WTSBp8ORrYU',
           1093: 'L8TOCOHUh0c', 1113: 'yPj-4ORufQw', 1145: 'vuwN2JM6Wfg'}
# seek buttons for YouTube embeds: only times stated in the Word file (Bilal Fadl: minutes 0:00-2:00)
YT_SEEK = {404: [('0:00', 0), ('2:00', 120)]}
EXTRA_LINKS = {1014: [('http://vb.elmstba.com/t39231.html', 'Link attached to the word «هيلا» in the Word file (third-party page; not checked)')]}

# verse/lyric style blocks: multi-line paragraphs shown as numbered verse lines
VERSE_BLOCKS = {576: 'hemi', 901: 'lines', 904: 'hemi', 1006: 'hemi', 1007: 'hemi', 1008: 'hemi', 1159: 'hemi', 1160: 'hemi', 1161: 'hemi'}
SPEECH_BLOCKS = {1095}
