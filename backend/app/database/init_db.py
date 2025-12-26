from .database import engine, Base, new_session
from .session import get_session
from .repo import DB


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with new_session() as session:
        if not await DB.mineral_types.exists_by_name('Макронутриенты', session=session):
            await DB.mineral_types.new(
                name='Макронутриенты',
                description='Это основа питания. К ним относятся белки, жиры, углеводы, а также вода и клетчатка.',
                session=session
            )
        if not await DB.mineral_types.exists_by_name('Водорастворимые', session=session):
            await DB.mineral_types.new(
                name='Водорастворимые',
                description='Растворяются в воде. Не накапливаются в организме (за исключением B12, \
                который запасается в печени). Избыток выводится с мочой, поэтому риск гипервитаминоза \
                (кроме крайних случаев) низок. Требуются регулярно, с пищей каждый день. \
                Многие разрушаются при термической обработке, на свету, при контакте с воздухом. \
                Готовка на пару и минимальная обработка помогают сохранить их.',
                session=session
            )
        if not await DB.mineral_types.exists_by_name('Жирорастворимые', session=session):
            await DB.mineral_types.new(
                name='Жирорастворимые',
                description='Растворяются в жирах и органических растворителях. Накапливаются в организме \
                (в основном в печени и жировой ткани). Поэтому риск гипервитаминоза (токсического эффекта \
                от передозировки) реален, особенно при бесконтрольном приеме добавок. Для их всасывания \
                в кишечнике необходимы жиры. Диета с крайне низким содержанием жиров или прием препаратов, \
                блокирующих усвоение жиров, могут привести к дефициту. Выводятся медленно.',
                session=session
            )
        if not await DB.mineral_types.exists_by_name('Макроминералы', session=session):
            await DB.mineral_types.new(
                name='Макроминералы',
                description='Требуются в количествах более 100 мг в сутки. Являются структурными \
                компонентами тканей (кости, зубы) и электролитами. Минералы, которые при растворении в жидкостях тела \
                (кровь, межклеточная жидкость) создают электрический заряд. Они регулируют: \
                \n- Баланс жидкости (осмотическое давление). \
                \n- pH-баланс (кислотно-щелочное равновесие). \
                \n- Проведение нервных импульсов и сокращение мышц (включая сердце).',
                session=session
            )
        if not await DB.mineral_types.exists_by_name('Микроминералы', session=session):
            await DB.mineral_types.new(
                name='Микроминералы',
                description='Требуются в очень малых количествах (обычно мг или мкг в сутки). \
                Чаще всего входят в состав активных центров ферментов (являются кофакторами) или гормонов. \
                Разница между дефицитом, нормой и токсичностью для них очень мала. Самолечение добавками \
                микроэлементов особенно опасно.',
                session=session
            )

        energy_type = await DB.mineral_types.by_name(
            name='Макронутриенты',
            session=session
        )
        if not await DB.minerals.exists_by_name(name='Белки', session=session):
            await DB.minerals.new(
                name='Белки',
                description='Строительный материал для клеток, тканей (мышцы, кожа, волосы), ферментов, гормонов, антител. Вторичный источник энергии.',
                intake=4,
                type_id=energy_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Жиры', session=session):
            await DB.minerals.new(
                name='Жиры',
                description='Самый концентрированный источник энергии, строительный материал для клеточных мембран и гормонов, среда для усвоения жирорастворимых витаминов (A, D, E, K), защита органов, терморегуляция.',
                intake=9,
                type_id=energy_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Углеводы', session=session):
            await DB.minerals.new(
                name='Углеводы',
                description='Быстрый и основной источник энергии для тела, особенно для мозга и мышц.',
                intake=4,
                type_id=energy_type.id,
                session=session,
            )

        water_type = await DB.mineral_types.by_name(
            name='Водорастворимые',
            session=session,
        )
        if not await DB.minerals.exists_by_name(name='C', session=session):
            await DB.minerals.new(
                name='C',
                description='(Аскорбиновая кислота) - Антиоксидант, важен для иммунитета, синтеза коллагена (кожа, суставы), заживления ран.',
                intake=90,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B1', session=session):
            await DB.minerals.new(
                name='B1',
                description='(Тиамин) - Участвует в энергетическом обмене, важен для работы нервной системы и мышц.',
                intake=1.1,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B2', session=session):
            await DB.minerals.new(
                name='B2',
                description='(Рибофлавин) - Участвует в энергетическом обмене, здоровье кожи и зрения.',
                intake=1.1,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B3', session=session):
            await DB.minerals.new(
                name='B3',
                description='(Ниацин, PP) - Важен для энергетического обмена, здоровья кожи, нервной системы и пищеварения.',
                intake=20,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B5', session=session):
            await DB.minerals.new(
                name='B5',
                description='(Пантотеновая кислота) - Участвует в синтезе гормонов и гемоглобина, метаболизме жиров и углеводов.',
                intake=5,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B6', session=session):
            await DB.minerals.new(
                name='B6',
                description='(Пиридоксин) - Участвует в синтезе белков, гемоглобина, нейромедиаторов, регулирует уровень гомоцистеина.',
                intake=1.5,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B7', session=session):
            await DB.minerals.new(
                name='B7',
                description='(Биотин, H) - 	Важен для здоровья кожи, волос, ногтей, участвует в метаболизме жиров и углеводов.',
                intake=0.05,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B9', session=session):
            await DB.minerals.new(
                name='B9',
                description='(Фолиевая кислота) - Критически важен для деления клеток, синтеза ДНК, предотвращения дефектов нервной трубки у плода.',
                intake=0.4,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='B12', session=session):
            await DB.minerals.new(
                name='B12',
                description='(Кобаламин) - Необходим для образования эритроцитов, работы нервной системы, синтеза ДНК.',
                intake=0.002,
                type_id=water_type.id,
                session=session,
            )

        fat_type = await DB.mineral_types.by_name(
            name='Жирорастворимые',
            session=session,
        )
        if not await DB.minerals.exists_by_name(name='A', session=session):
            await DB.minerals.new(
                name='A',
                description='(Ретинол) - Важен для зрения (особенно ночного), иммунитета, здоровья кожи и репродуктивной системы.',
                intake=0.8,
                type_id=fat_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='D', session=session):
            await DB.minerals.new(
                name='D',
                description='(Кальциферол) - «Солнечный витамин». Регулирует обмен кальция и фосфора, здоровье костей, иммунную функцию.',
                intake=0.014,
                type_id=fat_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='E', session=session):
            await DB.minerals.new(
                name='E',
                description='(Токоферол) - Мощный антиоксидант, защищает клетки от повреждений, важен для здоровья кожи и иммунитета.',
                intake=15,
                type_id=fat_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='K', session=session):
            await DB.minerals.new(
                name='K',
                description='(Филлохинон, Менахинон) - Необходим для синтеза белков свертывания крови и здоровья костей.',
                intake=0.11,
                type_id=fat_type.id,
                session=session,
            )

        macro_type = await DB.mineral_types.by_name(
            name='Макроминералы',
            session=session,
        )
        if not await DB.minerals.exists_by_name(name='Ca', session=session):
            await DB.minerals.new(
                name='Ca',
                description='(Кальций) - Основной компонент костей и зубов. Участвует в мышечном сокращении, работе нервов, свертывании крови.',
                intake=1100,
                type_id=macro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='P', session=session):
            await DB.minerals.new(
                name='P',
                description='(Фосфор) - Второй по важности минерал для костей и зубов. Участвует в энергетическом обмене (АТФ).',
                intake=700,
                type_id=macro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Mg', session=session):
            await DB.minerals.new(
                name='Mg',
                description='(Магний) - Участвует в более чем 300 ферментативных реакциях (энергия, синтез белка), работе мышц и нервов.',
                intake=400,
                type_id=macro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Na', session=session):
            await DB.minerals.new(
                name='Na',
                description='(Натрий) - Важен для поддержания водно-солевого баланса и работы нервов. Избыток вреден.',
                intake=2000,
                type_id=macro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='K', session=session):
            await DB.minerals.new(
                name='K',
                description='(Калий) - Регулирует кровяное давление, баланс жидкости, работу нервов и мышц.',
                intake=4000,
                type_id=water_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Cl', session=session):
            await DB.minerals.new(
                name='Cl',
                description='(Хлор) - Вместе с натрием регулирует баланс жидкостей, входит в состав желудочного сока (соляная кислота).',
                intake=2000,
                type_id=water_type.id,
                session=session,
            )

        micro_type = await DB.mineral_types.by_name(
            name='Микроминералы',
            session=session,
        )
        if not await DB.minerals.exists_by_name(name='Fe', session=session):
            await DB.minerals.new(
                name='Fe',
                description='(Железо) - Критически важно для переноса кислорода (гемоглобин) и производства энергии.',
                intake=15,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Zn', session=session):
            await DB.minerals.new(
                name='Zn',
                description='(Цинк) - Важен для иммунитета, заживления ран, синтеза белков и ДНК, чувства вкуса и обоняния.',
                intake=10,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Cu', session=session):
            await DB.minerals.new(
                name='Cu',
                description='(Медь) - Участвует в метаболизме железа, образовании соединительной ткани, работе нервной системы.',
                intake=1,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Se', session=session):
            await DB.minerals.new(
                name='Se',
                description='(Селен) - Мощный антиоксидант, важен для работы щитовидной железы и иммунитета.',
                intake=0.055,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='I', session=session):
            await DB.minerals.new(
                name='I',
                description='(Йод) - Необходим для синтеза гормонов щитовидной железы, регулирующих обмен веществ.',
                intake=0.15,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Mn', session=session):
            await DB.minerals.new(
                name='Mn',
                description='(Марганец) - Участвует в метаболизме углеводов, аминокислот, формировании костей и антиоксидантной защите.',
                intake=2.1,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Cr', session=session):
            await DB.minerals.new(
                name='Cr',
                description='(Хром) - Участвует в метаболизме глюкозы, усиливая действие инсулина.',
                intake=0.035,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='Mo', session=session):
            await DB.minerals.new(
                name='Mo',
                description='(Молибден) - Компонент ферментов, участвующих в метаболизме аминокислот и детоксикации.',
                intake=0.045,
                type_id=micro_type.id,
                session=session,
            )
        if not await DB.minerals.exists_by_name(name='F', session=session):
            await DB.minerals.new(
                name='F',
                description='(Фтор) - Укрепляет зубную эмаль и предотвращает кариес.',
                intake=4,
                type_id=micro_type.id,
                session=session,
            )
        await session.commit()
