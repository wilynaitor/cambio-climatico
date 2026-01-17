import discord
import random
import asyncio
from discord.ext import commands
import os
import pyttsx3 
from tips import tips
from preguntas import preguntas


voz_lock = asyncio.Lock()


# 🔽 DEFINE LA FUNCIÓN AQUÍ
async def log_event(guild: discord.Guild, embed: discord.Embed):
    canal = discord.utils.get(guild.text_channels, name="logs-bots")
    if canal:
        await canal.send(embed=embed)


def hablar_local(texto: str):
    engine = pyttsx3.init()        # 🔁 motor nuevo cada vez
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)

    for voz in engine.getProperty('voices'):
        if "spanish" in voz.name.lower():
            engine.setProperty('voice', voz.id)
            break

    engine.say(texto)
    engine.runAndWait()
    engine.stop()      


async def hablar_async(texto: str):
    async with voz_lock:  # 🔒 evita llamadas simultáneas
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, hablar_local, texto)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    guild = discord.Object(id=1360428419829203124)

    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print("Bot conectado")

    # LOG
    embed = discord.Embed(
        title="🟢 Bot iniciado",
        description=f"Conectado como {bot.user}",
        color=discord.Color.green()
    )
    await log_event(bot.guilds[0], embed)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    embed = discord.Embed(
        title="❌ Error en comando",
        description=str(error),
        color=discord.Color.red()
    )
    embed.add_field(name="Comando", value=interaction.command.name)
    embed.add_field(name="Usuario", value=interaction.user.mention)
    embed.add_field(name="Canal", value=interaction.channel.mention)

    await log_event(interaction.guild, embed)

    await interaction.response.send_message(
        "❌ Ocurrió un error ejecutando el comando.",
        ephemeral=True
    )


@bot.tree.command(name="log_test")
async def log_test(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔵 Slash command",
        description="Comando ejecutado correctamente",
        color=discord.Color.blue()
    )
    embed.add_field(name="Comando", value=interaction.command.name)
    embed.add_field(name="Usuario", value=interaction.user.mention)
    embed.add_field(name="Canal", value=interaction.channel.mention)

    await log_event(interaction.guild, embed)
    await interaction.response.send_message("Log enviado")


@bot.tree.command(name="ayuda", description="Muestra la ayuda del bot")
async def ayuda(interaction: discord.Interaction):
    help_text = (
        "**♻️ BOT DE RECICLAJE ♻️**\n\n"
        "**/amarillo** → Envases de plástico\n"
        "**/azul** → Papel y cartón\n"
        "**/verde** → Vidrio\n"
        "**/marron** → Residuos orgánicos\n"
        "**/gris** → Basura general\n"
        "**/mem** → Envía una imagen aleatoria\n"
        "**/trivia** → Pregunta de trivia sobre reciclaje\n"
        "**/tip** → Consejo ecológico\n"
    )
    await interaction.response.send_message(help_text)


@bot.tree.command(name="amarillo", description="Info y dudas frecuentes del contenedor amarillo")
async def amarillo(interaction: discord.Interaction):
    texto = (
        "El contenedor amarillo es para envases de plástico, latas y briks."
    )

    embed = discord.Embed(
        title="🟡 Contenedor Amarillo — Plásticos",
        color=discord.Color.yellow()
    )

    embed.add_field(
        name="✅ SÍ va",
        value="• Botellas\n• Envases\n• Tapas\n• Latas",
        inline=False
    )

    embed.add_field(
        name="❌ NO va",
        value="• Juguetes\n• Plásticos duros\n• Cubiertos",
        inline=False
    )

    embed.add_field(
        name="❓ Preguntas frecuentes",
        value=(
            "**¿Botella con tapa?** ✅ Sí\n"
            "**¿Envase sucio?** ⚠️ Mejor enjuagar\n"
            "**¿Bolsas de plástico?** ✅ Sí"
        ),
        inline=False
    )

    embed.add_field(
        name="🌍 Impacto climático",
        value="Reciclar plástico reduce el uso de petróleo y las emisiones.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


@bot.tree.command(name="azul", description="Info y dudas frecuentes del contenedor azul")
async def azul(interaction: discord.Interaction):
    texto = (
        "El contenedor azul es para papel y cartón limpios. "
        "No se deben tirar papeles sucios o con grasa."
    )

    embed = discord.Embed(
        title="🔵 Contenedor Azul — Papel y Cartón",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="✅ SÍ va",
        value="• Hojas\n• Revistas\n• Cajas limpias\n• Folletos",
        inline=False
    )

    embed.add_field(
        name="❌ NO va",
        value="• Servilletas usadas\n• Papel con grasa\n• Cartón mojado",
        inline=False
    )

    embed.add_field(
        name="❓ Preguntas frecuentes",
        value=(
            "**¿La caja de pizza?** ❌ Solo si está limpia\n"
            "**¿Papel arrugado?** ✅ Sí\n"
            "**¿Papel mojado?** ❌ No"
        ),
        inline=False
    )

    embed.add_field(
        name="🌍 Impacto climático",
        value="Reciclar papel reduce la tala de árboles que absorben CO₂.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


@bot.tree.command(name="verde", description="Info y dudas frecuentes del contenedor verde")
async def verde(interaction: discord.Interaction):
    texto = "El contenedor verde es para envases de vidrio, no para cristales."

    embed = discord.Embed(
        title="🟢 Contenedor Verde — Vidrio",
        color=discord.Color.green()
    )

    embed.add_field(
        name="✅ SÍ va",
        value="• Botellas de vidrio\n• Frascos\n• Tarros",
        inline=False
    )

    embed.add_field(
        name="❌ NO va",
        value="• Cristales\n• Espejos\n• Cerámica\n• Bombillas",
        inline=False
    )

    embed.add_field(
        name="❓ Preguntas frecuentes",
        value=(
            "**¿Con tapa?** ❌ Quitar tapa\n"
            "**¿Vidrio roto?** ✅ Sí\n"
            "**¿Vasos?** ❌ No"
        ),
        inline=False
    )

    embed.add_field(
        name="🌍 Impacto ambiental",
        value="El vidrio se recicla infinitas veces sin perder calidad.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


@bot.tree.command(name="marron", description="Info y dudas frecuentes del contenedor marrón")
async def marron(interaction: discord.Interaction):
    texto = "El contenedor marrón es para residuos orgánicos."

    embed = discord.Embed(
        title="🟤 Contenedor Marrón — Orgánicos",
        color=discord.Color.dark_gold()
    )

    embed.add_field(
        name="✅ SÍ va",
        value="• Restos de comida\n• Cáscaras\n• Posos de café\n• Servilletas sucias",
        inline=False
    )

    embed.add_field(
        name="❌ NO va",
        value="• Plásticos\n• Metales\n• Vidrio",
        inline=False
    )

    embed.add_field(
        name="❓ Preguntas frecuentes",
        value=(
            "**¿Huesos?** ⚠️ Depende del municipio\n"
            "**¿Bolsas compostables?** ✅ Sí\n"
            "**¿Servilletas usadas?** ✅ Sí"
        ),
        inline=False
    )

    embed.add_field(
        name="🌍 Impacto climático",
        value="Separar orgánicos reduce metano en vertederos.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


@bot.tree.command(name="gris", description="Info y dudas frecuentes del contenedor gris")
async def gris(interaction: discord.Interaction):
    texto = "El contenedor gris es para residuos no reciclables."

    embed = discord.Embed(
        title="⚫ Contenedor Gris — Basura General",
        color=discord.Color.dark_grey()
    )

    embed.add_field(
        name="🗑️ Qué va aquí",
        value="• Residuos no reciclables\n• Colillas\n• Pañales\n• Toallitas",
        inline=False
    )

    embed.add_field(
        name="❌ No debería ir",
        value="• Papel limpio\n• Plásticos reciclables\n• Vidrio",
        inline=False
    )

    embed.add_field(
        name="❓ Preguntas frecuentes",
        value=(
            "**¿Juguetes rotos?** ❌ Punto limpio\n"
            "**¿Cerámica?** ❌ Punto limpio\n"
            "**¿Polvo de barrer?** ✅ Sí"
        ),
        inline=False
    )

    embed.add_field(
        name="🌍 Impacto ambiental",
        value="Reducir este contenedor es clave para frenar la contaminación.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


class TriviaView(discord.ui.View):
    def __init__(self, pregunta_data, autor):
        super().__init__(timeout=30)
        self.pregunta = pregunta_data
        self.autor = autor
        for opcion in pregunta_data["opciones"]:
            self.add_item(TriviaButton(opcion, pregunta_data, autor))


class TriviaButton(discord.ui.Button):
    def __init__(self, opcion, pregunta_data, autor):
        super().__init__(
            label=opcion,
            style=discord.ButtonStyle.primary
        )
        self.opcion = opcion
        self.pregunta = pregunta_data
        self.autor = autor

    async def callback(self, interaction: discord.Interaction):

        if interaction.user != self.autor:
            await interaction.response.send_message(
                "❌ Esta trivia no es para ti.",
                ephemeral=True
            )
            return

        if self.opcion == self.pregunta["respuesta"]:
            titulo = "✅ ¡Correcto!"
            color = discord.Color.green()
            resultado = "¡Muy bien! 🌱"
        else:
            titulo = "❌ Incorrecto"
            color = discord.Color.red()
            resultado = f"La respuesta correcta era **{self.pregunta['respuesta']}**."

        

        embed = discord.Embed(
            title=titulo,
            description=(
                f"{resultado}\n\n"
                f"💡 **Explicación:** {self.pregunta['explicacion']}"
            ),
            color=color
        )

        texto = f"{embed.description} "

        for item in self.view.children:
            item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self.view)
        await hablar_async(texto)
        self.view.stop()


@bot.tree.command(name="trivia", description="Trivia interactiva con botones")
async def trivia(interaction: discord.Interaction):

    pregunta = random.choice(preguntas)
    texto = pregunta["pregunta"]

    embed = discord.Embed(
        title="♻️ Trivia de Reciclaje",
        description=f"**{pregunta['pregunta']}**\n\nElige la respuesta correcta:",
        color=discord.Color.blurple()
    )

    view = TriviaView(pregunta, interaction.user)
    await interaction.response.send_message(embed=embed, view=view)
    await hablar_async(texto)


@bot.tree.command(name="tip", description="Consejo ecológico aleatorio")
async def tip(interaction: discord.Interaction):

    tip = random.choice(tips)
    texto = tip

    embed = discord.Embed(
        title="💡 Consejo Ecológico",
        description=tip,
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)
    await hablar_async(texto)


@bot.tree.command(name="mem", description="Envía una imagen aleatoria")
async def mem(interaction: discord.Interaction):
    img_name = random.choice(os.listdir('images'))
    await interaction.response.send_message(file=discord.File(f'images/{img_name}'))


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
