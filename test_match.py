# -*- coding: utf-8 -*-

from nose.tools import eq_

import match
from match.Match import _cleanup_text, _match_by_edit_distance


# Excepts from blog entries from the CBC/Corporati corpus: http://ynada.com/cbc-corporati/
test_text = """It'? ?s hard to believe but Dreamforce is less than a week away!In preparation for salesforce. com'? ?s biggest event of the year, we'? ?ve cataloged all 150 breakout sessions on the Successforce. com site.   During the conference you can use this guide to plan your day. You can navigate by track or choose between the various session offered during a given time slot. On the session detail pages you'? ?ll find a list of speakers and their respective companies. We also have a spot where you can leave comments about the session, or post questions you'? ?d like to see the presenter cover. (Dreamforce Comments Feed)To bring Dreamforce to those who can't make it, we try to post much of the content online. Last year we had over 50k downloads after the conference, and this year we expect a dramatic increase this year as we introduce video. In each of the 12 breakout rooms we'? ?ll be recording video so you can connect with the presenter and see all the amazing product demos. The first video will be posted on Wednesday October 11th with additional sessions posted to the site as they are produced. For those looking for immediate gratification, we are also planning on posting the PowerPoint slides and other resources referenced in the presentation on the session detail pages.  We'? ?ve got a fantastic week ahead. You won'? ?t want to miss it. Make your last minute travel plans and get registered today!Last Friday when the temperature resulted in an \air stagnation alert\ (I have no idea) . I should have been done on Saturday but had to add those few extra days back in (since the program is based on building on intervals) .I am happy to confirm that I ran for 28 minutes today (well, by running I mean jogging that looks slow but totally rocks my heart rate) . Tomorrow, I run thirty minutes and give myself a pat on the back (it's OK, I'm going to call it stretching) .  Happy Chinese New YearWishing everyone a HAPPY CHINESE NEW YEAR! Chapter One: Rise of the monkeyFor thousand of years , a stone had been absorbing the\ki\ of the heaven and earth , finally one day , it exploded and Mosaic Monkey ( M & M in short ) was borned. This crappy ideas of mosaic monkey (inspired by Monkey god and crayon shin) had been floating in my mind for a few months so finally today i decided to scanned 2 of sketches and make it into a illustration. More will come. ... Chapter two: Enter the monkeyMosaic Monkey decided to take down all the demons in the jungle to become the King of the jungle. Kazaaaaa! !! (* inspired by Bruce lee: enter the dragon )************************************************************************************Recently, i came across a advertisement on a bus stop, it wrote this \\No one can survive on the diets of hope! \ So true. ... ..Who can? ?"
"Filed under: AOLTed checks in on what people are calling the  \data Valdez. \ It so nice having Ted blogging, sometimes I feel like I'm alone on the front lines. I wish other senior executives would start blogging at AOL (hint, hint) --or at least commenting (you guys know you can post a comment to Ted's blog or my blog right? ). I have to be honest with y'all: it's hard times at AOL right now, that's for sure. Every couple of steps we take going forward (Netscape, TMZ, Live8, moving to the free model, AIM Pro, AIM Pages, free five gigs of backup, 40% growth of advertising for Q2--beating Yahoo, MapQuests API, AOL Uncut Video) , we seem to get hit back by something horrible like \the call\ or \the data Valdez. \ The truth is the company is moving forward, but these things create a horrible perception problem, and it has a real world impact in that it de-motivates my teams and it makes it so much harder to get new people into the company. Smart folks ask me about stuff like \the call\ when I try to recruit them for AOL, and I have to assure them it isn't gonna happen again. It's not easy, and I wish I could tell you I always win that fight--but I don't. I was so angry today that I had to get off my computer and do a three-mile run. I'm back at my desk but I'm still seething--how could this happen? ! Everyone is working so hard to get AOL on the right track, and it all gets forgotten when this kind of thing happens. I think I'm gonna take the rest of the week off from blogging as a \cool down\period. I don't want to say something I regret, and I don't want to become the spokesperson for the entire company--that's not my job and it's not my desire. I just want to build cool stuff with cool people I respect. To my team (and everyone at AOL) , keep fighting the good fight. Put your anger into your game and stay focused. The darkest hour is the one before the dawn. We're gonna get through this. [Note: AOL staffers can feel free to post their comments below--anonymous or on the record. I'll turn them on for you if you use a fake email. ]  La version RC1 d’Operations Manager 2007 est disponible depuis http://connect.microsoft.com

Les améliorations sur la beta 2 sont les suivantes :

·         Process d’installation amélioré

·         Améliorations de l’interface utilisateur

·         Mises à jour de packs d’administration et apparition du pack Active Directory

·         Serveur Gateway (je tente la traduction de passerelleJ) et utilisation de certificats pour les périphériques hors domaine

·         Support d’architecture utilisant plusieurs serveurs d’administration

·         Amélioration de la stabilité

Les prochaines étapes visent un lancement mondial à San Diego lors du prochain Microsoft Management Summit (MMS), en mars prochain."""

test_sentences = [[u'It', u"'", u'??', u's', u'hard', u'to', u'believe', u'but', u'Dreamforce', u'is', u'less', u'than', u'a', u'week', u'away', u'!'],
                  [u'In', u'preparation', u'for', u'salesforce', u'.'],
                  [u'com', u"'", u'??', u's', u'biggest', u'event', u'of', u'the', u'year', u',', u'we',  u"'", u'??', u've', u'cataloged', u'all', u'150', u'breakout', u'sessions', u'on', u'the', u'Successforce', u'.'],
                  [u'com', u'site', u'.'],
                  [u'During', u'the', u'conference', u'you', u'can', u'use', u'this', u'guide', u'to', u'plan', u'your', u'day', u'.'],
                  [u'You', u'can', u'navigate', u'by', u'track', u'or', u'choose', u'between', u'the', u'various', u'session', u'offered', u'during', u'a', u'given', u'time', u'slot', u'.'],
                  [u'On', u'the', u'session', u'detail', u'pages', u'you', u"'", u'??', u'll', u'find', u'a', u'list', u'of', u'speakers', u'and', u'their', u'respective', u'companies', u'.'],
                  [u'We', u'also', u'have', u'a', u'spot', u'where', u'you', u'can', u'leave', u'comments', u'about', u'the', u'session', u',', u'or', u'post', u'questions', u'you',
                   u"'", u'??', u'd', u'like', u'to', u'see', u'the', u'presenter', u'cover', u'.'],
                  [u'-LRB-', u'Dreamforce', u'Comments', u'Feed', u'-RRB-'],
                  [u'To', u'bring', u'Dreamforce', u'to', u'those', u'who', u'ca', u"n't", u'make', u'it', u',', u'we', u'try', u'to', u'post', u'much', u'of', u'the', u'content', u'online', u'.'],
                  [u'Last', u'year', u'we', u'had', u'over', u'50k', u'downloads', u'after', u'the', u'conference', u',', u'and', u'this', u'year', u'we', u'expect', u'a', u'dramatic', u'increase', u'this', 
                   u'year', u'as', u'we', u'introduce', u'video', u'.'],
                  [u'In', u'each', u'of', u'the', u'12', u'breakout', u'rooms', u'we', u"'", u'??', u'll', u'be', u'recording', u'video', u'so', u'you', u'can', u'connect', u'with', u'the', u'presenter', u'and', u'see', 
                   u'all', u'the', u'amazing', u'product', u'demos', u'.'],
                  [u'The', u'first', u'video', u'will', u'be', u'posted', u'on', u'Wednesday', u'October', u'11th', u'with', u'additional', u'sessions', u'posted', u'to', u'the', u'site', u'as', u'they', u'are', u'produced', u'.'],
                  [u'For', u'those', u'looking', u'for', u'immediate', u'gratification', u',', u'we', u'are', u'also', u'planning', u'on', u'posting', u'the', u'PowerPoint', u'slides', u'and', u'other', 
                   u'resources', u'referenced', u'in', u'the', u'presentation', u'on', u'the', u'session', u'detail', u'pages', u'.'],
                  [u'We', u"'", u'??', u've', u'got', u'a', u'fantastic', u'week', u'ahead', u'.'],
                  [u'You', u'won', u"'", u'??', u't', u'want', u'to', u'miss', u'it', u'.'],
                  [u'Make', u'your', u'last', u'minute', u'travel', u'plans', u'and', u'get', u'registered', u'today', u'!'],
                  [u'Last', u'Friday', u'when', u'the', u'temperature', u'resulted', u'in', u'an', u'\x07', u'ir', u'stagnation', u'alert', u'\\', u'-LRB-', u'I', u'have', u'no', u'idea', u'-RRB-', u'.'],
                  [u'I', u'should', u'have', u'been', u'done', u'on', u'Saturday', u'but', u'had', u'to', u'add', u'those', u'few', u'extra', u'days', u'back', u'in', u'-LRB-', u'since', u'the', u'program', 
                   u'is', u'based', u'on', u'building', u'on', u'intervals', u'-RRB-', u'.'],
                  [u'I', u'am', u'happy', u'to', u'confirm', u'that', u'I', u'ran', u'for', u'28', u'minutes', u'today', u'-LRB-', u'well', u',', u'by', u'running', u'I', u'mean', u'jogging', u'that', u'looks', 
                   u'slow', u'but', u'totally', u'rocks', u'my', u'heart', u'rate', u'-RRB-', u'.'],
                  [u'Tomorrow', u',', u'I', u'run', u'thirty', u'minutes', u'and', u'give', u'myself', u'a', u'pat', u'on', u'the', u'back', u'-LRB-', u'it', u"'s", u'OK', u',', u'I',
                   u"'m", u'going', u'to', u'call', u'it', u'stretching', u'-RRB-', u'.'],
                  [u'Happy', u'Chinese', u'New', u'YearWishing', u'everyone', u'a', u'HAPPY', u'CHINESE', u'NEW', u'YEAR', u'!'],
                  [u'Chapter', u'One', u':', u'Rise', u'of', u'the', u'monkeyFor', u'thousand', u'of', u'years', u',', u'a', u'stone', u'had', u'been', u'absorbing', u'the', u'\\', u'ki', u'\\', u'of', u'the', 
                   u'heaven', u'and', u'earth', u',', u'finally', u'one', u'day', u',', u'it', u'exploded', u'and', u'Mosaic', u'Monkey', u'-LRB-', u'M', u'&', u'M', u'in', u'short', u'-RRB-', u'was', u'borned', u'.'],
                  [u'This', u'crappy', u'ideas', u'of', u'mosaic', u'monkey', u'-LRB-', u'inspired', u'by', u'Monkey', u'god', u'and', u'crayon', u'shin', u'-RRB-', u'had', u'been', u'floating', u'in', u'my', 
                   u'mind', u'for', u'a', u'few', u'months', u'so', u'finally', u'today', u'i', u'decided', u'to', u'scanned', u'2', u'of', u'sketches', u'and', u'make', u'it', u'into', u'a', u'illustration', u'.'],
                  [u'More', u'will', u'come', u'.', u'..'],
                  [u'Chapter', u'two', u':', u'Enter', u'the', u'monkeyMosaic', u'Monkey', u'decided', u'to', u'take', u'down', u'all', u'the', u'demons', u'in', u'the', u'jungle', u'to', u'become', u'the', 
                   u'King', u'of', u'the', u'jungle', u'.'],
                  [u'Kazaaaaa', u'!!!'],
                  [u'-LRB-', u'*', u'inspired', u'by', u'Bruce', u'lee', u':', u'enter', u'the', u'dragon', u'-RRB-', u'************************************************************************************Recently', 
                   u',', u'i', u'came', u'across', u'a', u'advertisement', u'on', u'a', u'bus', u'stop', u',', u'it', u'wrote', u'this', u'\\', u'No', u'one', u'can', u'survive', u'on', u'the', u'diets', u'of', u'hope', u'!'],
                  [u'\\', u'So', u'true', u'.', u'..'],
                  [u'..'],
                  [u'Who', u'can', u'??', u"''"],
                  [],
                  [u'``', u'Filed', u'under', u':', u'AOLTed', u'checks', u'in', u'on', u'what', u'people', u'are', u'calling', u'the', u'\\', u'data', u'Valdez', u'.'],
                  [u'\\', u'It', u'so', u'nice', u'having', u'Ted', u'blogging', u',', u'sometimes', u'I', u'feel', u'like', u'I',
                   u"'m", u'alone', u'on', u'the', u'front', u'lines', u'.'],
                  [u'I', u'wish', u'other', u'senior', u'executives', u'would', u'start', u'blogging', u'at', u'AOL', u'-LRB-', u'hint', u',', u'hint', u'-RRB-', u'--', u'or', u'at', u'least', u'commenting', u'-LRB-', 
                   u'you', u'guys', u'know', u'you', u'can', u'post', u'a', u'comment', u'to', u'Ted', u"'s", u'blog', u'or', u'my', u'blog', u'right', u'?', u'-RRB-'],
                  [u'.'],
                  [u'I', u'have', u'to', u'be', u'honest', u'with', u"y'all", u':', u'it', u"'s", u'hard', u'times', u'at', u'AOL', u'right', u'now', u',', u'that', u"'s", u'for', u'sure', u'.'],
                  [u'Every', u'couple', u'of', u'steps', u'we', u'take', u'going', u'forward', u'-LRB-', u'Netscape', u',', u'TMZ', u',', u'Live8', u',', u'moving', u'to', u'the', u'free', u'model', u',', u'AIM', 
                   u'Pro', u',', u'AIM', u'Pages', u',', u'free', u'five', u'gigs', u'of', u'backup', u',', u'40', u'%', u'growth', u'of', u'advertising', u'for', u'Q2', u'--', u'beating', u'Yahoo', u',', 
                   u'MapQuests', u'API', u',', u'AOL', u'Uncut', u'Video', u'-RRB-', u',', u'we', u'seem', u'to', u'get', u'hit', u'back', u'by', u'something', u'horrible', u'like', u'he', u'call', u'\\', 
                   u'or', u'he', u'data', u'Valdez', u'.'],
                  [u'\\', u'The', u'truth', u'is', u'the', u'company', u'is', u'moving', u'forward', u',', u'but', u'these', u'things', u'create', u'a', u'horrible', u'perception', u'problem', u',', u'and', 
                   u'it', u'has', u'a', u'real', u'world', u'impact', u'in', u'that', u'it', u'de-motivates', u'my', u'teams', u'and', u'it', u'makes', u'it', u'so', u'much', u'harder', u'to', u'get', u'new', 
                   u'people', u'into', u'the', u'company', u'.'],
                  [u'Smart', u'folks', u'ask', u'me', u'about', u'stuff', u'like', u'he', u'call', u'\\', u'when', u'I', u'try', u'to', u'recruit', u'them', u'for', u'AOL', u',', u'and', u'I', u'have', u'to', 
                   u'assure', u'them', u'it', u'is', u"n't", u'gonna', u'happen', u'again', u'.'],
                  [u'It', u"'s", u'not', u'easy', u',', u'and', u'I', u'wish', u'I', u'could', u'tell', u'you', u'I', u'always', u'win', u'that', u'fight', u'--', u'but', u'I', u'do', u"n't", u'.'],
                  [u'I', u'was', u'so', u'angry', u'today', u'that', u'I', u'had', u'to', u'get', u'off', u'my', u'computer', u'and', u'do', u'a', u'three-mile', u'run', u'.'],
                  [u'I', u"'m", u'back', u'at', u'my', u'desk', u'but', u'I', u"'m", u'still', u'seething', u'--', u'how', u'could', u'this', u'happen', u'?', u'!'],
                  [u'Everyone', u'is', u'working', u'so', u'hard', u'to', u'get', u'AOL', u'on', u'the', u'right', u'track', u',', u'and', u'it', u'all', u'gets', u'forgotten', u'when', u'this', u'kind', 
                   u'of', u'thing', u'happens', u'.'],
                  [u'I', u'think', u'I', u"'m", u'gonna', u'take', u'the', u'rest', u'of', u'the', u'week', u'off', u'from', u'blogging', u'as', u'a', u'\\', u'cool', u'down', u'\\', u'period', u'.'],
                  [u'I', u'do', u"n't", u'want', u'to', u'say', u'something', u'I', u'regret', u',', u'and', u'I', u'do',
                   u"n't", u'want', u'to', u'become', u'the', u'spokesperson', u'for', u'the', u'entire', u'company', u'--', u'that',
                   u"'s", u'not', u'my', u'job', u'and', u'it', u"'s", u'not', u'my', u'desire', u'.'],
                  [u'I', u'just', u'want', u'to', u'build', u'cool', u'stuff', u'with', u'cool', u'people', u'I', u'respect', u'.'],
                  [u'To', u'my', u'team', u'-LRB-', u'and', u'everyone', u'at', u'AOL', u'-RRB-', u',', u'keep', u'fighting', u'the', u'good', u'fight', u'.'],
                  [u'Put', u'your', u'anger', u'into', u'your', u'game', u'and', u'stay', u'focused', u'.'],
                  [u'The', u'darkest', u'hour', u'is', u'the', u'one', u'before', u'the', u'dawn', u'.'],
                  [u'We', u"'re", u'gonna', u'get', u'through', u'this', u'.'],
                  [u'-LRB-', u'Note', u':', u'AOL', u'staffers', u'can', u'feel', u'free', u'to', u'post', u'their', u'comments', u'below', u'--', u'anonymous', u'or', u'on', u'the', u'record', u'.'],
                  [u'I', u"'ll", u'turn', u'them', u'on', u'for', u'you', u'if', u'you', u'use', u'a', u'fake', u'email', u'.'],
                  [u'-RRB-'],
                  [u'La', u'version', u'RC1', u"d'Operations", u'Manager', u'2007', u'est', u'disponible', u'depuis', u'http://connect.microsoft.com'],
                  [],
                  [u'Les', u'am\xe9liorations', u'sur', u'la', u'beta', u'2', u'sont', u'les', u'suivantes', u':'],
                  [],
                  [u'\xb7', u'Process', u"d'installation", u'am\xe9lior\xe9'],
                  [u'\xb7', u'Am\xe9liorations', u'de', u"l'interface", u'utilisateur'],
                  [u'\xb7', u'Mises', u'\xe0', u'jour', u'de', u'packs', u"d'administration", u'et', u'apparition', u'du', u'pack', u'Active', u'Directory'],
                  [u'\xb7', u'Serveur', u'Gateway', u'-LRB-', u'je', u'tente', u'la', u'traduction', u'de', u'passerelleJ', u'-RRB-', u'et', u'utilisation', u'de', u'certificats', u'pour', 
                   u'les', u'p\xe9riph\xe9riques', u'hors', u'domaine'],
                  [u'\xb7', u'Support', u"d'architecture", u'utilisant', u'plusieurs', u'serveurs', u"d'administration"],
                  [u'\xb7', u'Am\xe9lioration', u'de', u'la', u'stabilit\xe9'],
                  [u'Les', u'prochaines', u'\xe9tapes', u'visent', u'un', u'lancement', u'mondial', u'\xe0', u'San', u'Diego', u'lors', u'du', u'prochain', u'Microsoft', u'Management', 
                   u'Summit', u'-LRB-', u'MMS', u'-RRB-', u',', u'en', u'mars', u'prochain', u'.']]

gold_results_all_sentences = [[(0, 64, u"It'? ?s hard to believe but Dreamforce is less than a week away!")],
                              [(64, 94, u'In preparation for salesforce.')],
                              [(95, 206, u"com'? ?s biggest event of the year, we'? ?ve cataloged all 150 breakout sessions on the Successforce. com site.")],
                              [(197, 206, u'com site.')],
                              [(209, 271, u'During the conference you can use this guide to plan your day.')],
                              [(272, 369, u'You can navigate by track or choose between the various session offered during a given time slot.')],
                              [(370, 463, u"On the session detail pages you'? ?ll find a list of speakers and their respective companies.")],
                              [(464, 591, u"We also have a spot where you can leave comments about the session, or post questions you'? ?d like to see the presenter cover.")],
                              [(592, 618, u'(Dreamforce Comments Feed)')],
                              [(618, 708, u"To bring Dreamforce to those who can't make it, we try to post much of the content online.")],
                              [(709, 843, u'Last year we had over 50k downloads after the conference, and this year we expect a dramatic increase this year as we introduce video.')],
                              [(844, 981, u"In each of the 12 breakout rooms we'? ?ll be recording video so you can connect with the presenter and see all the amazing product demos.")],
                              [(982, 1104, u'The first video will be posted on Wednesday October 11th with additional sessions posted to the site as they are produced.')],
                              [(1105, 1285, u'For those looking for immediate gratification, we are also planning on posting the PowerPoint slides and other resources referenced in the presentation on the session detail pages.')],
                              [(1287, 1323, u"We'? ?ve got a fantastic week ahead.")],
                              [(1324, 1353, u"You won'? ?t want to miss it.")],
                              [(1354, 1414, u'Make your last minute travel plans and get registered today!')],
                              [(1414, 1502, u'Last Friday when the temperature resulted in an \x07ir stagnation alert\\ (I have no idea) .')],
                              [(1503, 1638, u'I should have been done on Saturday but had to add those few extra days back in (since the program is based on building on intervals) .')],
                              [(1638, 1775, u'I am happy to confirm that I ran for 28 minutes today (well, by running I mean jogging that looks slow but totally rocks my heart rate) .')],
                              [(1776, 1885, u"Tomorrow, I run thirty minutes and give myself a pat on the back (it's OK, I'm going to call it stretching) .")],
                              [(1887, 1951, u'Happy Chinese New YearWishing everyone a HAPPY CHINESE NEW YEAR!')],
                              [(1952, 2146, u'Chapter One: Rise of the monkeyFor thousand of years , a stone had been absorbing the\\ki\\ of the heaven and earth , finally one day , it exploded and Mosaic Monkey ( M & M in short ) was borned.')],
                              [(2147, 2353, u'This crappy ideas of mosaic monkey (inspired by Monkey god and crayon shin) had been floating in my mind for a few months so finally today i decided to scanned 2 of sketches and make it into a illustration.')],
                              [(2354, 2372, u'More will come. ..')],
                              [(2374, 2500, u'Chapter two: Enter the monkeyMosaic Monkey decided to take down all the demons in the jungle to become the King of the jungle.')],
                              [(2501, 2513, u'Kazaaaaa! !!')],
                              [(2514, 2752, u'(* inspired by Bruce lee: enter the dragon )************************************************************************************Recently, i came across a advertisement on a bus stop, it wrote this \\No one can survive on the diets of hope!')],
                              [(2753, 2766, u'\\ So true. ..')],
                              [(2370, 2372, u'..'), (2764, 2766, u'..'), (2768, 2770, u'..')],
                              [(2770, 2783, u'Who can? ?"\n"')],
                              [],
                              [(2782, 2858, u'"Filed under: AOLTed checks in on what people are calling the  \\data Valdez.')],
                              [(2859, 2944, u"\\ It so nice having Ted blogging, sometimes I feel like I'm alone on the front lines.")],
                              [(2945, 3113, u"I wish other senior executives would start blogging at AOL (hint, hint) --or at least commenting (you guys know you can post a comment to Ted's blog or my blog right? )")],
                              # TODO
                              [(93, 94, u'.'), (195, 196, u'.'), (205, 206, u'.'), (270, 271, u'.'), (368, 369, u'.'), (462, 463, u'.'), (590, 591, u'.'), (707, 708, u'.'), (842, 843, u'.'), (980, 981, u'.'), (1103, 1104, u'.'), (1284, 1285, u'.'), (1322, 1323, u'.'), (1352, 1353, u'.'), (1501, 1502, u'.'), (1637, 1638, u'.'), (1774, 1775, u'.'), (1884, 1885, u'.'), (2145, 2146, u'.'), (2352, 2353, u'.'), (2368, 2369, u'.'), (2370, 2371, u'.'), (2371, 2372, u'.'), (2372, 2373, u'.'), (2499, 2500, u'.'), (2762, 2763, u'.'), (2764, 2765, u'.'), (2765, 2766, u'.'), (2766, 2767, u'.'), (2768, 2769, u'.'), (2769, 2770, u'.'), (2857, 2858, u'.'), (2943, 2944, u'.'), (3113, 3114, u'.'), (3196, 3197, u'.'), (3499, 3500, u'.'), (3731, 3732, u'.'), (3868, 3869, u'.'), (3949, 3950, u'.'), (4029, 4030, u'.'), (4216, 4217, u'.'), (4302, 4303, u'.'), (4452, 4453, u'.'), (4512, 4513, u'.'), (4577, 4578, u'.'), (4625, 4626, u'.'), (4670, 4671, u'.'), (4700, 4701, u'.'), (4792, 4793, u'.'), (4843, 4844, u'.'), (4925, 4926, u'.'), (4935, 4936, u'.'), (5562, 5563, u'.')],
                              [(3115, 3197, u"I have to be honest with y'all: it's hard times at AOL right now, that's for sure.")],
                              [(3198, 3500, u'Every couple of steps we take going forward (Netscape, TMZ, Live8, moving to the free model, AIM Pro, AIM Pages, free five gigs of backup, 40% growth of advertising for Q2--beating Yahoo, MapQuests API, AOL Uncut Video) , we seem to get hit back by something horrible like \the call\\ or \the data Valdez.')],
                              [(3501, 3732, u'\\ The truth is the company is moving forward, but these things create a horrible perception problem, and it has a real world impact in that it de-motivates my teams and it makes it so much harder to get new people into the company.')],
                              [(3733, 3869, u"Smart folks ask me about stuff like \the call\\ when I try to recruit them for AOL, and I have to assure them it isn't gonna happen again.")],
                              [(3870, 3950, u"It's not easy, and I wish I could tell you I always win that fight--but I don't.")],
                              [(3951, 4030, u'I was so angry today that I had to get off my computer and do a three-mile run.')],
                              [(4031, 4099, u"I'm back at my desk but I'm still seething--how could this happen? !")],
                              [(4100, 4217, u'Everyone is working so hard to get AOL on the right track, and it all gets forgotten when this kind of thing happens.')],
                              [(4218, 4303, u"I think I'm gonna take the rest of the week off from blogging as a \\cool down\\period.")],
                              [(4304, 4453, u"I don't want to say something I regret, and I don't want to become the spokesperson for the entire company--that's not my job and it's not my desire.")],
                              [(4454, 4513, u'I just want to build cool stuff with cool people I respect.')],
                              [(4514, 4578, u'To my team (and everyone at AOL) , keep fighting the good fight.')],
                              [(4579, 4626, u'Put your anger into your game and stay focused.')],
                              [(4627, 4671, u'The darkest hour is the one before the dawn.')],
                              [(4672, 4701, u"We're gonna get through this.")],
                              [(3042, 3114, u"(you guys know you can post a comment to Ted's blog or my blog right? ).")],
                              [(4794, 4844, u"I'll turn them on for you if you use a fake email.")],
                              # TODO
                              [(617, 618, u')'), (1499, 1500, u')'), (1635, 1636, u')'), (1772, 1773, u')'), (1882, 1883, u')'), (2133, 2134, u')'), (2221, 2222, u')'), (2557, 2558, u')'), (3015, 3016, u')'), (3112, 3113, u')'), (3416, 3417, u')'), (4545, 4546, u')'), (5243, 5244, u')'), (5543, 5544, u')')],
                              [(4848, 4939, u'La version RC1 d\u2019Operations Manager 2007 est disponible depuis http://connect.microsoft.com')],
                              [],
                              [(4941, 4993, u'Les am\xe9liorations sur la beta 2 sont les suivantes :')],
                              [],
                              [(4995, 5031, u'\xb7         Process d\u2019installation am\xe9')],
                              [(5038, 5072, u'\xb7         Am\xe9liorations de l\u2019inter')],
                              [(5090, 5177, u'\xb7         Mises \xe0 jour de packs d\u2019administration et apparition du pack Active Directory')],
                              [(5179, 5310, u'\xb7         Serveur Gateway (je tente la traduction de passerelleJ) et utilisation de certificats pour les p\xe9riph\xe9riques hors domaine')],
                              [(5312, 5381, u'\xb7         Support d\u2019architecture utilisant plusieurs serveurs d\u2019admin')],
                              [(5392, 5430, u'\xb7         Am\xe9lioration de la stabilit\xe9')],
                              [(5432, 5563, u'Les prochaines \xe9tapes visent un lancement mondial \xe0 San Diego lors du prochain Microsoft Management Summit (MMS), en mars prochain.')]]


def test_match_full_sentences_regression():
    ''' Regression tests for match.match() '''
    for (test_sentence, gold_result) in zip(test_sentences, gold_results_all_sentences):
        current = match.match(test_text, test_sentence)
        message = "test: {}\ngold: {}\ncurrent: {}\n".format(
            str(test_sentence), str(gold_result), str(current))
        yield (eq_, current, gold_result, message)


def test_match_lines_with_tokenized_sentences():
    ''' Unit test for match.match_lines() where each thing to be matched is a tokenized sentence '''
    # data from the Twitter Political Corpus: https://www.usna.edu/Users/cs/nchamber/data/twitter/
    original_text = """Taking it easy now that my knees have liquid in them...hence the pain... Damn straight I'll be ready for my next sprint...this Sunday!  People are still talking about my @reply to @bradiewebb saying I hate him cause he didn't reply. It was a joke, douche bags.  RT@beeeebzy: RT @ayshneck: jimmy rollins did in fact figure out mo. he figured out that he can't hit him. NEW PREDICTION Phils in 08  @jayssaalexia RT pois eh;tem que juntar o povo do twitter,e quando tiver passando panico.Todo mundo perguntar se vo falar do #zina...  @cullenluv hey lady u still on? How's ur nite going so far?  @dhollings i want to be together. lets work it out ok. lets be a family again. it's okay. I promise.  @MsShortSale ....Open House in NMB 11-01-09, Quad-Condo Complex,$2,399,000.00 for all (4) or will sell individually.  Ã©â€¢Â·Ã£Ââ€žÃ©â€“â€œÃ¤ÂºÂºÃ£ÂÂ«Ã¤Â¼Å¡Ã£ÂÂ£Ã£ÂÂ¦Ã£Ââ€žÃ£ÂÂªÃ£Ââ€žÃ£Ââ€ºÃ£Ââ€žÃ£Ââ€¹Ã£â‚¬ÂÃ¤ÂºÂºÃ©â€“â€œÃ£â€šâ€™Ã§â€ºÂ´Ã¦Å½Â¥Ã¨Â¦â€¹Ã£â€šâ€¹Ã£ÂÂ®Ã£ÂÅ’Ã¥â€¡â€žÃ£ÂÂÃ¦â‚¬â€“Ã£ÂÂÃ¦â€žÅ¸Ã£ÂËœÃ£â€šâ€¹Ã£â‚¬â€š"""
    tokenized_sentences = [["Taking", "it", "easy", "now", "that", "my", "knees", "have", "liquid", "in", "them", "...", "hence", "the", "pain", "..."],
                           ["Damn", "straight", "I", "'ll", "be", "ready", "for", "my", "next", "sprint", "...", "this", "Sunday", "!"],
                           ["@", "jayssaalexia", "RT", "pois", "eh", ";", "tem", "que", "juntar", "o", "povo", "do", "twitter", ",", "e", "quando", "tiver", "passando", 
                            "panico", ".", "Todo", "mundo", "perguntar", "se", "vo", "falar", "do", "#", "zina", "..."],
                           ["Open", "House", "in", "NMB", "11-01-09", ",", "Quad-Condo", "Complex", ",", "$2,399,000.00", "for", "all", "-LRB-", "4", "-RRB-", "or", "will",
                            "sell", "individually", "."]]
    gold = [(0, 72, 'Taking it easy now that my knees have liquid in them...hence the pain...'),
            (73, 134, "Damn straight I'll be ready for my next sprint...this Sunday!"),
            (396, 529,
             '@jayssaalexia RT pois eh;tem que juntar o povo do twitter,e quando tiver passando panico.Todo mundo perguntar se vo falar do #zina...'),
            (711, 810, 'Open House in NMB 11-01-09, Quad-Condo Complex,$2,399,000.00 for all (4) or will sell individually.')]
    current = match.match_lines(original_text, tokenized_sentences)
    eq_(current, gold)


def test_match_lines_with_single_words():
    ''' Unit test for match.match_lines() where each thing to be matched is a single word '''
    # data from the Twitter Political Corpus: https://www.usna.edu/Users/cs/nchamber/data/twitter/
    original_text = """Global Voices Online Â» Alex Castro: A liberal, libertarian and libertine Brazilian blogger http://ff.im/-6izrC  Do the Conservatives Have a Death Wish? http://bit.ly/323Kq5  RT @Joshuabradenp: The Conservative stands on the shoulders of our Founders... While the Liberal stands on their throats! #p2 #ucot @JoeNBC  RE: @tvnewser Overall excellence? All this is about... is having Liberals handing out their awards to NBC, the biggest Lâ€¦ http://disq.us/px0  I thought conservatives we're champions of personal responsibility, the crux of this msg. Maybe they just hate the messenger? #hypocrisy"""
    gold = [(39, 46, 'liberal'), (198, 210, 'Conservative'), (264, 271, 'Liberal')]
    current = match.match_lines(original_text, ["liberal", "conservative"])
    eq_(current, gold)


def test_match_without_supplying_cleaned_text_single_word():
    ''' Unit test for match.match() without user-supplied cleaned text, matching on a single word '''
    # data from the Twitter Political Corpus: https://www.usna.edu/Users/cs/nchamber/data/twitter/ 
    original_text = """LIVING MY LIFE ONE STEP AT A TIME~NO NEED TO RUSH WHEN YOU HAVE PLENTY OF TIME~DON'T WORRY OVER THOSE WHO NEVER MADE IT TO YA FUTURE THE  @SpaceAstro the whole state of Arizona doesn't do Daylight Savings Time  #News #Environment #Nature Turmoil from climate change poses security risks http://economictimes.indiatimes.com/articleshow/5175652.cms  celebrates Halloween and time-travel with good friends, a scary movie, clingy cats, and hazelnut spice rum. Adieu, October; hello, November!  Working on my first video for the new #youtube channel. It's definitely going to be an acoustic cover of Times Like These - Foo Fighters #ff  of Beastly Behavior Sometimes the PEN is mightier than the sword or my tongue is sharper than my gun (but NOT always) When your ready to"""
    # see issue #6 for a discussion about how to handle matches on portions of hyphenated words
    gold = [(29, 33, 'TIME'), (74, 78, 'TIME'), (205, 209, 'Time'), (373, 377, 'time')]
    current = match.match(original_text, "time")
    eq_(current, gold)


def test_match_supplying_cleaned_text_single_word():
    ''' Unit test for match.match() with user-supplied cleaned text, matching on a single word '''
    # text from https://www.nytimes.com/2019/09/24/science/cats-humans-bonding.html
    original_text = """Dogs are man’s best friend. They’re sociable, faithful and obedient. Our relationship with cats, on the other hand, is often described as more transactional. Aloof, mysterious and independent, cats are with us only because we feed them.

Or maybe not. On Monday, researchers reported that cats are just as strongly bonded to us as dogs or infants, vindicating cat lovers across the land.

“I get that a lot — ‘Well, I knew that, I know that cats like to interact with me,’” said Kristyn Vitale, an animal behavior scientist at Oregon State University and lead author of the new study, published in Current Biology. “But in science, you don’t know that until you test it.”"""
    
    cleaned_text = """Dogs are man's best friend. They're sociable, faithful and obedient. Our relationship with cats, on the other hand, is often described as more transactional. Aloof, mysterious and independent, cats are with us only because we feed them.

Or maybe not. On Monday, researchers reported that cats are just as strongly bonded to us as dogs or infants, vindicating cat lovers across the land.

\"I get that a lot - 'Well, I knew that, I know that cats like to interact with me,'\" said Kristyn Vitale, an animal behavior scientist at Oregon State University and lead author of the new study, published in Current Biology. "But in science, you don’t know that until you test it.\""""
    gold = [(91, 95, 'cats'), (193, 197, 'cats'), (289, 293, 'cats'), (441, 445, 'cats')]
    current = match.match(original_text, "cats", clean_text=cleaned_text)
    eq_(current, gold)


def test_match_without_supplying_cleaned_text_tokenized_phrase():
    ''' Unit test for match.match() with no user-supplied cleaned text, matching on a tokenized phrase '''
    # https://www.poetryfoundation.org/poems/47247/in-just
    original_text = """in Just-\nspring          when the world is mud-\nluscious the little\nlame balloonman\n\nwhistles          far          and wee\n\nand eddieandbill come\n
running from marbles and\npiracies and it's\nspring\n\nwhen the world is puddle-wonderful\n\nthe queer\nold balloonman whistles\nfar          and             wee\nand bettyandisbel come dancing\n\nfrom hop-scotch and jump-rope and\n\nit's\nspring\nand\n\n         the\n\n                  goat-footed\n\nballoonMan          whistles\nfar\nand\nwee"""
    # see issue #7
    tokenized_phrase = ["marbles", "and", "piracies"]
    gold = [(161, 181, 'marbles and\npiracies')]
    current = match.match(original_text, tokenized_phrase)
    eq_(current, gold)


def test_match_supplying_cleaned_text_tokenized_phrase():
    ''' Unit test for match.match() with no supplied cleaned text, matching on a tokenized phrase '''
    # data from the Twitter Political Corpus: https://www.usna.edu/Users/cs/nchamber/data/twitter/
    original_text = """I refuse to be a Socialist!! I had fun last night thanks Court! ... http://lnk.ms/3DZ1C  Itâ€™s called â€œcommunism,â€ folks. http://bit.ly/RedFL"""
    cleaned_text = """I refuse to be a Socialist!! I had fun last night thanks Court! ... http://lnk.ms/3DZ1C  It's called \"communism,\" folks. http://bit.ly/RedFL"""
    tokenized_phrase = ["It", "'s", "called", '"', "communism", ",", '"']
    gold = [(89, 113, 'Itâ€™s called â€œcommuni')]  # TODO: obviously not quite right...consider what can be done
    current = match.match(original_text, tokenized_phrase, clean_text=cleaned_text)
    eq_(current, gold)


def test_untokenize():
    ''' Unit test for untokenize() '''
    # from the same corpus as the regression tests
    original_text = "Chapter two: Enter the monkeyMosaic Monkey decided to take down all the demons in the jungle to become the King of the jungle. Kazaaaaa! !! (* inspired by Bruce lee: enter the dragon )************************************************************************************Recently, i came across a advertisement on a bus stop, it wrote this \\No one can survive on the diets of hope! \ So true. ... ..Who can? ?”"
    gold = 'Chapter\\s+two:\\s+Enter\\s+the\\s+monkeyMosaic\\s+Monkey\\s+decided\\s+to\\s+take\\s+down\\s+all\\s+the\\s+demons\\s+in\\s+the\\s+jungle\\s+to\\s+become\\s+the\\s+King\\s+of\\s+the\\s+jungle.\\s+Kazaaaaa!!!\\s+(\\\\*\\s+inspired\\s+by\\s+Bruce\\s+lee:\\s+enter\\s+the\\s+dragon\\s+)\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\*\\\\******************************************************Recently,\\s+i\\s+came\\s+across\\s+a\\s+advertisement\\s+on\\s+a\\s+bus\\s+stop,\\s+it\\s+wrote\\s+this \\No\\s+one\\s+can\\s+survive\\s+on\\s+the\\s+diets\\s+of\\s+hope! \\\\s+So\\s+true.\\s+[\\.…]{1,3}..Who\\s+can?\\s+?”'
    current = match.untokenize(original_text)
    eq_(current, gold)


def test_cleanup_text():
    ''' Unit test for _cleanup_text() '''
    # symbols from the sidebar of https://en.wikipedia.org/wiki/Quotation_mark
    original_text = "“ ”   \" \" ‘ ’   ' ' « » 「 」[ ]  ( )  { }  ⟨ ⟩ ,  ،  、‒  –  —  ― …  ...  . . .  ⋯  ᠁  ฯ ‹ ›  « » ‘ ’  “ ”  ' '  " " /  ⧸  ⁄ · ‱ • † ‡ ⹋  ° ” 〃¡ ¿ ※ × № ÷ º ª % ‰ ¶ ± ∓ ′  ″  ‴ § ‖  ¦ © ð ℗ ® ℠ ™ ¤ ؋ ​₳ ​ ฿ ​₿ ​ ₵ ​¢ ​₡ ​₢ ​ $ ​₫ ​₯ ​֏ ​ ₠ ​€ ​ ƒ ​₣ ​ ₲ ​ ₴ ​ ₭ ​ ₺ ​₾ ​ ₼ ​ℳ ​₥ ​ ₦ ​ ₧ ​₱ ​₰ ​£ ​ å å å ​﷼ ​៛ ​₽ ​₹ ₨ ​ ₪ ​ ৳ ​₸ ​₮ ​ ₩ ​ ¥ ​å ⁂ ❧ ☞ ‽ ⸮ ◊ ⁀"
    gold = '"\u2009"   "\u2009" \'\u2009\'   \'\u2009\' « » 「 」[ ]  ( )  { }  ⟨ ⟩ ,  ،  、‒  -  —  ― …  ...  . . .  ⋯  ᠁  ฯ ‹ ›  « » \' \'  " "  \' \'   /  ⧸  ⁄ · ‱ • † ‡ ⹋  ° " 〃¡ ¿ ※ × № ÷ º ª % ‰ ¶ ± ∓ ′  ″  ‴ § ‖  ¦ © ð ℗ ® ℠ ™ ¤ ؋ \u200b₳ \u200b ฿ \u200b₿ \u200b ₵ \u200b¢ \u200b₡ \u200b₢ \u200b $ \u200b₫ \u200b₯ \u200b֏ \u200b ₠ \u200b€ \u200b ƒ \u200b₣ \u200b ₲ \u200b ₴ \u200b ₭ \u200b ₺ \u200b₾ \u200b ₼ \u200bℳ \u200b₥ \u200b ₦ \u200b ₧ \u200b₱ \u200b₰ \u200b£ \u200b å å å \u200b﷼ \u200b៛ \u200b₽ \u200b₹ ₨ \u200b ₪ \u200b ৳ \u200b₸ \u200b₮ \u200b ₩ \u200b ¥ \u200bå ⁂ ❧ ☞ ‽ ⸮ ◊ ⁀'
    current = _cleanup_text(original_text)
    eq_(current, gold)


def test_match_by_edit_distance():
    ''' Unit test for _match_by_edit_distance() '''
    # data from the Twitter Political Corpus: https://www.usna.edu/Users/cs/nchamber/data/twitter/
    original_text = "Cant believe Barack Obama & his \"I dont want them to do a lot of talking. I dont mind cleanin up the mess\" WTF! F*#@ you Obama, shame on you"
    current = _match_by_edit_distance(original_text, "Can't")
    eq_(current, "Cant")
    
