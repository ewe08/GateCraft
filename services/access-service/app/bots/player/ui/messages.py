WELCOME_TEXT = (
    "🛡️ <b>GateCraft</b> — secure access for our private Minecraft server.\n\n"
    "This server is protected against port-scanning griefers.\n"
    "To join, register your Minecraft nickname and wait for admin approval.\n\n"
    "Commands:\n"
    "• /register &lt;nick&gt; — request access\n"
    "• /status — check your status\n"
    "• /online — show online players\n"
)

ASK_NICKNAME_TEXT = (
    "📝 Please send your Minecraft nickname.\n\n"
    "Allowed format: <code>A-Za-z0-9_</code> (3–16 chars)."
)

REGISTER_SENT_TEXT = (
    "✅ Your request has been sent to admins.\n"
    "You'll get a message once it's approved."
)

ALREADY_PENDING_TEXT = (
    "⏳ You already have a pending request.\n"
    "Please wait for admin approval."
)

ALREADY_APPROVED_TEXT = (
    "🎉 You are already approved and whitelisted.\n"
    "You can join the server now!"
)

INVALID_NICK_TEXT = (
    "❌ Invalid nickname format.\n"
    "Use only letters, numbers and underscores (3–16 chars)."
)

SERVICE_UNAVAILABLE_TEXT = (
    "⚠️ Service is temporarily unavailable.\n"
    "Please try again later."
)

STATUS_NOT_REGISTERED_TEXT = (
    "ℹ️ You are not registered yet.\n"
    "Use /register &lt;nick&gt; to request access."
)

STATUS_PENDING_TEXT = (
    "⏳ Your request is pending admin approval."
)

STATUS_APPROVED_TEXT = (
    "✅ You are approved and whitelisted.\n"
    "Have fun!"
)

STATUS_REJECTED_TEXT = (
    "❌ Your request was rejected.\n"
    "Contact admins if you think it's a mistake."
)

ONLINE_EMPTY_TEXT = "🟢 No players online right now."
ONLINE_FORMAT_TEXT = "🟢 Online players ({count}):\n{players}"

# Notifications sent directly to players by admin actions
NOTIFY_APPROVED_TEXT = (
    "✅ <b>Your request has been approved</b>\n"
    "Nickname: <code>{nickname}</code>\n"
    "You are whitelisted — you can join the server now!"
)

NOTIFY_REJECTED_TEXT = (
    "❌ <b>Your request was rejected</b>\n"
    "Nickname: <code>{nickname}</code>\n"
    "If you think this is a mistake, contact the admins."
)
