import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import asyncio
# https://github.com/TeKrop/overfast-api
# https://overfast-api.tekrop.fr
lang = {
    "Hero Specific" : "Особые показатели героя",
    "Best" : "Лучшее",
    "Eliminations - Most in Game" : "Убийств (макс. за матч)",
    "All Damage Done - Most in Game" : "Макс. урона нанесено за матч",    
    "Defensive Assists - Most in Game" : "Защитных содействий (макс. за матч)",
    "Offensive Assists - Most in Game" : "Боевых содействий (макс. за матч)",
    "Objective Kill" : "Убийств у объектов",     
    "Objective Kills - Most in Game" : "Убийств у объектов (макс. за матч)",   
    "Objective Time - Most in Game" : "Макс. выполнение задач за матч",
    "Multikill - Best" : "Лучшее множественное убийство",
    "Solo Kills - Most in Game" : "Одиночных убийств (макс. за матч)",
    "Time Spent on Fire - Most in Game" : "Макс. времени в ударе за матч",
    "Melee Final Blows - Most in Game" : "Смертельных ударов в рукопашной (макс. за матч)",
    "Environmental Kills - Most in Game" : "Несчастных случаев подстроено (макс. за матч)",
    "Kill Streak - Best" : "Лучшая серия убийств",
    "Weapon Accuracy" : "Меткость",
    "Win Percentage" : "Процент побед",
    "Hero Damage Done - Most in Game" : "Макс. урона по героям за матч",
    "Barrier Damage Done - Most in Game" : "Урона по барьерам (макс. за матч)",
    "Assists - Most in Game" : "Содействий (макс. за матч)",
    "Objective Contest Time - Most in Game" : "Время состязания (задача, макс. за матч)",
    "Recon Assists - Most in Game" : "Содействий с обнаружением (макс. за матч)",
    "Average" : "В среднем",
    "Hero Damage Done - Avg per 10 Min" : "Урона по героям в среднем за 10 мин.",
    "Deaths - Avg per 10 Min" : "Смертей (в среднем за 10 мин.)",
    "Assists - Avg per 10 min" : "Содействий (в среднем за 10 мин.)",
    "Eliminations - Avg per 10 Min" : "Убийств (в среднем за 10 мин.)",
    "Healing Done - Avg per 10 Min" : "Объем исцеления (в среднем за 10 мин.)",
    "Objective Kills - Avg per 10 Min" : "Убийств у объектов (в среднем за 10 мин.)",
    "Objective Time - Avg per 10 Min" : "Выполнение задач (в среднем за 10 мин.)",
    "Final Blows - Avg per 10 Min" : "Смертельных ударов (в среднем за 10 мин.)",
    "Time Spent on Fire - Avg per 10 Min" : "Время в ударе (в среднем за 10 мин.)",      
    "Objective Contest Time - Avg per 10 Min" : "Время состязания (задача, в среднем за 10 мин.)",
    "Solo Kills - Avg per 10 Min" : "Одиночных убийств (в среднем за 10 мин.)",
    "Game" : "Игра",
    "Time Played" : "Время в игре",
    "Games Played" : "Матчей сыграно",
    "Games Won" : "Матчей выиграно",
    "Games Lost" : "Матчей проиграно",
    "Hero Wins" : "Побед героя",
    "Combat" : "Бой",
    "Environmental Kill" : "Несчастных случаев подстроено",
    "Environmental Kills" : "Несчастных случаев подстроено",
    "Multikill" : "Множественных убийств",
    "Multikills" : "Множественных убийств",
    "Hero Damage Done" : "Урона по героям",
    "Deaths" : "Смертей",
    "Elimination" : "Убийств",
    "Eliminations" : "Убийств",
    "Damage Done" : "Урона нанесено",
    "Objective Kills" : "Убийств у объектов",
    "Final Blow" : "Смертельных ударов",
    "Final Blows" : "Смертельных ударов",
    "Objective Time" : "Выполнение задач",
    "Melee Final Blow" : "Смертельных ударов в рукопашной",
    "Melee Final Blows" : "Смертельных ударов в рукопашной",
    "Time Spent on Fire" : "Время в ударе",
    "Objective Contest Time" : "Время состязания (задача)",
    "Solo Kills" : "Одиночных убийств",
    "Assists" : "Содействий",
    "Recon Assists" : "Содействий с обнаружением",
    "Healing Done" : "Объем исцеления",
    "Defensive Assists" : "Защитных содействий",
    "Offensive Assists" : "Боевых содействий",
    "Match Awards" : "Награды за матчи",
    "Cards" : "Карт в конце матча",
    "Self Healing" : "Самолечение",
    "Self Healing - Most in Game" : "Макс. самолечения за матч",
    "Enemies Slept" : "Врагов усыплено",
    "Nano Boost Assists" : "Содействий со стимулятором",
    "Unscoped Accuracy - Best in Game" : "Лучшая меткость без прицела за матч",
    "Enemies Slept - Most in Game" : "Врагов усыплено (макс. за матч)",
    "Nano Boost Assists - Most in Game" : "Содействий со стимулятором (макс. за матч)",
    "Biotic Grenade Kills" : "Убийств «Биотической гранатой»",
    "Damage Amplified" : "Бонусного урона",
    "Damage Amplified - Most in Game" : "Бонусного урона (макс. за матч)",
    "Healing Amplified" : "Бонусного исцеления",
    "Healing Amplified - Most in Game" : "Бонусного исцеления (макс. за матч)",
    "Biotic Grenade Kills - Avg per 10 Min" : "Убийств «Биотической гранатой» (в среднем за 10 мин.)",
    "Enemies Slept - Avg per 10 Min" : "Врагов усыплено (в среднем за 10 мин.)",
    "Nano Boost Assists - Avg per 10 Min" : "Содействий со стимулятором (в среднем за 10 мин.)",
    "Unscoped Accuracy" : "Меткость без прицела",
    "Self Healing - Avg per 10 Min" : "Самолечение (в среднем за 10 мин.)",
    "Damage Amplified - Avg per 10 Min" : "Бонусного урона (в среднем за 10 мин.)",
    "Scoped Accuracy" : "Меткость в снайперском режиме",
    "Dynamite Kill - Most in Game" : "Убийство «Динамитом» (макс. за матч)",
    "Scoped Critical Hits" : "Критических попаданий (снайпер)",
    "Scoped Critical Hits - Most in Game" : "Критических попаданий (снайпер, макс. за матч)",
    "Dynamite Kills" : "Убийств «Динамитом»",
    "Dynamite Kills - Most in Game" : "Убийств «Динамитом» (макс. за матч)",
    "Coach Gun Kills" : "Убийств «Обрезом»",
    "Coach Gun Kills - Most in Game" : "Убийств «Обрезом» (макс. за матч)",
    "Bob Kill" : "Боб убил",
    "Bob Kills" : "Убийство у Боба",
    "Bob Kill - Most in Game" : "Убийство при помощи Боба (макс. за матч)",
    "Bob Kills - Most in Game" : "Убийство при помощи Боба (макс. за матч)",
    "Scoped Critical Hit Kills" : "Убийств критическим попаданием (снайпер)",
    "Long Range Final Blow" : "Смертельных ударов издалека",
    "Long Range Final Blows" : "Смертельных ударов издалека",
    "Long Range Final Blows - Most in Game" : "Смертельных ударов издалека (макс. за матч)",  
    "Dynamite Kills - Avg per 10 Min" : "Убийств «Динамитом» (в среднем за 10 мин.)",
    "Bob Kills - Avg per 10 Min" : "Убийств при помощи Боба (в среднем за 10 мин.)",
    "Coach Gun Kills - Avg per 10 Min" : "Убийств «Обрезом» (в среднем за 10 мин.)",
    "Scoped Critical Hits - Avg per 10 Min" : "Критических попаданий (снайпер, в среднем за 10 мин.)",
    "Scoped Critical Hit Kills - Avg per 10 Min" : "Убийств критическим попаданием (снайпер, в среднем за 10 мин.)",
    "Amplification Matrix Assists" : "Содействий с «Усиливающей матрицей»",
    "Healing Accuracy - Best in Game" : "Лучшая меткость (гранаты)",
    "Amplification Matrix Assists - Best in Game" : "Содействий с «Усиливающей матрицей» (макс. за матч)",
    "Immortality Field Deaths Prevented" : "Смертей предотвращено «Полем бессмертия»",
    "Immortality Field Deaths Prevented - Most in Game" : "Смертей предотвращено «Полем бессмертия» (макс. за матч)",
    "Healing Amplified - Avg per 10 Min" : "Бонусного исцеления (в среднем за 10 мин.)",
    "Amplification Matrix Assists - Avg per 10 Min" : "Содействий с «Усиливающей матрицей» (в среднем за 10 мин.)",
    "Immortality Field Deaths Prevented - Avg per 10 Min" : "Смертей предотвращено «Полем бессмертия» (в среднем за 10 мин.)",
    "Healing Accuracy" : "Меткость (гранаты)",
    "Artillery Kills" : "Убийств артиллерией",
    "Artillery Kills - Most in Game" : "Убийств артиллерией (макс. за матч)",
    "Recon Kills" : "Убийств в режиме разведки",
    "Recon Kills - Most in Game" : "Убийств в режиме разведки (макс. за матч)",
    "Assault Kills" : "Убийств штурмовиком",
    "Tank Kills - Most in Game" : "Убийств в режиме танка (макс. за матч)",
    "Tactical Grenade Kills" : "Убийств тактической гранатой",
    "Tactical Grenade Kills - Most in Game" : "Убийств тактической гранатой (макс. за матч)",
    "Artillery Kills - Avg per 10 Min" : "Убийств артиллерией (в среднем за 10 мин.)",
    "Tactical Grenade Kills - Avg per 10 Min" : "Убийств тактической гранатой (в среднем за 10 мин.)",    
    "Assault Kills - Avg per 10 Min" : "Убийств штурмовиком (в среднем за 10 мин.)",
    "Recon Kills - Avg per 10 Min" : "Убийств в режиме разведки (в среднем за 10 мин.)",
    "Overhealth Provided" : "Доп. здоровья предоставлено",
    "Overhealth Provided - Most in Game" : "Доп. здоровья предоставлено (макс. за матч)",
    "Whipshots Attempted" : "Попыток использовать «Хлесткий удар»",
    "Players Knocked Back" : "Игроков отброшено",
    "Players Knocked Back - Avg per 10 Min NYI" : "Игроков отброшено (в среднем за 10 мин., NYI)",  
    "Overhealth Provided - Avg per 10 Min" : "Доп. здоровья предоставлено (в среднем за 10 мин.)",
    "Whipshot Accuracy" : "Меткость «Хлесткого удара»",
    "Inspire Uptime Percentage" : "Время действия «Воодушевления»",
    "Deadeye Kill" : "Убийств «Метким стрелком»",
    "Deadeye Kills" : "Убийств «Метким стрелком»",
    "Deadeye Kill - Most in Game" : "Убийств «Метким стрелком» (макс. за матч)",
    "Deadeye Kills - Most in Game" : "Убийств «Метким стрелком» (макс. за матч)",
    "Fan the Hammer Kills" : "Убийств беглым огнем",
    "Fan the Hammer Kills - Most in Game" : "Убийств беглым огнем (макс. за матч)",
    "Magnetic Grenade Kills" : "Убийств «Магнитной гранатой»",
    "Magnetic Grenade Kills - Most in Game" : "Убийств «Магнитной гранатой» (макс. за матч)",
    "Magnetic Grenade Kills - Avg per 10 Min" : "Убийств «Магнитной гранатой» (в среднем за 10 мин.)",
    "Magnetic Grenade Attach Rate" : "Доля прицепленных магнитных гранат",
    "Deadeye Kills - Avg per 10 Min" : "Убийств «Метким стрелком» (в среднем за 10 мин.)",
    "Fan the Hammer Kills - Avg per 10 Min" : "Убийств беглым огнем (в среднем за 10 мин.)",
    "Self-Destruct Kills" : "Убийств «Самоуничтожением»",
    "Self-Destruct Kills - Most in Game" : "Убийств «Самоуничтожением» (макс. за матч)",
    "Micro Missile Kills" : "Убийств микроракетой",
    "Call Mech Kills" : "Убийств вызовом мехи",
    "Call Mech Kills - Most in Game" : "Убийств вызовом мехи (макс. за матч)",
    "Micro Missile Kills - Most in Game" : "Убийств микроракетой (макс. за матч)",
    "Call Mech Kill - Most in Game" : "Убийство вызовом мехи (макс. за матч)",
    "Self-Destruct Kills - Avg per 10 Min" : "Убийств «Самоуничтожением» (в среднем за 10 мин.)",
    "Call Mech Kills - Avg per 10 Min" : "Убийств вызовом мехи (в среднем за 10 мин.)",
    "Micro Missile Kills - Avg per 10 Min" : "Убийств микроракетой (в среднем за 10 мин.)",
    "Meteor Strike Kills" : "Убийств «Ударом метеора»",
    "Meteor Strike Kills - Most in Game" : "Убийств «Ударом метеора» (макс. за матч)",
    "Overhealth Created" : "Накоплено доп. здоровья",
    "Overhealth Created - Most in Game" : "Накоплено доп. здоровья (макс. за матч)",
    "Rocket Punch Kills" : "Убийств «Реактивным ударом»",
    "Seismic Slam Kills" : "Убийств «Дрожью земли»",
    "Seismic Slam Kills - Most in Game" : "Убийств «Дрожью земли» (макс. за матч)",
    "Rocket Punch Kills - Most in Game" : "Убийств «Реактивным ударом» (макс. за матч)",
    "Rocket Punch Kills - Avg per 10 Min" : "Убийств «Реактивным ударом» (в среднем за 10 мин.)",
    "Seismic Slam Kills - Avg per 10 Min" : "Убийств «Дрожью земли» (в среднем за 10 мин.)",
    "Overhealth Created - Avg per 10 Min" : "Накоплено доп. здоровья (в среднем за 10 мин.)",
    "Meteor Strike Kills - Avg per 10 Min" : "Убийств «Ударом метеора» (в среднем за 10 мин.)",
    "Focusing Beam Kills" : "Убийств «Направленным лучом»",
    "Focusing Beam Kills - Most in Game" : "Убийств «Направленным лучом»",     
    "Sticky Bombs Kills" : "Убийств «Бомбами-липучками»",
    "Sticky Bombs Kills - Most in Game" : "Убийств «Бомбами-липучками» (макс. за матч)",
    "Duplicate Kills" : "Убийств во время «Дубликации»",
    "Duplicate Kills - Most in Game" : "Убийств во время «Дубликации» (макс. за матч)",
    "Sticky Bombs Direct Hits - Most in Game" : "Прямых попаданий «Бомбами-липучками» (макс. за матч)",       
    "Duplicate Kills - Avg per 10 Min" : "Убийств во время «Дубликации» (в среднем за 10 мин.)",
    "Focusing Beam Accuracy" : "Меткость «Направленного луча»",
    "Focusing Beam Kills - Avg per 10 Min" : "Убийств «Направленным лучом» (в среднем за 10 мин.)",
    "Sticky Bombs Direct Hit Accuracy" : "Меткость «Бомб-липучек» (прямые попадания)",
    "Sticky Bombs Kills - Avg per 10 Min" : "Убийств «Бомбами-липучками» (в среднем за 10 мин.)",
    "Sticky Bombs Direct Hits - Avg per 10 Min" : "Прямых попаданий «Бомбами-липучками» (в среднем за 10 мин.)",    
    "Dragonblade Kills" : "Убийств «Клинком дракона»",
    "Dragonblade Kills - Most in Game" : "Убийств «Клинком дракона» (макс. за матч)",
    "Damage Reflected" : "Урона отражено",
    "Damage Reflected - Most in Game" : "Макс. урона отражено за матч",
    "Swift Strike Resets" : "Сбросов «Молниеносного удара» (макс. за матч)",
    "Swift Strike Resets - Most in Game" : "Сбросов «Молниеносного удара» (макс. за матч)",
    "Dragonblade Kills - Avg per 10 Min" : "Убийств «Клинком дракона» (в среднем за 10 мин.)",
    "Damage Reflected - Avg per 10 Min" : "Урона отражено (в среднем за 10 мин.)",
    "Dragonstrike Kills" : "Убийств «Ударом дракона»",
    "Dragonstrike Kills - Most in Game" : "УБийств «Ударом дракона» (макс. за матч)",
    "Storm Arrow Kills" : "Убийств «Шквалом»",
    "Storm Arrow Kills - Most in Game" : "Убийств «Шквалом» (макс. за матч)",
    "Dragonstrike Kills - Avg per 10 Min" : "Убийств «Ударом дракона» (в среднем за 10 мин.)",
    "Storm Arrow Kills - Avg per 10 Min" : "Убийств «Шквалом» (в среднем за 10 мин.)",
    "Jagged Blade Kills" : "Убийств «Зазубренным клинком»",
    "Jagged Blade Kills - Most in Game" : "Убийств «Зазубренным клинком» (макс. за матч)",
    "Jagged Blade Accuracy - Best in Game" : "Лучшая меткость «Зазубренного клинка» за матч",
    "Carnage Kills" : "Убийств с «Карнажем»",
    "Carnage Kills - Most in Game" : "Убийств с «Карнажем» (макс. за матч)",
    "Rampage Kills" : "Убийств с «Буйством»",
    "Rampage Kills - Most in Game" : "Убийств с «Буйством» (макс. за матч)",
    "Wound Uptime Percentage" : "Процент эффективного поддержания «Раны»",
    "Jagged Blade Accuracy" : "Меткость «Зазубренного клинка»",
    "Jagged Blade Kills - Avg per 10 Min" : "Убийств «Зазубренным клинком» (в среднем за 10 мин.)",
    "Carnage Kills - Avg per 10 Min" : "Убийств с «Карнажем» (в среднем за 10 мин.)",
    "Rampage Kills - Avg per 10 Min" : "Убийств с «Буйством» (в среднем за 10 мин.)",
    "Enemies Trapped - Most in Game" : "Врагов попалось в «Капкан» (макс. за матч)",
    "Enemies Trapped" : "Врагов попалось в «Капкан»",
    "RIP-Tire Kills - Most in Game" : "Убийств «Адской шиной» (макс. за матч)",
    "RIP-Tire Kills" : "Убийств «Адской шиной»",
    "Concussion Mine Kills" : "Убийств «Фугасной миной»",
    "Concussion Mine Kills - Most in Game" : "Убийств «Фугасной миной» (макс. за матч)",
    "Direct Hit Accuracy" : "МЕткость (прямые попадания)",
    "Enemies Trapped - Avg per 10 Min" : "Врагов попалось в «Капкан» (в среднем за 10 мин.)",
    "Concussion Mine Kills - Avg per 10 Min" : "Убийств «Фугасной миной» (в среднем за 10 мин.)",
    "RIP-Tire Kills - Avg per 10 Min" : "Убийств «Адской шиной» (в среднем за 10 мин.)",
    "Negative Effects Cleansed - Most in Game" : "Отрицательных эффектов снято (макс. за матч)",      
    "Kitsune Rush Assists" : "Содействий с помощью «Рывка кицунэ»",
    "Kitsune Rush Assists - Most in Game" : "Содействий с помощью «Рывка кицунэ» (макс. за матч)",
    "Kunai Kills" : "Убийств кунаем",
    "Kunai Kills - Most in Game" : "Убийств кунаем (макс. за матч)",
    "Negative Effects Cleansed - Avg per 10 Min" : "Отрицательных эффектов снято (в среднем за 10 мин.)",   
    "Kitsune Rush Assists - Avg per 10 Min" : "Содействий с помощью «Рывка кицунэ» (в среднем за 10 мин.)",
    "Kunai Kills - Avg per 10 Min" : "Убийств кунаем (в среднем за 10 мин.)",
    "Sound Barriers Provided" : "Наложений «Звукового барьера»",
    "Sound Barriers Provided - Most in Game" : "Наложений «Звукового барьера» (макс. за матч)",
    "Players Knocked Back - Most in Game" : "Игроков отброшено (макс. за матч)",
    "Players Knocked Back - Avg per 10 Min" : "Игроков отброшено (в среднем за 10 мин.)",
    "Sound Barriers Provided - Avg per 10 Min" : "Наложений «Звукового барьера» (в среднем за 10 мин.)",     
    "Enemies Frozen" : "Врагов заморожено",
    "Enemies Frozen - Most in Game" : "Врагов заморожено (макс. за матч)",
    "Blizzard Kills - Most in Game" : "Убийств «Вьюгой» (макс. за матч)",
    "Blizzard Kills" : "Убийств «Вьюгой»",
    "Blizzard Kills - Avg per 10 Min" : "Убийств «Вьюгой» (в среднем за 10 мин.)",
    "Icicle Accuracy" : "Меткость сосулек",
    "Enemies Frozen - Avg per 10 Min" : "Врагов заморожено (в среднем за 10 мин.)",
    "Icicle Critical Accuracy" : "Меткость сосульки (крит.)",
    "Blaster Kills" : "Убийств бластером",
    "Blaster Kills - Most in Game" : "Убийств бластером (макс. за матч)",
    "Players Resurrected" : "Игроков воскрешено",
    "Players Resurrected - Most in Game" : "Игроков воскрешено (макс. за матч)",
    "Players Resurrected - Avg per 10 Min" : "Игроков воскрешено (в среднем за 10 мин.)",
    "Blaster Kills - Avg per 10 Min" : "Убийств бластером (в среднем за 10 мин.)",
    "Coalescence Kills" : "Убийств «Коалесценцией»",
    "Coalescence Kills - Most in Game" : "Убийств «Коалесценцией» (макс. за матч)",
    "Coalescence Healing" : "Исцеление «Коалесценцией»",
    "Coalescence Healing - Most in Game" : "Объем исцеления «Коалесценцией» (макс. за матч)",
    "Biotic Orb Kills" : "Убийств «Биотической сферой»",
    "Biotic Orb Kills - Most in Game" : "Убийств «Биотической сферой» (макс. за матч)",
    "Secondary Fire Accuracy" : "Меткость (доп. режим огня)",
    "Ally Coalescence Efficiency" : "Эффективность воздействия «Коалесценции» на союзников",
    "Biotic Orb Kills  - Avg per 10 Min" : "Убийств «Биотической сферой» (в среднем за 10 мин.)",
    "Enemy Coalescence Efficiency" : "Эффективность воздействия «Коалесценции» на противников",
    "Coalescence Kills - Avg per 10 Min" : "Убийств «Биотической сферой» (макс. за матч)",
    "Coalescence Healing - Avg per 10 Min" : "Объем исцеления «Коалесценцией» (в среднем за 10 мин.)",
    "Biotic Orb Kills - Avg per 10 Min" : "Убийств «Биотической сферой» (в среднем за 10 мин.)",
    "Terra Surge Kills" : "Убийств «Встряской земли»",
    "Terra Surge Kills - Most in Game" : "Убийств «Встряской земли» (макс. за матч)",
    "Energy Javelin Kills" : "Убийств энергетическим копьем",
    "Javelin Spin Kills" : "Убийств «Вращением копья»",
    "Energy Javelin Kills NYI" : "Убийств энергетическим копьем",
    "Javelin Spin Kills NYI" : "Убийств «Вращением копья»",
    "Terra Surge Kills - Avg per 10 Min" : "Убийств «Встряской земли» (в среднем за 10 мин.)",
    "Javelin Spin Kills - Avg per 10 Min" : "Убийств «Вращением копья» (в среднем за 10 мин.)",
    "Energy Javelin Kills - Avg per 10 Min" : "Убийств энергетическим копьем (в среднем за 10 мин.)",        
    "Rocket Direct Hits" : "Прямых попаданий ракетой",
    "Barrage Kills" : "Убийств «Ракетным залпом»",
    "Rocket Direct Hits - Most in Game" : "Прямых попаданий ракетой (макс. за матч)",
    "Barrage Kills - Most in Game" : "Убийств «Ракетным залпом» (макс. за матч)",
    "Long Range Final Blow - Most in Game" : "Смертельный удар издалека (макс. за матч)",    
    "Barrage Kills - Avg per 10 Min" : "Убийств «Ракетным залпом» (в среднем за 10 мин.)",
    "Airtime Percentage" : "Процент времени в воздухе",
    "Rocket Direct Hits - Avg per 10 Min" : "Прямых попаданий ракетой (в среднем за 10 мин.)",
    "Pummel Kills" : "Убийств «Резким ударом»",
    "Pummel Kills - Most in Game" : "Убийств «Резким ударом» – рекорд матча",
    "Ravenous Vortex Kills" : "Убийств «Ненасытным вихрем»",
    "Ravenous Vortex Kills - Most in Game" : "Убийств «Ненасытным вихрем» – рекорд матча",
    "Annihilation Kills" : "Убийств «Аннигиляцией»",
    "Annihilation Kills - Most in Game" : "Убийств «Аннигиляцией» – рекорд матча",
    "Annihilation Kills - Avg per 10 Min" : "Убийств «Аннигиляцией» (в среднем за 10 мин.)",
    "Ravenous Vortex Kills - Avg per 10 Min" : "Убийств «Ненасытным вихрем» (в среднем за 10 мин.)",
    "Pummel Accuracy" : "Точность «Резкого удара»",
    "Pummel Kills - Avg per 10 Min" : "Убийств с «Резким ударом» (в среднем за 10 мин.)",
    "Death Blossom Kills" : "Убийств «Цветком смерти»",
    "Death Blossom Kills - Most in Game" : "Убийств «Цветком смерти» (макс. за матч)",
    "Death Blossom Kills - Avg per 10 Min" : "Убийств «Цветком смерти» (в среднем за 10 мин.)",      
    "Charge Kills" : "Убийств «Рывком»",
    "Charge Kills - Most in Game" : "Убийств «Рывком» (макс. за матч)",
    "Fire Strike Kills" : "Убийств «Огненным ударом»",
    "Fire Strike Kills - Most in Game" : "Убийств «Огненным ударом» (макс. за матч)",
    "Earthshatter Kills" : "Убийств «Землетрясением»",
    "Earthshatter Kills - Most in Game" : "Убийств «Землетрясением» (макс. за матч)",
    "Earthshatter Direct Hits" : "Прямых попаданий «Землетрясением»",
    "Charge Kills - Avg per 10 Min" : "Убийств «Рывком» (в среднем за 10 мин.)",
    "Earthshatter Kills - Avg per 10 Min" : "Убийств «Землетрясением» (в среднем за 10 мин.)",        
    "Earthshatter Direct Hits - Avg per 10 Min" : "Прямых попаданий «Землетрясения» (в среднем за 10 мин.)",   
    "Fire Strike Kills - Avg per 10 Min" : "Убийств «Огненным ударом» (в среднем за 10 мин.)",
    "Whole Hog Kills - Most in Game" : "Убийств «Турбосвинством» (макс. за матч)",
    "Whole Hog Kill - Most in Game" : "Убийств «Турбосвинством» (макс. за матч)",
    "Whole Hog Kill" : "Убийств «Турбосвинством»",
    "Whole Hog Kills" : "Убийств «Турбосвинством»",
    "Chain Hook Accuracy - Best in Game" : "Лучшая меткость с крюком за матч",
    "Chain Hook Kills" : "Убийств броском крюка",
    "Whole Hog Kills - Avg per 10 Min" : "Убийств «Турбосвинством» (в среднем за 10 мин.)",
    "Chain Hook Kills - Avg per 10 Min" : "Убийств броском крюка (в среднем за 10 мин.)",
    "Chain Hook Accuracy" : "Точность броска крюка",
    "Accretion Kills - Most in Game" : "Убийств «Аккрецией» (макс. за матч)",
    "Accretion Kills" : "Убийств «Аккрецией»",
    "Gravitic Flux Kills" : "Убийств «Гравитационным колодцем»",
    "Gravitic Flux Kills - Most in Game" : "Убийств «Гравитационным колодцем» (макс. за матч)", 
    "Accretion Kills - Avg per 10 Min" : "Убийств «Аккрецией» (в среднем за 10 мин.)",
    "Gravitic Flux Kills - Avg per 10 Min" : "Убийств «Гравитационным колодцем» (в среднем за 10 мин.)",
    "Charged Shot Kills - Most in Game" : "Убийств заряженным выстрелом (макс. за матч)",
    "Charged Shot Kills" : "Убийств заряженным выстрелом",
    "Charged Shot Accuracy - Best in Game" : "Лучшая меткость за матч (заряженные выстрелы)",
    "Overclock Kills - Most in Game" : "Убийств с «Разгоном» (макс. за матч)",
    "Overclock Kills" : "Убийств с «Разгоном»",
    "Disruptor Shot Kills" : "Убийств дезинтегрирующим выстрелом",
    "Disruptor Shot Kills - Most in Game" : "Убийств дезинтегрирующим выстрелом (макс. за матч)",
    "Charged Shot Critical Accuracy" : "Меткость крит. попаданий (заряженные выстрелы)",
    "Overclock Kills - Avg per 10 Min" : "Убийств с «Разгоном» (в среднем за 10 мин.)",
    "Disruptor Shot Kills - Avg per 10 Min" : "Убийств «Дезинтегрирующим выстрелом» (в среднем за 10 мин.)",     
    "Charged Shot Kills - Avg per 10 Min" : "Убийств заряженным выстрелом (в среднем за 10 мин.)",
    "Charged Shot Accuracy" : "Меткость (заряженные выстрелы)",
    "Helix Rocket Kills - Most in Game" : "Убийств «Ракетным ударом» (макс. за матч)",
    "Helix Rocket Kills" : "Убийств «Ракетным ударом»",
    "Tactical Visor Kills" : "Убийств с «Тактическим визором»",
    "Tactical Visor Kills - Most in Game" : "Убийств с «Тактическим визором» (макс. за матч)",  
    "Helix Rocket Kills - Avg per 10 Min" : "Убийств «Ракетным ударом» (в среднем за 10 мин.)",
    "Tactical Visor Kills - Avg per 10 Min" : "Убийств с «Тактическим визором» (в среднем за 10 мин.)",       
    "Helix Rocket Accuracy" : "Меткость ракетного удара",
    "EMP Kills" : "Убийств «Импульсом»",
    "EMP Kills - Most in Game" : "Убийств «Импульсом» (макс. за матч)",
    "EMP Kills - Avg per 10 Min" : "Убийств «Импульсом» (в среднем за 10 мин.)",
    "Low Health Teleports" : "Телепортов с низким здоровьем",
    "Low Health Teleports - Most in Game" : "Телепортов с низким здоровьем (макс. за матч)",
    "Low Health Teleports - Avg per 10 Min" : "Телепортов с низким здоровьем (в среднем за 10 мин.)",
    "Enemies Hacked" : "Врагов взломано",
    "Enemies Hacked - Most in Game" : "Врагов взломано (макс. за матч)",
    "Enemies Hacked - Avg per 10 Min" : "Врагов взломано (в среднем за 10 мин.)",
    "Sentry Turret Kills" : "Убийств защитными турелями",
    "Sentry Turret Kills - Most in Game" : "Убийств защитными турелями (макс. за матч)",
    "Players Teleported" : "Убийств защитными турелями (макс. за матч)",
    "Players Teleported - Most in Game" : "Убийств защитными турелями (макс. за матч)",
    "Players Teleported - Avg per 10 Min" : "Телепортаций (в среднем за 10 мин.)",
    "Primary Fire Accuracy" : "Меткость (осн. режим огня)",
    "Sentry Turret Kills - Avg per 10 Min" : "Убийства турелей — в среднем за 10 мин.",
    "Average Damage Multiplier" : "Средний множитель урона",
    "Secondary Direct Hits - Avg per 10 Min" : "Прямых попаданий в альт. режиме огня (в среднем за 10 мин.)",
    "Turret Kills" : "Убийств турелью",
    "Turret Kills - Most in Game" : "Убийств турелью (макс. за матч)",
    "Molten Core Kills" : "Убийств во время «Перегрева»",
    "Molten Core Kills - Most in Game" : "Убийств во время «Перегрева» (макс. за матч)",
    "Hammer Kills" : "Убийств молотом",
    "Hammer Kills - Most in Game" : "Убийств молотом (макс. за матч)",
    "Overload Kills" : "Убийств при «Перегрузке»",
    "Overload Kills - Most in Game" : "Убийств при «Перегрузке» (макс. за матч)",
    "Turret Kills - Avg per 10 Min" : "Убийств турелью (в среднем за 10 мин.)",
    "Hammer Kills - Avg per 10 Min" : "Убийств молотом (в среднем за 10 мин.)",
    "Molten Core Kills - Avg per 10 Min" : "Убийств во время «Перегрева» (в среднем за 10 мин.)",
    "Low Health Recalls" : "Возвратов из-за недостатка здоровья",
    "Low Health Recalls - Most in Game" : "Возвратов из-за недостатка здоровья (макс. за матч)",
    "Low Health Recalls - Avg per 10 Min" : "Возвратов из-за недостатка здоровья (в среднем за 10 мин.)",
    "Pulse Bomb Kills" : "Убийств «Импульсной бомбой»",
    "Pulse Bomb Kills - Most in Game" : "Убийств «Импульсной бомбой» (макс. за матч)",
    "Pulse Bombs Attached - Most in Game" : "«Импульсных бомб» прицеплено (макс. за матч)",
    "Pulse Bombs Attached" : "«Импульсных бомб» прицеплено",
    "Pulse Bomb Kills - Avg per 10 Min" : "«Импульсных бомб» прицеплено (в среднем за 10 мин.)",       
    "Pulse Bombs Attached - Avg per 10 Min" : "Убийств «Импульсной бомбой» (в среднем за 10 мин.)",
    "Venom Mine Kill" : "Убийств «Ядовитой миной»",
    "Venom Mine Kills" : "Убийств «Ядовитой миной»",
    "Venom Mine Kill - Most in Game" : "Убийств «Ядовитой миной» (макс. за матч)",
    "Venom Mine Kills - Most in Game" : "Убийств «Ядовитой миной» (макс. за матч)",
    "Scoped Accuracy - Best in Game" : "Лучшая меткость снайпера за матч",
    "Venom Mine Kills - Avg per 10 Min" : "Убийств «Ядовитой миной» (в среднем за 10 мин.)",
    "Long Range Final Blows - Avg per 10 Min" : "Смертельных ударов издалека (в среднем за 10 мин.)",
    "Scoped Critical Hit Accuracy" : "Меткость в снайперском режиме (крит.)",
    "Jump Pack Kills" : "Убийств «Прыжковым ранцем»",
    "Jump Pack Kills - Most in Game" : "Убийств «Прыжковым ранцем» (макс. за матч)",
    "Primal Rage Kills" : "Убийств во время «Ярости зверя»",
    "Primal Rage Kills - Most in Game" : "Убийств во время «Ярости зверя» (макс. за матч)",
    "Melee Kills" : "Убийств в ближнем бою",
    "Jump Kills" : "Убийств прыжком",
    "Weapon Kill" : "Убийств оружием",
    "Weapon Kills" : "Убийств оружием",
    "Primal Rage Kills  - Avg per 10 Min" : "Убийств во время «Ярости зверя» (в среднем за 10 мин.)",        
    "Jump Pack Kills - Avg per 10 Min" : "Убийств с помощью «Прыжкового ранца» (в среднем за 10 мин.)",      
    "Piledriver Kills" : "Убийств «Копром»",
    "Grappling Claw Kill" : "Убийств «Кошкой»",
    "Grappling Claw Kills" : "Убийств «Кошкой»",
    "Minefield Kills" : "Убийств «Минным полем»",
    "Grappling Claw Kills - Most in Game" : "Убийств «Кошкой» (макс. за матч)",
    "Grappling Claw Kill - Most in Game" : "Убийств «Кошкой» (макс. за матч)",
    "Minefield Kills - Most in Game" : "Убийств «Минным полем» (макс. за матч)",
    "Piledriver Kills - Most in Game" : "Убийств «Копром» (макс. за матч)",
    "Grappling Claw Kills - Avg per 10 Min" : "Убийств «Кошкой» (в среднем за 10 мин.)",
    "Piledriver Kills - Avg per 10 Min" : "Убийств «Копром» (в среднем за 10 мин.)",
    "Minefield Kills - Avg per 10 Min" : "Убийств «Минным полем» (в среднем за 10 мин.)",
    "Graviton Surge Kills" : "Убийств «Гравитонным импульсом»",
    "Graviton Surge Kills - Most in Game" : "Убийств «Гравитонным импульсом» (макс. за матч)",
    "High Energy Kills - Most in Game" : "Убийств при полной зарядке (макс. за матч)",
    "High Energy Kills" : "Убийств при полной зарядке",
    "Average Energy - Best in Game" : "Лучшее поддержание энергии за матч",
    "Graviton Surge Kills - Avg per 10 Min" : "Убийств «Гравитонным импульсом» (в среднем за 10 мин.)",
    "High Energy Kills - Avg per 10 Min" : "Убийств при полной зарядке (в среднем за 10 мин.)",
    "Average Energy" : "Средний уровень энергии",
    "Transcendence Healing - Most in Game" : "Исцеление «Трансцендентностью» (макс. за матч)",
    "Transcendence Healing" : "Объем исцеления «Трансцендентностью»",
    "Charged Volley Kills" : "Убийств заряженным залпом",
    "Charged Volley Kills - Most in Game" : "Убийств заряженным залпом (макс. за матч)",
    "Charged Volley Accuracy" : "Меткость (заряженные залпы)",
    "Charged Volley Kills - Avg per 10 Min" : "Убийств заряженным залпом (в среднем за 10 мин.)",
    "Final Blows - Most in Game" : "Смертельных ударов (макс. за матч)",
    "Healing Done - Most in Game" : "Макс. исцеления за матч",
    "Elimination - Most in Life" : "Убийств (макс. за жизнь)",
    "Eliminations - Most in Life" : "Убийств (макс. за жизнь)",
    "Elimination - Most in Game" : "Убийств (макс. за матч)",
    "All Damage Done - Most in Life" : "Макс. урона нанесено за одну жизнь",
    "Weapon Accuracy - Best in Game" : "Лучшая меткость за матч (оружие)",
    "Hero Damage Done - Most in Life" : "Макс. урона по героям за одну жизнь",
    "Obj Contest Time - Most in Game" : "Время борьбы за объект (макс. за матч)",
    "Melee Final Blows - Avg per 10 Min" : "Смертельных ударов в рукопашной (в среднем за 10 мин.)",
    "All Damage Done - Avg per 10 Min" : "Нанесено урона (в среднем за 10 мин.)",
    "Eliminations per Life" : "Убийств за одну жизнь",
    "Obj Contest Time - Avg per 10 Min" : "Время борьбы за объект (в среднем за 10 мин.)",
    "Obj Contest Time" : "Время борьбы за объект",
    "Defensive Assists - Avg per 10 Min" : "Защитных содействий (в среднем за 10 мин.)",
    "Offensive Assists - Avg per 10 Min" : "Боевых содействий (в среднем за 10 мин.)",
    "Critical Hits - Most in Game" : "Критических попаданий (макс. за матч)",
    "Critical Hits - Most in Life" : "Критических попаданий (макс. за одну жизнь)",
    "Critical Hit Kills - Avg per 10 Min" : "Убийств крит. попаданием (в среднем за 10 мин.)",
    "Critical Hit Kills - Most in Game" : "Убийств крит. попаданием (макс. за матч)",
    "Critical Hits - Avg per 10 Min" : "Критических попаданий (в среднем за 10 мин.)",
    "Melee Final Blow - Most in Game" : "Смертельных ударов в рукопашной (макс. за матч)",
    "Final Blow - Most in Game" : "Смертельных ударов (макс. за матч)",
    "Critical Hit Kill - Most in Game" : "Убийств крит. попаданием (макс. за матч)",
    "Environmental Kill - Most in Game" : "Несчастных случаев подстроено (макс. за матч)",
    "Assist - Most in Game" : "Содействие (макс. за матч)",
    "Assist" : "Помочь",
    "Swift Strike Resets - Avg per 10 Min NYI" : "Сбросов «Молниеносного удара» (в среднем за 10 мин., NYI)",
    "Recon Assists - Avg per 10 Min" : "Содействий с обнаружением (в среднем за 10 мин.)",
    "Solo Kill - Most in Game" : "Одиночных убийств (макс. за матч)",
    "Defensive Assist" : "Защитных содействий",
    "Thorn Volley Kills" : "Убийств «Градом шипов»",
    "Thorn Volley Kills - Most in Game" : "Убийств «Градом шипов» (макс. за матч)",
    "Life Grip Deaths Prevented" : "Смертей предотвращено «Хваткой жизни»",
    "Life Grip Deaths Prevented - Most in Game" : "Смертей предотвращено «Хваткой жизни» (макс. за матч)",
    "Life Grip Deaths Prevented - Avg per 10 Min" : "Смертей предотвращено «Хваткой жизни» (в среднем за 10 мин.)",
    "Thorn Volley Kills - Avg per 10 Min" : "Убийств «Градом шипов» (в среднем за 10 мин.)",
    "Captive Sun Damage - Most in Game" : "Урон от «Пленного солнца» (макс. за матч)",
    "Sunstruck Detonations - Most in Game" : "Взрывов «Солнечного удара» (макс. за матч)",
    "Sunstruck Detonations - Avg per 10 Min" : "Взрывов «Солнечного удара» (в среднем за 10 мин.)",
    "Captive Sun Damage - Avg per 10 Min" : "Урон от «Пленного солнца» (в среднем за 10 мин.)",
    "Solo Kill" : "Одиночных убийств",
    "All Damage Done" : "Макс. урона нанесено",
    "Critical Hits" : "Критических попаданий",
    "Critical Hit Kill": "Убийств крит. попаданием",
    "Critical Hit Accuracy" : "Меткость (крит.)",
    "Critical Hit Kills" : "Убийств крит. попаданием",
    "Environmental Kills - Avg per 10 Min" : "Несчастных случаев подстроено (в среднем за 10 мин.)",
    "Players Knocked Back - Most in Game NY" : "Игроков отброшено (макс. за матч, NYI)",
    "Knockback Kills - Most in Game" : "Убийств отбрасыванием (макс. за матч)",
    "Objective Kill - Most in Game" : "Убийств у объектов (макс. за матч)",
    "Recon Assist" : "Содействие с обнаружением",
    "Recon Assist - Most in Game" : "Содействие с обнаружением (макс. за матч)"
}

def time(time):
    hour = time // 3600
    if hour > 1:
        min = (time % 3600) / 3600 * 60
        min = int(min)
        if hour < 10:
            hour = "0" + str(hour)
        else: 
            hour = str(hour)
    else:
        hour = None
        min = time // 60
    if min < 10:
        min = "0" + str(min)
    else: 
        min = str(min)
    sec = time % 60
    if sec < 10:
        sec = "0" + str(sec)
    else: 
        sec = str(sec)
    if hour is None:
        time = min + ":" + sec
    else:
        time =  hour + ":" + min + ":" + sec
    return time

'''
hero_list = ["all-heroes", "ana", "ashe", "baptiste", "bastion", "brigitte", "cassidy",
            "dva", "doomfist", "echo", "genji", "hanzo", "illari", "junker-queen", 
            "junkrat", "kiriko", "lifeweaver", "lucio", "mei", "mercy", "moira", "orisa", 
            "pharah", "ramattra", "reaper", "reinhardt", "roadhog", "sigma", "sojourn", 
            "soldier-76", "sombra", "symmetra", "torbjorn", "tracer", "widowmaker", 
            "winston", "wrecking-ball", "zarya", "zenyatta"]
'''

class overwatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Статистика Overwatch")
    @application_checks.guild_only()
    async def overwatch(self, interaction: Interaction, name : str = SlashOption(description="Введите имя пользователя"), gamemode : str = SlashOption(description="Выберите режим (quickplay - по умолчанию)", choices= ["quickplay", "competitive"], required=False), platform : str = SlashOption(description="Выберите платформу (pc - по умолчанию)", choices= ["pc", "console"], required=False), hero : str = SlashOption(description="Выберите героя (all-heroes - по умолчанию, names - посмотреть список персонажей)", required=False)):
        if gamemode is None:
            gamemode = "quickplay"
        if platform is None:
            platform = "pc"
        if hero is None:
            hero = "all-heroes"
        if hero == "names":
            embed = nextcord.Embed(
                title = "Список персонажей",
                colour = nextcord.Color.yellow(),
                description = "ana, ashe, baptiste, bastion, brigitte, cassidy, dva, doomfist, echo, genji, hanzo, illari, junker-queen, junkrat, kiriko, lifeweaver, lucio, mei, mercy, moira, orisa, pharah, ramattra, reaper, reinhardt, roadhog, sigma, sojourn, soldier-76, sombra, symmetra, torbjorn, tracer, widowmaker, winston, wrecking-ball, zarya, zenyatta"
                )
            embed.set_thumbnail(
                url = "https://cdn.discordapp.com/attachments/1089234712834363392/1142538430656557297/Overwatch_circle_logo.svg.png"
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.defer()
            good = False
            list = name.split("#")
            name = list[0] + "-" + list[1]
            response_user = requests.get(f"https://overfast-api.tekrop.fr/players/{name}")
            await asyncio.sleep(0.2)
            if hero != "all-heroes":
                response_hero = requests.get(f"https://overfast-api.tekrop.fr/heroes/{hero}?locale=en-us")
                await asyncio.sleep(0.2)
            response_stats = requests.get(f"https://overfast-api.tekrop.fr/players/{name}/stats?gamemode={gamemode}&platform={platform}&hero={hero}")
            await asyncio.sleep(0.2)
            if response_user.status_code and response_stats.status_code == 200:
                if hero != "all-heroes":
                    if response_hero.status_code == 200:
                        data_user = response_user.json()
                        data_hero = response_hero.json()
                        data_stats = response_stats.json()
                        good = True
                    else:
                        await interaction.followup.send('Ошибка при выполнении запроса')
                else:
                    data_user = response_user.json()
                    data_stats = response_stats.json()
                    good = True
            else:
                await interaction.followup.send('Ошибка при выполнении запроса')
            if good is True:
                username = list[0]
                text = ""
                if gamemode == "quickplay":
                    gamemode_ = "безрейт. игра"
                else:
                    gamemode_ = "рейт. игра"
                if hero == "all-heroes":
                    username = data_user['summary']['username']
                    avatar = data_user['summary']['avatar']
                    text = f"**Общая статистика - {gamemode_}**\n"
                else:
                    hero_name = data_hero['name']
                    text = f"**Статистика - {gamemode_}**\n"
                    text = text + f"**{hero_name}**\n"
                    avatar = data_hero['portrait']
                for category in data_stats[f'{hero}']: #all-heroes
                    if "hero_specific" in category['category']:
                        # Для определенного героя
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                if "Матчей выиграно" in text:
                                    pass
                                else:
                                    text += f"{lab}: {stat['value']}\n"
                    if "best" in category['category']:
                        # Лучшее
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                if "Матчей выиграно" in text:
                                    pass
                                else:
                                    text += f"{lab}: {stat['value']}\n"
                    if "average" in category['category']:
                        # Среднее
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                if "Матчей выиграно" in text:
                                    pass
                                else:
                                    text += f"{lab}: {stat['value']}\n"
                    if "game" in category['category']:
                        # Игра
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                if "Матчей выиграно" in text:
                                    pass
                                else:
                                    text += f"{lab}: {stat['value']}\n"
                    if "combat" in category['category']:
                        # Бой
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                if "Матчей выиграно" in text:
                                    pass
                                else:
                                    text += f"{lab}: {stat['value']}\n"
                    if "assists" in category['category']:
                        # Помощь
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                text += f"{lab}: {stat['value']}\n"
                    if "cards" in category['category']:
                        # Помощь
                        cat = lang.get(category['label'])
                        text += f"***{cat}***\n"
                        for stat in category['stats']:
                            lab = lang.get(stat['label'])
                            if lab is None:
                                lab = stat['label']
                            if "time" in stat['key'] or "Time" in stat['label']:
                                text += f"{lab}: {time(stat['value'])}\n"
                            elif "scoped" in stat['key'] or "Scoped" in stat['label'] or "Percentage" in stat['label'] or "percentage" in stat['label'] or "Accuracy" in stat['label']:
                                text += f"{lab}: {stat['value']}%\n"
                            else:
                                text += f"{lab}: {stat['value']}\n"
                embed = nextcord.Embed(
                    title = username,
                    colour = nextcord.Color.yellow(),
                    description = text
                    )
                embed.set_thumbnail(
                    url = avatar
                    )
                await interaction.followup.send(embed=embed)
    
    @overwatch.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.followup.send("Проверьте правильность никнейма и не закрыт ли профиль.")

def setup(bot):
    bot.add_cog(overwatch(bot))