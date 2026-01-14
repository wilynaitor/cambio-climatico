import discord
import random
import asyncio
from discord.ext import commands
import os
import pyttsx3 


# 🔽 DEFINE LA FUNCIÓN AQUÍ
async def log_event(guild: discord.Guild, embed: discord.Embed):
    canal = discord.utils.get(guild.text_channels, name="logs-bots")
    if canal:
        await canal.send(embed=embed)

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


@bot.tree.command(name="amarillo",
                  description="Info sobre el contenedor amarillo")
async def amarillo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🟡 Contenedor Amarillo",
        description="Aquí van **envases de plástico**, **latas** y **briks**.",
        color=discord.Color.yellow()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="azul", description="Info sobre el contenedor azul")
async def azul(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔵 Contenedor Azul",
        description="Aquí van **papel** y **cartón**.",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="verde", description="Info sobre el contenedor verde")
async def verde(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🟢 Contenedor Verde",
        description="Aquí va **vidrio**.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="marron", description="Info sobre el contenedor marrón")
async def marron(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🟤 Contenedor Marrón",
        description="Aquí van **residuos orgánicos**.",
        color=discord.Color.dark_gold()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="gris", description="Info sobre el contenedor gris")
async def gris(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚫ Contenedor Gris",
        description="Aquí va **basura general**.",
        color=discord.Color.dark_grey()
    )
    await interaction.response.send_message(embed=embed)

preguntas = [
    {
        "pregunta": "¿Dónde se tira un cuaderno usado sin espiral?",
        "opciones": ["Azul", "Amarillo", "Gris", "Verde"],
        "respuesta": "Azul",
        "explicacion": "El papel y cartón limpios van al contenedor azul."
    },
    {
        "pregunta": "¿Cuántas veces se puede reciclar el papel?",
        "opciones": ["Una vez", "Dos veces", "Hasta 7 veces", "Infinitas veces"],
        "respuesta": "Hasta 7 veces",
        "explicacion": "Las fibras del papel se degradan y permiten reciclarlo hasta unas 7 veces."
    },
    {
        "pregunta": "¿Qué tipo de plástico NO se debe reciclar en el contenedor amarillo?",
        "opciones": ["Botellas", "Envases", "Juguetes", "Bolsas"],
        "respuesta": "Juguetes",
        "explicacion": "Los juguetes no son envases y deben ir a puntos limpios o basura general."
    },
    {
        "pregunta": "¿Reciclar papel ayuda a ahorrar qué recurso?",
        "opciones": ["Petróleo", "Árboles", "Gas", "Metal"],
        "respuesta": "Árboles",
        "explicacion": "Reciclar papel reduce la tala de árboles y el consumo de agua."
    }
]


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

        for item in self.view.children:
            item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self.view)
        self.view.stop()



@bot.tree.command(name="trivia", description="Trivia interactiva con botones")
async def trivia(interaction: discord.Interaction):

    pregunta = random.choice(preguntas)

    embed = discord.Embed(
        title="♻️ Trivia de Reciclaje",
        description=f"**{pregunta['pregunta']}**\n\nElige la respuesta correcta:",
        color=discord.Color.blurple()
    )

    view = TriviaView(pregunta, interaction.user)
    await interaction.response.send_message(embed=embed, view=view)



tips = [
    "🏠 Coloca contenedores de reciclaje en casa para facilitar el hábito.",
    "🧠 Infórmate sobre las reglas de reciclaje de tu ciudad.",
    "👨‍👩‍👧‍👦 Enseña a otros a reciclar y multiplica el impacto positivo."
]



@bot.tree.command(name="tip", description="Consejo ecológico aleatorio")
async def tip(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(tips))


@bot.tree.command(name="mem", description="Envía una imagen aleatoria")
async def mem(interaction: discord.Interaction):
    img_name = random.choice(os.listdir('images'))
    await interaction.response.send_message(file=discord.File(f'images/{img_name}'))


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

 