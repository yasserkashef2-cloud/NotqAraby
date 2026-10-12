# -*- coding: utf-8 -*-
"""Maps every supplied audio/video file (Audiovisuals.zip) to an item and an anchor block of the source file.
`src` is the path inside the zip. `after` is the index of the source block after which the player is placed.
Mapping is by CONTENT (file names and numbering in the zip do not always match the exercise numbers in the Word file;
mismatches are listed in data/flags.py and in SOURCES_REPORT.md)."""
L1='تسجيلات الدرس الأول/'; L2='تسجيلات الدرس التاني/'; L3='تسجيلات الدرس الثالث/'
L4='تسجيلات الدرس الرابع/'; L5='تسجيلات الدرس الخامس/'

def M(id,src,item,after,role,kind=None,note=None,seek=None,heavy=False):
    return dict(id=id,src=src,item=item,after=after,role=role,kind=kind or ('video' if src.lower().endswith('.mp4') else 'audio'),note=note,seek=seek or [],heavy=heavy)

MEDIA=[
 # ---- Lesson 1 : emphatics -------------------------------------------------
 M('l1-sad-video',L1+'1 مخرج ص.mp4','1.1',92,'Articulation video'),
 M('l1-sad-sustained',L1+'تمرينات النطق المستمر ص.m4a','1.1',97,'Sustained sound'),
 M('l1-sad-pairs',L1+'التسجيل الثاني - الكلمات الفارقة (ص).m4a','1.1',103,'Minimal pairs'),
 M('l1-sad-contexts',L1+'التسجيل الثالث - سياقات ص.m4a','1.1',110,'Sound contexts'),
 M('l1-sad-effects',L1+'التسجيل الرابع -تأثير صوت ص على الأصوات المجاورة.m4a','1.1',116,'Neighbouring-sound effects'),
 M('l1-dad-video',L1+'6 مخرج ض.mp4','1.2',148,'Articulation video'),
 M('l1-dad-sustained',L1+'تمرين النطق المتكرر ض.m4a','1.2',153,'Repeated sound'),
 M('l1-dad-pairs',L1+'التسجيل السابع - الكلمات الفارقة صوت ض.m4a','1.2',160,'Minimal pairs'),
 M('l1-dad-contexts',L1+'التسجيل الثامن - سياقات صوت ض.m4a','1.2',170,'Sound contexts'),
 M('l1-dad-effects',L1+'التسجيل التاسع التأثيرات الصوتية لصوت ض.m4a','1.2',177,'Neighbouring-sound effects'),
 M('l1-ta-video',L1+'6 مخرج ط.mp4','1.3',224,'Articulation video'),
 M('l1-ta-sustained',L1+'تمرين النطق المتكرر ط.m4a','1.3',229,'Repeated sound'),
 M('l1-ta-pairs',L1+'تسجيل 12 الكلمات الفارقة صوت ط.m4a','1.3',240,'Minimal pairs'),
 M('l1-ta-contexts',L1+'تسجيل 13 سياقات ط.m4a','1.3',247,'Sound contexts'),
 M('l1-ta-effects',L1+'تسجيل 14 تأثير صوت ط على الأصوات المجاورة.m4a','1.3',262,'Neighbouring-sound effects'),
 M('l1-za-video',L1+'16مخرج ظ.mp4','1.4',305,'Articulation video'),
 M('l1-za-sustained',L1+'تمرين النطق المستمر ظ.m4a','1.4',310,'Sustained sound'),
 M('l1-za-pairs',L1+'تسجيل 17 الكلمات الفارقة ظ.m4a','1.4',323,'Minimal pairs'),
 M('l1-za-contexts',L1+'تسجيل 18 سياقات صوت ظ.m4a','1.4',336,'Sound contexts'),
 M('l1-za-effects',L1+'تسجيل 19 تأثير ظ على الأصوات المجاورة.m4a','1.4',344,'Neighbouring-sound effects'),
 M('l1-verbs',L1+'تحولات الاوزان من الفصحى للعامية.m4a','1.5',374,'Verb patterns, MSA to colloquial'),
 M('l1-bilal',L1+'عصير الكتب مع بلال فضل - الحلقة 12.mp4','1.6',399,'Listening video (full episode)',
   heavy=True,note='158 MB, 52 min in the zip. Re-encoded for the web (see README); the exercise uses minutes 0:00-2:00.',
   seek=[('0:00',0),('2:00',120)]),
 M('l1-abufiras',L1+'أراك عصي الدمع إلقاء رائع .. جديد_Segment_0_x264.mp4','1.7',413,'Recitation video'),
 # ---- Lesson 2 : q / h ----------------------------------------------------
 M('l2-qaf-video',L2+'مخرج ق 1.mp4','2.1',434,'Articulation video',note='The zip holds two byte-identical copies (مخرج ق 1 / مخرج ق 2); one is used.'),
 M('l2-qaf-sustained',L2+'تمرين النطق المتكرر صوت ق.m4a','2.1',439,'Repeated sound'),
 M('l2-qaf-pairs',L2+'التسجيل الثاني الكلمات الفارقة.m4a','2.1',446,'Minimal pairs',note='File name does not name the sound; matched to ق/ك by its place in the Lesson 2 folder and exercise order.'),
 M('l2-qaf-contexts',L2+'التسجيل الثالث سياقات صوت ق.m4a','2.1',455,'Sound contexts'),
 M('l2-qaf-verbs',L2+'تسجيل 4تحولات الاوزان من الفصحى للعامية صوت ق.m4a','2.1',480,'Verb patterns, MSA to colloquial',note='File is numbered 4; the Word file calls this exercise 5.'),
 M('l2-qaf-twister',L2+'صوت ق قبر حرب tongue twister.mp3','2.1',496,'Tongue twister'),
 M('l2-ha-video',L2+'مخرج الحاء الشيخ أيمن سويد من برنامج اتقان التلاوة.mp4','2.2',507,'Articulation video'),
 M('l2-ha-sustained',L2+'تمرين النطق المستمر صوت ح.m4a','2.2',512,'Sustained sound'),
 M('l2-ha-pairs',L2+'تسجيل 5 الكلمات الفارقة صوت ح.m4a','2.2',527,'Minimal pairs',note='File is numbered 5; the Word file calls this exercise 10.'),
 M('l2-ha-contexts',L2+'تسجيل 6سياقات ح.m4a','2.2',535,'Sound contexts',note='File is numbered 6; the Word file calls this exercise 11.'),
 M('l2-ha-verbs',L2+'تسجيل7تحولات الاوزان من الفصحى للعامية صوت ح.m4a','2.2',556,'Verb patterns, MSA to colloquial',note='File is numbered 7; the Word file calls this exercise 12.'),
 M('l2-muhalhil',L2+'صوت ح شعر المهلهل.mp3','2.2',576,'Poem recitation'),
 # ---- Lesson 3 : ayn ------------------------------------------------------
 M('l3-ayn-video',L3+'مخرج ع و ح.mp4','3.1',610,'Articulation video'),
 M('l3-ayn-clip',L1+'ع متقطع.mp4','3.1',610,'Short clip (interrupted ayn)',note='Found in the Lesson 1 folder of the zip; matched to ع by its content (the first frame shows the articulation chart of ع). Placed in Lesson 3.'),
 M('l3-ayn-sustained',L3+'تمرين النطق المستمر صوت ع.m4a','3.1',615,'Sustained sound'),
 M('l3-ayn-pairs',L3+'تسجيل 1 الكلمات الفارقة صوت ع.m4a','3.1',623,'Minimal pairs'),
 M('l3-ayn-contexts',L3+'تسجي 2 سياقات صوت ع.m4a','3.1',633,'Sound contexts'),
 M('l3-ayn-verbs',L3+'تحولات الاوزان من الفصحى للعامية صوت ع.m4a','3.1',656,'Verb patterns, MSA to colloquial'),
 # ---- Lesson 4 : gh / kh --------------------------------------------------
 M('l4-ghayn-video',L4+'مخرج الغين الشيخ أيمن سويد من برنامج اتقان التلاوة.mp4','4.1',714,'Articulation video'),
 M('l4-ghayn-sustained',L4+'تمرين النطق المستمر صوت غ.m4a','4.1',719,'Sustained sound'),
 M('l4-ghayn-contexts',L4+'سياقات صوت غ.m4a','4.1',731,'Sound contexts'),
 M('l4-ghayn-verbs',L4+'تحولات الاوزان نم الفصحى للعامية صوت غ.m4a','4.1',744,'Verb patterns, MSA to colloquial'),
 M('l4-kha-video',L4+'مخرج الخاء الشيخ أيمن سويد من برنامج اتقان التلاوة.mp4','4.2',778,'Articulation video'),
 M('l4-kha-sustained',L4+'تمرين النطق المستمر خ.m4a','4.2',783,'Sustained sound'),
 M('l4-kha-pairs',L4+'صوت خ و غ كلمات فارقة.m4a','4.2',794,'Minimal pairs'),
 M('l4-kha-contexts',L4+'سياقات صوتية صوت خ.m4a','4.2',802,'Sound contexts'),
 M('l4-kha-verbs',L4+'تحولات الاوزان من الفصحى للعامية صوت خ.m4a','4.2',816,'Verb patterns, MSA to colloquial'),
 # ---- Lesson 5 : l / r ----------------------------------------------------
 M('l5-lam-video',L5+'ل.mp4','5.1',854,'Lecture video (lam)',
   seek=[('0:00',0),('3:00',180),('3:02',182),('3:20',200)],
   note='Video frames checked: the articulation-place slide for lam is at about 1:00-2:00 and the emphatic/non-emphatic comparison slide at about 4:05.'),
 M('l5-lam-sustained',L5+'تمرين النطق المستمر صوت ل.m4a','5.1',859,'Sustained sound'),
 M('l5-lam-pairs',L5+'لام مرققة ولام مفخمة.m4a','5.1',868,'Emphatic / non-emphatic lam'),
 M('l5-lam-contexts',L5+'سياقات صوت ل.m4a','5.1',876,'Sound contexts'),
 M('l5-lam-verbs',L5+'تحولات الاوزان من الفصحى للعامية صوت ل.m4a','5.1',887,'Verb patterns, MSA to colloquial'),
 M('l5-imamali',L5+'من شعر الامام علي صوت ل .mp3','5.1',901,'Poem recitation'),
 M('l5-ra-video',L5+'ر.MP4','5.2',932,'Lecture video (ra)',
   seek=[('0:00',0),('1:00',60),('5:03',303)],
   note='Video frames checked: at 1:00 the slide shows the articulation place of ra (the Word file says lam); at 5:03 the emphatic/non-emphatic comparison slide.'),
 M('l5-ra-sustained',L5+'تمرين النطق المستمر صوت ر.m4a','5.2',930,'Sustained sound'),
 M('l5-ra-pairs',L5+'الكلمات الفارقة ل ر.m4a','5.2',943,'Minimal pairs (r / l)'),
 M('l5-ra-contexts',L5+'سياقات صوت ر.m4a','5.2',950,'Sound contexts'),
 M('l5-ra-combos',L5+'سياقات صوت ر+خ , ر+غ و رمشددة , ر+ع.m4a','5.2',959,'ra with kh, gh, ayn and geminated ra'),
 M('l5-ra-verbs',L5+'تحولات الاوزان من الفصحى للعامية صوت ر.m4a','5.2',996,'Verb patterns, MSA to colloquial'),
 M('l5-mutanabbi',L5+'رائعة المتنبى_Segment_0_x264.mp4','5.2',1004,'Recitation video'),
]
