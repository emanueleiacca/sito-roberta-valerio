# Testi aggiuntivi per filtri, temi e raggruppamenti (traduzioni automatiche: da rivedere).
EXK = ['filter','all','themes','places','sort','sortOriginal','sortRecent','sortAZ','featuredOnly','reset','noResult','outlets','related','fragments','themesIntro']
EX = {
'fr': ['Filtrer','Tout','Thèmes','Pays','Trier','Ordre d’origine','Plus récents','A–Z','À la une','Tout afficher','Aucun résultat','Médias','À voir aussi','Fragments','Explorer par thème'],
'it': ['Filtra','Tutti','Temi','Paesi','Ordina','Ordine originale','Più recenti','A–Z','In evidenza','Mostra tutto','Nessun risultato','Testate','Da vedere anche','Frammenti','Esplora per tema'],
'en': ['Filter','All','Themes','Countries','Sort','Original order','Most recent','A–Z','Featured','Show all','No results','Outlets','See also','Fragments','Explore by theme'],
'es': ['Filtrar','Todo','Temas','Países','Ordenar','Orden original','Más recientes','A–Z','Destacados','Mostrar todo','Sin resultados','Medios','Ver también','Fragmentos','Explorar por tema'],
'de': ['Filtern','Alle','Themen','Länder','Sortieren','Ursprüngliche Reihenfolge','Neueste zuerst','A–Z','Highlights','Alle anzeigen','Keine Ergebnisse','Medien','Siehe auch','Fragmente','Nach Thema entdecken'],
'pt': ['Filtrar','Tudo','Temas','Países','Ordenar','Ordem original','Mais recentes','A–Z','Destaques','Mostrar tudo','Sem resultados','Meios','Ver também','Fragmentos','Explorar por tema'],
'nl': ['Filteren','Alles','Thema’s','Landen','Sorteren','Oorspronkelijke volgorde','Nieuwste eerst','A–Z','Uitgelicht','Alles tonen','Geen resultaten','Media','Zie ook','Fragmenten','Ontdek per thema'],
'ru': ['Фильтр','Все','Темы','Страны','Сортировка','Исходный порядок','Сначала новые','А–Я','Избранное','Показать всё','Ничего не найдено','Издания','Смотрите также','Фрагменты','Искать по теме'],
'tr': ['Filtrele','Tümü','Temalar','Ülkeler','Sırala','Özgün sıra','En yeniler','A–Z','Öne çıkanlar','Tümünü göster','Sonuç yok','Yayınlar','Ayrıca bakın','Parçalar','Temaya göre keşfet'],
'ar': ['تصفية','الكل','المواضيع','البلدان','ترتيب','الترتيب الأصلي','الأحدث','أ–ي','مختارات','عرض الكل','لا نتائج','الصحف والمجلات','انظر أيضًا','لقطات','استكشف حسب الموضوع'],
'zh': ['筛选','全部','主题','国家','排序','原始顺序','最新','A–Z','精选','显示全部','无结果','媒体','另见','片段','按主题浏览'],
'ja': ['絞り込み','すべて','テーマ','国','並べ替え','元の順','新しい順','A–Z','注目','すべて表示','結果なし','媒体','関連作品','断片','テーマで探す'],
}
THK = ['youth','women','conflict','exile','borders','environment','education','inclusion','culture','daily']
TH = {
'fr': ['Jeunesse','Femmes','Conflits et après-guerre','Exil et migrations','Frontières et divisions','Territoires et environnement','Éducation','Handicap et inclusion','Cultures et traditions','Vie quotidienne'],
'it': ['Giovinezza','Donne','Conflitti e dopoguerra','Esilio e migrazioni','Confini e divisioni','Territori e ambiente','Istruzione','Disabilità e inclusione','Culture e tradizioni','Vita quotidiana'],
'en': ['Youth','Women','Conflict and aftermath','Exile and migration','Borders and divisions','Land and environment','Education','Disability and inclusion','Cultures and traditions','Everyday life'],
'es': ['Juventud','Mujeres','Conflictos y posguerra','Exilio y migraciones','Fronteras y divisiones','Territorio y medio ambiente','Educación','Discapacidad e inclusión','Culturas y tradiciones','Vida cotidiana'],
'de': ['Jugend','Frauen','Konflikt und Nachkrieg','Exil und Migration','Grenzen und Trennungen','Land und Umwelt','Bildung','Behinderung und Inklusion','Kulturen und Traditionen','Alltag'],
'pt': ['Juventude','Mulheres','Conflitos e pós-guerra','Exílio e migrações','Fronteiras e divisões','Território e ambiente','Educação','Deficiência e inclusão','Culturas e tradições','Vida quotidiana'],
'nl': ['Jeugd','Vrouwen','Conflict en nasleep','Ballingschap en migratie','Grenzen en scheidslijnen','Land en milieu','Onderwijs','Beperking en inclusie','Culturen en tradities','Dagelijks leven'],
'ru': ['Молодёжь','Женщины','Конфликты и послевоенье','Изгнание и миграция','Границы и разделения','Земля и окружающая среда','Образование','Инвалидность и инклюзия','Культуры и традиции','Повседневная жизнь'],
'tr': ['Gençlik','Kadınlar','Çatışma ve savaş sonrası','Sürgün ve göç','Sınırlar ve bölünmeler','Toprak ve çevre','Eğitim','Engellilik ve kapsayıcılık','Kültürler ve gelenekler','Gündelik yaşam'],
'ar': ['الشباب','النساء','النزاعات وما بعد الحرب','المنفى والهجرة','الحدود والانقسامات','الأرض والبيئة','التعليم','الإعاقة والإدماج','الثقافات والتقاليد','الحياة اليومية'],
'zh': ['青年','女性','冲突与战后','流亡与移民','边界与分裂','土地与环境','教育','残障与包容','文化与传统','日常生活'],
'ja': ['若者','女性','紛争と戦後','亡命と移民','国境と分断','土地と環境','教育','障害とインクルージョン','文化と伝統','日常'],
}
for k in EX: assert len(EX[k]) == len(EXK), k
for k in TH: assert len(TH[k]) == len(THK), k
