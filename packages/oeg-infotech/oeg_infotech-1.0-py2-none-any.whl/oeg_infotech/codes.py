# coding: utf-8
"""
Infotech official dictionaries
"""


class PigType:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    codes for pig tools
    """
    MFL = '990005096296'
    TFI = '990004033563'
    CALIPER_MECH = '990004033561'
    NAVIGATE = '6907295'

    ULTRASONIC = '990004033557'
    CALIPER_MAGN = '990004033558'
    EMAP = '6907298'
    COMBO = '6915601'
    CLEANER = '990004033560'
    CALIPER_TOOL = '990004033562'


class PassType:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    codes for PIGPASS
    """
    COMPLEX = '2088658'
    COMPLEX_SKS = '2088661'
    COMPLEX_NAV = '5345726'
    NAVIGATE = '990003167701'
    CALIPER = '2088660'
    TFI = '2088662'
    ULTRASONIC = '2088663'
    EXPERIMENTAL = '2088664'
    EMAP = '6943277'


class Tube:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    Tube types
    """
    BEZSHOV = '2097789'
    DVUSHOV = '2097792'
    UNKNOWN = '2097790'
    ODNOSHOV = '2097791'
    SPIRAL = '2097787'


class Company:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    codes for companies
    """
    BSPC = '990003448249'
    AVTOGAZ = '990006595572'
    AEROCOSM = '4616685'
    BKH = '6857461'
    GPAS = '1555253'
    DIASCAN = '990003167648'
    DIAPROM = '5664849'
    OEG = '1555222'
    PODVGAZENERGO = '990003448250'
    PODVODDIAG = '4682910'
    PODVODSERV = '4851206'
    ROZEN = '990003448248'
    SNG = '1555204'
    TUBOSCAN = '5663438'
    VNUTRITRUBDIAG = '6939219'


class MethodsKBD:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    codes for methods of KBD calculation
    """
    API579 = '4982902'
    ASME = '990005096289'
    BS7910 = '990005096288'
    DNV = '990005096506'
    NGKS = '60000213471'
    GAZNADZOR2008 = '990005096276'
    ASMEB31G = '990005096290'
    STO112 = '990005096286'
    STO173 = '6907365'
    ASME2012 = '6907367'
    GAZNADZOR2013 = '6907370'
    VRD = '6907372'


class Feature:  # pylint: disable=old-style-class,no-init,too-few-public-methods
    """
    codes for detected features
    """
    ANOMALY = '990006537198'  # 990006537148 ANOM Аномалия 990006537148 OTHE
    NESVAR_STYK = '990006537195'  # 990006537148 ANOM Несваренный стык патрона 990006537195 UWCA
    POTERYA_CONTACTA = '990006548776'  # 990006537148 ANOM Аномалия 990006537148 OTHE
    EXCENTR_CASE = '990006537194'  # 990006537148 ANOM Эксцентричный патрон 990006537194 EXCA
    ANOMAL_KOLTSEVOGO = '990006537187'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    ANOMAL_OBLTSOVKI = '990006537186'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    CORROZ_KOLTSEVOGO = '990006537185'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    NEPROVAR_UTYAZH = '990006537184'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    NO_USILEN_KOLTSEVOGO = '990008404344'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    PODKLAD_KOLTSO = '990006548775'  # 330000002264 OTHE Другое 330000002264 -
    PODREZ = '990006537148'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    PRAVKA_KROMOK = '990006548774'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    PROVIS_KORNYA = '990007322160'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    SMESCHENIE_KROMOK = '990007289509'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    VNUTRI_SHOV_DEFEKT = '6907237'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    PODGIB_KROMKY = '6907241'  # 990006537148 ANOM Аномалия кольцевого шва 990006537187 GWAN
    ANOMAL_PRODOLNOGO = '990006537188'  # 990006537148 ANOM Аномалия продольного шва 990006537188 LWAN
    VYSHLIFOVKA_PRODOLNOGO = '990007322148'  # 990006537148 ANOM Аномалия продольного шва 990006537188 LWAN
    FORMA_PRODOLNOGO = '990007322161'  # 990006537148 ANOM Аномалия продольного шва 990006537188 LWAN
    ANOMAL_SPIRALNOGO = '990006537189'  # 990006537148 ANOM Аномалия спирального шва 990006537189 SWAN
    VYSHLIFOVKA_SPIRALNOGO = '990007322164'  # 990006537148 ANOM Аномалия спирального шва 990006537189 SWAN
    FORMA_SPIRALNOGO = '990007322162'  # 990006537148 ANOM Аномалия спирального шва 990006537189 SWAN
    DENT = '230000190556'  # 990006537148 ANOM Вмятина 230000190556 DENT
    DENT_METAL_LOSS = '990006537191'  # 990006537148 ANOM Вмятина с дефектами потери металла 990006537191 DEML
    VNUTRYSTEN_RASSLOENIE = '990006537192'  # 990006537148 ANOM Внутристенное расслоение 990006537192 LAMI
    GOFRA = '990006537193'  # 990006537148 ANOM Гофра 990006537147 WRIN
    FACTORY_DEFEKT = '990006537199'  # 990006537148 ANOM Заводской дефект 990006537199 MIAN
    METALL_DEFEKT = '990004698865'  # 990006537148 ANOM Заводской дефект 990006537199 MIAN
    VYSHLIFOVKA = '990004698880'  # 990006537148 ANOM Вышлифовка 990004698880 GRIN
    ZONE_VERT_CRACKS = '990007322158'  # 990006537148 ANOM Зона поперечных трещин 990007322158 CSCC
    ZONE_HOR_CRACKS = '990004698849'  # 990006537148 ANOM Зона продольных трещин 990004698849 SCC
    ZONE_CORROZ = '990006537202'  # 990006537148 ANOM Кластер коррозии 990006537152 COCL
    CAVERNA = '990007289502'  # 990006537148 ANOM Коррозия 990007289504 CORR
    CORROZ = '990007289504'  # 990006537148 ANOM Коррозия 990007289504 CORR
    KANAVKA_VERT = '990004698855'  # 990006537148 ANOM Коррозия 990007289504 CORR
    METALL_LOSS = '990004698869'  # 990006537148 ANOM Коррозия 990007289504 CORR
    KANAVKA_HOR = '990004698848'  # 990006537148 ANOM Коррозия 990007289504 CORR
    POINT_CORROZ = '30000179093'  # 990006537148 ANOM Коррозия 990007289504 CORR
    MECHANICAL_DEFEKT = '3760623'  # 990006537148 ANOM Механическое повреждение 3760623 ARTD
    RANDOM_ARC = '990006537209'  # 990006537148 ANOM Случайная дуга 990006537209 ARCS
    RASSL_NO_POVERHNOST = '990006537210'  # 990006537148 ANOM Расслоение с выходом на поверхность 990006537210 LAMI
    ZAVARKA = '990006537213'  # 990006537148 ANOM Технологический дефект 240000166873 TECH
    ZAVARKA_OTVERST = '990006537212'  # 990006537148 ANOM Технологический дефект 240000166873 TECH
    TECHNOLOGY_DEFEKT = '240000166873'  # 990006537148 ANOM Технологический дефект 240000166873 TECH
    CRACK_VERT_SHOV = '990006537214'  # 990006537148 ANOM Трещина на кольцевом шве 990006537214 GWCR
    CRACK_HOR_SHOV = '990007322154'  # 990006537148 ANOM Трещина на продольном шве 990007322154 LWCR
    CRACK_SPIRAL_SHOV = '990007322159'  # 990006537148 ANOM Трещина на спиральном шве 990007322159 SWCR
    NESPLOSHNOST_PT = '990006548777'  # 990006537148 ANOM Трещиноподобный дефект 990006537159 CRAC
    CRACK_VERT = '990004698875'  # 990006537148 ANOM Трещиноподобный дефект 990006537159 CRAC
    CRACK_HOR = '990006537215'  # 990006537148 ANOM Трещиноподобный дефект 990006537159 CRAC
    OVAL = '990006537217'  # 990006537148 ANOM Овализация 990006537217 OVAL
    METALL_OUT = '990006537218'  # 990006536987 ADME Металл снаружи 990006537218 TMTM
    ISOL_STYK = '990006537366'  # 990006537366 ISOL Изоляционный стык 990006537366 -
    CURVE_INSERT = '990006537221'  # 330000002264 OTHE Другое 330000002264 -
    SEGMENT_INSERT = '990006537219'  # 330000002264 OTHE Другое 330000002264 -
    HOMUT = '990006537362'  # 990006536987 ADME Хомут 990006537362 CLAMP
    PIG_RUN = '330000001577'  # 330000001577 PIGL Камера запуска 330000001577 PIGL
    PIG_RECEIVE = '1102945'  # 1102945 PIGR Камера приема 1102945 PIGR
    MARKER = '990006537229'  # 990006537229 MARK Маркер 990006537229 -
    MARKER_RING = '990006537228'  # 990006537229 MARK Маркер 990006537229 -
    MARKER_MAGN = '990006537230'  # 990006537230 MGNT Маркер магнитный 990006537230 -
    ZAVAR_BOBYSHKI = '990006537370'  # 990006537370 LUWD Заварка бобышки 990006537370 -
    ZAVAR_OKNA = '990006537234'  # 990006537234 WIWD Заварка окна 990006537234 -
    REMONT_NAKLAD = '990006537232'  # 990006537169 REPA Место ремонта 990006537169 OTHE
    METALL_CASE_START = '990006537169'  # 990006537169 REPA Металлическая упрочняющая муфта, начало 6907292 WSLB
    METALL_CASE_END = '990006537169'  # 990006537169 REPA Металлическая упрочняющая муфта, конец 6907290 WSLE
    KOMPOS_CASE_START = '6907288'  # 990006537169 REPA Композитная упрочняющая муфта, начало 6907288 СSLB
    KOMPOS_CASE_END = '6907283'  # 990006537169 REPA Композитная упрочняющая муфта, конец 6907283 СSLE
    WRONG_CONSTRUCT = '990006537239'  # 990006537170 OTHE Особенность 990006537170 -
    UNKNOWN = '990006537238'  # 990006537170 OTHE Особенность 990006537170 -
    DU1000_DU1200 = '6587147'  # 990006537170 OTHE Особенность 990006537170 -
    DU1200_DU1000 = '6587146'  # 990006537170 OTHE Особенность 990006537170 -
    DU1200_DU1400 = '6587148'  # 990006537170 OTHE Особенность 990006537170 -
    DU1400_DU1200 = '6587149'  # 990006537170 OTHE Особенность 990006537170 -
    TUBE_ARMATURE = '990006537365'  # 990006537170 OTHE Особенность 990006537170 -
    ELEMENT_OBUSTROY = '990006537364'  # 990006537170 OTHE Особенность 990006537170 -
    WATER_START = '990006911721'  # 990006537170 OTHE Пересечение с водной преградой, начало 6907276 CROSB
    WATER_END = '990006911716'  # 990006537170 OTHE Пересечение с водной преградой, конец 990006911717 CROSE
    FLANETS = '990006911715'  # 990006537170 OTHE Соединение трубных секций 990006912121 FLANG
    OTVOD_VREZKA = '990006537240'  # 990006537240 OFFT Отвод-врезка 990006537240 -
    CASE_START = '990006537242'  # 990006537242 CASB Патрон начало 990006537242 -
    CASE_END = '990006537241'  # 990006537173 CASE Патрон конец 990006537173 -
    PRIGRUZ_RING = '990006537245'  # 990007412848 ANCH Пригруз 990007412848 -
    PRIGRUZ_START = '990006537243'  # 990007412848 ANCH Пригруз 990007412848 -
    PRIGRUZ_END = '990006537244'  # 990007412848 ANCH Пригруз 990007412848 -
    TROYNIK = '990007183153'  # 990007183153 TEE Тройник 990007183153 -
    WALL_THICK = '990006537248'  # 990006537247 WELD Изменение толщины стенки трубы 990006537248 CHWT
    TURN_START = '990006537252'  # 990006537247 WELD Отвод (поворот) начало 990006537252 BENB
    TURN_END = '990006537250'  # 990006537247 WELD Отвод (поворот) конец 990006537250 BENE
    TURN_SEGM_START = '990006537251'  # 990006537247 WELD Отвод (поворот) начало 990006537252 BENB
    TURN_SEGM_END = '990006537249'  # 990006537247 WELD Отвод (поворот) конец 990006537250 BENE
    TURN_SEGM = '990007182542'  # 990006537247 WELD Отвод сегментный 990007182541 BENE
    WELD = '990006537247'  # 990006537247 WELD Шов кольцевой 990006537247 -
    ZADVIZHKA = '990007183184'  # 240004546504 VALV Кран 240004546504 -
    VALVE = '110000924874'  # 240004546504 VALV Кран 240004546504 -


NAME = {

  # PigType
  PigType.MFL: u"Дефектоскоп магнитный продольного намагничивания",
  PigType.TFI: u"Дефектоскоп магнитный поперечного намагничивания",
  PigType.CALIPER_MECH: u"Рычажный (профилемер)",
  PigType.NAVIGATE: u"Поршень навигационно-топографический",
  PigType.ULTRASONIC: u"Ультразвуковой дефектоскоп",
  PigType.CALIPER_MAGN: u"Магнитный профилемер",
  PigType.EMAP: u"Дефектоскоп электромагнитный акустический",
  PigType.COMBO: u"Комбинированный дефектоскоп",
  PigType.CLEANER: u"Очистной скребок",
  PigType.CALIPER_TOOL: u"Поршень-шаблон",

  # PassType
  PassType.COMPLEX: u"Комплексное внутритрубное обследование",
  PassType.COMPLEX_SKS: u"Комплексное внутритрубное обследование + СКС",
  PassType.COMPLEX_NAV: u"Комплексное внутритрубное обследование+навигация",
  PassType.NAVIGATE: u"Навигационно-профильное обследование",
  PassType.CALIPER: u"Профильное обследование",
  PassType.TFI: u"Стресc-коррозионное обследование",
  PassType.ULTRASONIC: u"Ультразвуковое обследование (УЗК)",
  PassType.EXPERIMENTAL: u"Экспериментальное обследование",
  PassType.EMAP: u"ЭМАП-обследование",

  # Tube
  Tube.BEZSHOV: u"Бесшовная",
  Tube.DVUSHOV: u"Двухшовная",
  Tube.UNKNOWN: u"Неопределенная секция",
  Tube.ODNOSHOV: u"Одношовная",
  Tube.SPIRAL: u"Спиралешовная",

  # Company
  Company.BSPC: u"BSPC B.V",
  Company.AVTOGAZ: u"Автогаз, ОАО",
  Company.AEROCOSM: u"Аэрокосмический мониторинг и технологии, ЗАО",
  Company.BKH: u"Бейкер Хьюз Технологии и трубопроводный сервис, АО",
  Company.GPAS: u"Газприборавтоматикасервис, ЗАО",
  Company.DIASCAN: u"ЦТД Диаскан, ОАО",
  Company.DIAPROM: u"НТЦ Диапром, ООО",
  Company.OEG: u"Оргэнергогаз, ОАО",
  Company.PODVGAZENERGO: u"Подводгазэнергосервис, ООО",
  Company.PODVODDIAG: u"Подводдиагностика, ООО",
  Company.PODVODSERV: u"Подводсервис, ООО",
  Company.ROZEN: u"Розен",
  Company.SNG: u"НПО Спецнефтегаз, ЗАО",
  Company.TUBOSCAN: u"Тьюбоскан, ООО",
  Company.VNUTRITRUBDIAG: u"НПЦ Внутритрубная диагностика, ООО",

  # MethodsKBD
  MethodsKBD.API579: u"API 579 Трещины, Уровень 2",
  MethodsKBD.ASME: u"ASME B31G-1991",
  MethodsKBD.BS7910: u"BS 7910:2005",
  MethodsKBD.DNV: u"DNV-RP-F101-2004",
  MethodsKBD.NGKS: u"Методика определения опасности повреждений стенки трубопроводов по данным обследования "
                   u"магнитными дефектоскопами, ультразвуковыми дефектоскопами и профилемерами, "
                   u"ЗАО 'Нефтегазкомплектсервис', 2000",
  MethodsKBD.GAZNADZOR2008: u"Инструкция по оценке дефектов труб... ООО Газнадзор, 2006/2008",
  MethodsKBD.ASMEB31G: u"Модифицированный ASME B31G, 1993",
  MethodsKBD.STO112: u"СТО Газпром 2-2.3-112",
  MethodsKBD.STO173: u"СТО Газпром 2-2.3-173",
  MethodsKBD.ASME2012: u"ASME B31G-2012",
  MethodsKBD.GAZNADZOR2013: u"Инструкция по оценке дефектов труб... ООО Газнадзор, 2013",
  MethodsKBD.VRD: u"ВРД 39-1.10-004-99",

  # Feature
  Feature.ANOMALY: u"Аномалия неизвестной природы",
  Feature.NESVAR_STYK: u"Несваренный стык патрона",
  Feature.POTERYA_CONTACTA: u"Потеря контакта с трубой",
  Feature.EXCENTR_CASE: u"Эксцентричный патрон",
  Feature.ANOMAL_KOLTSEVOGO: u"Аномалия кольцевого шва",
  Feature.ANOMAL_OBLTSOVKI: u"Аномалия облицовки шва",
  Feature.CORROZ_KOLTSEVOGO: u"Коррозия на кольцевом шве",
  Feature.NEPROVAR_UTYAZH: u"Непровар / утяжина",
  Feature.NO_USILEN_KOLTSEVOGO: u"Отсутствие усиления сварного шва",
  Feature.PODKLAD_KOLTSO: u"Подкладное кольцо",
  Feature.PODREZ: u"Подрез",
  Feature.PRAVKA_KROMOK: u"Правка кромок",
  Feature.PROVIS_KORNYA: u"Провис корня шва",
  Feature.SMESCHENIE_KROMOK: u"Смещение кромок",
  Feature.VNUTRI_SHOV_DEFEKT: u"Внутришовный дефект",
  Feature.PODGIB_KROMKY: u"Подгиб кромки со смещением",
  Feature.ANOMAL_PRODOLNOGO: u"Аномалия продольного шва",
  Feature.VYSHLIFOVKA_PRODOLNOGO: u"Место вышлифовки продольного шва",
  Feature.FORMA_PRODOLNOGO: u"Нарушение формы продольного шва",
  Feature.ANOMAL_SPIRALNOGO: u"Аномалия спирального шва",
  Feature.VYSHLIFOVKA_SPIRALNOGO: u"Место вышлифовки спирального шва",
  Feature.FORMA_SPIRALNOGO: u"Нарушение формы спирального шва",
  Feature.DENT: u"Вмятина",
  Feature.DENT_METAL_LOSS: u"Вмятина с дефектами потери металла",
  Feature.VNUTRYSTEN_RASSLOENIE: u"Внутристенное расслоение",
  Feature.GOFRA: u"Гофра",
  Feature.FACTORY_DEFEKT: u"Заводской дефект",
  Feature.METALL_DEFEKT: u"Металлургический дефект",
  Feature.VYSHLIFOVKA: u"Вышлифовка",
  Feature.ZONE_VERT_CRACKS: u"Зона поперечных трещин",
  Feature.ZONE_HOR_CRACKS: u"Зона продольных трещин",
  Feature.ZONE_CORROZ: u"Зона коррозии",
  Feature.CAVERNA: u"Каверна",
  Feature.CORROZ: u"Коррозия",
  Feature.KANAVKA_VERT: u"Поперечная канавка",
  Feature.METALL_LOSS: u"Потеря металла",
  Feature.KANAVKA_HOR: u"Продольная канавка",
  Feature.POINT_CORROZ: u"Точечная коррозия",
  Feature.MECHANICAL_DEFEKT: u"Механическое повреждение",
  Feature.RANDOM_ARC: u"Случайная дуга",
  Feature.RASSL_NO_POVERHNOST: u"Расслоение с выходом на поверхность",
  Feature.ZAVARKA: u"Заварка",
  Feature.ZAVARKA_OTVERST: u"Заварка отверстия",
  Feature.TECHNOLOGY_DEFEKT: u"Технологический дефект",
  Feature.CRACK_VERT_SHOV: u"Трещина на кольцевом шве",
  Feature.CRACK_HOR_SHOV: u"Трещина на продольном шве",
  Feature.CRACK_SPIRAL_SHOV: u"Трещина на спиральном шве",
  Feature.NESPLOSHNOST_PT: u"Несплошность плоскостного типа",
  Feature.CRACK_VERT: u"Поперечная трещина",
  Feature.CRACK_HOR: u"Продольная трещина",
  Feature.OVAL: u"Овализация",
  Feature.METALL_OUT: u"Металл снаружи",
  Feature.ISOL_STYK: u"Изоляционный стык",
  Feature.CURVE_INSERT: u"Кривая вставка",
  Feature.SEGMENT_INSERT: u"Сегментная вставка",
  Feature.HOMUT: u"Хомут",
  Feature.PIG_RUN: u"Камера запуска",
  Feature.PIG_RECEIVE: u"Камера приема",
  Feature.MARKER: u"Маркер",
  Feature.MARKER_RING: u"Маркерное кольцо",
  Feature.MARKER_MAGN: u"Маркер магнитный",
  Feature.ZAVAR_BOBYSHKI: u"Заварка бобышки",
  Feature.ZAVAR_OKNA: u"Заварка окна",
  Feature.REMONT_NAKLAD: u"Ремонтная накладка, вышлифовка и т.п.",
  Feature.METALL_CASE_START: u"Металлическая упрочняющая муфта, начало",
  Feature.METALL_CASE_END: u"Металлическая упрочняющая муфта, конец",
  Feature.KOMPOS_CASE_START: u"Композитная упрочняющая муфта, начало",
  Feature.KOMPOS_CASE_END: u"Композитная упрочняющая муфта, конец",
  Feature.WRONG_CONSTRUCT: u"Недопустимый конструктивный элемент",
  Feature.UNKNOWN: u"Нераспознанный объект",
  Feature.DU1000_DU1200: u"Переход с диаметра ДУ 1000 мм на ДУ 1200 мм.",
  Feature.DU1200_DU1000: u"Переход с диаметра ДУ 1200 мм на ДУ 1000 мм.",
  Feature.DU1200_DU1400: u"Переход с диаметра ДУ 1200 мм на ДУ 1400 мм.",
  Feature.DU1400_DU1200: u"Переход с диаметра ДУ 1400 мм на ДУ 1200 мм.",
  Feature.TUBE_ARMATURE: u"Трубная арматура",
  Feature.ELEMENT_OBUSTROY: u"Элемент обустройства",
  Feature.WATER_START: u"Начало водной преграды",
  Feature.WATER_END: u"Конец водной преграды",
  Feature.FLANETS: u"Фланцевые соединения",
  Feature.OTVOD_VREZKA: u"Отвод-врезка",
  Feature.CASE_START: u"Патрон начало",
  Feature.CASE_END: u"Патрон конец",
  Feature.PRIGRUZ_RING: u"Пригруз кольцевой",
  Feature.PRIGRUZ_START: u"Участок пригрузов начало",
  Feature.PRIGRUZ_END: u"Участок пригрузов конец",
  Feature.TROYNIK: u"Тройник",
  Feature.WALL_THICK: u"Изменение толщины стенки трубы",
  Feature.TURN_START: u"Отвод (поворот) начало",
  Feature.TURN_END: u"Отвод (поворот) конец",
  Feature.TURN_SEGM_START: u"Сегментный участок начало",
  Feature.TURN_SEGM_END: u"Сегментный участок конец",
  Feature.TURN_SEGM: u"Секторный отвод",
  Feature.WELD: u"Шов кольцевой",
  Feature.ZADVIZHKA: u"Задвижка",
  Feature.VALVE: u"Шаровой кран",
}
