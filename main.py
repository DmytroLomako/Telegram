import modules
import aiogram 

aiogram._asyncio.run(modules.dispatcher.start_polling(modules.bot))