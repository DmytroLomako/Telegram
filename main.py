import modules
import asyncio
import tkinter as tk

async def update_gui():
    while True:
        try:
            modules.app.update()
            await asyncio.sleep(1/120)
        except tk.TclError: 
            break

async def main():
    def on_closing():
        modules.app.quit()
        for task in asyncio.all_tasks():
            task.cancel()

    modules.app.protocol("WM_DELETE_WINDOW", on_closing)

    bot_task = asyncio.create_task(modules.dispatcher.start_polling(modules.bot))
    gui_task = asyncio.create_task(update_gui())

    try:
        await asyncio.gather(bot_task, gui_task)
    except asyncio.CancelledError:
        print("Application closed")
    except Exception as e:
        print(f"Error: {e}")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Shutting down...")