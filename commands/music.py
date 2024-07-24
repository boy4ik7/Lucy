from mafic import NodePool, Player, Playlist, Track, TrackEndEvent, TrackStartEvent, errors, CPUStats, MemoryStats, Timescale, Filter, LowPass
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import asyncio

# 24.07.2024
# V1.0
LOW = True
TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT
node_pools = {}       


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.node_pools = {}
        self.interaction_list = {}
        self.track_queues = {}

    class playback_button(nextcord.ui.View):
        def __init__(self, parent, timeout, node_pools, interaction_list, track_queues):
            super().__init__()
            self.timeout = timeout
            self.parent = parent
            self.node_pools = node_pools
            self.interaction_list = interaction_list
            self.track_queues = track_queues
        
        # resume/pause
        @nextcord.ui.button(label="⏯️", style=nextcord.ButtonStyle.blurple)
        async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            await self.parent.resume_pause_track(self=self, interaction=interaction)

        # skip
        @nextcord.ui.button(label="⏭", style=nextcord.ButtonStyle.blurple)
        async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            voice_state = interaction.user.voice
            if voice_state is not None and voice_state.channel is not None:
                await self.parent.skip_track(self=self, interaction=interaction)
                #self.stop()
            else:
                await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

        # stop
        @nextcord.ui.button(label="⏹", style=nextcord.ButtonStyle.red)
        async def button3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            voice_state = interaction.user.voice
            if voice_state is not None and voice_state.channel is not None:
                self.stop()
                await self.parent.stop_music(self=self, interaction=interaction)
            else:
                await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)
        
        # playlist
        @nextcord.ui.button(label="📃", style=nextcord.ButtonStyle.gray)
        async def button4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            await self.parent.show_playlist(self=self, interaction=interaction)

        # +
        @nextcord.ui.button(label="➕", style=nextcord.ButtonStyle.green)
        async def button5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            voice_state = interaction.user.voice
            if voice_state is not None and voice_state.channel is not None:
                modal = self.text_in(parent=self.parent, node_pools=self.node_pools, interaction_list=self.interaction_list, track_queues=self.track_queues)
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

        class text_in(nextcord.ui.Modal):
            def __init__(self, parent, node_pools, interaction_list, track_queues):
                super().__init__(
                    "Добавление музыки",
                    timeout= 60,
                )
                self.node_pools = node_pools
                self.parent = parent
                self.interaction_list = interaction_list
                self.track_queues = track_queues
                self.name = nextcord.ui.TextInput(
                    label="Введите запрос или ссылку: ",
                    min_length=1,
                    max_length=2000,
                )
                self.add_item(self.name)
                
            async def callback(self, interaction: nextcord.Interaction) -> None:
                query = self.name.value
                await self.parent.add_track(self=self, interaction=interaction, query=query)

        class playlist_button(nextcord.ui.View):
            def __init__(self, parent, track_queues=None, interaction_list=None):
                super().__init__()
                self.timeout = 60
                self.parent = parent
                self.track_queues = track_queues
                self.interaction_list = interaction_list
            
            @nextcord.ui.button(label="🧹", style=nextcord.ButtonStyle.red)
            async def buttun1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
                guild_id = interaction.guild.id
                if guild_id in self.track_queues and self.track_queues[guild_id]:
                    self.track_queues[guild_id].clear()
                    self.interaction_list[guild_id].clear()
                    await interaction.response.send_message("Список очищен.")
                #self.stop()

    class playlist_button(nextcord.ui.View):
        def __init__(self, parent, track_queues=None, interaction_list=None):
            super().__init__()
            self.timeout = 60
            self.parent = parent
            self.track_queues = track_queues
            self.interaction_list = interaction_list
        
        @nextcord.ui.button(label="🧹", style=nextcord.ButtonStyle.red)
        async def buttun1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            guild_id = interaction.guild.id
            if guild_id in self.track_queues and self.track_queues[guild_id]:
                self.track_queues[guild_id].clear()
                self.interaction_list[guild_id].clear()
                await interaction.response.send_message("Список очищен.")

    async def start_next_track(self, player, guild_id):
        if guild_id in self.track_queues and self.track_queues[guild_id]:
            next_track = self.track_queues[guild_id].pop(0)
            #self.interaction_list[guild_id].pop(0)
            await player.play(next_track)

    async def add_track(self, interaction, query):
        await interaction.response.defer()
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            guild_id = interaction.guild.id
            node_pool = self.node_pools.get(guild_id)

            if node_pool is None:
                node_pool = NodePool(self.bot)
                await node_pool.create_node(
                    host="127.0.0.1",
                    port=2333,
                    label=f"NODE_{guild_id}",
                    password="youshallnotpass",
                )
                self.node_pools[guild_id] = node_pool
                node_pool = self.node_pools.get(guild_id) 

            if not interaction.guild.voice_client: 
                player = await voice_state.channel.connect(cls=Player)
                await player.guild.change_voice_state(channel=voice_state.channel, self_deaf=True)
                if LOW is True:
                    filter = Filter(#timescale = Timescale(speed = 1.0, pitch=1.0, rate=1.0),
                                volume=0.5,
                                low_pass=LowPass(smoothing = 5.0)
                            )
                else:
                    filter = Filter(volume=0.5)
                await player.add_filter(filter, label = "Low")
            else:
                player = interaction.guild.voice_client

            tracks = await player.fetch_tracks(query)

            if not tracks:
                return await interaction.followup.send("Не найдено.")

            guild_id = interaction.guild.id
            if guild_id not in self.track_queues:
                self.track_queues[guild_id] = []
                self.interaction_list[guild_id] = []

            if isinstance(tracks, Playlist):
                playlist = tracks
                for track in playlist.tracks:
                    self.track_queues[guild_id].append(track)
                    self.interaction_list[guild_id].append(interaction)
                
                if not player.current:
                    await self.start_next_track(player, guild_id)
                
                await interaction.followup.send(f"Плейлист **{playlist.name}** добавлен в очередь.")
                #await self.play_playlist(interaction, player, tracks)

            else:
                track = tracks[0]
                self.track_queues[guild_id].append(track)
                self.interaction_list[guild_id].append(interaction)
                if not player.current:
                    await self.start_next_track(player, guild_id)
                #else:
                await interaction.followup.send(f"**{track.title}** добавлен в очередь.")
                #await self.play_track(interaction, player, tracks[0])
        else:
            await interaction.followup.send("Вы не находитесь в голосовом канале.")

    async def stop_music(self, interaction):
        await interaction.response.defer()
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            if interaction.guild.voice_client:
                await interaction.followup.send("Бот, остановлен.")
                player = interaction.guild.voice_client
                await player.pause()
                await player.disconnect()
                guild_id = interaction.guild.id
                node_pool = self.node_pools.pop(guild_id) 
                await node_pool.close()
                if guild_id in self.track_queues and self.track_queues[guild_id]:
                    self.track_queues[guild_id].clear()
                    self.interaction_list[guild_id].clear()
            else:
                await interaction.followup.send("Бот не находится в голосовом канале.", ephemeral=True)
        else:
            await interaction.followup.send("Вы не находитесь в голосовом канале.", ephemeral=True)

    async def skip_track(self, interaction):
        await interaction.response.defer()
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            if interaction.guild.voice_client:
                player = interaction.guild.voice_client
                await player.stop()
                await interaction.followup.send("Готово", ephemeral=True)
            else:
                await interaction.followup.send("Ничего не воспроизводится", ephemeral=True)
        else:
            await interaction.followup.send("Вы не находитесь в голосовом канале.", ephemeral=True)

    async def show_playlist(self, interaction):
        await interaction.response.defer()
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            guild_id = interaction.guild.id
            queues = self.track_queues[guild_id]
            check_list = len(queues)
            if check_list == 0:
                text = "*Пусто* \n Используйте **play**"
            else:
                text = "Изменить порядок списка - **queue**\n"
                name = None
                number = None
                for i in range(len(queues)):
                    name = str(queues[i].title)
                    number = str(i)
                    #time = self.get_time(queues[i].length)
                    length = queues[i].length
                    length = int(length / 1000)
                    sec = length % 60
                    if sec < 10:
                        sec = str(sec)
                        x = "0"
                        sec = x + sec
                    min = length // 60
                    if min < 10:
                        min = str(min)
                        x = "0"
                        min = x + min
                    time = str(min) + ":" + str(sec)
                    text = text + number + ". " + name + " " +"(" + time +")" + "\n"
            embed = nextcord.Embed(
            title="Список воспроизведения",
            description=text,
            color=nextcord.Color.green())
            view = self.playlist_button(parent=music, track_queues=self.track_queues, interaction_list=self.interaction_list)
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.followup.send("Вы не находитесь в голосовом канале.", ephemeral=True)

    async def queue_playlist(self, interaction, position, moving_position):
        await interaction.response.defer()
        try:
            guild_id = interaction.guild.id
            list = len(self.track_queues[guild_id])
            if position > list or moving_position > list:
                await interaction.followup.send("Ошибка. Проверьте значение позиций.", ephemeral=True)
            elif position < 0 or moving_position < 0:
                await interaction.followup.send("Ошибка. Проверьте значение позиций.", ephemeral=True)
            else:
                position -= 1
                moving_position -= 1
                track_to_move = self.track_queues[guild_id].pop(moving_position)
                self.track_queues[guild_id].insert(position, track_to_move)
                user_to_move = self.interaction_list[guild_id].pop(moving_position)
                self.interaction_list[guild_id].insert(position, user_to_move)
                await interaction.followup.send(f"**{track_to_move.title}** перемещён на {position + 1} место.")
                await self.show_playlist(interaction)
        except:
            await interaction.followup.send("Ошибка.", ephemeral=True)

    async def resume_pause_track(self, interaction):
        await interaction.response.defer()
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            player = interaction.guild.voice_client
            if player.paused:
                await player.resume()
                await interaction.followup.send("Готово.", ephemeral=True) 
            else:
                await player.pause()
                await interaction.followup.send("Пауза.")
                await asyncio.sleep(1200) # 20 min 
                if player.paused:
                    #self.stop_music(interaction=interaction)
                    if interaction.guild.voice_client:
                        #await interaction.channel.send("Бот покинул голосовой канал.")
                        player = interaction.guild.voice_client
                        await player.disconnect()
                        guild_id = interaction.guild.id
                        node_pool = self.node_pools.pop(guild_id)
                        await node_pool.close()
                        if guild_id in self.track_queues and self.track_queues[guild_id]:
                            self.track_queues[guild_id].clear()
                            self.interaction_list[guild_id].clear()
        else:
            await interaction.followup.send("Вы не находитесь в голосовом канале.", ephemeral=True)     

    def get_time(self, length):
        length = int(length / 1000)
        sec = length % 60
        if sec < 10:
            sec = str(sec)
            x = "0"
            sec = x + sec
        min = length // 60
        if min < 10:
            min = str(min)
            x = "0"
            min = x + min
        time = str(min) + ":" + str(sec) 
        return time

    @commands.Cog.listener()            
    async def on_track_stuck(self, event):
        guild_id = event.player.guild.id
        interaction = self.interaction_list[guild_id].pop(0)#self.interaction_list[guild_id][0]
        await self.skip_track(interaction=interaction)
        await interaction.channel.send("Трэк завис, пропускаем...")

    @commands.Cog.listener()
    async def on_track_end(self, event):
        await self.start_next_track(event.player, event.player.guild.id)

    @commands.Cog.listener()
    async def on_track_start(self, event):
        guild_id = event.player.guild.id
        name = event.track.title
        length = event.track.length
        artwork_url = event.track.artwork_url
        url = event.track.uri
        time = self.get_time(length)
        interaction = self.interaction_list[guild_id].pop(0)#self.interaction_list[guild_id][0]
        embed = nextcord.Embed(
            title=f"♪ {name} ♫",
            description=f"{time}\n"
                        f"**[Источник]({url})**\n"
                        f"От: {interaction.user.mention}\n"
                        "Продолжить/Пауза - **resume_pause**\n"
                        "Пропустить трек - **skip**\n"
                        "Посмотреть список воспроизведения - **playlist**\n"
                        "Остановить музыку - **stop**\n",
            color=interaction.user.color) #nextcord.Color.green()
        embed.set_thumbnail(url=artwork_url)
        duration = int(length) / 1000
        view = self.playback_button(parent=music, timeout=duration, node_pools=self.node_pools, interaction_list=self.interaction_list, track_queues=self.track_queues)
        await interaction.channel.send(embed=embed, view=view)
        await asyncio.sleep(duration)
        #if len(self.track_queues[guild_id]) == 0:
            #await interaction.channel.send("Список закончился.")
        await asyncio.sleep(duration+600) # 10 min
        if len(self.track_queues[guild_id]) == 0:
            #await interaction.channel.send("Бот покинул голосовой канал.")
            player = interaction.guild.voice_client
            await player.disconnect()
            guild_id = interaction.guild.id
            node_pool = self.node_pools.pop(guild_id)
            await node_pool.close()
            if guild_id in self.track_queues and self.track_queues[guild_id]:
                self.track_queues[guild_id].clear()
                self.interaction_list[guild_id].clear()      
        #print('info \n',name, url, length, time, artwork_url)

    @nextcord.slash_command(description="Изменить порядок плейлиста")
    @application_checks.guild_only()
    async def queue(self, interaction: Interaction, moving_position: int = SlashOption(description="Что переместить?"), position : int = SlashOption(description="На какое место переместить? (1 поумолчанию)", required = False, default=1)):
        await self.queue_playlist(interaction, position, moving_position)

    @nextcord.slash_command(description="Продолжить/Пауза")
    @application_checks.guild_only()
    async def resume_pause(self, interaction: Interaction):
        await self.resume_pause_track(interaction)

    @nextcord.slash_command(description="Воспроизвести музыку с YouTube")
    @application_checks.guild_only()
    async def play(self, interaction: Interaction, query: str = SlashOption(description="Запрос или ссылка на YouTube")):
        await self.add_track(interaction, query)

    @nextcord.slash_command(description="Пропустить трек")
    @application_checks.guild_only()
    async def skip(self, interaction: Interaction):
        await self.skip_track(interaction)

    @nextcord.slash_command(description="Остановить музыку")
    @application_checks.guild_only()
    async def stop(self, interaction: Interaction):
        await self.stop_music(interaction)

    @nextcord.slash_command(description="Посмотреть список воспроизведения")
    @application_checks.guild_only()
    async def playlist(self, interaction: Interaction):
        await self.show_playlist(interaction)

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Команда отдалки")
    async def music_info(self, interaction: Interaction):
        guilds = self.bot.guilds
        view = self.music_info_server_select(guilds, track_queues=self.track_queues, interaction_list = self.interaction_list, node_pools = self.node_pools)
        await interaction.response.send_message(view=view) 
    
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="LOW")
    async def music_low(self, interaction: Interaction, mode : str = SlashOption(description="Выберите режим (LOW - по умолчанию)", choices= ["HIGH", "LOW"])):
        global LOW
        if mode == "HIGH":
            LOW = False
        else:
            LOW = True
        await interaction.response.send_message(f"LOW - {LOW}")

    class music_info_server_select(nextcord.ui.View):
        def __init__(self, guilds, track_queues, interaction_list, node_pools):
            super().__init__(
                timeout= 30,
            )
            self.guilds = guilds
            self.track_queues = track_queues
            self.interaction_list = interaction_list
            self.node_pools = node_pools
             
            self.select = nextcord.ui.StringSelect( 
                placeholder = "Выберите сервер",
                min_values = 1,
                max_values = 1,
                options = [ 
                    nextcord.SelectOption(
                        label=f"{guild.name}",
                        value=f"{guild.id}+{guild.name}"
                        #description=f"{guild.name}"
                    ) for guild in self.guilds
                ]
            )
            
            self.select.callback = self.select_callback
            self.add_item(self.select)


        async def select_callback(self, select):
            data = self.select.values[0].split("+")
            server_name = data[1] + " ID:" + data[0]
            guild_id = int(data[0])
            skobki = "```"
            text = ""
            text2 = text
            text2 += skobki
            bot_voice_state = select.guild.voice_client
            text += skobki
            text += "Сервер: " + server_name +"\n"
            try:
                tracks = self.track_queues[guild_id]
                users = self.interaction_list[guild_id]
                for track in tracks:
                    text += str(track.title) + "\n"
                text += f"Сумма: {len(tracks)}"
                for interaction in users:
                    text2 += str(interaction.user.id) + "\n"
                text2 += f"Сумма: {len(users)}"
            except:
                text += "\nПусто"
                text2 += "\nПусто"
            text2 += skobki
            text += skobki
            await select.channel.send(text)
            await select.channel.send(text2)
            node_info = []
            for guild_id, node_pool in self.node_pools.items():
                for node in node_pool.nodes:
                    node_info.append(f"Guild ID: {guild_id}, Node Label: {node.label}")
            if not node_info:
                await select.channel.send("```Нет активных узлов.```")
            else:
                await select.channel.send("```"+"\n".join(node_info)+"```")

def setup(bot):
    bot.add_cog(music(bot))