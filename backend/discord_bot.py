import os
import discord
import random
from discord.ext import commands
from discord.ext import tasks

bot = commands.Bot(command_prefix='?>') #กำหนด Prefix
@bot.event
async def on_ready() : #เมื่อระบบพร้อมใช้งาน
    print("Bot Started!") #แสดงผลใน CMD
@bot.event
async def on_message(message) : #ดักรอข้อความใน Chat
    if message.content.startswith('?>ping') : #เมื่อข้อความในตัวแรกมีคำว่า ping
       await message.channel.send('Pong ~ Meow ><') #ข้อความที่ต้องการตอบกลับ
bot.run('7bdad8710636ed0fe093339d40a7034ecfe52ae062e77d09b3d292f6faaf0d43') #รันบอท (โดยนำ TOKEN จากบอทที่เราสร้างไว้นำมาวาง)
