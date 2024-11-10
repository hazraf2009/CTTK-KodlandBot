import discord
from discord.ext import commands
import os
from main import genn_pass
import random
import requests
from load_model import get_class

# Membaca token dari file token.txt
with open("token.txt", "r") as f:
    token = f.read()

# Database resep sederhana
resep = {
    'pisang': 'Pisang yang sudah matang dapat dijadikan smoothie atau pisang goreng.',
    'roti': 'Roti yang sudah keras bisa dijadikan roti panggang atau roti tawar.',
    'sisa nasi': 'Sisa nasi bisa dijadikan nasi goreng atau bola-bola nasi.',
    'sayuran': 'Sisa sayuran bisa dijadikan sup atau tumis sayuran.',
    # Dapat menambahkan resep lain sesuai kebutuhan
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command("resep") # $resep Pisang
async def resep_daur_ulang(ctx, item: str):
    # Mengecek apakah item ada dalam database resep
    if item.lower() in resep:
        await ctx.send(f"Rekomendasi untuk mengolah {item.capitalize()}: {resep[item.lower()]}")
    else:
        await ctx.send(f"Maaf, resep untuk mengolah {item.capitalize()} tidak ditemukan.")

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def passw(ctx, panjang = 5):
    await ctx.send(genn_pass(panjang))

@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir("images"))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(f"Menyimpan gambar ke ./{attachment.filename}")
            #proses gambar ke model
            class_name, confidence_score = get_class("converted_keras\keras_model.h5", "converted_keras\labels.txt", file_name)
            if confidence_score <= 0.50:
                info = "GAMBAR APA INI COKKKK..... TAK TAH"
            info = f"Gambar ini adalah: {class_name} \nDengan tingkat kepercayaan: {confidence_score}"
            #tampilkan ke bot discord
            await ctx.send(info)
            
    
    else:
        await ctx.send("Kamu lupa memberikan gambar")

bot.run(token)