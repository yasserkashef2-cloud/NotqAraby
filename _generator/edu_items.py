# -*- coding: utf-8 -*-
"""EDUCATIONAL ADDITIONS for each item: intro, pre-tasks, six open questions (typed), cultural prompts, notes.
Everything in this file is written for this book; none of it is part of the supplied course materials.
`go` targets:  m:<media id>  |  b:<source block index>  |  p:1095:<n> (paragraph n of the statement)  |  yt:<source block of the link>
`ts` (optional) = a time that IS stated in the course file."""

QTYPES = {
    'gen':   ('فهم عام', 'General understanding'),
    'det':   ('تفصيل داعم', 'Supporting detail'),
    'interp': ('تفسير', 'Interpretation'),
    'infer': ('استنتاج', 'Inference'),
    'lang':  ('تحليل لغوي', 'Language analysis'),
    'comp':  ('مقارنة', 'Comparison'),
    'eval':  ('تقويم', 'Evaluation'),
}


def Q(t, ar, en, go=None, ts=None):
    return dict(t=t, ar=ar, en=en, go=go, ts=ts)


# ---------------------------------------------------------------------------------------------------------------------
# sound items: question set built from a template + sound-specific names, using only media that exist for the item
SOUNDS = {
    # id: (name_ar, name_en, contrast_ar, contrast_en, media-prefix, roles available, first block)
    '1.1': ('ص', 'ṣād', 'س', 'sīn', 'l1-sad', ['video', 'sustained', 'pairs', 'contexts', 'effects'], 85),
    '1.2': ('ض', 'ḍād', 'د', 'dāl', 'l1-dad', ['video', 'sustained', 'pairs', 'contexts', 'effects'], 139),
    '1.3': ('ط', 'ṭāʾ', 'ت', 'tāʾ', 'l1-ta', ['video', 'sustained', 'pairs', 'contexts', 'effects'], 213),
    '1.4': ('ظ', 'ẓāʾ', 'ذ', 'dhāl', 'l1-za', ['video', 'sustained', 'pairs', 'contexts', 'effects'], 293),
    '2.1': ('ق', 'qāf', 'ك', 'kāf', 'l2-qaf', ['video', 'sustained', 'pairs', 'contexts', 'verbs', 'twister'], 423),
    '2.2': ('ح', 'ḥāʾ', 'هـ', 'hāʾ', 'l2-ha', ['video', 'sustained', 'pairs', 'contexts', 'verbs'], 498),
    '3.1': ('ع', 'ʿayn', 'ء', 'hamza', 'l3-ayn', ['video', 'sustained', 'pairs', 'contexts', 'verbs'], 599),
    '4.1': ('غ', 'ghayn', 'خ', 'khāʾ', 'l4-ghayn', ['video', 'sustained', 'contexts', 'verbs'], 705),
    '4.2': ('خ', 'khāʾ', 'غ', 'ghayn', 'l4-kha', ['video', 'sustained', 'pairs', 'contexts', 'verbs'], 769),
    '5.1': ('ل', 'lām', 'ر', 'rāʾ', 'l5-lam', ['video', 'sustained', 'pairs', 'contexts', 'verbs'], 835),
    '5.2': ('ر', 'rāʾ', 'ل', 'lām', 'l5-ra', ['video', 'sustained', 'pairs', 'contexts', 'verbs', 'combos'], 917),
}


def sound_questions(iid):
    n_ar, n_en, c_ar, c_en, pre, roles, first = SOUNDS[iid]
    m = lambda r: ('m:%s-%s' % (pre, r)) if r in roles else ('b:%d' % first)
    qs = [
        Q('gen', 'شاهدوا فيديو المخرج: ما الذي تلاحظونه في وضع اللسان والشفتين عند نطق /%s/؟ صفوه بكلماتكم قبل أن تقرأوا الوصف المكتوب.' % n_ar,
          'Watch the articulation video: what do you notice about the tongue and lips for /%s/? Describe it in your own words before reading the written description.' % n_ar, m('video')),
        Q('det', 'اختاروا ثلاث كلمات من تسجيل الكلمات الفارقة أو من الجدول، وحدّدوا في كل واحدة منها الفرق الذي تسمعونه بين /%s/ و/%s/.' % (n_ar, c_ar),
          'Pick three words from the minimal-pair recording or table and say, for each, what difference you hear between /%s/ and /%s/.' % (n_ar, c_ar), m('pairs') if 'pairs' in roles else 'b:%d' % first),
        Q('interp', 'في تمرين النطق المستمر، أين تشعرون بالتوتر في الفم أو الحلق؟ وكيف يختلف هذا الإحساس عن نطق /%s/؟' % c_ar,
          'In the sustained-sound exercise, where do you feel tension in the mouth or throat, and how does that differ from /%s/?' % c_ar, m('sustained')),
        Q('infer', 'هل يتغير نطق الأصوات المجاورة لـ/%s/ حسب موقعه في الكلمة؟ استمعوا إلى تسجيل السياقات وقدّموا دليلاً من كلمتين.' % n_ar,
          'Do the neighbouring sounds change depending on where /%s/ sits in the word? Listen to the contexts recording and support your answer with two words.' % n_ar, m('effects') if 'effects' in roles else m('contexts')),
        Q('lang', ('في جدول الأوزان قارنوا نطق فعل واحد في الفصحى وفي العامية: ما الذي تغيّر في الصوت /%s/ أو حوله؟' % n_ar) if 'verbs' in roles else
          'اختاروا كلمتين من قوائم الكلمات وقسّموهما إلى مقاطع، ثم حدّدوا المقطع الذي يقع فيه /%s/.' % n_ar,
          ('In the verb table compare one verb in Standard Arabic and in the colloquial: what changes in /%s/ or around it?' % n_ar) if 'verbs' in roles else
          'Choose two words from the word lists, divide them into syllables, and say in which syllable /%s/ falls.' % n_ar,
          m('verbs') if 'verbs' in roles else 'b:%d' % first),
        Q('eval', 'سجّلوا خمس كلمات فيها /%s/ وقيّموا دقة نطقكم من 1 إلى 10 كما يطلب التمرين. ما الكلمة الأصعب، وما الذي ستفعلونه لتحسينها؟' % n_ar,
          'Record five words containing /%s/ and rate your accuracy from 1 to 10, as the exercise asks. Which word was hardest, and what will you do to improve it?' % n_en, m('sustained')),
    ]
    return qs


def sound_culture(iid):
    n_ar, n_en, c_ar, c_en = SOUNDS[iid][:4]
    return [dict(ar='فكّروا في لغتكم الأولى أو في لغة تعرفونها جيداً: هل لها صوت يُنطق بطرق مختلفة بين المناطق أو الأجيال أو الأشخاص؟ اذكروا مثالاً محدداً واحداً (كلمة وطريقتي نطق).',
                 en='Think of your first language or another you know well: does it have a sound pronounced in different ways across regions, generations or individuals? Give one specific example (a word and two pronunciations).')]


INTROS = {
    '1.1': ('تتناول هذه الفقرة الصاد /ص/ مقارنةً بالسين، وفيها فيديو للمخرج وتسجيلات للنطق المستمر والكلمات الفارقة والسياقات.',
            'This section works on ṣād /ṣ/ against sīn, with an articulation video and recordings for sustained sound, minimal pairs and contexts.'),
    '1.2': ('تتناول هذه الفقرة الضاد /ض/ مقارنةً بالدال، مع فيديو المخرج وتسجيلات التمارين.',
            'This section works on ḍād /ḍ/ against dāl, with the articulation video and exercise recordings.'),
    '1.3': ('تتناول هذه الفقرة الطاء /ط/ مقارنةً بالتاء، مع فيديو المخرج وتسجيلات التمارين.',
            'This section works on ṭāʾ /ṭ/ against tāʾ, with the articulation video and exercise recordings.'),
    '1.4': ('تتناول هذه الفقرة الظاء /ظ/ مقارنةً بالذال والثاء والزاي في السياقات.',
            'This section works on ẓāʾ /ẓ/ against dhāl, thāʾ and zāy in context.'),
    '1.5': ('هنا تنتقلون من الأصوات المفردة إلى الأفعال: كيف تتحول أوزان الأفعال التي فيها مفخمات من الفصحى إلى العامية. استمعوا إلى التسجيل وقارنوا الأعمدة.',
            'Here you move from single sounds to verbs: how verb patterns containing emphatics change from Standard Arabic to the colloquial. Listen, then compare the columns.'),
    '1.6': ('استماع إلى مقطع من برنامج «عصير الكتب» (الدقائق 0:00–2:00). المطلوب هنا هو الاستماع وتدريب النطق، لا قراءة نص جاهز.',
            'A listening exercise on a clip from the programme "Aṣīr al-Kutub" (minutes 0:00–2:00). The task is to listen and practise pronunciation, not to read a ready-made text.'),
    '1.7': ('أبيات من «أراك عصيّ الدمع» لأبي فراس الحمداني، للتدرّب على نطق المفخمات في الشعر الفصيح بعد الاستماع إلى الإلقاء.',
            'Verses from "Arāka ʿaṣiyya d-damʿ" by Abū Firās al-Ḥamdānī, for practising the emphatics in classical verse after listening to the recitation.'),
    '2.1': ('تتناول هذه الفقرة القاف /ق/ مقارنةً بالكاف، وتنتهي بجملة تتابع صوتي صعبة (قبر – حرب).',
            'This section works on qāf /q/ against kāf and ends with a tongue twister.'),
    '2.2': ('تتناول هذه الفقرة الحاء /ح/ مقارنةً بالهاء، وتنتهي بأبيات للمهلهل بن ربيعة للتدرّب على الحاء والهاء معاً.',
            'This section works on ḥāʾ /ħ/ against hāʾ and ends with verses by al-Muhalhil ibn Rabīʿa for practising ḥ and h together.'),
    '3.1': ('تتناول هذه الفقرة العين /ع/ مقارنةً بالهمزة، مع فيديو المخرج وتسجيلات التمارين.',
            'This section works on ʿayn /ʕ/ against the hamza, with the articulation video and exercise recordings.'),
    '4.1': ('تتناول هذه الفقرة الغين /غ/ في كلمات وسياقات وأفعال، مع فيديو المخرج.',
            'This section works on ghayn /ɣ/ in words, contexts and verbs, with the articulation video.'),
    '4.2': ('تتناول هذه الفقرة الخاء /خ/ مقارنةً بالغين، مع فيديو المخرج وتسجيلات التمارين.',
            'This section works on khāʾ /x/ against ghayn, with the articulation video and exercise recordings.'),
    '5.1': ('تتناول هذه الفقرة اللام المرققة والمفخمة، وتضم أبياتاً منسوبة إلى الإمام علي بن أبي طالب وجملة تتابع صوتي صعبة.',
            'This section works on non-emphatic and emphatic lām, with verses attributed to Imam ʿAlī ibn Abī Ṭālib and a tongue twister.'),
    '5.2': ('تتناول هذه الفقرة الراء /ر/ المكررة المرققة والمفخمة، وتنتهي بأبيات للمتنبي وأغنية للتدرّب في الصف.',
            'This section works on the trilled rāʾ /r/, non-emphatic and emphatic, and ends with verses by al-Mutanabbī and a song for class practice.'),
    '6.1': ('البيان الذي أُذيع في 23 يوليو 1952، بصوت الرئيس الراحل محمد أنور السادات كما في الملف. نص طويل بالفصحى لتدريب النطق والنبر والتنغيم.',
            'The statement broadcast on 23 July 1952, in the voice of the late President Muhammad Anwar al-Sadat as the file states. A long Standard Arabic text for pronunciation, stress and intonation.'),
    '7.1': ('قصيدة بالعامية المصرية الحديثة لهشام الجخ. نصها محجوب هنا لأنه نص حديث محمي، فاستمعوا إليها من الرابط.',
            'A modern poem in Egyptian colloquial by Hesham al-Gakh. Its text is not reproduced here because it is modern and protected; listen through the link.'),
    '8.1': ('أغنية من تراث الملحون المغربي، من نظم إدريس بن علي، بالدارجة المغربية.',
            'A song from the Moroccan Malḥūn tradition, composed by Idrīs ibn ʿAlī, in Moroccan Darija.'),
}

PRE = {
    'sound': [('قبل الاستماع: ضعوا يدكم أمام فمكم وانطقوا /%s/ ثم /%s/. ماذا تلاحظون؟', 'Before listening: put a hand in front of your mouth and say /%s/ then /%s/. What do you notice?')],
}


def sound_pre(iid):
    n_ar, n_en, c_ar, c_en = SOUNDS[iid][:4]
    return [dict(ar='قبل الاستماع: انطقوا /%s/ ثم /%s/ وضعوا يدكم أمام فمكم. ماذا تلاحظون في كمية الهواء وفي الإحساس بالحلق؟' % (n_ar, c_ar),
                 en='Before listening: say /%s/ then /%s/ with a hand in front of your mouth. What do you notice about the air and about the throat?' % (n_ar, c_ar)),
            dict(ar='توقّعوا: أي الصوتين ستجدونه أصعب في الكلمات؟ ولماذا؟', en='Predict: which of the two sounds will be harder in words, and why?')]


# ---------------------------------------------------------------------------------------------------------------------
# hand-written sets for the non-template items
TEXT = {}

TEXT['1.5'] = dict(
    pre=[dict(ar='قبل الاستماع: انظروا إلى عمود الفصحى وعمود العامية في الجدول، واكتبوا فعلاً واحداً تتوقعون أن يتغير نطقه.', en='Before listening: look at the Standard and colloquial columns and note one verb whose pronunciation you expect to change.')],
    qs=[Q('gen', 'ما الفكرة العامة للتسجيل: ماذا يحدث للفعل عند الانتقال من الفصحى إلى العامية؟', 'What is the general idea of the recording: what happens to a verb when moving from Standard Arabic to the colloquial?', 'm:l1-verbs'),
        Q('det', 'اختاروا فعلين من الجدول واكتبوا ما يتغير في الصوت المفخم فيهما.', 'Choose two verbs from the table and write what changes in their emphatic sound.', 'b:379'),
        Q('interp', 'لماذا تظنون أن الجدول يضع النطق الصوتي بجانب الكتابة؟ كيف يساعدكم ذلك؟', 'Why do you think the table puts a phonetic transcription next to the spelling? How does it help you?', 'b:382'),
        Q('infer', 'هل يمكنكم استنتاج قاعدة من فعلين تتغير فيهما الحركات بالطريقة نفسها؟ اذكروا الفعلين وصيغوا القاعدة.', 'Can you infer a rule from two verbs that change in the same way? Name them and state the rule.', 'b:386'),
        Q('lang', 'استمعوا إلى النبر في الأفعال: في أي مقطع يقع في الفصحى وفي العامية؟', 'Listen to the stress in the verbs: on which syllable does it fall in Standard and in the colloquial?', 'm:l1-verbs'),
        Q('eval', 'ما الفعل الذي يصعب عليكم نطقه في العامية؟ سجّلوه ثلاث مرات وقارنوا.', 'Which verb is hardest for you in the colloquial? Record it three times and compare.', 'm:l1-verbs')],
    cult=[dict(ar='هل يتكلم من حولكم عاميات أو لهجات متعددة؟ صفوا موقفاً محدداً سمعتم فيه فعلاً واحداً بنطقين مختلفين.', en='Do people around you speak several colloquials or dialects? Describe one specific moment when you heard one verb pronounced two ways.')],
)

TEXT['1.6'] = dict(
    pre=[dict(ar='قبل الاستماع: ماذا تتوقعون أن يقول مقدّم برنامج عن الكتب في أول دقيقتين؟ اكتبوا ثلاث كلمات تتوقعونها.', en='Before listening: what do you expect a book-programme host to say in the first two minutes? Write three words you expect.'),
         dict(ar='الاستماع الأول للفكرة العامة فقط، والثاني للتفاصيل.', en='First listening for the gist only, second for details.')],
    qs=[Q('gen', 'عن ماذا يتحدث المقدّم في الدقيقتين الأوليين؟ لخّصوا في جملتين.', 'What is the host talking about in the first two minutes? Summarise in two sentences.', 'm:l1-bilal', '0:00'),
        Q('det', 'اكتبوا ثلاث كلمات سمعتموها وفيها صوت مفخم (ص ض ط ظ) وكيف نطقها المتحدث.', 'Write three words you heard containing an emphatic (ṣ ḍ ṭ ẓ) and how the speaker pronounced them.', 'm:l1-bilal', '0:00'),
        Q('interp', 'كيف تصفون نبرة المتحدث (جادّة، ساخرة، دافئة…)؟ ما الذي في صوته يدل على ذلك؟', 'How would you describe the speaker\'s tone (serious, ironic, warm…)? What in his voice shows that?', 'm:l1-bilal', '0:00'),
        Q('infer', 'ما نوع اللغة التي يتكلم بها: فصحى خالصة أم عامية أم مزيج؟ دلّوا بكلمتين.', 'What kind of language does he speak: pure Standard, colloquial, or a mixture? Show with two words.', 'm:l1-bilal', '2:00'),
        Q('lang', 'اختاروا جملة سمعتموها وحلّلوا سرعة الكلام والوقفات والتنغيم فيها.', 'Choose a sentence you heard and analyse its speed, pauses and intonation.', 'm:l1-bilal', '0:00'),
        Q('eval', 'قيّموا من 1 إلى 10 مدى فهمكم للمقطع، وحدّدوا ما الذي أعاق الفهم: السرعة أم المفردات أم اللهجة؟', 'Rate from 1 to 10 how well you understood the clip and say what got in the way: speed, vocabulary or dialect.', 'm:l1-bilal', '2:00')],
    cult=[dict(ar='يتحدث البرنامج عن الكتب. كيف تصل الكتب إلى القراء في المكان الذي تعرفونه (مكتبات، معارض، إنترنت، استعارة بين الأصدقاء…)؟ اذكروا مثالاً محدداً من تجربتكم.', en='The programme is about books. How do books reach readers in a place you know (libraries, fairs, online, lending between friends…)? Give one specific example from your own experience.')],
)

TEXT['1.7'] = dict(
    pre=[dict(ar='قبل الاستماع: انظروا إلى الأبيات دون قراءتها بصوت عالٍ. أي الكلمات فيها صوت مفخم؟', en='Before listening: look at the verses without reading aloud. Which words contain an emphatic?'),
         dict(ar='استمعوا إلى الإلقاء أولاً ثم تدرّبوا في مجموعات كما يطلب التمرين.', en='Listen to the recitation first, then practise in groups as the exercise asks.')],
    qs=[Q('gen', 'ما الحالة العامة التي يعبّر عنها الأبيات: من يتكلم، ولمن، وبأي شعور؟', 'What general situation do the verses express: who is speaking, to whom, and with what feeling?', 'b:417'),
        Q('det', 'ماذا يقول الشاعر عن دمعه وعن صبره في البيتين الأول والثاني؟', 'What does the poet say about his tears and his patience in the first two lines?', 'b:417'),
        Q('interp', 'ما معنى أن يكون الدمع «عصيّاً» ثم يُذلَّل؟ كيف يبني الشاعر صورة التناقض؟', 'What does it mean for tears to be "obstinate" and then subdued? How does the poet build the contrast?', 'b:417'),
        Q('infer', 'ماذا نفهم من الأبيات عن مكانة الشاعر وعن نظرته إلى إظهار المشاعر؟', 'What do the verses tell us about the poet\'s standing and his view of showing feelings?', 'b:417'),
        Q('lang', 'اختاروا خمس كلمات فيها مفخمات من الأبيات واذكروا موضع الصوت المفخم في كل منها.', 'Choose five words with emphatics from the verses and give the position of the emphatic in each.', 'm:l1-abufiras'),
        Q('eval', 'قارنوا إلقاءكم بإلقاء المسجّل: أين اختلف النبر أو الإيقاع؟ وما الذي ستعدّلونه؟', 'Compare your delivery with the recorded one: where did stress or rhythm differ, and what will you change?', 'm:l1-abufiras')],
    cult=[dict(ar='هل تُلقى القصائد في الأماكن التي تعرفونها؟ متى وأين؟ صفوا مناسبة محددة حضرتموها أو سمعتم عنها.', en='Are poems recited in places you know? When and where? Describe one specific occasion you attended or heard about.'),
          dict(ar='يتحدث الأبيات عن إخفاء المشاعر. ما مواقف يُنتظر فيها من الناس إخفاء مشاعرهم أو إظهارها في مجتمعكم، وهل يختلف الناس في ذلك؟', en='The verses speak of hiding feelings. In your community, when are people expected to hide or show feelings, and do individuals differ?')],
)

TEXT['2.2'] = dict(
    extra_qs={
        4: Q('infer', 'في بيت المهلهل: ما الحدث الذي يُعلن؟ وما الذي يدل على تأثره به؟', 'In al-Muhalhil\'s verse: what event is announced, and what shows his reaction to it?', 'b:576'),
        5: Q('lang', 'استمعوا إلى إلقاء بيتي المهلهل: أين تسمعون الحاء والهاء في الكلمات؟ هل تحافظون على الفرق بينهما كما يطلب التمرين؟', 'Listen to the two verses of al-Muhalhil: where do you hear ḥ and h? Can you keep them distinct, as the exercise asks?', 'm:l2-muhalhil')},
    cult=[dict(ar='الأغنية والجملة الطويلة في آخر الفقرة تُستعمل للتسلية. هل لديكم ألعاب لغوية أو تراكيب صعبة النطق في لغتكم؟ اذكروا واحداً.', en='The song and long sentence at the end are for fun. Do you have tongue twisters or word games in your language? Name one.')],
)

TEXT['5.1'] = dict(
    extra_qs={
        4: Q('lang', 'اقرأوا أبيات الإمام علي أفقياً ثم رأسياً كما يطلب الملف: ماذا تلاحظون؟ ما أثر ذلك في التدريب على اللام؟', 'Read the verses attributed to Imam ʿAlī across and then down, as the file says: what do you notice, and how does it serve the lām drill?', 'b:901'),
        5: Q('interp', 'ما معنى الأبيات: من يلوم صديقه، وما التناقض الذي يعبّر عنه الشاعر؟', 'What do the verses mean: who blames a friend, and what contradiction does the poet express?', 'b:901')},
    cult=[dict(ar='تتناول الأبيات الصداقة واللوم. كيف يُعبَّر عن العتاب بين الأصدقاء في بيئة تعرفونها؟ اذكروا موقفاً محدداً أو عبارة معروفة.', en='The verses are about friendship and blame. How is reproach between friends expressed in a setting you know? Give one specific situation or well-known phrase.')],
)

TEXT['5.2'] = dict(
    extra_qs={
        4: Q('interp', 'في بيت المتنبي «أنا الذي نظر العمى إلى أدبي»: ما الصورة التي يرسمها الشاعر عن نفسه؟ كيف يبالغ؟', 'In al-Mutanabbī\'s line "I am the one whose literature even the blind can see": what image of himself does he draw, and how does he exaggerate?', 'b:1006'),
        5: Q('lang', 'استمعوا إلى فيديو المتنبي: أين تسمعون اللام والراء في الأبيات؟ حافظوا على الفرق بينهما كما يطلب التمرين.', 'Listen to the al-Mutanabbī video: where do you hear lām and rāʾ in the verses? Keep them distinct, as the exercise asks.', 'm:l5-mutanabbi')},
    cult=[dict(ar='يتحدث المتنبي عن نفسه بفخر كبير. متى يُعدّ التفاخر مقبولاً في بيئة تعرفونها ومتى لا يُقبل؟ اذكروا مثالاً محدداً، وهل يرى الناس في ذلك آراء مختلفة؟', en='Al-Mutanabbī speaks of himself with great pride. When is boasting acceptable in a setting you know and when not? Give a specific example — do people there differ in their views?')],
)

TEXT['6.1'] = dict(
    pre=[dict(ar='قبل الاستماع: ماذا تعرفون عن أحداث 23 يوليو 1952 في مصر؟ اكتبوا ما تعرفونه أو ما تتوقعون أن يرد في بيان أول يوم.', en='Before listening: what do you know about the events of 23 July 1952 in Egypt? Write what you know, or what you expect a first-day statement to contain.'),
         dict(ar='استمعوا إلى البيان مرة للفكرة العامة، ومرة أخرى لتحديد الكلمات التي فيها أصوات خاصة بالعربية.', en='Listen once for the gist and again to pick out words with sounds specific to Arabic.')],
    qs=[Q('gen', 'ما الرسالة الأساسية للبيان؟ لخّصوها في ثلاث جمل.', 'What is the statement\'s main message? Summarise it in three sentences.', 'p:1095:1'),
        Q('det', 'ما الأسباب التي يذكرها المتحدث لوصف الفترة السابقة؟ اذكروا ثلاثة.', 'What reasons does the speaker give to describe the previous period? Name three.', 'p:1095:1'),
        Q('interp', 'ماذا يقول البيان عن الجيش وما أُجري فيه؟ كيف يبرّر ذلك؟', 'What does the statement say about the army and what was done in it? How does it justify this?', 'p:1095:2'),
        Q('infer', 'لمن يتوجه الخطاب في الفقرة الأخيرة ولماذا؟ ماذا نستنتج من ذلك عن الجمهور المقصود؟', 'To whom does the last paragraph speak, and why? What does that suggest about the intended audience?', 'p:1095:5'),
        Q('lang', 'اختاروا خمس كلمات من البيان فيها أصوات خاصة بالعربية، وقسّموها إلى مقاطع، وحدّدوا موضع النبر.', 'Choose five words from the statement containing sounds specific to Arabic, divide them into syllables, and mark the stress.', 'p:1095:3'),
        Q('eval', 'كيف تقيّمون إلقاءكم للبيان من حيث الوضوح والتنغيم؟ سجّلوا فقرة واحدة وقارنوها بالأصل.', 'How do you rate your delivery of the statement in clarity and intonation? Record one paragraph and compare it with the original.', 'yt:1093')],
    cult=[dict(ar='للبيانات الرسمية الإذاعية أسلوب خاص في كل مكان. ما الذي يميّز أسلوب الإعلان الرسمي في سياق تعرفونه، وهل يتفق الناس على تقييمه؟ اذكروا مثالاً محدداً.', en='Official broadcast statements have a distinctive style everywhere. What marks the style of an official announcement in a setting you know, and do people agree about it? Give a specific example.'),
          dict(ar='البيان وثيقة تاريخية. كيف يمكن أن يختلف الناس في تقييم حدث واحد بعد عقود؟ اذكروا مثالاً من تاريخ تعرفونه، دون إصدار حكم على جماعة بأكملها.', en='The statement is a historical document. How can people differ in judging one event decades later? Give an example from a history you know, without judging a whole group.')],
)

TEXT['7.1'] = dict(
    pre=[dict(ar='قبل الاستماع: استمعوا إلى الإلقاء من الرابط دون نص مكتوب. حاولوا تحديد الموضوع والحالة الشعورية.', en='Before listening: listen to the recitation through the link without a written text. Try to identify the topic and the mood.')],
    qs=[Q('gen', 'ما موضوع القصيدة كما فهمتموه من الاستماع؟', 'What is the poem about, as you understood it from listening?', 'yt:1113'),
        Q('det', 'اكتبوا ثلاث عبارات أو كلمات سمعتموها وتتكرر أو تلفت الانتباه.', 'Write three words or phrases you heard that repeat or stand out.', 'yt:1113'),
        Q('interp', 'كيف يعبّر الإلقاء (الصوت، الإيقاع، الوقفات) عن المعنى؟', 'How does the delivery (voice, rhythm, pauses) express the meaning?', 'yt:1113'),
        Q('infer', 'ماذا نفهم عن العلاقة بين المتحدث والشخص الذي يخاطبه؟', 'What do we understand about the relationship between the speaker and the person addressed?', 'yt:1113'),
        Q('lang', 'اختاروا ثلاث كلمات عامية سمعتموها وفيها صوت من أصوات الوحدة الأولى، وقارنوها بنطقها في الفصحى.', 'Choose three colloquial words you heard containing a sound from Unit 1 and compare them with their Standard pronunciation.', 'yt:1113'),
        Q('eval', 'ما الأجزاء التي صعب عليكم فهمها أو نطقها؟ سجّلوا تصحيحياً كما يطلب التمرين وقيّموا التغيّر.', 'Which parts were hard to follow or pronounce? Make a corrective recording as the exercise asks and rate the change.', 'yt:1113')],
    cult=[dict(ar='الشعر العامي الحديث ينتشر اليوم عبر الفيديو. ما أشكال الأدب المنطوق التي يتابعها الناس في بيئة تعرفونها؟ اذكروا مثالاً محدداً.', en='Modern colloquial poetry circulates today through video. What forms of spoken literature do people follow in a setting you know? Give a specific example.')],
)

TEXT['8.1'] = dict(
    pre=[dict(ar='قبل الاستماع: ما تعرفونه عن الدارجة المغربية؟ أي أصوات تتوقعون أن تتغير عن الفصحى؟', en='Before listening: what do you know about Moroccan Darija? Which sounds do you expect to differ from Standard Arabic?')],
    qs=[Q('gen', 'ما الموضوع العام للقصيدة: من المتكلم ولمن يتوجه؟', 'What is the poem\'s general topic: who is the speaker and to whom does he speak?', 'b:1159'),
        Q('det', 'ماذا يطلب المتكلم من فاطمة في المطلع؟ وماذا يشتكي منه؟', 'What does the speaker ask of Fāṭima in the opening, and what does he complain of?', 'b:1159'),
        Q('interp', 'ما الصور التي يستعملها الشاعر لحبّه (النار، السقام، الشوق)؟ كيف تُقرأ هنا؟', 'What images does the poet use for his love (fire, sickness, longing)? How do they read here?', 'b:1159'),
        Q('infer', 'ماذا يفهم القارئ من ذكر «الرقيب» و«الحسود» في المقطع الثاني؟', 'What does the reader understand from the mention of "the watcher" and "the envious" in the second part?', 'b:1160'),
        Q('lang', 'اختاروا ثلاث كلمات دارجة من النص وقارنوها بالفصحى: ما الصوت الذي يتغير؟', 'Choose three Darija words from the text and compare them with Standard Arabic: which sound changes?', 'b:1159'),
        Q('eval', 'قيّموا إلقاءكم لجزء من القصيدة: هل حافظتم على إيقاع الأبيات والتنغيم؟ ماذا ستعدّلون؟', 'Rate your recitation of part of the poem: did you keep the rhythm and intonation? What will you adjust?', 'yt:1145')],
    cult=[dict(ar='الملحون فن غنائي شعري له جمهوره. ما الفنون الغنائية التقليدية التي ما زالت حيّة في بيئة تعرفونها، ومن يستمع إليها؟ اذكروا مثالاً محدداً، وهل تتنوع أذواق الناس في ذلك؟', en='Malḥūn is a sung poetic art with its own audience. Which traditional sung arts are alive in a setting you know, and who listens? Give a specific example — and do tastes vary?')],
)


def item_edu(iid):
    """returns dict(intro=(ar,en), pre=[...], qs=[...], cult=[...])"""
    intro = INTROS[iid]
    if iid in SOUNDS:
        qs = sound_questions(iid)
        t = TEXT.get(iid, {})
        for k, q in (t.get('extra_qs') or {}).items():
            qs[k] = q
        return dict(intro=intro, pre=sound_pre(iid), qs=qs, cult=sound_culture(iid) + t.get('cult', []))
    t = TEXT[iid]
    return dict(intro=intro, pre=t['pre'], qs=t['qs'], cult=t['cult'])


if __name__ == '__main__':
    for it in ['1.1', '1.5', '2.2', '6.1', '8.1']:
        e = item_edu(it)
        print(it, len(e['qs']), len(e['pre']), len(e['cult']))
