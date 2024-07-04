import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import yt_dlp

TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

class get_link_stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Получить список потоков/поток на видео Youtube")
    @application_checks.guild_only()
    async def get_link_stream(self, interaction: Interaction, link: str = SlashOption(description="Ссылка на видео"), id: str = SlashOption(description="id потока, check для проверки")):
        if "https://" in link:
            info = "```Доступные потоки: \n" + "ID - Качество | Формат | Битрейт | Размер \n"
            mes = await interaction.response.send_message("Проверяем...")
            if id == "check":
                ydl_opts_ = {
                'quiet': True,
                'listformats': True,
                'noplaylist': True
                }
                with yt_dlp.YoutubeDL(ydl_opts_) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                formats = info_dict['formats']
                for format_info in formats:
                    ext = format_info['ext']
                    abr = format_info.get('abr', 'N/A')
                    if abr != "N/A":
                        if abr == None:
                            abr = 0
                        abr = str(int(abr))
                    filesize = format_info.get('filesize', 'N/A')
                    format = format_info.get('format', 'N/A')
                    if filesize != "N/A":
                        if filesize == None:
                            filesize = 0
                        filesize = str(round(float(filesize)*0.000001, 2))
                    info = info + format + " | " + ext + " | " + abr
                    if abr != "N/A":
                        info = info + "k"
                    info = info + " | " + filesize 
                    if filesize != "N/A":
                        info = info + " Mb"
                    info = info + "\n"
                info = info +"```"
            else:
                ydl_opts_ = {
                'quiet': True,
                'format': id,
                'noplaylist': True
                }
                with yt_dlp.YoutubeDL(ydl_opts_) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    if 'url' in info_dict:
                        info = "Ссылка на поток: " + info_dict['url']
                    else:
                        info = "Ссылка на поток не найдена."
            await mes.edit(info)
        else:
            await interaction.response.send_message("Не корректная ссылка.")

def setup(bot):
    bot.add_cog(get_link_stream(bot))