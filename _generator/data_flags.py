# -*- coding: utf-8 -*-
"""Source problems found in the supplied Word file. NOTHING here edits the source: the generator keeps the original text,
shows a visible flag next to it and lists the proposed correction in the report.
Each flag: block index in source.json, the exact substring in that block (or in a cell of that table), note (EN), fix (proposed).
Found by reading the file and by automatic checks; the list is NOT exhaustive."""
F=lambda b,t,note,fix: dict(block=b,text=t,note=note,fix=fix)
FLAGS=[
 # --- typos in headings / instructions -----------------------------------------------------------------------------
 F(113,'لسياقات','Table header: stray first letter.','السياقات'),
 F(325,'لزاي','Table header: missing alif-lām article.','الزاي'),
 F(306,'ااستمعوا','Doubled alif.','استمعوا'),
 F(778,'اشاهدوا','Extra alif before the imperative.','شاهدوا'),
 F(854,'اشاهدوا','Extra alif before the imperative.','شاهدوا'),
 F(484,'الساس','Typo in the exercise number.','السادس'),
 F(507,'صوت "ق"','This exercise is about the sound ḥā’ (ح) but names qāf (ق).','صوت "ح"'),
 F(793,'"ع" و "ء"','This exercise is about kh / gh, but the instruction names ʿayn / hamza (copied from the previous lesson).','"خ" و "غ"'),
 F(345,'لصوت "ط التأثيرات','Heading is garbled: two headings run together and a closing quotation mark is missing.','التأثيرات الصوتية لصوت "ظ"'),
 F(262,'إستمعوا إلى التسجيل الرابع','Exercise 14 refers to "recording four"; the recordings of this exercise are numbered fourteen.','إلى التسجيل الرابع عشر'),
 F(1099,'التمرين التاسع','In Lesson 6 the exercise sequence jumps to "ninth"; the preceding exercise is the second.','التمرين الثالث'),
 F(676,'التامن','Dialect spelling / typo.','الثامن'),
 F(1044,'التامن','Dialect spelling / typo.','الثامن'),
 F(1087,'سجلوه الكلمات','Typo (verb form).','سجلوا الكلمات'),
 F(1029,'اصلي','Missing hamza.','أصلي'),
 F(1146,'ثراث','Typo.','تراث'),
 F(1095,'آطمئن','Alif-madda instead of hamza on alif.','أطمئن'),
 F(87,'not spread""','Stray double quotation marks.','not spread'),
 F(231,'ق ا','Stray letters before the picture (probably a left-over label).','(delete)'),
 # --- timestamps and cross-references -----------------------------------------------------------------------------
 F(863,'3:2','Ambiguous time ("3:2" could be 3:02 or 3:20); also a stray letter "ا" before "و". Frame check of the video: the emphatic/non-emphatic comparison slide appears at about 4:05.','Give the time as mm:ss (e.g. 3:20) and delete the stray "ا"'),
 F(932,'اللام المرققه','The video named here for the sound rā’ shows the articulation of rā’ at 1:00 (frame check), not lām.','"الراء"'),
 F(932,'5:3','Time written as "5:3". Frame check: the emphatic/non-emphatic comparison slide appears at 5:03.','5:03'),
 # --- verb-pattern labels ---------------------------------------------------------------------------------------
 F(558,'احْتَلَّ','احتلّ is Form VIII (افتعلّ), but the row is labelled Form IX (افعلّ).','Move to the Form VIII row, or choose a Form IX verb such as احمرّ'),
 F(749,'اغْتَرَّ','اغترّ is Form VIII (افتعلّ), but the row is labelled Form IX (افعلّ).','Move to Form VIII'),
 F(997,'اسْتَقَرَّ','استقرّ is Form X (استفعلّ), but the row is labelled Form IX (افعلّ).','Move to Form X'),
 # --- vocalisation / transcription artefacts in tables -----------------------------------------------------
 F(817,'بخ\u0651\u064bر','Tanwīn sign (ً) typed instead of fatḥa.','بَخَّرَ'),
 F(379,'قصًّرْ','Tanwīn sign (ً) typed instead of fatḥa.','قَصَّرْ'),
 F(386,'اسْتًطْرَدْ','Tanwīn sign (ً) typed instead of fatḥa.','اسْتَطْرَدْ'),
 F(386,'اسْتَطْردَ','Missing fatḥa on the rā’.','اسْتَطْرَدَ'),
 F(386,'Ŧa:læbæ','Capital Ŧ is used here but lower-case ŧ elsewhere for the same sound.','ŧa:læbæ'),
 F(558,'ħaṣaỊa','"Ị" (I with dot) typed instead of "l".','ħaṣala'),
 F(558,'ħaṣaỊ','"Ị" (I with dot) typed instead of "l".','ħaṣal'),
 F(558,'daħħak','ḍād is written đ in the Form-IV row but d here.','đaħħak'),
 F(658,'rsælaʕæ','Transcription of أرسل lacks the initial ʔ and the second vowel does not match.','ʔærsælæ'),
 F(658,'dʔæʕæ','Transcription of colloquial قعد is garbled (compare ʔæʕʕæd in the next row).','ʔæʕæd'),
 F(658,'ʔetwæʕʕd','Missing vowel e before the final d.','ʔetwæʕʕed'),
 F(890,'إتكلّ','Colloquial form of تكلّم lacks the letter mīm.','إتكلّم'),
 F(997,'تَكَسر','Missing shadda: the colloquial form on the same row is إتْكَسَّرْ.','تَكَسَّر'),
 F(486,'qaran','Long vowel not marked, unlike the other tables (qa:ran / qa:ren).','qa:ran'),
 F(817,'Xæbæzæ','Capital X vs lower-case x for the same sound within the table.','xæbæzæ'),
 F(997,'ra: dᴣæʕæ','Stray space inside the transcription.','ra:dᴣæʕæ'),
 # --- context tables ----------------------------------------------------------------------------------------
 F(259,'اطلق','The context label is أطْ, but the words are written without the hamza (أطلق، أطعم، أطول).','أطلق / أطعم / أطول'),
 F(457,'سبق','The word سبق is listed under both قَ and قْ; its qāf is final, so only the second listing fits.','keep under قْ only'),
 F(882,'لعل','The word لعل is listed under both لَ and ل (final); only one position can be meant for a given letter.','keep one listing'),
 F(958,'قٌرْأن','Tanwīn/ḍamma typed oddly; the usual form is قُرْآن.','قُرْآن'),
 F(958,'غٌ','Tanwīn sign typed instead of ḍamma.','غُرَّة'),
 F(958,'رْجارْ','Word not recognised in the lists; possibly a typing slip.','(author to confirm)'),
 # --- verses --------------------------------------------------------------------------------------------------------
 F(912,'لًحَاليح','The vocalised version contains tanwīn signs (ً) that look like typing artefacts; compare the unvocalised sentence in the same lesson.','سبع لَحاليح اسْتَلَحْلَحْناهم …'),
 F(417,'أما للهوى','Table cell order: in the file the second hemistich is the first cell of each row. The book prints the hemistichs in poetic order (first hemistich first), as the page looks when the Word file is rendered.','(layout only)'),
]
