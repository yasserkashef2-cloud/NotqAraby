# -*- coding: utf-8 -*-
"""EDUCATIONAL ADDITIONS at unit / page level (nothing here is from the supplied course file, except where a `src` reference
points at a block of it, in which case the text is pulled from the source at build time)."""

# ---------------------------------------------------------------------------------------------------------------------
# Expression sets ("connectors-equivalent" page). The supplied course has no connectors page, so this is an educational addition
# adapted to what this course trains: discussing sounds and texts aloud.
EXPR = {
 'opinion': dict(ar='للتعبير عن الرأي', en='Giving an opinion', rows=[
    ('أرى أن نطقي لهذا الصوت…', 'I think my pronunciation of this sound…'),
    ('في رأيي أن الفرق واضح بين الصوتين.', 'In my opinion the difference between the two sounds is clear.'),
    ('يبدو لي أن هذه الكلمة أصعب من غيرها.', 'It seems to me that this word is harder than the others.'),
    ('لا أوافق على أن…', 'I do not agree that…'),
    ('أتفق مع زميلي في أن…', 'I agree with my classmate that…'),
    ('أفضّل أن أسمع التسجيل مرة أخرى قبل أن أحكم.', 'I would rather hear the recording again before I judge.')]),
 'analysis': dict(ar='للتحليل والتفسير', en='Analysing and explaining', rows=[
    ('السبب في ذلك أن مكان اللسان مختلف.', 'The reason is that the tongue position is different.'),
    ('يدل هذا على أن…', 'This shows that…'),
    ('نلاحظ أن الصوت يتغير عندما يأتي بعد…', 'We notice that the sound changes when it follows…'),
    ('من هنا نستنتج أن…', 'From this we conclude that…'),
    ('يتضح من التسجيل أن النبر يقع على…', 'The recording shows that the stress falls on…'),
    ('والدليل على ذلك كلمة…', 'The evidence for this is the word…')]),
 'comparison': dict(ar='للمقارنة', en='Comparing', rows=[
    ('ينطق هذا الصوت في الفصحى …، أما في العامية فـ…', 'In Standard Arabic this sound is …, whereas in the colloquial it is …'),
    ('يشبه النطق الأول الثاني من حيث…، لكنه يختلف في…', 'The first pronunciation resembles the second in…, but differs in…'),
    ('على عكس الفصحى، تميل الدارجة إلى…', 'Unlike Standard Arabic, Darija tends to…'),
    ('كلا الصوتين مجهور، غير أن…', 'Both sounds are voiced, but…'),
    ('بالمقارنة مع تسجيلي الأول، أصبح نطقي…', 'Compared with my first recording, my pronunciation has become…'),
    ('من جهة…، ومن جهة أخرى…', 'On the one hand…, on the other hand…')]),
}

# ---------------------------------------------------------------------------------------------------------------------
# Proficiency maps. `src` = ('u', unit id, k): k-th bullet of that unit's objective cell in the Word file (verbatim, pulled at build time)
#                      or ('b', block index): a whole source paragraph.
MAPS = {
 '1': dict(rows=[
    dict(src=('u', '1', 0), can_ar='أميّز بالسمع بين الأصوات الخاصة بالعربية وما يقاربها في كلمات قصيرة.', can_en='I can hear the difference between Arabic-specific sounds and their near neighbours in short words.', skill='listening',
         ref_ar='أي زوج من الأصوات ما زلتم تخلطون بينه عند الاستماع؟ أعطوا كلمتين.', ref_en='Which pair of sounds do you still confuse when listening? Give two words.'),
    dict(src=('u', '1', 1), can_ar='أسمع موضع النبر في كلمات وجمل قصيرة وأنطقه.', can_en='I can hear where the stress falls in single words and short sentences and say it.', skill='speaking',
         ref_ar='اختاروا جملة قصيرة وضعوا علامة على موضع النبر. هل اتفق معكم زميل؟', ref_en='Choose a short sentence and mark the stress. Did a classmate agree?'),
    dict(src=('u', '1', 2), can_ar='أنطق المفخمات والحلقيات والأصوات الخلفية واللام والراء منفردة وفي سياقات الكلمات.', can_en='I can say the emphatics, pharyngeals, back sounds, lām and rāʾ alone and in word contexts.', skill='speaking',
         ref_ar='ما الصوت الذي تشعرون أنه الأكثر تقدماً عندكم، والأقل؟ ما الدليل من تسجيلاتكم؟', ref_en='Which sound feels strongest and which weakest? What evidence do your recordings give?'),
    dict(src=('u', '1', 3), can_ar='أحوّل نطق فعل من وزنه الفصيح إلى وزنه العامي أو الدارجي حسب جداول الدروس.', can_en='I can shift a verb from its Standard pronunciation to the colloquial or Darija one, following the lesson tables.', skill='speaking',
         ref_ar='اختاروا فعلاً واحداً وانطقوه بالصيغ الثلاث. أيها أصعب وكيف تتدربون عليه؟', ref_en='Choose one verb and say it in the three forms. Which is hardest and how will you practise it?'),
    dict(src=('u', '1', 4), can_ar='أؤدي جملاً متتابعة الأصوات المتشابهة دون خطأ بسرعة معتدلة.', can_en='I can perform sentences of similar-sounding words without error at a moderate pace.', skill='speaking',
         ref_ar='كم محاولة احتجتم لتقولوا جملة التتابع بلا خطأ؟ ماذا فعلتم لتحسين ذلك؟', ref_en='How many attempts did you need to say a tongue twister without error? What helped?'),
    ]),
 '2': dict(rows=[
    dict(src=('b', 1031), can_ar='أسمع الأصوات الخاصة بالفصحى في نص طويل وأحدد الكلمات التي تحويها.', can_en='I can hear Standard Arabic sounds in a long text and pick out the words that contain them.', skill='listening',
         ref_ar='كم كلمة مميّزة وجدتموا في الاستماع الأول وكم في الثاني؟', ref_en='How many distinctive words did you find on the first listening and how many on the second?'),
    dict(src=('b', 1032), can_ar='أنطق الأصوات الخاصة بالفصحى في نص طويل.', can_en='I can pronounce Standard Arabic sounds in a long text.', skill='reading aloud',
         ref_ar='أي مقطع من النص أخطأتم فيه أكثر، ولماذا؟', ref_en='Which part of the text did you get wrong most, and why?'),
    dict(src=('b', 1033), can_ar='أنطق كلمة منفردة بعد أن لاحظتها في السياق، مع صوتها ونبرها.', can_en='I can say a word on its own after noticing it in context, with its sound and stress.', skill='speaking',
         ref_ar='اختاروا كلمة تحدٍّ وانطقوها منفردة وفي جملة. هل يتغير النبر؟', ref_en='Choose a challenge word and say it alone and in a sentence. Does the stress change?'),
    dict(src=('b', 1034), can_ar='أميّز النبر الطويل بالسمع وأنطقه في كلمة منفردة وجملة ونص.', can_en='I can hear long stress and produce it in a single word, a sentence and a text.', skill='speaking',
         ref_ar='سجّلوا جملة طويلة وحددوا أين رفعتم الصوت. هل كان ذلك مقصوداً؟', ref_en='Record a long sentence and mark where you raised your voice. Was it intended?'),
    dict(src=('b', 1035), can_ar='ألاحظ التنغيم وأؤديه في جمل طويلة.', can_en='I can notice intonation and reproduce it in long sentences.', skill='speaking',
         ref_ar='قارنوا تنغيم جملة خبرية وأخرى استفهامية من النصوص. ما الفرق؟', ref_en='Compare the intonation of a statement and a question from the texts. What is the difference?'),
    dict(src=('u', '2', 0), can_ar='أنطق نصاً طويلاً يحوي صوتاً معيناً بحركاته ونبره، وأتابع التنغيم.', can_en='I can read a long text containing a given sound with its vowels and stress, and follow its intonation.', skill='reading aloud',
         ref_ar='سجّلوا فقرة من أحد النصوص وقارنوها بالأصل. أين اختلف التنغيم؟', ref_en='Record a paragraph from one of the texts and compare it with the original. Where did intonation differ?'),
    dict(src=('u', '2', 1), can_ar='ألاحظ التنغيم سمعاً وأتدرب على أدائه نطقاً.', can_en='I can notice intonation by ear and practise performing it.', skill='speaking',
         ref_ar='ما الجملة التي نجح تنغيمها عندكم؟ كيف عرفتم؟', ref_en='Which sentence did you get the intonation right on? How did you know?'),
    dict(src=('b', 1039), can_ar='أسمع الأصوات الخاصة بالعامية في نص طويل (الدرس السابع).', can_en='I can hear colloquial sounds in a long text (Lesson 7).', skill='listening',
         ref_ar='أي أصوات عامية وجدتموها أصعب في الاستماع؟', ref_en='Which colloquial sounds were hardest to catch?'),
    dict(src=('b', 1047), can_ar='أسمع الأصوات الخاصة بالدارجة في نص طويل (الدرس الثامن).', can_en='I can hear Darija sounds in a long text (Lesson 8).', skill='listening',
         ref_ar='ما الأصوات التي لاحظتم أنها تختلف عن العامية المصرية؟', ref_en='Which sounds did you notice differ from Egyptian colloquial?'),
    ]),
}
MAP_NOTE = ('هذه خريطة للتأمل الذاتي وليست شهادة ولا اختباراً. العبارات المقتبسة أهداف المادة كما وردت في الملف المصدري، والباقي إضافة تعليمية.',
            'This map is for self-reflection, not a certificate or a test. The quoted lines are the course objectives from the supplied file; the rest is an educational addition.')
SELF_LEVELS = [('0', 'لم أبدأ', 'Not started'), ('1', 'أحتاج مساعدة', 'With help'), ('2', 'أحياناً', 'Sometimes'), ('3', 'غالباً', 'Usually'), ('4', 'بثقة', 'Confidently')]

# ---------------------------------------------------------------------------------------------------------------------
FINAL = {
 '1': dict(
    title_ar='المهمة الختامية للوحدة الأولى: ملف النطق', title_en='Unit 1 final task: a pronunciation portfolio',
    brief_ar='أعدّوا ملفاً صوتياً قصيراً يجمع ما تدربتم عليه. يستعمل الملف أدوات المادة نفسها: التسجيل مع التغذية الراجعة المتأخرة، وتقييم الدقة من 1 إلى 10، والتسجيل التصحيحي.',
    brief_en='Prepare a short audio portfolio of what you have practised. It uses the course\'s own tools: recording with delayed feedback, rating accuracy from 1 to 10, and a corrective recording.',
    steps=[('اختاروا صوتين من أصوات الوحدة (أحدهما كان صعباً عليكم).', 'Choose two sounds from the unit (one that was hard for you).'),
           ('سجّلوا خمس كلمات لكل صوت منفردة، ثم جملة تتابع صعبة واحدة.', 'Record five words per sound, then one tongue twister.'),
           ('سجّلوا مقطعاً من أحد النصوص (أبو فراس أو المتنبي أو المهلهل).', 'Record a passage from one of the texts (Abū Firās, al-Mutanabbī or al-Muhalhil).'),
           ('قيّموا كل تسجيل من 1 إلى 10 وسجّلوا تسجيلاً تصحيحياً للأضعف.', 'Rate each recording from 1 to 10 and make a corrective recording of the weakest.'),
           ('اعرضوا الملف على زميل واطلبوا ملاحظة واحدة عن النبر وأخرى عن الصوت.', 'Share it with a classmate and ask for one comment on stress and one on a sound.')],
    check=[('سجّلتُ كل ما هو مطلوب.', 'I recorded everything required.'), ('قيّمت نطقي وكتبت ملاحظتين.', 'I rated myself and wrote two comments.'),
           ('أعدتُ تسجيل الجزء الأضعف.', 'I re-recorded the weakest part.'), ('حصلتُ على ملاحظة من زميل.', 'I received a classmate\'s comment.')]),
 '2': dict(
    title_ar='المهمة الختامية للوحدة الثانية: بيان وإلقاء', title_en='Unit 2 final task: write and deliver a statement',
    brief_ar='تجمع هذه المهمة بين تمرينين وردا في الملف: كتابة بيان قصير وإلقائه في الصف، ثم إلقاء جزء من إحدى القصيدتين.',
    brief_en='This task joins two exercises from the file: writing a short statement and delivering it in class, then reciting part of one of the two poems.',
    steps=[('اكتبوا بياناً قصيراً (خمس جمل أو أكثر) بالفصحى عن موضوع تختارونه.', 'Write a short statement (five sentences or more) in Standard Arabic on a topic you choose.'),
           ('حدّدوا في بيانكم الكلمات التي فيها أصوات خاصة بالعربية وقسّموها إلى مقاطع.', 'Mark the words containing Arabic-specific sounds in your statement and divide them into syllables.'),
           ('تدربوا على إلقائه مع التنغيم المناسب ثم قدّموه أمام الصف.', 'Rehearse it with suitable intonation, then deliver it to the class.'),
           ('اختاروا جزءاً من قصيدة «الغزال فاطمة» وألقوه مع الانتباه إلى أصوات الدارجة.', 'Choose a part of "Al-Ghazāl Fāṭima" and recite it, attending to the Darija sounds.'),
           ('قيّموا إلقاءكم وسجّلوا نقطتين تريدون تحسينهما.', 'Evaluate your delivery and note two points to improve.')],
    check=[('كتبتُ البيان وحددتُ الكلمات.', 'I wrote the statement and marked the words.'), ('ألقيتُ البيان أمام الصف.', 'I delivered it to the class.'),
           ('تدربتُ على جزء من القصيدة المغربية.', 'I practised part of the Moroccan poem.'), ('كتبتُ نقطتين للتحسين.', 'I wrote two points to improve.')]),
}

# ---------------------------------------------------------------------------------------------------------------------
# Phonetics page: cloze exercise built from the course's own bullets (the `src` block holds the evidence shown in the feedback).
CLOZE = [
 dict(ar='عند نطق /ص/ الأحبال الصوتية ___.', en='For /ṣ/ the vocal folds ___.', opts=['تهتز', 'لا تهتز'], ok=1, src=89, id='ص'),
 dict(ar='عند نطق /ض/ الأحبال الصوتية ___.', en='For /ḍ/ the vocal folds ___.', opts=['تهتز', 'لا تهتز'], ok=0, src=143, id='ض'),
 dict(ar='عند نطق /ط/ لا يوجد اهتزاز، لكن وسط اللسان يكون ___.', en='For /ṭ/ there is no vibration, but the middle of the tongue is ___.', opts=['مقعراً', 'مسطحاً'], ok=0, src=216, id='ط'),
 dict(ar='في نطق /ظ/ يكون طرف اللسان ___.', en='For /ẓ/ the tip of the tongue is ___.', opts=['بين الأسنان', 'خلف الأسنان العليا'], ok=0, src=294, id='ظ'),
 dict(ar='عند نطق /ق/ ___ هواء من الفم.', en='For /q/ ___ air comes out of the mouth.', opts=['يخرج', 'لا يخرج'], ok=1, src=426, id='ق'),
 dict(ar='صوت /غ/ ينطق بشكل ___.', en='The sound /ɣ/ is produced in a ___ way.', opts=['مستمر', 'انفجاري'], ok=0, src=707, id='غ'),
 dict(ar='في /ر/ ___ اللسان من فوق لتحت بسرعة.', en='In /r/ the tongue ___ quickly up and down.', opts=['يهتز', 'يثبت'], ok=0, src=922, id='ر'),
 dict(ar='في /ل/ المرققة آخر اللسان ___.', en='In non-emphatic /l/ the back of the tongue is ___.', opts=['لا يرتفع', 'يرتفع'], ok=0, src=837, id='ل'),
]

# extra comparison expressions for the phonetics page
PHON_EXPR = [
 ('تختلف الفصحى عن العامية في…', 'Standard Arabic differs from the colloquial in…'),
 ('كلا الصوتين لهما نفس المخرج تقريباً، لكن…', 'Both sounds have roughly the same place of articulation, but…'),
 ('الفرق بين الصوتين هو أن أحدهما…', 'The difference between the two sounds is that one…'),
]

# feature grouping of the sounds (educational organisation; the descriptions themselves are the course's bullets, pulled from the source)
PHON_GROUPS = [
 ('المفخمات', 'The emphatics', ['1.1', '1.2', '1.3', '1.4']),
 ('الأصوات الخلفية والحلقية', 'Back and pharyngeal sounds', ['2.1', '2.2', '3.1', '4.1', '4.2']),
 ('اللام والراء', 'Lām and rāʾ', ['5.1', '5.2']),
]
PHON_HOW = {  # item -> source block of its "how do you pronounce" heading (bullets follow)
    '1.1': 85, '1.2': 139, '1.3': 213, '1.4': 293, '2.1': 423, '2.2': 498, '3.1': 599, '4.1': 705, '4.2': (771, 775), '5.1': 835, '5.2': 917}
