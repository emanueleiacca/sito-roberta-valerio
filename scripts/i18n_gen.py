#!/usr/bin/env python3
# Genera src/i18n.js (testi dell'interfaccia in 12 lingue). Traduzioni automatiche: da far rivedere.
import json, sys
OUT = sys.argv[1]

L = {  # code: (native name, rtl)
 'fr': 'Français', 'it': 'Italiano', 'en': 'English', 'es': 'Español', 'de': 'Deutsch', 'pt': 'Português',
 'nl': 'Nederlands', 'ru': 'Русский', 'tr': 'Türkçe', 'ar': 'العربية', 'zh': '中文', 'ja': '日本語',
}
keys = ['tagline','work','portraits','publications','commissions','about','featured','allWork','open','back','originalText',
        'video','contact','draft','desc','menu','close','prev','next','language','sommaire','photos','follow','epigraph','commIntro','soon']
T = {
'fr': ['Photographe reporter et portraitiste','Reportages','Portraits','Publications','Commandes','À propos','À la une','Tous les reportages','Voir','Retour','Texte original en','Vidéo','Contact','Version de travail',
       'Photographe reporter et portraitiste. Reportages société, portraits et travaux personnels sur les mutations de la société contemporaine.','Menu','Fermer','Précédent','Suivant','Langue','Sommaire','photos','Suivre au quotidien sur Instagram',
       'Ce qui change, et celles et ceux qui le vivent.','Travaux de commande pour la presse, l’édition et les entreprises.','bientôt'],
'it': ['Fotografa reporter e ritrattista','Reportage','Ritratti','Pubblicazioni','Su commissione','Chi sono','In evidenza','Tutti i reportage','Vedi','Indietro','Testo originale in','Video','Contatti','Versione di lavoro',
       'Fotografa reporter e ritrattista. Reportage sociali, ritratti e lavori personali sulle trasformazioni della società contemporanea.','Menu','Chiudi','Precedente','Successivo','Lingua','Sommario','foto','Seguila ogni giorno su Instagram',
       'Ciò che cambia, e chi lo vive.','Lavori su commissione per stampa, editoria e aziende.','presto'],
'en': ['Documentary photographer and portraitist','Work','Portraits','Publications','Commissions','About','Featured','All work','View','Back','Original text in','Video','Contact','Work in progress',
       'Documentary photographer and portraitist. Social reportage, portraits and personal work on the changes of contemporary society.','Menu','Close','Previous','Next','Language','Contents','photos','Follow daily on Instagram',
       'What is changing, and the people living it.','Commissioned work for press, publishing and companies.','soon'],
'es': ['Fotógrafa reportera y retratista','Reportajes','Retratos','Publicaciones','Encargos','Sobre mí','Destacados','Todos los reportajes','Ver','Volver','Texto original en','Vídeo','Contacto','Versión de trabajo',
       'Fotógrafa reportera y retratista. Reportajes sociales, retratos y trabajos personales sobre las transformaciones de la sociedad contemporánea.','Menú','Cerrar','Anterior','Siguiente','Idioma','Índice','fotos','Síguela a diario en Instagram',
       'Lo que cambia, y quienes lo viven.','Trabajos por encargo para prensa, edición y empresas.','pronto'],
'de': ['Reportage- und Porträtfotografin','Reportagen','Porträts','Veröffentlichungen','Auftragsarbeiten','Über mich','Highlights','Alle Reportagen','Ansehen','Zurück','Originaltext auf','Video','Kontakt','Arbeitsversion',
       'Reportage- und Porträtfotografin. Gesellschaftsreportagen, Porträts und persönliche Arbeiten über den Wandel der zeitgenössischen Gesellschaft.','Menü','Schließen','Zurück','Weiter','Sprache','Inhalt','Fotos','Täglich auf Instagram folgen',
       'Was sich verändert – und die Menschen, die es erleben.','Auftragsarbeiten für Presse, Verlage und Unternehmen.','bald'],
'pt': ['Fotógrafa repórter e retratista','Reportagens','Retratos','Publicações','Encomendas','Sobre','Destaques','Todas as reportagens','Ver','Voltar','Texto original em','Vídeo','Contacto','Versão de trabalho',
       'Fotógrafa repórter e retratista. Reportagens sociais, retratos e trabalhos pessoais sobre as transformações da sociedade contemporânea.','Menu','Fechar','Anterior','Seguinte','Idioma','Índice','fotos','Siga diariamente no Instagram',
       'O que muda, e quem o vive.','Trabalhos por encomenda para imprensa, edição e empresas.','em breve'],
'nl': ['Reportage- en portretfotograaf','Reportages','Portretten','Publicaties','Opdrachten','Over mij','Uitgelicht','Alle reportages','Bekijk','Terug','Originele tekst in','Video','Contact','Werkversie',
       'Reportage- en portretfotograaf. Maatschappelijke reportages, portretten en persoonlijk werk over de veranderingen van de hedendaagse samenleving.','Menu','Sluiten','Vorige','Volgende','Taal','Inhoud','foto’s','Volg dagelijks op Instagram',
       'Wat verandert, en de mensen die het meemaken.','Opdrachtwerk voor pers, uitgeverijen en bedrijven.','binnenkort'],
'ru': ['Фотограф-репортёр и портретист','Репортажи','Портреты','Публикации','Заказные работы','Обо мне','Избранное','Все репортажи','Смотреть','Назад','Оригинал текста на','Видео','Контакты','Рабочая версия',
       'Фотограф-репортёр и портретист. Социальные репортажи, портреты и личные проекты о переменах в современном обществе.','Меню','Закрыть','Назад','Далее','Язык','Содержание','фото','Ежедневно в Instagram',
       'Что меняется — и те, кто это переживает.','Заказные работы для прессы, издательств и компаний.','скоро'],
'tr': ['Foto muhabiri ve portre fotoğrafçısı','Röportajlar','Portreler','Yayınlar','Sipariş işler','Hakkında','Öne çıkanlar','Tüm röportajlar','Gör','Geri','Özgün metin dili:','Video','İletişim','Çalışma sürümü',
       'Foto muhabiri ve portre fotoğrafçısı. Çağdaş toplumun dönüşümü üzerine toplumsal röportajlar, portreler ve kişisel çalışmalar.','Menü','Kapat','Önceki','Sonraki','Dil','İçindekiler','fotoğraf','Instagram’da her gün takip edin',
       'Değişenler ve onu yaşayanlar.','Basın, yayıncılık ve şirketler için sipariş işler.','yakında'],
'ar': ['مصوِّرة صحفية ومصوِّرة بورتريه','ريبورتاجات','بورتريهات','منشورات','أعمال بالتكليف','نبذة','مختارات','كل الريبورتاجات','عرض','رجوع','النص الأصلي بالـ','فيديو','تواصل','نسخة عمل',
       'مصوِّرة صحفية ومصوِّرة بورتريه. ريبورتاجات اجتماعية وبورتريهات وأعمال شخصية حول تحولات المجتمع المعاصر.','القائمة','إغلاق','السابق','التالي','اللغة','الفهرس','صور','تابعوها يوميًا على إنستغرام',
       'ما الذي يتغيّر، ومن يعيشونه.','أعمال بالتكليف للصحافة والنشر والشركات.','قريبًا'],
'zh': ['纪实摄影师与人像摄影师','纪实报道','人像','刊载作品','委托作品','关于','精选','全部报道','查看','返回','原文语言：','视频','联系','工作版本',
       '纪实摄影师与人像摄影师。关注当代社会变迁的社会报道、人像与个人作品。','菜单','关闭','上一个','下一个','语言','目录','张照片','在 Instagram 上每日关注',
       '正在改变的一切，以及经历它的人。','为媒体、出版和企业完成的委托作品。','即将推出'],
'ja': ['ドキュメンタリー／ポートレート写真家','ルポルタージュ','ポートレート','掲載作品','依頼仕事','プロフィール','注目','すべてのルポルタージュ','見る','戻る','原文の言語：','動画','お問い合わせ','制作中バージョン',
       'ドキュメンタリー／ポートレート写真家。現代社会の変化をテーマにした社会ルポ、ポートレート、個人作品。','メニュー','閉じる','前へ','次へ','言語','目次','枚','Instagramで毎日更新',
       '変わりゆくもの、そしてそれを生きる人びと。','報道・出版・企業のための依頼仕事。','近日公開'],
}
LN = {  # nomi delle lingue dei testi originali (fr/en/it)
 'fr': {'fr':'français','en':'anglais','it':'italien'}, 'it': {'fr':'francese','en':'inglese','it':'italiano'},
 'en': {'fr':'French','en':'English','it':'Italian'}, 'es': {'fr':'francés','en':'inglés','it':'italiano'},
 'de': {'fr':'Französisch','en':'Englisch','it':'Italienisch'}, 'pt': {'fr':'francês','en':'inglês','it':'italiano'},
 'nl': {'fr':'het Frans','en':'het Engels','it':'het Italiaans'}, 'ru': {'fr':'французском','en':'английском','it':'итальянском'},
 'tr': {'fr':'Fransızca','en':'İngilizce','it':'İtalyanca'}, 'ar': {'fr':'الفرنسية','en':'الإنجليزية','it':'الإيطالية'},
 'zh': {'fr':'法语','en':'英语','it':'意大利语'}, 'ja': {'fr':'フランス語','en':'英語','it':'イタリア語'},
}
OUTLETS = 'Air France Madame, 6 mois, Traveller, Le Parisien Weekend, Le Monde, D La Repubblica, Icon Design, Elle, Marie Claire…'
BIO = {
'fr': ['Née en Italie, elle vit en France depuis 1998.', f'Photographe reporter et portraitiste, elle travaille pour la presse en réalisant des reportages société, voyage, lifestyle ({OUTLETS}).', 'Elle poursuit parallèlement des travaux personnels axés sur le questionnement et les mutations de la société contemporaine.'],
'it': ['Nata in Italia, vive in Francia dal 1998.', f'Fotografa reporter e ritrattista, lavora per la stampa realizzando reportage di società, viaggio e lifestyle ({OUTLETS}).', 'Parallelamente porta avanti lavori personali incentrati sulle domande e sulle trasformazioni della società contemporanea.'],
'en': ['Born in Italy, she has lived in France since 1998.', f'A documentary photographer and portraitist, she works for the press, producing reportage on society, travel and lifestyle ({OUTLETS}).', 'In parallel, she pursues personal projects focused on the questions and transformations of contemporary society.'],
'es': ['Nacida en Italia, vive en Francia desde 1998.', f'Fotógrafa reportera y retratista, trabaja para la prensa realizando reportajes de sociedad, viajes y estilo de vida ({OUTLETS}).', 'Paralelamente desarrolla trabajos personales centrados en los interrogantes y las transformaciones de la sociedad contemporánea.'],
'de': ['In Italien geboren, lebt sie seit 1998 in Frankreich.', f'Als Reportage- und Porträtfotografin arbeitet sie für die Presse und realisiert Gesellschafts-, Reise- und Lifestyle-Reportagen ({OUTLETS}).', 'Parallel dazu verfolgt sie persönliche Projekte, die die Fragen und den Wandel der zeitgenössischen Gesellschaft in den Mittelpunkt stellen.'],
'pt': ['Nascida em Itália, vive em França desde 1998.', f'Fotógrafa repórter e retratista, trabalha para a imprensa realizando reportagens de sociedade, viagem e lifestyle ({OUTLETS}).', 'Em paralelo, desenvolve trabalhos pessoais centrados nas questões e nas transformações da sociedade contemporânea.'],
'nl': ['Geboren in Italië, woont ze sinds 1998 in Frankrijk.', f'Als reportage- en portretfotograaf werkt ze voor de pers en maakt ze reportages over maatschappij, reizen en lifestyle ({OUTLETS}).', 'Daarnaast werkt ze aan persoonlijke projecten rond de vragen en veranderingen van de hedendaagse samenleving.'],
'ru': ['Родилась в Италии, с 1998 года живёт во Франции.', f'Фотограф-репортёр и портретист, она работает для прессы, снимая репортажи об обществе, путешествиях и образе жизни ({OUTLETS}).', 'Параллельно она ведёт личные проекты, посвящённые вопросам и переменам современного общества.'],
'tr': ['İtalya’da doğdu, 1998’den beri Fransa’da yaşıyor.', f'Foto muhabiri ve portre fotoğrafçısı olarak basın için toplum, seyahat ve yaşam tarzı röportajları yapıyor ({OUTLETS}).', 'Bunun yanında çağdaş toplumun soruları ve dönüşümleri üzerine kişisel projeler yürütüyor.'],
'ar': ['وُلدت في إيطاليا وتعيش في فرنسا منذ عام 1998.', f'مصوِّرة صحفية ومصوِّرة بورتريه، تعمل لصالح الصحافة وتنجز ريبورتاجات عن المجتمع والسفر ونمط الحياة ({OUTLETS}).', 'وبالتوازي، تواصل أعمالًا شخصية تتمحور حول التساؤلات وتحولات المجتمع المعاصر.'],
'zh': ['她出生于意大利，自1998年起生活在法国。', f'作为纪实摄影师和人像摄影师，她为媒体拍摄社会、旅行和生活方式类报道（{OUTLETS}）。', '同时，她也持续进行围绕当代社会的疑问与变迁的个人创作。'],
'ja': ['イタリア生まれ、1998年からフランス在住。', f'ドキュメンタリー／ポートレート写真家として、社会、旅、ライフスタイルのルポルタージュを報道媒体のために手がける（{OUTLETS}）。', '並行して、現代社会の問いと変化をめぐる個人プロジェクトにも取り組んでいる。'],
}
GREET = ['Bonjour','Ciao','Hello','مرحبا','Hola','Hallo','Olá','Привет','Merhaba','你好','こんにちは']
from i18n_extra import EX, EXK, TH, THK
UI = {}
for code, vals in T.items():
    assert len(vals) == len(keys), (code, len(vals), len(keys))
    UI[code] = dict(zip(keys, vals)); UI[code]['langNames'] = LN[code]; UI[code].update(dict(zip(EXK, EX[code]))); UI[code]['themeNames'] = dict(zip(THK, TH[code]))
js = "// File GENERATO da i18n_gen.py -- traduzioni automatiche (da far rivedere a madrelingua).\n"
js += f"export const LOCALES = {json.dumps(list(L), ensure_ascii=False)};\nexport const DEFAULT_LOCALE = 'fr';\n"
js += f"export const LANG_NAME = {json.dumps(L, ensure_ascii=False)};\nexport const isRtl = (l) => l === 'ar';\n"
js += f"export const GREETINGS = {json.dumps(GREET, ensure_ascii=False)};\n"
js += f"export const UI = {json.dumps(UI, ensure_ascii=False, indent=1)};\n"
js += f"export const BIO = {json.dumps(BIO, ensure_ascii=False, indent=1)};\n"
js += "export function t(lang, key) { return (UI[lang] && UI[lang][key]) ?? UI.fr[key]; }\n"
js += "export function lp(lang, path = '/') { return `/${lang}${path}`; }\n"
open(OUT, 'w', encoding='utf-8').write(js)
print('ok', len(L), 'lingue')
