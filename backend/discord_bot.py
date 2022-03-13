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
bot.run('OTUyNDgyOTY0NTQ0MDU3MzU1.Yi2q4w.ZB6oFloQ-pOhxe4gz0YfyJ0FnTM') #รันบอท (โดยนำ TOKEN จากบอทที่เราสร้างไว้นำมาวาง)
