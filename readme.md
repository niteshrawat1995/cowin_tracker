Step To Setup:

1. make sure you have python 3.6 and pip
2. create a virtual env and activate it
    $ virtualenv -p python3 venv .
    $ source venv/bin/activate
3. install requirements:
    $ pip install -r requirements.txt
4. create a .env file using .env.sample and fill the creds
5. update the script to add your PINCODE and run the script to check for any errors
    $ python cowin_tracker.py
6. set the script to crontab
    $ crontab -e
    # inside the file add following line
    * * * * * cd <project_dir> && source venv/bin/activate && python cowin_tracker.py
7. pincode and min_age_limit will be set in main()

NOTE: Once you have booked a slot, please remove the script from crontab
Hope you will get appointment faster with this !! :)
