# from apscheduler.schedulers.background import BackgroundScheduler
# from .views import disable_old_locations, delete_disabled_locations
#
# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(disable_old_locations, 'interval', seconds=30)
#     scheduler.add_job(delete_disabled_locations, 'interval', hours=6)
#     scheduler.start()
#     scheduler.print_jobs()