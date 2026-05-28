# bot.py - Bot Discord Fantasy RPG chính

import discord
from discord.ext import commands
import asyncio
import os
import random
from datetime import datetime

# Import các module của chúng ta
from character import (CLASSES, TRAITS, create_new_character, get_character_stats_text,
                       level_up, calc_atk, calc_matk, calc_def, calc_mdef, calc_crit, calc_spd)
from skills_data import SKILLS, get_skill_choices, get_skills_info, RARITY_HIDDEN
from database import Database
from ai_gm import setup_gemini, process_action, generate_training_result, generate_world_event

# ══════════════════════════════════════════
# CẤU HÌNH BOT
# ══════════════════════════════════════════

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
db = Database()

# Khởi tạo Gemini
gemini_model = None

# Theo dõi người chơi đang trong quá trình tạo nhân vật
creating_char = {}
# Theo dõi cooldown hành động
action_cooldowns = {}
# Lưu pending skill choices
pending_skills = {}
pending_statup = {}

# ══════════════════════════════════════════
# SỰ KIỆN BOT
# ══════════════════════════════════════════

@bot.event
async def on_ready():
    global gemini_model
    gemini_model = setup_gemini(GEMINI_API_KEY)
    print(f"⚔️ Bot {bot.user.name} đã online!")
    print(f"🌍 Thế giới Aeternium đã mở cửa!")
    await bot.change_presence(activity=discord.Game(name="🗡️ Fantasy RPG | !help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Thiếu thông tin! Dùng `!help` để xem hướng dẫn.")
    else:
        print(f"Lỗi: {error}")

# ══════════════════════════════════════════
# LỆNH HELP
# ══════════════════════════════════════════

@bot.command(name='help', aliases=['h', 'trợgiúp'])
async def help_cmd(ctx):
    embed = discord.Embed(
        title="⚔️ Fantasy RPG - Hướng Dẫn",
        description="Chào mừng đến với Aeternium! Thế giới của ma thuật và phiêu lưu!",
        color=0xFFD700
    )
    embed.add_field(
        name="🧙 Tạo Nhân Vật",
        value="`!create` - Tạo nhân vật mới\n`!profile` hoặc `!p` - Xem thông số nhân vật\n`!delete` - Xóa nhân vật (cẩn thận!)",
        inline=False
    )
    embed.add_field(
        name="⚔️ Hành Động",
        value="`!do [hành động]` - Làm bất cứ điều gì!\n`!train [chỉ số] [mô tả]` - Tập luyện nâng chỉ số\n`!rest` - Nghỉ ngơi hồi phục HP/MP",
        inline=False
    )
    embed.add_field(
        name="📊 Phát Triển",
        value="`!skills` - Xem kỹ năng của bạn\n`!chooseskill` - Chọn kỹ năng mới (cần Skill Point)\n`!statup [chỉ số]` - Nâng chỉ số (cần Stat Point)\n`!allskills` - Xem tất cả kỹ năng",
        inline=False
    )
    embed.add_field(
        name="🌍 Thế Giới",
        value="`!world` - Xem thông tin thế giới\n`!location` - Xem vị trí hiện tại\n`!leaderboard` hoặc `!top` - Bảng xếp hạng",
        inline=False
    )
    embed.add_field(
        name="💡 Ví Dụ Hành Động",
        value='`!do Tôi tấn công con Goblin trước mặt bằng kiếm`\n`!do Tôi lẻn vào kho báu của lãnh chúa`\n`!do Tôi thử học phép thuật lửa từ cuốn sách cổ`\n`!train STR Tôi tập chặt gỗ trong rừng cả ngày`',
        inline=False
    )
    embed.set_footer(text="Aeternium Fantasy RPG | Mọi hành động đều có hậu quả!")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# TẠO NHÂN VẬT
# ══════════════════════════════════════════

@bot.command(name='create', aliases=['tạo', 'new'])
async def create_character(ctx):
    user_id = ctx.author.id
    
    if db.has_player(user_id):
        char = db.get_player(user_id)
        await ctx.send(f"⚠️ Bạn đã có nhân vật **{char['name']}** (Level {char['level']})!\nDùng `!delete` để xóa nhân vật cũ trước.")
        return
    
    creating_char[user_id] = {"step": "name"}
    
    embed = discord.Embed(
        title="⚔️ Tạo Nhân Vật Mới",
        description="Hành trình của bạn trong Aeternium sắp bắt đầu!\n\n**Bước 1/3:** Nhập tên nhân vật của bạn:",
        color=0x00FF7F
    )
    embed.set_footer(text="Nhập tên trong vòng 60 giây")
    await ctx.send(embed=embed)
    
    def check_name(m):
        return m.author.id == user_id and m.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', check=check_name, timeout=60)
        name = msg.content.strip()
        if len(name) > 25 or len(name) < 2:
            await ctx.send("❌ Tên phải từ 2-25 ký tự!")
            del creating_char[user_id]
            return
        creating_char[user_id]["name"] = name
    except asyncio.TimeoutError:
        await ctx.send("⏰ Hết thời gian! Dùng `!create` để thử lại.")
        del creating_char[user_id]
        return
    
    # Chọn class
    class_list = list(CLASSES.items())
    class_text = ""
    for i, (class_name, class_data) in enumerate(class_list, 1):
        class_text += f"`{i}.` {class_name}\n   *{class_data['desc']}*\n\n"
    
    embed = discord.Embed(
        title="⚔️ Chọn Class",
        description=f"Chào mừng **{name}**!\n\n**Bước 2/3:** Chọn class nhân vật (nhập số):\n\n{class_text}",
        color=0x00BFFF
    )
    await ctx.send(embed=embed)
    
    def check_class(m):
        return (m.author.id == user_id and m.channel == ctx.channel 
                and m.content.strip().isdigit() 
                and 1 <= int(m.content.strip()) <= len(class_list))
    
    try:
        msg = await bot.wait_for('message', check=check_class, timeout=60)
        class_choice = class_list[int(msg.content.strip()) - 1][0]
        creating_char[user_id]["class"] = class_choice
    except asyncio.TimeoutError:
        await ctx.send("⏰ Hết thời gian! Dùng `!create` để thử lại.")
        del creating_char[user_id]
        return
    
    # Chọn trait
    trait_list = list(TRAITS.items())
    trait_text = ""
    for i, (trait_name, trait_data) in enumerate(trait_list, 1):
        trait_text += f"`{i}.` **{trait_name}** - {trait_data['desc']}\n"
    
    embed = discord.Embed(
        title="✨ Chọn Đặc Tính (Trait)",
        description=f"**Bước 3/3:** Chọn đặc tính bẩm sinh của **{name}** (nhập số):\n\n{trait_text}",
        color=0xFF69B4
    )
    await ctx.send(embed=embed)
    
    def check_trait(m):
        return (m.author.id == user_id and m.channel == ctx.channel 
                and m.content.strip().isdigit() 
                and 1 <= int(m.content.strip()) <= len(trait_list))
    
    try:
        msg = await bot.wait_for('message', check=check_trait, timeout=60)
        trait_choice = trait_list[int(msg.content.strip()) - 1][0]
    except asyncio.TimeoutError:
        await ctx.send("⏰ Hết thời gian! Dùng `!create` để thử lại.")
        del creating_char[user_id]
        return
    
    # Tạo nhân vật
    char = create_new_character(
        creating_char[user_id]["name"],
        creating_char[user_id]["class"],
        trait_choice
    )
    
    db.save_player(user_id, char)
    if user_id in creating_char:
        del creating_char[user_id]
    
    # Thông báo tạo thành công
    stats = char["stats"]
    embed = discord.Embed(
        title=f"🎉 {char['name']} đã ra đời!",
        description=f"Hành trình của **{char['name']}** trong thế giới Aeternium bắt đầu từ **{char['location']}**!",
        color=0xFFD700
    )
    embed.add_field(name="Class", value=char['class'], inline=True)
    embed.add_field(name="Trait", value=char['trait'], inline=True)
    embed.add_field(name="Level", value=char['level'], inline=True)
    embed.add_field(name="❤️ HP", value=f"{char['hp']}/{char['max_hp']}", inline=True)
    embed.add_field(name="💙 MP", value=f"{char['mp']}/{char['max_mp']}", inline=True)
    embed.add_field(name="💰 Vàng", value=char['gold'], inline=True)
    embed.add_field(
        name="📊 Chỉ Số",
        value=f"STR:{stats['STR']} | AGI:{stats['AGI']} | INT:{stats['INT']}\nVIT:{stats['VIT']} | WIS:{stats['WIS']} | LCK:{stats['LCK']}",
        inline=False
    )
    embed.add_field(
        name="🎯 Kỹ Năng Khởi Đầu",
        value=", ".join(char['skills']),
        inline=False
    )
    embed.add_field(
        name="🎒 Vật Phẩm",
        value=", ".join(char['inventory']),
        inline=False
    )
    embed.set_footer(text="Dùng !do [hành động] để bắt đầu phiêu lưu!")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# XEM NHÂN VẬT
# ══════════════════════════════════════════

@bot.command(name='profile', aliases=['p', 'char', 'nhânvật', 'stats'])
async def profile(ctx, member: discord.Member = None):
    target = member or ctx.author
    char = db.get_player(target.id)
    
    if not char:
        msg = "Bạn chưa có nhân vật!" if target == ctx.author else f"{target.display_name} chưa có nhân vật!"
        await ctx.send(f"❌ {msg} Dùng `!create` để tạo.")
        return
    
    stats = char["stats"]
    
    # HP/MP bars
    def make_bar(cur, mx, length=12):
        filled = int((cur/mx)*length) if mx > 0 else 0
        return "█"*filled + "░"*(length-filled)
    
    embed = discord.Embed(
        title=f"📜 {char['name']}",
        color=0xFFD700
    )
    embed.add_field(name="Class", value=char['class'], inline=True)
    embed.add_field(name="Trait", value=char['trait'], inline=True)
    embed.add_field(name="Level", value=f"**{char['level']}**", inline=True)
    
    embed.add_field(
        name="❤️ HP",
        value=f"{char['hp']}/{char['max_hp']}\n{make_bar(char['hp'], char['max_hp'])}",
        inline=True
    )
    embed.add_field(
        name="💙 MP",
        value=f"{char['mp']}/{char['max_hp']}\n{make_bar(char['mp'], char['max_mp'])}",
        inline=True
    )
    embed.add_field(
        name="⭐ EXP",
        value=f"{char['exp']}/{char['exp_next']}\n{make_bar(char['exp'], char['exp_next'])}",
        inline=True
    )
    
    embed.add_field(
        name="📊 Chỉ Số Cơ Bản",
        value=(f"💪 **STR** {stats['STR']}  |  🏃 **AGI** {stats['AGI']}\n"
               f"🧠 **INT** {stats['INT']}  |  🛡️ **VIT** {stats['VIT']}\n"
               f"📖 **WIS** {stats['WIS']}  |  🍀 **LCK** {stats['LCK']}"),
        inline=False
    )
    embed.add_field(
        name="⚔️ Chỉ Số Chiến Đấu",
        value=(f"ATK: **{calc_atk(stats)}**  |  MATK: **{calc_matk(stats)}**\n"
               f"DEF: **{calc_def(stats)}**  |  MDEF: **{calc_mdef(stats)}**\n"
               f"CRIT: **{calc_crit(stats)}%**  |  SPD: **{calc_spd(stats)}**"),
        inline=False
    )
    
    if char.get('stat_points', 0) > 0 or char.get('skill_points', 0) > 0:
        embed.add_field(
            name="🎓 Points Chưa Dùng",
            value=f"📊 Stat Points: **{char.get('stat_points', 0)}** | 🎓 Skill Points: **{char.get('skill_points', 0)}**\nDùng `!statup` và `!chooseskill`!",
            inline=False
        )
    
    embed.add_field(name="📍 Vị Trí", value=char['location'], inline=True)
    embed.add_field(name="💰 Vàng", value=char['gold'], inline=True)
    embed.add_field(name="⚔️ Kills", value=char['kills'], inline=True)
    embed.add_field(
        name="🎯 Kỹ Năng",
        value=", ".join(char['skills'][:8]) + (f"... (+{len(char['skills'])-8})" if len(char['skills']) > 8 else ""),
        inline=False
    )
    embed.set_author(name=target.display_name, icon_url=target.display_avatar.url)
    embed.set_footer(text="!do [hành động] để phiêu lưu | !skills để xem đầy đủ kỹ năng")
    
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# HÀNH ĐỘNG CHÍNH - Trái tim của game
# ══════════════════════════════════════════

@bot.command(name='do', aliases=['action', 'làm', 'hành động'])
async def do_action(ctx, *, action: str = None):
    user_id = ctx.author.id
    
    if not action:
        await ctx.send("❌ Bạn muốn làm gì? Ví dụ: `!do Tôi tấn công con Goblin bằng kiếm`")
        return
    
    char = db.get_player(user_id)
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật! Dùng `!create` để tạo.")
        return
    
    if char['hp'] <= 0:
        await ctx.send(f"💀 **{char['name']}** đã bất tỉnh! Dùng `!rest` để hồi phục.")
        return
    
    # Cooldown 3 giây
    now = datetime.now().timestamp()
    if user_id in action_cooldowns and now - action_cooldowns[user_id] < 3:
        remaining = int(3 - (now - action_cooldowns[user_id]))
        await ctx.send(f"⏳ Chờ {remaining} giây nữa nhé!", delete_after=3)
        return
    action_cooldowns[user_id] = now
    
    # Gửi trạng thái "đang xử lý"
    processing_msg = await ctx.send(f"⚔️ *{char['name']} đang hành động...*")
    
    try:
        # Gọi AI GM
        result = await process_action(gemini_model, char, action)
        
        # Áp dụng kết quả
        hp_change = result.get('hp_change', 0)
        mp_change = result.get('mp_change', 0)
        exp_gain = result.get('exp_gain', 0)
        gold_change = result.get('gold_change', 0)
        new_item = result.get('new_item')
        location_change = result.get('location_change')
        status_effect = result.get('status_effect')
        hidden_trigger = result.get('hidden_condition_trigger')
        
        # Cập nhật HP
        char['hp'] = max(0, min(char['max_hp'], char['hp'] + hp_change))
        # Cập nhật MP  
        char['mp'] = max(0, min(char['max_mp'], char['mp'] + mp_change))
        # Cập nhật EXP
        char['exp'] += max(0, exp_gain)
        # Cập nhật Vàng
        char['gold'] = max(0, char['gold'] + gold_change)
        # Cập nhật vị trí
        if location_change:
            char['location'] = location_change
        # Thêm vật phẩm
        if new_item:
            char['inventory'].append(new_item)
        # Cập nhật kills
        if result.get('outcome') in ['success', 'critical_success'] and 'giết' in action.lower() or 'hạ gục' in action.lower():
            char['kills'] = char.get('kills', 0) + 1
        
        # Lưu log câu chuyện
        char['story_log'].append(f"[Lv{char['level']}] {action[:50]}... → {result.get('outcome', 'unknown')}")
        if len(char['story_log']) > 20:
            char['story_log'] = char['story_log'][-20:]
        
        # Kiểm tra điều kiện ẩn
        if hidden_trigger:
            conditions = char.get('hidden_conditions', {})
            if hidden_trigger in conditions:
                conditions[hidden_trigger] = conditions.get(hidden_trigger, 0) + 1
            char['hidden_conditions'] = conditions
        
        # Màu embed theo kết quả
        outcome = result.get('outcome', 'success')
        color_map = {
            'success': 0x00FF7F,
            'critical_success': 0xFFD700,
            'partial': 0xFFA500,
            'fail': 0xFF4444,
            'critical_fail': 0x8B0000,
            'unexpected': 0xFF69B4
        }
        color = color_map.get(outcome, 0x7289DA)
        
        # Outcome emoji
        outcome_emoji = {
            'success': '✅ Thành Công',
            'critical_success': '🌟 Đại Thành Công!',
            'partial': '⚡ Thành Công Một Phần',
            'fail': '❌ Thất Bại',
            'critical_fail': '💀 Thất Bại Thảm Hại!',
            'unexpected': '🌀 Bất Ngờ!'
        }.get(outcome, '✅')
        
        # Tạo embed kết quả
        embed = discord.Embed(
            title=f"{outcome_emoji}",
            description=result.get('narrative', 'Điều gì đó đã xảy ra...'),
            color=color
        )
        
        # Hiển thị thay đổi chỉ số
        changes = []
        if hp_change != 0:
            icon = "❤️+" if hp_change > 0 else "❤️"
            changes.append(f"{icon}{hp_change} HP")
        if mp_change != 0:
            icon = "💙+" if mp_change > 0 else "💙"
            changes.append(f"{icon}{mp_change} MP")
        if exp_gain > 0:
            changes.append(f"⭐+{exp_gain} EXP")
        if gold_change != 0:
            icon = "💰+" if gold_change > 0 else "💰"
            changes.append(f"{icon}{gold_change} Vàng")
        if new_item:
            changes.append(f"🎁 Nhận: {new_item}")
        if status_effect:
            changes.append(f"🔮 {status_effect}")
        
        if changes:
            embed.add_field(name="📊 Thay Đổi", value=" | ".join(changes), inline=False)
        
        # HP bar hiện tại
        hp_bar = "█" * int((char['hp']/char['max_hp'])*12) + "░" * (12 - int((char['hp']/char['max_hp'])*12))
        embed.add_field(
            name="❤️ HP Hiện Tại",
            value=f"{char['hp']}/{char['max_hp']} {hp_bar}",
            inline=True
        )
        embed.add_field(
            name="📍 Vị Trí",
            value=char['location'],
            inline=True
        )
        
        if result.get('next_prompt'):
            embed.add_field(name="🎯 Tiếp Theo", value=result['next_prompt'], inline=False)
        
        embed.set_footer(text=f"{char['name']} | Lv.{char['level']} | {char['class']}")
        
        # Kiểm tra level up
        level_messages = level_up(char)
        
        # Kiểm tra bất tỉnh
        if char['hp'] <= 0:
            embed.add_field(
                name="💀 BẤT TỈNH!",
                value=f"**{char['name']}** đã ngã xuống! Dùng `!rest` để hồi phục (mất 50% HP tối đa khi dậy).",
                inline=False
            )
        
        # Lưu dữ liệu
        db.save_player(user_id, char)
        
        # Xóa tin nhắn "đang xử lý"
        await processing_msg.delete()
        await ctx.send(embed=embed)
        
        # Thông báo level up
        for lv_msg in level_messages:
            lv_embed = discord.Embed(description=lv_msg, color=0xFFD700)
            await ctx.send(embed=lv_embed)
            
    except Exception as e:
        await processing_msg.delete()
        await ctx.send(f"⚠️ Có lỗi xảy ra. Thử lại nhé! (Lỗi: {str(e)[:100]})")

# ══════════════════════════════════════════
# TẬP LUYỆN
# ══════════════════════════════════════════

@bot.command(name='train', aliases=['tập', 'luyện'])
async def train(ctx, stat: str = None, *, description: str = "Tập luyện chăm chỉ"):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật! Dùng `!create`.")
        return
    
    valid_stats = ["STR", "AGI", "INT", "VIT", "WIS", "LCK"]
    
    if not stat or stat.upper() not in valid_stats:
        await ctx.send(f"❌ Chỉ số không hợp lệ!\nCác chỉ số có thể tập: `{' | '.join(valid_stats)}`\nVí dụ: `!train STR Tôi tập chặt gỗ cả ngày`")
        return
    
    stat = stat.upper()
    
    if char['hp'] < char['max_hp'] * 0.2:
        await ctx.send(f"❌ HP quá thấp để tập luyện! Nghỉ ngơi trước: `!rest`")
        return
    
    processing_msg = await ctx.send(f"🏋️ *{char['name']} đang tập luyện {stat}...*")
    
    try:
        result = await generate_training_result(gemini_model, char, stat, description)
        
        # Tăng chỉ số
        stat_gain = result.get('stat_gain', 0.1)
        exp_gain = result.get('exp_gain', 15)
        
        # Lưu fractional gains
        training_log = char.get('training_log', {})
        current = training_log.get(stat, 0) + stat_gain
        
        stat_increased = False
        if current >= 1.0:
            char['stats'][stat] += int(current)
            training_log[stat] = current - int(current)
            stat_increased = True
        else:
            training_log[stat] = current
        
        char['training_log'] = training_log
        char['exp'] += exp_gain
        
        # Chi phí HP/MP khi tập
        hp_cost = int(char['max_hp'] * 0.05)
        char['hp'] = max(1, char['hp'] - hp_cost)
        
        embed = discord.Embed(
            title=f"💪 Tập Luyện {stat}",
            description=result.get('narrative', 'Buổi tập luyện kết thúc.'),
            color=0x00BFFF
        )
        
        progress = training_log.get(stat, 0)
        progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
        
        if stat_increased:
            embed.add_field(
                name="🎉 Chỉ Số Tăng!",
                value=f"**{stat}** tăng lên **{char['stats'][stat]}**!",
                inline=False
            )
        else:
            embed.add_field(
                name=f"📈 Tiến Trình {stat}",
                value=f"{progress_bar} {int(progress*100)}%\nCần tập thêm để tăng chỉ số!",
                inline=False
            )
        
        embed.add_field(name="⭐ EXP", value=f"+{exp_gain}", inline=True)
        embed.add_field(name="❤️ HP Tiêu Hao", value=f"-{hp_cost}", inline=True)
        
        if result.get('insight'):
            embed.add_field(name="💭 Nhận Thức", value=f"*{result['insight']}*", inline=False)
        
        level_messages = level_up(char)
        db.save_player(user_id, char)
        
        await processing_msg.delete()
        await ctx.send(embed=embed)
        
        for lv_msg in level_messages:
            lv_embed = discord.Embed(description=lv_msg, color=0xFFD700)
            await ctx.send(embed=lv_embed)
            
    except Exception as e:
        await processing_msg.delete()
        await ctx.send(f"⚠️ Lỗi: {str(e)[:100]}")

# ══════════════════════════════════════════
# NGHỈ NGƠI
# ══════════════════════════════════════════

@bot.command(name='rest', aliases=['nghỉ', 'ngủ', 'hồi phục'])
async def rest(ctx):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    
    if char['hp'] == char['max_hp'] and char['mp'] == char['max_mp']:
        await ctx.send(f"✅ **{char['name']}** đang ở trạng thái hoàn hảo, không cần nghỉ ngơi!")
        return
    
    if char['hp'] <= 0:
        # Hồi sinh sau khi bất tỉnh
        char['hp'] = int(char['max_hp'] * 0.5)
        char['mp'] = int(char['max_mp'] * 0.5)
        msg = f"🏥 **{char['name']}** tỉnh dậy sau khi bất tỉnh với {char['hp']} HP và {char['mp']} MP."
    else:
        old_hp = char['hp']
        old_mp = char['mp']
        char['hp'] = char['max_hp']
        char['mp'] = char['max_mp']
        hp_gain = char['hp'] - old_hp
        mp_gain = char['mp'] - old_mp
        msg = f"😴 **{char['name']}** nghỉ ngơi và hồi phục hoàn toàn!\n❤️ +{hp_gain} HP | 💙 +{mp_gain} MP"
    
    db.save_player(user_id, char)
    
    rest_scenarios = [
        "Ngồi bên đống lửa trại, nhìn ngắm bầu trời đêm đầy sao...",
        "Tìm được một quán trọ nhỏ và ngủ ngon một giấc...",
        "Thiền định trong im lặng, để năng lượng lưu thông trong cơ thể...",
        "Nằm dài trên thảm cỏ xanh, lắng nghe tiếng gió thổi...",
        "Uống một bình thuốc hồi phục và cảm thấy sức mạnh trở lại...",
    ]
    
    embed = discord.Embed(
        title="😴 Nghỉ Ngơi",
        description=f"*{random.choice(rest_scenarios)}*\n\n{msg}",
        color=0x98FB98
    )
    embed.set_footer(text=f"{char['name']} | HP: {char['hp']}/{char['max_hp']}")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# XEM KỸ NĂNG
# ══════════════════════════════════════════

@bot.command(name='skills', aliases=['kỹnăng', 'skill'])
async def show_skills(ctx):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    
    skills_info = get_skills_info(char['skills'])
    
    embed = discord.Embed(
        title=f"📚 Kỹ Năng của {char['name']}",
        description=f"Tổng số kỹ năng: **{len(char['skills'])}**",
        color=0x9B59B6
    )
    
    # Nhóm theo độ hiếm
    by_rarity = {}
    for skill in skills_info:
        r = skill['rarity']
        if r not in by_rarity:
            by_rarity[r] = []
        by_rarity[r].append(skill)
    
    rarity_order = ["🟡 Huyền Thoại", "🟣 Siêu Hiếm", "🔵 Hiếm", "⚪ Thường", "❓ Ẩn"]
    
    for rarity in rarity_order:
        if rarity in by_rarity:
            skill_text = ""
            for s in by_rarity[rarity]:
                type_icon = "⚡" if s['type'] == 'active' else "🔮"
                mp_text = f" [MP:{s['mp']}]" if s.get('mp', 0) > 0 else ""
                skill_text += f"{type_icon} **{s['name']}**{mp_text}\n*{s['desc'][:60]}...*\n" if len(s['desc']) > 60 else f"{type_icon} **{s['name']}**{mp_text}\n*{s['desc']}*\n"
            
            if skill_text:
                embed.add_field(name=rarity, value=skill_text[:1000], inline=False)
    
    embed.set_footer(text="⚡ Active - cần dùng chủ động | 🔮 Passive - tự động kích hoạt")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# CHỌN KỸ NĂNG MỚI (khi lên cấp)
# ══════════════════════════════════════════

@bot.command(name='chooseskill', aliases=['chọnkỹnăng', 'pickskill'])
async def choose_skill(ctx):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    
    if char.get('skill_points', 0) <= 0:
        await ctx.send(f"❌ Bạn không có Skill Point! Hãy lên cấp để nhận Skill Point.")
        return
    
    # Tạo danh sách 3 kỹ năng để chọn
    choices = get_skill_choices(3, char['skills'], char['level'])
    
    if not choices:
        await ctx.send("❌ Không tìm được kỹ năng phù hợp!")
        return
    
    pending_skills[user_id] = choices
    skills_info = get_skills_info(choices)
    
    embed = discord.Embed(
        title="🎓 Chọn Kỹ Năng Mới!",
        description=f"Bạn có **{char.get('skill_points', 0)} Skill Point**. Chọn 1 trong 3 kỹ năng dưới đây:\nNhập **1**, **2**, hoặc **3**:",
        color=0xFFD700
    )
    
    for i, skill in enumerate(skills_info, 1):
        type_icon = "⚡ Active" if skill['type'] == 'active' else "🔮 Passive"
        mp_info = f" | MP: {skill['mp']}" if skill.get('mp', 0) > 0 else ""
        embed.add_field(
            name=f"`{i}.` {skill['rarity']} **{skill['name']}**",
            value=f"{type_icon}{mp_info}\n{skill['desc']}",
            inline=False
        )
    
    await ctx.send(embed=embed)
    
    def check(m):
        return (m.author.id == user_id and m.channel == ctx.channel 
                and m.content.strip() in ['1', '2', '3'])
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=30)
        choice_idx = int(msg.content.strip()) - 1
        chosen_skill = choices[choice_idx]
        
        char['skills'].append(chosen_skill)
        char['skill_points'] = char.get('skill_points', 1) - 1
        db.save_player(user_id, char)
        
        skill_info = SKILLS[chosen_skill]
        embed = discord.Embed(
            title=f"✨ Học Được: {chosen_skill}!",
            description=f"**{char['name']}** đã học được kỹ năng mới!\n\n{skill_info['rarity']} **{chosen_skill}**\n*{skill_info['desc']}*",
            color=0xFFD700
        )
        embed.set_footer(text=f"Skill Points còn lại: {char.get('skill_points', 0)}")
        await ctx.send(embed=embed)
        
    except asyncio.TimeoutError:
        if user_id in pending_skills:
            del pending_skills[user_id]
        await ctx.send("⏰ Hết thời gian! Dùng `!chooseskill` lại để chọn.")

# ══════════════════════════════════════════
# NÂNG CHỈ SỐ
# ══════════════════════════════════════════

@bot.command(name='statup', aliases=['nângchỉsố', 'upgrade'])
async def stat_up(ctx, stat: str = None):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    
    if char.get('stat_points', 0) <= 0:
        await ctx.send("❌ Bạn không có Stat Point! Lên cấp để nhận điểm.")
        return
    
    valid_stats = ["STR", "AGI", "INT", "VIT", "WIS", "LCK"]
    
    if not stat or stat.upper() not in valid_stats:
        stats = char['stats']
        embed = discord.Embed(
            title="📊 Nâng Chỉ Số",
            description=f"Bạn có **{char.get('stat_points', 0)} Stat Points**.\nGõ `!statup [chỉ số]` để nâng.\nVí dụ: `!statup STR`",
            color=0x00BFFF
        )
        embed.add_field(
            name="Chỉ Số Hiện Tại",
            value=(f"💪 **STR** {stats['STR']} - Tấn công vật lý\n"
                   f"🏃 **AGI** {stats['AGI']} - Tốc độ, né đòn\n"
                   f"🧠 **INT** {stats['INT']} - Phép thuật\n"
                   f"🛡️ **VIT** {stats['VIT']} - HP, phòng thủ\n"
                   f"📖 **WIS** {stats['WIS']} - MP, phép phòng\n"
                   f"🍀 **LCK** {stats['LCK']} - May mắn, crit"),
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    stat = stat.upper()
    char['stats'][stat] += 1
    char['stat_points'] = char.get('stat_points', 1) - 1
    
    # Cập nhật HP/MP nếu tăng VIT/WIS
    if stat == 'VIT':
        char['max_hp'] += 10
        char['hp'] += 10
    elif stat == 'WIS':
        char['max_mp'] += 8
        char['mp'] += 8
    
    db.save_player(user_id, char)
    
    stat_names = {
        "STR": "💪 Sức Mạnh", "AGI": "🏃 Tốc Độ", "INT": "🧠 Trí Tuệ",
        "VIT": "🛡️ Thể Lực", "WIS": "📖 Khôn Ngoan", "LCK": "🍀 May Mắn"
    }
    
    embed = discord.Embed(
        title=f"📈 {stat_names[stat]} Tăng!",
        description=f"**{char['name']}** đã tăng {stat_names[stat]} lên **{char['stats'][stat]}**!",
        color=0x00FF7F
    )
    embed.set_footer(text=f"Stat Points còn lại: {char.get('stat_points', 0)}")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# THÔNG TIN THẾ GIỚI
# ══════════════════════════════════════════

@bot.command(name='world', aliases=['thếgiới', 'lore'])
async def world_info(ctx):
    embed = discord.Embed(
        title="🌍 Thế Giới Aeternium",
        description="Thế giới của ma thuật, kiếm đạo và vô vàn bí ẩn...",
        color=0x4B0082
    )
    embed.add_field(
        name="📍 Các Khu Vực",
        value=("🏘️ **Làng Edenia** - Điểm khởi đầu, an toàn\n"
               "🏙️ **Thành Ironhold** - Thành phố lớn, đầy cơ hội\n"
               "🌲 **Rừng Blackthorn** - Nguy hiểm, nhiều quái vật\n"
               "⛰️ **Núi Dragonfang** - Rồng trú ngụ, kho báu\n"
               "🏰 **Tháp Babel** - Thử thách từng tầng\n"
               "💀 **Catacombs** - Tầng ngầm bí ẩn\n"
               "🌊 **Biển Stormhaven** - Sinh vật biển khổng lồ\n"
               "🏚️ **Ruined Citadel** - Tàn tích đế quốc cổ"),
        inline=False
    )
    embed.add_field(
        name="👹 Hệ Thống Cấp Bậc Quái Vật",
        value="F < E < D < C < B < A < S < SS (Trùm Cuối)",
        inline=False
    )
    embed.add_field(
        name="📜 Lịch Sử",
        value="Aeternium được tạo bởi 7 Thần Nguyên Thủy. Đế Quốc Ma Thuật Orsted từng thống trị tất cả trước khi sụp đổ vì chiến tranh Rồng. Giờ đây, thế giới chia nhỏ thành nhiều thế lực...",
        inline=False
    )
    embed.set_footer(text="Lấy cảm hứng từ Mushoku Tensei, Berserk, Re:Zero, Overlord")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# BẢNG XẾP HẠNG
# ══════════════════════════════════════════

@bot.command(name='leaderboard', aliases=['top', 'rank', 'bảngxếphạng'])
async def leaderboard(ctx):
    all_players = db.get_all_players()
    
    if not all_players:
        await ctx.send("❌ Chưa có ai tạo nhân vật!")
        return
    
    sorted_players = sorted(
        all_players.items(),
        key=lambda x: (x[1].get('level', 1), x[1].get('exp', 0)),
        reverse=True
    )[:10]
    
    embed = discord.Embed(
        title="🏆 Bảng Xếp Hạng Aeternium",
        color=0xFFD700
    )
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    board_text = ""
    for i, (uid, char) in enumerate(sorted_players):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        board_text += f"{medal} **{char['name']}** - Lv.{char['level']} {char['class']}\n"
        board_text += f"   ⚔️ {char.get('kills', 0)} kills | 📍 {char['location']}\n"
    
    embed.description = board_text or "Chưa có dữ liệu"
    embed.set_footer(text="Phiêu lưu nhiều hơn để leo rank!")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# XEM VỊ TRÍ
# ══════════════════════════════════════════

@bot.command(name='location', aliases=['vị trí', 'where', 'ởđâu'])
async def location(ctx):
    char = db.get_player(ctx.author.id)
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    await ctx.send(f"📍 **{char['name']}** đang ở: **{char['location']}**")

# ══════════════════════════════════════════
# XÓA NHÂN VẬT
# ══════════════════════════════════════════

@bot.command(name='delete', aliases=['xóa', 'reset'])
async def delete_char(ctx):
    user_id = ctx.author.id
    char = db.get_player(user_id)
    
    if not char:
        await ctx.send("❌ Bạn không có nhân vật nào!")
        return
    
    await ctx.send(f"⚠️ **CẢNH BÁO!** Bạn có chắc muốn xóa nhân vật **{char['name']}** (Level {char['level']})?\nGõ `XÁC NHẬN` trong 15 giây để xác nhận. Không thể hoàn tác!")
    
    def check(m):
        return m.author.id == user_id and m.channel == ctx.channel and m.content == "XÁC NHẬN"
    
    try:
        await bot.wait_for('message', check=check, timeout=15)
        db.delete_player(user_id)
        await ctx.send(f"💀 Nhân vật **{char['name']}** đã bị xóa. Dùng `!create` để tạo mới.")
    except asyncio.TimeoutError:
        await ctx.send("✅ Hủy xóa nhân vật.")

# ══════════════════════════════════════════
# INVENTORY
# ══════════════════════════════════════════

@bot.command(name='inventory', aliases=['inv', 'túiđồ', 'items'])
async def inventory(ctx):
    char = db.get_player(ctx.author.id)
    if not char:
        await ctx.send("❌ Bạn chưa có nhân vật!")
        return
    
    items = char.get('inventory', [])
    embed = discord.Embed(
        title=f"🎒 Túi Đồ của {char['name']}",
        description="\n".join(f"• {item}" for item in items) if items else "*Túi đồ trống*",
        color=0x8B4513
    )
    embed.set_footer(text=f"💰 Vàng: {char['gold']}")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════
# SỰ KIỆN THẾ GIỚI (Admin only)
# ══════════════════════════════════════════

@bot.command(name='worldevent', aliases=['event'])
@commands.has_permissions(administrator=True)
async def world_event(ctx):
    char = db.get_player(ctx.author.id)
    location = char['location'] if char else "Aeternium"
    
    event = await generate_world_event(gemini_model, location)
    
    embed = discord.Embed(
        title="🌍 Sự Kiện Thế Giới!",
        description=event.get('event', 'Điều gì đó đang xảy ra trong Aeternium...'),
        color=0xFF4500
    )
    await ctx.send("@here", embed=embed)

# ══════════════════════════════════════════
# CHẠY BOT
# ══════════════════════════════════════════

if __name__ == '__main__':
    if not DISCORD_TOKEN:
        print("❌ Lỗi: Không tìm thấy DISCORD_TOKEN!")
    elif not GEMINI_API_KEY:
        print("❌ Lỗi: Không tìm thấy GEMINI_API_KEY!")
    else:
        print("🚀 Đang khởi động bot...")
        bot.run(DISCORD_TOKEN)
