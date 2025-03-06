import datetime
from disnake.ext import commands, tasks
from disnake import File, ButtonStyle
from disnake.ui import Button, View
from disnake import components
from disnake import TextInputStyle
import disnake
import time
import pymongo
from config import *
client = pymongo.MongoClient("mongodb+srv://test:test@kolund.c04hlak.mongodb.net/?retryWrites=true&w=majority")
coll = client.ave.verify
coll2 = client.ave.pingtime
coll3 = client.ave.fullstatsverify
coll4 = client.ave.fullstatsverifyday

cooldown = {}


class mrmr(disnake.ui.Modal):
    def __init__(self, member: disnake.Member, author: disnake.Member, bot):
        components = [
            disnake.ui.TextInput(
                label="Отзыв:",
                placeholder="Крутой чел 10/10",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=50,
            )
        ]
        super().__init__(
            title="Отзыв",
            custom_id="Отзыв",
            components=components,
        )
        self.member = member
        self.author = author
        self.bot = bot
    async def callback(self, inter):
        channel = self.bot.get_channel(int(config['otzivi']))
        embed = disnake.Embed(title="Оставили новый отзыв!", description = f"> {inter.text_values['name']}", color=0x2F3136)
        embed.add_field(name = f"Оставил отзыв", value = f"・{self.member.mention}\n・{self.member.id}")
        embed.add_field(name = f"Верифицировал", value = f"・{self.author.mention}\n・{self.author.id}")
        await channel.send(embed = embed)
        await inter.response.edit_message(view = None)


class otziv(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member

    @disnake.ui.button(label = "Отзыв")
    async def back2unban2zxczxc(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(mrmr(self.member, self.author, self.bot))

class add(disnake.ui.UserSelect):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(placeholder = "Добавить твинк")
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed

    async def callback(self, interaction):
        usir = self.values[0]

        find = coll.find_one({"id": self.member.id})
        listik = find['twink']

        listik.append(usir.id)
        coll.update_one({"id": self.member.id}, {"$set":{"twink": listik}})
        text = ''
        count = 0
        if len(listik) == 0:
            text = 'Отсутствует'
        else:
            for x in find['twink']:
                count +=1
                text += f'**{count}.** <@{x}>\n'

        limit = False
        udal = False
        if len(find['twink']) == 0:
            udal = True

        if len(find['twink']) == 10:
            limit = True
        embed = disnake.Embed(title = "Твинки пользователя", description = text,color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        stratud = tvink_butoni(self.bot, self.author, self.member, limit, udal, self.embed)
        await stratud.start(interaction, embed)


class Dropdown1(disnake.ui.Select):
    def __init__(self, bot, author:disnake.member, member: disnake.Member, interaction, embed):
        self.bot = bot
        self.author = author
        self.embed = embed
        self.member = member
        self.interaction = interaction
        self.spisok = coll.find_one({"id": self.member.id})['twink']
        optioons = []
        names = []
        for index, r in enumerate(self.spisok):
            names.append(r)
            memume = interaction.guild.get_member(int(r))
            optioons.append(disnake.SelectOption(label=f"{memume.name}", description=f"{memume.id}"))
        super().__init__(
            options=optioons,
            placeholder="Выберите твинк!",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: disnake.Interaction):
        for index, r in enumerate(self.spisok):
            memume = interaction.guild.get_member(int(r))
            if self.values[0] == f"{memume.name}":
                find = coll.find_one({"id": self.member.id})
                listik = find['twink']

                listik.remove(memume.id)
                coll.update_one({"id": self.member.id}, {"$set":{"twink": listik}})
                text = ''
                count = 0
                if len(listik) == 0:
                    text = '**Отсутствуют**'
                else:
                    for x in find['twink']:
                        count +=1
                        text += f'**{count}.** <@{x}>\n'

                limit = False
                udal = False
                if len(find['twink']) == 0:
                    udal = True

                if len(find['twink']) == 10:
                    limit = True
                embed = disnake.Embed(title = "Твинки пользователя", description = text,color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
                stratud = tvink_butoni(self.bot, self.author, self.member, limit, udal, self.embed)
                await stratud.start(interaction, embed)
        

class add_sel(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed
        self.add_item(add(self.bot, self.author, self.member, self.embed))

        

class rem_sel(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, interaction, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed
        self.interaction = interaction
        self.add_item(Dropdown1(self.bot, self.author, self.member, self.interaction, self.embed))    
        

        


class tvink_butoni:
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, limit, udal, embed):
        self.bot = bot
        self.author = author
        self.member = member
        self.limit = limit
        self.udal = udal
        self.embed = embed
        class tvink(disnake.ui.View):
            def __init__(this, interaction):
                super().__init__()
            @disnake.ui.button(style = ButtonStyle.green, label = "Добавить", disabled = self.limit)
            async def back2unban22(this, _, button_interaction):
                if button_interaction.author != self.author:
                    await button_interaction.response.defer()
                    return
                await button_interaction.response.edit_message(view=add_sel(self.bot, self.author, self.member, self.embed))



            @disnake.ui.button(style = ButtonStyle.red,label = "Удалить", disabled = self.udal)
            async def back2unban2(this, _, button_interaction):
                if button_interaction.author != self.author:
                    await button_interaction.response.defer()
                    return

                await button_interaction.response.edit_message(view=rem_sel(self.bot, self.author, self.member, button_interaction, self.embed))

            @disnake.ui.button(style = ButtonStyle.grey,label = "Назад")
            async def back2unban2z(this, _, button_interaction):
                if button_interaction.author != self.author:
                    await button_interaction.response.defer()
                    return

                find = coll.find_one({"id": self.member.id})
                embed = disnake.Embed(color =  0x2f3136)
                divice = None
                if self.member.is_on_mobile() == True:
                    divice = "Телефон"
                else:
                    divice = "Компьютер"
                embed.set_author(name=f"Информация о {self.member}", icon_url=self.member.display_avatar)
                embed.add_field(name = "Присоединился", value = f"<t:{int(self.member.joined_at.timestamp())}:R>", inline = True)
                embed.add_field(name = "Создан аккаунт", value = f"<t:{int(self.member.created_at.timestamp())}:R>", inline = True)
                embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
                embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
                embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
                embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)
                embed.set_image(url = "")
                await button_interaction.response.edit_message(embed = embed, view=buton(self.bot, self.author, self.member, self.embed))
        self.view = tvink

    async def start(self, interaction, embed):
        await interaction.response.edit_message(embed = embed, view=self.view(interaction))

class veref_catalog(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed

    @disnake.ui.button(label = "Мужская роль")
    async def back2unban2zxczxc(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        await interaction.response.defer()
        embed = disnake.Embed(title = "Успешная верификация",description = f"{self.author.mention}, пользователь {self.member.mention}\n\nБыла выдана роль: **Мужская гендер**",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        role = interaction.guild.get_role(int(config['man']))
        role2 = interaction.guild.get_role(int(config['girl']))
        veref = interaction.guild.get_role(int(config['unverify'])) 
        await self.member.add_roles(role)
        await self.member.remove_roles(veref)
        await self.member.remove_roles(role2)
        await interaction.edit_original_message(embed = embed, view = None)

        embed_member = disnake.Embed(title = f"Добро пожаловать на {config['server_name']}", description = f"Вас верифицировал {interaction.author.mention}, можете оставить **отзыв!**", color=0x2F3136).set_thumbnail(url = "https://cdn.discordapp.com/attachments/1071445931683217479/1071448573977301103/cc7dfba298f24408385cfea27ce35742.png")
        embed_member.set_thumbnail(url = interaction.author.avatar)
        embed_member.set_footer(text = "У вас на это 5 минут.")
        await self.member.send(embed = embed_member, view = otziv(self.bot, self.author, self.member))




        channel = interaction.guild.get_channel(int(config['logi']))
        embed_member = disnake.Embed(title = "Верификация", color=0x2F3136)
        embed_member.add_field(name = f"{config['dot']} Саппорт", value = f"・{self.author.mention}\n・{self.author.id}", inline = True)
        embed_member.add_field(name = f"{config['dot']} Пользователь", value = f"・{self.member.mention}\n・{self.member.id}", inline = True)
        await channel.send(embed = embed_member)
        coll3.update_one({"id": self.author.id}, {"$inc": {"verify": 1}})


    @disnake.ui.button(label = "Женская роль")
    async def back1unban1zxczxc(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        await interaction.response.defer()
        embed = disnake.Embed(title = "Успешная верификация",description = f"{self.author.mention}, пользователь {self.member.mention}\n\nБыла выдана роль: **Женский гендер**",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        role = interaction.guild.get_role(int(config['girl']))
        role2 = interaction.guild.get_role(int(config['man']))
        veref = interaction.guild.get_role(int(config['unverify'])) 
        await self.member.add_roles(role)
        await self.member.remove_roles(veref)
        await self.member.remove_roles(role2)
        await interaction.edit_original_message(embed = embed, view = None)

        embed_member = disnake.Embed(title = f"Добро пожаловать на {config['server_name']}", description = f"Вас верифицировал {interaction.author.mention}, можете оставить **отзыв!**", color=0x2F3136).set_thumbnail(url = "https://cdn.discordapp.com/attachments/1071445931683217479/1071448573977301103/cc7dfba298f24408385cfea27ce35742.png")
        embed_member.set_thumbnail(url = interaction.author.avatar)
        embed_member.set_footer(text = "У вас на это 5 минут.")
        await self.member.send(embed = embed_member, view = otziv(self.bot, self.author, self.member))




        channel = interaction.guild.get_channel(int(config['logi']))
        embed_member = disnake.Embed(title = "Верификация", color=0x2F3136)
        embed_member.add_field(name = f"{config['dot']} Саппорт", value = f"・{self.author.mention}\n・{self.author.id}", inline = True)
        embed_member.add_field(name = f"{config['dot']} Пользователь", value = f"・{self.member.mention}\n・{self.member.id}", inline = True)
        await channel.send(embed = embed_member)
        coll3.update_one({"id": self.author.id}, {"$inc": {"verify": 1}})




        channel = interaction.guild.get_channel(int(config['logi']))
        embed_member = disnake.Embed(title = "Верификация", color=0x2F3136)
        embed_member.add_field(name = f"{config['dot']} Саппорт", value = f"・{self.author.mention}\n・{self.author.id}", inline = True)
        embed_member.add_field(name = f"{config['dot']} Пользователь", value = f"・{self.member.mention}\n・{self.member.id}", inline = True)
        await channel.send(embed = embed_member)
        coll3.update_one({"id": self.author.id}, {"$inc": {"verify": 1}})





    @disnake.ui.button(style = ButtonStyle.blurple, label = "Назад", row = 1)
    async def back2unban2zxczxcz(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return

        find = coll.find_one({"id": self.member.id})
        embed = disnake.Embed(color =  0x2f3136)
        divice = None
        if self.member.is_on_mobile() == True:
            divice = "Телефон"
        else:
            divice = "Компьютер"
        embed.set_author(name=f"Информация о {self.member}", icon_url=self.member.display_avatar)
        embed.add_field(name = "Присоединился", value = f"<t:{int(self.member.joined_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Создан аккаунт", value = f"<t:{int(self.member.created_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
        embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
        embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
        embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)

        await interaction.response.edit_message(embed = embed, view = buton(self.bot, self.author, self.member, self.embed))

class lx_clas2(disnake.ui.Select):
    def __init__(self, bot, embed, member: disnake.Member, author: disnake.Member):
        super().__init__(
            placeholder="Выберите нужное",
            min_values=1,
            max_values=1,
            options=[
                disnake.SelectOption(label="Неадекват"),
                disnake.SelectOption(label="Меньше 13 лет"),
                disnake.SelectOption(label="Джампинг"),
                disnake.SelectOption(label="Свастика"),
                disnake.SelectOption(label="Ник"),
                disnake.SelectOption(label="Цифры"),
                disnake.SelectOption(label="Аватарка"),
                disnake.SelectOption(label="Обход наказания") 
            ]
        )

        self.member = member
        self.author = author
        self.bot = bot
        self.embed = embed

    async def callback(self, interaction: disnake.Interaction):
        if interaction.author != self.author:
            pass
            return

        prichina = self.values[0]
        embed = disnake.Embed(title = "Выдача недопуска",description = f"{self.author.mention}, вы **успешно** выдали недопуск пользователю {self.member.mention} по причину **{prichina}**",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        role = interaction.guild.get_role(int(config['nedopusk']))
        veref = interaction.guild.get_role(int(config['unverify']))
        await self.member.add_roles(role)
        await self.member.remove_roles(veref)
        await interaction.response.edit_message(embed = embed, view = veref_nedop1(self.bot, self.author, self.member, self.embed))
        coll.update_one({"id": self.member.id}, {"$set":{"prichnedopusk": prichina}})
        coll.update_one({"id": self.member.id}, {"$inc":{"nedopusk": 1}})
        coll3.update_one({"id": self.author.id}, {"$inc": {"unverify": 1}})
class lx_classic(disnake.ui.View):
    def __init__(self, bot, embed, member: disnake.Member, author: disnake.Member):
        super().__init__(timeout = None)
        self.member = member
        self.author = author
        self.bot = bot
        self.embed = embed
        self.add_item(lx_clas2(self.bot, self.embed, self.member, self.author))
    @disnake.ui.button(style = ButtonStyle.blurple, label = "Назад", row = 1)
    async def back2unban2zxczxcz(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author: 
            await interaction.response.defer()
            return

        find = coll.find_one({"id": self.member.id})
        embed = disnake.Embed(color =  0x2f3136)
        divice = None
        if self.member.is_on_mobile() == True:
            divice = "Телефон"
        else:
            divice = "Компьютер"
        embed.set_author(name=f"Информация о {self.member}", icon_url=self.member.display_avatar)
        embed.add_field(name = "Присоединился", value = f"<t:{int(self.member.joined_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Создан аккаунт", value = f"<t:{int(self.member.created_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
        embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
        embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
        embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)
        await interaction.response.edit_message(embed = embed, view = buton(self.bot, self.author, self.member, self.embed))
class veref_nedop1(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed

    @disnake.ui.button(style = ButtonStyle.blurple, label = "Назад", row = 1)
    async def back2unban2zxczxcz(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author: 
            await interaction.response.defer()
            return
        find = coll.find_one({"id": self.member.id})
        embed = disnake.Embed(color =  0x2f3136)
        divice = None
        if self.member.is_on_mobile() == True:
            divice = "Телефон"
        else:
            divice = "Компьютер"
        embed.set_author(name=f"Информация о {self.member}", icon_url=self.member.display_avatar)
        embed.add_field(name = "Присоединился", value = f"<t:{int(self.member.joined_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Создан аккаунт", value = f"<t:{int(self.member.created_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
        embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
        embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
        embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)
        await interaction.response.edit_message(embed = embed, view = buton(self.bot, self.author, self.member, self.embed))

class veref_nedop(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed

    @disnake.ui.button(label = "Выдать недопуск")
    async def back(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return

        embed = disnake.Embed(title = "Выдача недопуска",description = f"{self.author.mention}, укажите **причину** выдачи недопуска пользователю {self.member.mention}",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        zxc = await interaction.response.edit_message(embed = embed, view = lx_classic(self.bot, self.embed, self.member, self.author))

    @disnake.ui.button(label = "Снять недопуск")
    async def back2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        embed = disnake.Embed(title = "Снятие недопуска",description = f"{self.author.mention}, вы **успешно** сняли недопуск пользователю {self.member.mention}",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        zxc = await interaction.response.edit_message(embed = embed, view = veref_nedop1(self.bot, self.author, self.member, self.embed))
        role = interaction.guild.get_role(int(config['nedopusk']))
        veref = interaction.guild.get_role(int(config['unverify']))
        await self.member.remove_roles(role)
        await self.member.add_roles(veref)

    @disnake.ui.button(style = ButtonStyle.blurple, label = "Назад", row = 1)
    async def back2unban2zxczxcz(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author: 
            await interaction.response.defer()
            return
        find = coll.find_one({"id": self.member.id})
        embed = disnake.Embed(color =  0x2f3136)
        divice = None
        if self.member.is_on_mobile() == True:
            divice = "Телефон"
        else:
            divice = "Компьютер"
        embed.set_author(name=f"Информация о {self.member}", icon_url=self.member.display_avatar)
        embed.add_field(name = "Присоединился", value = f"<t:{int(self.member.joined_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Создан аккаунт", value = f"<t:{int(self.member.created_at.timestamp())}:R>", inline = True)
        embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
        embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
        embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
        embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)
        await interaction.response.edit_message(embed = embed, view = buton(self.bot, self.author, self.member, self.embed))

class buton(disnake.ui.View):
    def __init__(self, bot, author: disnake.Member, member: disnake.Member, embed):
        super().__init__(timeout = 120)
        self.bot = bot
        self.author = author
        self.member = member
        self.embed = embed

    @disnake.ui.button(style = ButtonStyle.green, label = "Верифицировать")
    async def back2unban2zxc(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        embed = disnake.Embed(title = "Чтобы пропустить участника на сервер",description = f"{self.author.mention}, выберите **гендер** который будет **выдан** пользователю {self.member.mention}",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        await interaction.response.edit_message(embed = embed,  view = veref_catalog(self.bot, self.author, self.member, self.embed))

    @disnake.ui.button(style = ButtonStyle.grey, label = "Недопуск")
    async def back2unban2zxcяяя(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        embed = disnake.Embed(title = "Выдача недопуска",description = f"{self.author.mention}, выберите **действие** которое будет **совершено** по отношению к пользователю {self.member.mention}",color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        await interaction.response.edit_message(embed = embed,  view = veref_nedop(self.bot, self.author, self.member, self.embed))





    @disnake.ui.button(style = ButtonStyle.grey, label = "Твинки")
    async def back2unban2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return

        find = coll.find_one({"id": self.member.id})
        text = ''
        count = 0
        if len(find['twink']) == 0:
            text = '**Отсутствуют.**'
        else:
            for x in find['twink']:
                count +=1
                text += f'**{count}.** <@{x}>\n'

        limit = False
        udal = False
        if len(find['twink']) == 0:
            udal = True

        if len(find['twink']) == 10:
            limit = True
        embed = disnake.Embed(title = "Твинки пользователя", description = text,color =  0x2f3136).set_thumbnail(url = self.member.display_avatar)
        stratud = tvink_butoni(self.bot, self.author, self.member, limit, udal, self.embed)
        await stratud.start(interaction, embed)

    @disnake.ui.button(style = ButtonStyle.red, label = "Отмена")
    async def back2unban2zzxz(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.defer()
            return
        await interaction.message.delete()



class DropdownView2(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

        self.add_item(Dropdownroles2())


class video(commands.Cog, name="video"):
    def __init__(self, bot):
        self.bot = bot
        self.get_m.start()
        self.voice_check.start()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        find = coll.find_one({"id": member.id})
        if find:
            coll.update_one({"id": member.id}, {"$inc":{"perezaxod": 1}})
        else:
            post = {
            "id": member.id,
            "nedopusk": 0,
            "perezaxod": 0,
            "data": int(time.time()),
            "twink": [],
            "prichnedopusk": "Отсутствует"
            }
            coll.insert_one(post)

    class YourCog(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

    @commands.slash_command(name="verify", description="Верифицировать пользователя.")
    async def create(self, interaction, member: disnake.Member):
        # Получаем объекты ролей, которым разрешено использование команды
        allowed_roles = [
            interaction.guild.get_role(1202280368968052747), # ID роли support
        ]

        # Проверяем, есть ли у участника хотя бы одна из разрешенных ролей
        if any(role in allowed_roles for role in interaction.author.roles):
            # Проверяем, прошло ли более 3 секунд с момента последнего использования команды пользователем
            if interaction.author.id in cooldown and time.time() - cooldown[interaction.author.id] < 0:
                # Если не прошло, сообщаем пользователю, что нужно подождать перед повторным использованием команды
                await interaction.response.send_message("Подождите некоторое время перед повторным использованием команды.", ephemeral=True)
                return
            await interaction.response.defer()
            post = {
            "id": member.id,
            "nedopusk": 0,
            "perezaxod": 0,
            "data": int(time.time()),
            "twink": [],
            "prichnedopusk": "Отсутствует"
            }

            find = coll.find_one({"id": member.id})
            if find:
                pass
            else:
                coll.insert_one(post)
            find = coll.find_one({"id": member.id})
            embed = disnake.Embed(color =  0x2f3136)
            divice = None
            if member.is_on_mobile() == True:
                divice = "Телефон"
            else:
                divice = "Компьютер"
            embed.set_author(name=f"Информация о {member}", icon_url=member.display_avatar)
            embed.add_field(name = "Присоединился", value = f"<t:{int(member.joined_at.timestamp())}:R>", inline = True)
            embed.add_field(name = "Создан аккаунт", value = f"<t:{int(member.created_at.timestamp())}:R>", inline = True)
            embed.add_field(name = "Устройство", value = f"{divice}", inline = True)
            embed.add_field(name = "Недопущен", value = f"{find['nedopusk']} раз(и)", inline = True)
            embed.add_field(name = "Причина", value = f"{find['prichnedopusk']}", inline = True)
            embed.add_field(name = "Перезаход", value = f"{find['perezaxod']} раз(и)", inline = True)
            await interaction.send(embed = embed, view = buton(self.bot, interaction.author, member, embed))
        else:
            await interaction.response.send_message("У вас нет роли для использования данной команды", ephemeral=True)

    @commands.slash_command(name="support", description="Получить статистику саппорта")
    async def support(self, interaction, member: disnake.Member = None):
        if interaction.response.is_done():
            return
        await interaction.response.defer()

        if member is None:
            member = interaction.author

        role = interaction.guild.get_role(int(config['support']))

        if role not in member.roles:
            embed = disnake.Embed(
                title='Статистика саппорта',
                description=f"{member.mention}, **Вы** не являетесь {role.mention}",
                color=0x2f3136
            ).set_thumbnail(url=member.display_avatar)
            await interaction.edit_original_message(embed=embed)
            return

        find = coll3.find_one({"id": member.id})
        if find:
            timezxczxc = f"{find['online'] // 3600} ч. {(find['online'] // 60) % 60} мин."
            embed = disnake.Embed(
                title=f"Статистика — {member}",
                description=f"> {config['dot']}  **Онлайн в прихожей:**\n```{timezxczxc}```",
                color=0x2f3136
            ).set_thumbnail(url=member.display_avatar)
            embed.add_field(name=f"> {config['dot']}  **Выдано верификаций:**", value=f"```{find['verify']} чел.```", inline=True)
            embed.add_field(name=f"> {config['dot']}  **Выдано недопусков:**", value=f"```{find['unverify']} чел.```", inline=True)
            await interaction.edit_original_message(embed=embed)
        else:
            post = {
                "id": member.id,
                "online": 0,
                "verify": 0,
                "unverify": 0,
            }
            if coll3.count_documents({"id": member.id}) == 0:
                coll3.insert_one(post)
            fin2 = coll3.find_one({"id": member.id})
            timezxczxc = f"{fin2['online'] // 3600} ч. {(fin2['online'] // 60) % 60} мин."
            embed = disnake.Embed(
                title=f"Статистика — {member}",
                description=f"> {config['dot']}**Онлайн в прихожей:**\n```{timezxczxc}```",
                color=0x2f3136
            ).set_thumbnail(url=member.display_avatar)
            embed.add_field(name=f"> {config['dot']}  **Выдано верификаций:**", value=f"```{fin2['verify']} чел.```", inline=True)
            embed.add_field(name=f"> {config['dot']}  **Выдано недопусков:**", value=f"```{fin2['unverify']} чел.```", inline=True)
            await interaction.edit_original_message(embed=embed)

    @tasks.loop(minutes=5)
    async def get_m(self):
        for x in coll.find():
            for i in x['twink']:
                guild = self.bot.get_guild(int(config['guild_id']))
                try:
                    member = guild.get_member(int(i))
                    avatar = member.display_avatar
                except:
                    lsti = x['twink']
                    lsti.remove(i)
                    coll.update_one({"id": x['id']}, {"$set": {"twink": lsti}})

    @tasks.loop(minutes=5)
    async def voice_check(self):
        for guild in self.bot.guilds:
            if guild.id == int(config['guild_id']):
                for channel in guild.voice_channels:
                    channelszxc = [1125650576022175855, 1125650621513609367, 1125650646448746546, 1125650697636024371, 1171129379506622535] # ID каналов Верификации для слежки за онлайном support
                    if channel.id in channelszxc:
                        for member in channel.members:
                            role = guild.get_role(int(config['support']))
                            if role in member.roles:
                                find = coll3.find_one({"id": member.id})
                                if find:
                                    coll3.update_one({"id": member.id}, {"$inc": {"online": 60}})
                                else:
                                    post = {
                                        "id": member.id,
                                        "online": 0,
                                        "verify": 0,
                                        "unverify": 0,
                                    }
                                    if coll3.count_documents({"id": member.id}) == 0:
                                        coll3.insert_one(post)
                                    coll3.update_one({"id": member.id}, {"$inc": {"online": 60}})




def setup(bot):
    bot.add_cog(video(bot))